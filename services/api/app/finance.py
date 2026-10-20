"""V2 deterministic financial agent + internal sandbox. Nothing in this module moves real money."""
from __future__ import annotations
from .timeutils import iso_utc
import hashlib, json, os, re, secrets
from datetime import datetime, timedelta, timezone
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import (User, PaymentCase, Document, Extraction, Investigation, Quote,
    PaymentApproval, SandboxAccount, SandboxTransfer, LedgerEntry, Notification)
from .audit import append_event

ROOT = Path(__file__).resolve().parents[3]
BENEFICIARIES = json.loads((ROOT/'data/fixtures/synthetic_beneficiaries.json').read_text())['entries']
# INTENTIONALLY SYNTHETIC, DO NOT EXPOSE THESE AS MARKET RATES/REAL QUOTES.
SIMULATED_RATES = {'GBP':Decimal('160.00'), 'USD':Decimal('125.00'), 'CAD':Decimal('91.00')}
Q = Decimal('0.01')
def as_money(n): return str(Decimal(str(n)).quantize(Q, rounding=ROUND_HALF_EVEN))
def utcnow(): return datetime.now(timezone.utc)
def parse_dt(t): return t.replace(tzinfo=timezone.utc) if t.tzinfo is None else t

def j(v): return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def digest(v): return hashlib.sha256(j(v).encode()).hexdigest()
def owned_case(db:Session,case_id:str,user_id:str)->PaymentCase:
    c=db.get(PaymentCase,case_id)
    if not c or c.user_id!=user_id: raise HTTPException(404,'Case not found')
    return c

def extraction_out(x:Extraction):
    return {'id':x.id,'case_id':x.case_id,'document_id':x.document_id,'engine':x.engine,
        'document_hash':x.document_hash,'fields':json.loads(x.fields_json),'issues':json.loads(x.issues_json),
        'source_class':'USER_UPLOADED_UNVERIFIED','created_at':iso_utc(x.created_at)}

def read_document(d:Document)->tuple[str,str]:
    from .storage import configured_storage
    try:location=configured_storage().resolve(d.internal_path)
    except ValueError:raise HTTPException(409,'Source file outside configured private storage')
    if not location.is_file() or hashlib.sha256(location.read_bytes()).hexdigest()!=d.sha256:
        raise HTTPException(409,'Source file missing or changed')
    ext=location.suffix.lower()
    if ext=='.txt':
        text=location.read_text(encoding='utf-8')
        if len(text)>100_000:raise HTTPException(422,'Document text exceeds supported 100,000-character limit')
        return text, 'DETERMINISTIC_LABELLED_TEXT'
    if ext=='.pdf':
        try:
            from pypdf import PdfReader
        except ImportError: raise HTTPException(503,'PDF text extraction requires pypdf; see requirements')
        try:
            reader=PdfReader(str(location),strict=True)
            if len(reader.pages)>15:raise HTTPException(422,'Maximum 15 PDF pages supported')
            text='\n'.join(page.extract_text() or '' for page in reader.pages)
            if not text.strip():raise HTTPException(422,'Image-only PDF: OCR not available in current V2 mode')
            if len(text)>100_000:raise HTTPException(422,'PDF text exceeds supported 100,000-character limit')
            return text, 'PYPDF_TEXT_ONLY'
        except HTTPException:raise
        except Exception:raise HTTPException(422,'Could not parse PDF')
    if ext in ('.png','.jpg','.jpeg'):
        # Optional installed OCR path; refuse rather than hallucinate text when binary is absent.
        if os.getenv('ENABLE_LOCAL_OCR','0')!='1':
            raise HTTPException(503,'Image OCR disabled. Set ENABLE_LOCAL_OCR=1 and install Tesseract.')
        try:
            from PIL import Image
            import pytesseract
            with Image.open(location) as im:
                if im.width*im.height>12_000_000: raise HTTPException(422,'Image resolution exceeds 12 MP')
                text=pytesseract.image_to_string(im,timeout=15)
                if len(text)>100_000:raise HTTPException(422,'OCR text exceeds supported limit')
                return text, 'TESSERACT_LOCAL_OCR_UNVERIFIED'
        except HTTPException:raise
        except ImportError:raise HTTPException(503,'OCR Python dependencies unavailable')
        except Exception:raise HTTPException(422,'Image OCR failed')
    raise HTTPException(415,'Unsupported document type')

PATTERNS = {
    'institution':r'(?:institution|university|college)\s*[:#-]\s*(.+)',
    'invoice_id':r'(?:invoice\s*(?:id|number|no\.?|#)|reference)\s*[:#-]\s*([\w/-]+)',
    'amount':r'(?:amount|total\s*(?:due|payable)?|tuition\s*fee)\s*[:#-]\s*(?:[A-Z]{3}\s*)?([\d,]+(?:\.\d{1,2})?)',
    'currency':r'(?:currency)\s*[:#-]\s*(GBP|USD|CAD|EUR|BDT|CNY|AUD|SGD)',
    'beneficiary':r'(?:beneficiary|payee|recipient)\s*[:#-]\s*(.+)',
    'account':r'(?:account(?:\s*(?:number|no\.?))?|iban)\s*[:#-]\s*([\w-]+)',
    'deadline':r'(?:payment\s*deadline|due\s*date|deadline)\s*[:#-]\s*(\d{4}-\d{2}-\d{2})',
    'student':r'(?:student(?:\s*name)?)\s*[:#-]\s*(.+)'
}

def extract_fields(raw:str):
    """Anchored label parser; not a language model. Confidence is parser confidence, not truth."""
    fields={}; issues=[]
    lines=raw.splitlines()
    if len(lines)>1000:issues.append('DOCUMENT_LINE_LIMIT_EXCEEDED')
    if '\x00' in raw:issues.append('INVALID_CONTROL_CHARACTER')
    for key,pattern in PATTERNS.items():
        matches=[]
        for number,line in enumerate(lines[:1000],1):
            match=re.fullmatch(r'\s*'+pattern+r'\s*',line,flags=re.I)
            if not match:
                if key=='amount' and re.match(r'\s*(?:amount|total(?:\s*(?:due|payable))?|tuition\s*fee)\s*[:#-]',line,re.I):
                    issues.append('INVALID_AMOUNT')
                continue
            value=match.group(1).strip()
            if key=='amount':
                if not re.fullmatch(r'(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d{1,2})?',value):
                    issues.append('INVALID_AMOUNT');continue
                value=value.replace(',','')
                try:
                    amount=Decimal(value)
                    if not amount.is_finite() or amount<=0 or amount>1_000_000 or amount.as_tuple().exponent<-2:
                        issues.append('INVALID_AMOUNT');continue
                    value=as_money(amount)
                except Exception: issues.append('INVALID_AMOUNT');continue
            if key=='currency':value=value.upper()
            if key=='deadline':
                try:datetime.strptime(value,'%Y-%m-%d')
                except ValueError:issues.append('INVALID_DEADLINE');continue
            if any(ord(ch)<32 for ch in value) or len(value)>180:issues.append('INVALID_'+key.upper());continue
            matches.append((value,number))
        if matches:
            value,number=matches[0]
            if len({v.casefold() for v,_ in matches})>1:issues.append('CONFLICTING_'+key.upper())
            fields[key]={'value':value,'line':number,'confidence':0.95 if key not in ('beneficiary','institution') else 0.85,'verified':False,'source':'document_text'}
        if key not in fields:issues.append('MISSING_'+key.upper())
    if not raw.strip():issues.append('EMPTY_TEXT')
    return fields, sorted(set(issues))

def extract_document(db:Session,case_id:str,doc_id:str,owner_id:str):
    c=owned_case(db,case_id,owner_id)
    d=db.get(Document,doc_id)
    if not d or d.case_id!=c.id or d.user_id!=owner_id:raise HTTPException(404,'Document not found')
    previous=db.scalar(select(Extraction).where(Extraction.document_id==doc_id))
    if previous:return extraction_out(previous)
    raw,engine=read_document(d)
    fields,issues=extract_fields(raw)
    x=Extraction(case_id=c.id,document_id=d.id,owner_id=owner_id,engine=engine,document_hash=d.sha256,fields_json=j(fields),issues_json=j(issues))
    db.add(x);db.flush();append_event(db,owner_id,'INVOICE_EXTRACT','extraction',x.id,{'document_hash':d.sha256,'missing':issues})
    db.commit();return extraction_out(x)

def investigate(db:Session,case_id:str,extraction_id:str,owner_id:str):
    c=owned_case(db,case_id,owner_id)
    x=db.get(Extraction,extraction_id)
    if not x or x.case_id!=c.id or x.owner_id!=owner_id: raise HTTPException(404,'Extraction not found')
    fields=json.loads(x.fields_json)
    get=lambda name: fields.get(name,{}).get('value','')
    mismatches=[]
    if get('institution').casefold()!=c.institution.casefold():mismatches.append('INSTITUTION_MISMATCH')
    if get('amount')!=c.amount:mismatches.append('AMOUNT_MISMATCH')
    if get('currency')!=c.currency:mismatches.append('CURRENCY_MISMATCH')
    match=next((b for b in BENEFICIARIES if
        b['institution'].casefold()==get('institution').casefold() and
        b['beneficiary'].casefold()==get('beneficiary').casefold() and
        b['account'].casefold()==get('account').casefold() and
        b['currency']==get('currency') and b['country']==c.destination_country),None)
    if not match:mismatches.append('BENEFICIARY_NOT_IN_SYNTHETIC_REGISTRY')
    missing=[v for v in ['institution','invoice_id','amount','currency','beneficiary','account','deadline'] if not get(v)]
    parser_issues=json.loads(x.issues_json)
    if missing or parser_issues:state='NEEDS_CLARIFICATION'
    elif mismatches:state='BLOCKED'
    else:state='SANDBOX_FIXTURE_MATCH'
    result={'state':state,'document_id':x.document_id,'extraction_id':x.id,
        'evidence_hash':x.document_hash,'beneficiary_id':match['id'] if match else None,
        'missing_fields':missing,'conflicts':mismatches,'parser_issues':parser_issues,
        'clarification_questions':([f'Please provide or correct the {key} field in a new invoice.' for key in missing]
            + [f'Please resolve {issue.lower().replace("_"," ")} in the source document.' for issue in parser_issues]),
        'checks':[{'check':'Uploaded invoice fields','source':'UNVERIFIED_USER_DOCUMENT','result':'PARSED_NOT_AUTHENTICATED'},
                  {'check':'Beneficiary matches demo registry','source':'LOCAL_SYNTHETIC_FIXTURE','result':'MATCH' if match else 'NO_MATCH'},
                  {'check':'Real provider/corridor eligibility','source':'NONE','result':'UNKNOWN_REQUIRES_REAL_WORLD_REVIEW'}],
        'tool_trace':['load_extraction','compare_case','lookup_local_synthetic_registry','check_critical_fields'],
        'reasoning_mode':'BOUNDED_DETERMINISTIC_NON_LLM',
        'conclusion':'Eligible for INTERNAL SANDBOX ONLY' if state=='SANDBOX_FIXTURE_MATCH' else 'No sandbox execution allowed'}
    inv=Investigation(case_id=c.id,owner_id=owner_id,extraction_id=x.id,state=state,result_json=j(result))
    db.add(inv);db.flush();append_event(db,owner_id,'INVESTIGATE','case',c.id,{'result':state,'investigation_id':inv.id})
    db.commit();return {'id':inv.id,**result}

def investigation_out(i:Investigation):return {'id':i.id,**json.loads(i.result_json)}
def quote_out(q:Quote):return {'id':q.id,'case_id':q.case_id,'investigation_id':q.investigation_id,'provider':q.provider,
    'beneficiary_id':q.beneficiary_id,'recipient':q.recipient,'target_amount':q.amount,'target_currency':q.currency,
    'source_amount':q.source_amount,'source_currency':q.source_currency,'rate':q.synthetic_rate,'fee':q.synthetic_fee,
    'evidence_hash':q.evidence_hash,'expires_at':iso_utc(q.expires_at), 'expired':parse_dt(q.expires_at)<=utcnow(),
    'source_class':'SYNTHETIC_INTERNAL_QUOTE_NOT_MARKET_EXECUTABLE'}

def make_quote(db:Session,case_id:str,inv_id:str,owner_id:str,provider:str='CAMPUS_SIM_A'):
    financial_write_lock(db,owner_id)
    c=owned_case(db,case_id,owner_id); inv=db.get(Investigation,inv_id)
    legacy_countries={'United Kingdom':'GBP','United States':'USD','Canada':'CAD'}
    if c.origin_country!='Bangladesh' or (c.source_currency or 'BDT')!='BDT' or legacy_countries.get(c.destination_country)!=c.currency or (c.destination_currency or c.currency)!=c.currency:
        raise HTTPException(409,'No authorized provider quote for this corridor. Planning and evidence only.')
    if c.status in ('SIMULATED_COMPLETED','SIMULATED_UNKNOWN'):raise HTTPException(409,'Case already completed or unresolved')
    if not inv or inv.case_id!=case_id or inv.owner_id!=owner_id:raise HTTPException(404,'Investigation not found')
    if inv.state!='SANDBOX_FIXTURE_MATCH':raise HTTPException(409,'Investigation must pass synthetic fixture checks')
    result=json.loads(inv.result_json); x=db.get(Extraction,inv.extraction_id)
    # Recheck the user-editable case against the original invoice, rather than
    # relying solely on a historical investigation verdict.
    fields=json.loads(x.fields_json)
    val=lambda key:fields.get(key,{}).get('value','')
    if val('institution').casefold()!=c.institution.casefold() or val('amount')!=c.amount or val('currency')!=c.currency:
        raise HTTPException(409,'Case details differ from the investigated invoice')
    if not any(b['id']==result['beneficiary_id'] and b['institution'].casefold()==c.institution.casefold() for b in BENEFICIARIES):
        raise HTTPException(409,'Synthetic beneficiary registry mismatch')
    if x.document_hash!=result['evidence_hash']:raise HTTPException(409,'Stale investigation evidence')
    if provider not in ('CAMPUS_SIM_A','CAMPUS_SIM_B'):raise HTTPException(422,'Unknown simulator provider')
    rate=SIMULATED_RATES[c.currency]
    if provider=='CAMPUS_SIM_B':rate+=Decimal('1.75')
    base=Decimal(c.amount)*rate
    fee=(base * (Decimal('0.012') if provider=='CAMPUS_SIM_A' else Decimal('0.009'))+Decimal('350')).quantize(Q)
    source=(base+fee).quantize(Q)
    item=next(b for b in BENEFICIARIES if b['id']==result['beneficiary_id'])
    quote=Quote(case_id=c.id,owner_id=owner_id,investigation_id=inv.id,evidence_hash=x.document_hash,provider=provider,
        beneficiary_id=item['id'],recipient=item['beneficiary'],amount=c.amount,currency=c.currency,
        source_amount=as_money(source),synthetic_rate=as_money(rate),synthetic_fee=as_money(fee),
        expires_at=utcnow()+timedelta(minutes=15))
    db.add(quote);db.flush()
    from .bpce import seal_quote
    seal_quote(db,quote)
    append_event(db,owner_id,'QUOTE_CREATED','quote',quote.id,{'provider':provider,'mode':'SIMULATED'})
    db.commit();return quote_out(quote)

def fingerprint(q:Quote,c:PaymentCase):
    return digest({'case_id':c.id,'institution':c.institution,'destination':c.destination_country,'amount':c.amount,
        'currency':c.currency,'quote_id':q.id,'provider':q.provider,'beneficiary_id':q.beneficiary_id,
        'source_amount':q.source_amount,'evidence_hash':q.evidence_hash,'expiry':q.expires_at.isoformat()})

def approve(db:Session,case_id:str,quote_id:str,owner_id:str,acknowledge:str):
    financial_write_lock(db,owner_id)
    c=owned_case(db,case_id,owner_id);q=db.get(Quote,quote_id)
    if not q or q.case_id!=case_id or q.owner_id!=owner_id:raise HTTPException(404,'Quote not found')
    if acknowledge!='I AUTHORIZE THIS INTERNAL SANDBOX PAYMENT':raise HTTPException(422,'Transaction-specific confirmation text required')
    if parse_dt(q.expires_at)<=utcnow():raise HTTPException(409,'Quote expired')
    inv=db.get(Investigation,q.investigation_id);x=db.get(Extraction,inv.extraction_id)
    if inv.state!='SANDBOX_FIXTURE_MATCH' or q.evidence_hash!=x.document_hash:raise HTTPException(409,'Source evidence changed')
    if (q.amount,q.currency)!=(c.amount,c.currency):raise HTTPException(409,'Amount or currency changed')
    if db.scalar(select(PaymentApproval).where(PaymentApproval.quote_id==q.id)):
        raise HTTPException(409,'This quote has already been authorized')
    from .bpce import bound_fingerprint
    app=PaymentApproval(case_id=case_id,owner_id=owner_id,quote_id=q.id,fingerprint=bound_fingerprint(db,q,c))
    db.add(app);db.flush();append_event(db,owner_id,'SANDBOX_APPROVAL','approval',app.id,{'quote_id':quote_id,'fingerprint':app.fingerprint})
    db.commit();return {'id':app.id,'quote_id':quote_id,'status':'ACTIVE','scope_hash':app.fingerprint,'notice':'Authorization is valid ONLY for the internal synthetic simulator.'}

def account(db:Session,owner_id:str):
    a=db.scalar(select(SandboxAccount).where(SandboxAccount.user_id==owner_id))
    if a is None:
        a=SandboxAccount(user_id=owner_id,currency='BDT',balance='3000000.00',is_synthetic=True)
        db.add(a);db.flush()
    return a

def financial_write_lock(db:Session,owner_id:str):
    """Serialize owner balance/state updates; refresh rows after waiting for the lock."""
    connection=db.connection()
    if db.bind.dialect.name=='sqlite':
        if not connection.connection.driver_connection.in_transaction:
            connection.exec_driver_sql('BEGIN IMMEDIATE')
    elif db.bind.dialect.name=='postgresql':
        db.execute(select(User.id).where(User.id==owner_id).with_for_update())
    else:
        raise HTTPException(503,'Financial simulator requires a supported transactional database')
    db.expire_all()

def transfer_out(t:SandboxTransfer):
    return {'id':t.id,'case_id':t.case_id,'quote_id':t.quote_id,'approval_id':t.approval_id,'status':t.status,
        'source_debit':t.debit_amount,'source_currency':'BDT','target_amount':t.paid_amount,'target_currency':t.paid_currency,
        'provider_reference':t.provider_reference,'created_at':iso_utc(t.created_at),
        'simulator_result':json.loads(t.result_json),'mode':'INTERNAL_SANDBOX_SYNTHETIC_NO_REAL_MONEY'}

def execute(db:Session,case_id:str,approval_id:str,owner_id:str,key:str,outcome:str):
    if not re.fullmatch(r'[A-Za-z0-9._:-]{8,100}',key):raise HTTPException(422,'Invalid idempotency key (8–100 safe characters)')
    if outcome not in ('SUCCESS','DECLINED','TIMEOUT'):raise HTTPException(422,'Unsupported simulator outcome')
    # SQLite serializes concurrent sandbox writes. Combined with DB unique idempotency
    # and case-level completed/unknown guard, this avoids TOCTOU duplicate debits.
    financial_write_lock(db,owner_id)
    c=owned_case(db,case_id,owner_id)
    existing=db.scalar(select(SandboxTransfer).where(SandboxTransfer.owner_id==owner_id,SandboxTransfer.idempotency_key==key))
    if existing:
        if existing.case_id!=case_id or existing.approval_id!=approval_id or existing.requested_outcome!=outcome:
            raise HTTPException(409,'Idempotency key is bound to a different request')
        return transfer_out(existing)
    another=db.scalar(select(SandboxTransfer).where(SandboxTransfer.case_id==case_id,SandboxTransfer.status.in_(['COMPLETED','UNKNOWN'])))
    if another:raise HTTPException(409,'This case already has a completed or unresolved simulator transfer')
    app=db.get(PaymentApproval,approval_id)
    if not app or app.case_id!=case_id or app.owner_id!=owner_id:raise HTTPException(404,'Approval not found')
    q=db.get(Quote,app.quote_id)
    if app.status!='ACTIVE':raise HTTPException(409,'Approval already used or inactive')
    if parse_dt(q.expires_at)<=utcnow():app.status='EXPIRED';db.commit();raise HTTPException(409,'Quote expired; obtain a fresh authorization')
    inv=db.get(Investigation,q.investigation_id)
    x=db.get(Extraction,inv.extraction_id)
    doc=db.get(Document,x.document_id)
    if not Path(doc.internal_path).is_file() or hashlib.sha256(Path(doc.internal_path).read_bytes()).hexdigest()!=q.evidence_hash:
        raise HTTPException(409,'Financial source evidence missing or modified')
    from .bpce import bound_fingerprint
    try:
        current_fingerprint=bound_fingerprint(db,q,c)
    except HTTPException:
        app.status='INVALIDATED';db.commit()
        raise
    if current_fingerprint!=app.fingerprint or x.document_hash!=q.evidence_hash:
        app.status='INVALIDATED';db.commit();raise HTTPException(409,'Critical payment details changed')
    a=account(db,owner_id)
    cost=Decimal(q.source_amount)
    if outcome=='SUCCESS' and Decimal(a.balance)<cost:raise HTTPException(409,'Insufficient synthetic sandbox balance')
    t=SandboxTransfer(owner_id=owner_id,case_id=case_id,quote_id=q.id,approval_id=app.id,
        idempotency_key=key,status={'SUCCESS':'COMPLETED','DECLINED':'FAILED','TIMEOUT':'UNKNOWN'}[outcome],
        requested_outcome=outcome,debit_amount=q.source_amount,paid_amount=q.amount,paid_currency=q.currency,
        provider_reference='SIM-'+secrets.token_hex(12).upper(),
        result_json=j({'engine':'DETERMINISTIC_SANDBOX_V2','provider_response':outcome,
            'note':'No real bank or payment service was contacted.'}))
    db.add(t);db.flush()
    app.status='CONSUMED'   # even UNKNOWN is not reusable until reconciled
    c.status='SIMULATED_'+t.status
    if t.status=='COMPLETED':
        a.balance=as_money(Decimal(a.balance)-cost)
        db.add(LedgerEntry(transfer_id=t.id,account_id=a.id,currency='BDT',signed_amount=as_money(-cost)))
        db.add(LedgerEntry(transfer_id=t.id,account_id='SIMULATOR_BDT_CLEARING',currency='BDT',signed_amount=as_money(cost)))
    db.add(Notification(owner_id=owner_id,case_id=case_id,code='PAYMENT_'+t.status,
        message='Internal simulator '+t.status.lower()+' — no real money moved.'))
    append_event(db,owner_id,'SANDBOX_EXECUTE','transfer',t.id,{'outcome':t.status,'idempotency_key_hash':hashlib.sha256(key.encode()).hexdigest()})
    db.commit();return transfer_out(t)

def reconcile(db:Session,t:SandboxTransfer,owner_id:str,confirmation:str):
    financial_write_lock(db,owner_id)
    db.refresh(t)
    if t.owner_id!=owner_id:raise HTTPException(404,'Transfer not found')
    if t.status!='UNKNOWN':raise HTTPException(409,'Only unknown transfers can be reconciled')
    if confirmation not in ('CONFIRMED_FAILED','CONFIRMED_SUCCESS'):raise HTTPException(422,'Invalid simulator confirmation')
    if confirmation=='CONFIRMED_SUCCESS':
        # DEMO ONLY. Never infer success from a timeout; explicit sandbox reconciliation required.
        a=account(db,owner_id);cost=Decimal(t.debit_amount)
        if not cost.is_finite() or cost<=0:raise HTTPException(409,'Invalid immutable transfer debit')
        if Decimal(a.balance)<cost:raise HTTPException(409,'Insufficient synthetic funds for reconciliation')
        a.balance=as_money(Decimal(a.balance)-cost)
        db.add(LedgerEntry(transfer_id=t.id,account_id=a.id,currency='BDT',signed_amount=as_money(-cost)))
        db.add(LedgerEntry(transfer_id=t.id,account_id='SIMULATOR_BDT_CLEARING',currency='BDT',signed_amount=as_money(cost)))
        t.status='COMPLETED'
    else:t.status='FAILED'
    db.get(PaymentCase,t.case_id).status='SIMULATED_'+t.status
    t.result_json=j({'engine':'DETERMINISTIC_SANDBOX_V2','reconciled_as':confirmation,'mode':'USER_SELECTED_SIMULATED_OUTCOME'})
    append_event(db,owner_id,'SANDBOX_RECONCILE','transfer',t.id,{'status':t.status})
    db.add(Notification(owner_id=owner_id,case_id=t.case_id,code='PAYMENT_RECONCILED',message='Internal simulator reconciled as '+t.status+'.'))
    db.commit();return transfer_out(t)
