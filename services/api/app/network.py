"""V5.4 read-only, bilateral, non-custodial planning network.

Corridor discovery is NOT provider availability, legal permission, an FX offer or a
payment. Failed financial references never fall back to invented data.
"""
from __future__ import annotations
import hashlib
import json
import re
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN
from typing import Literal
from urllib.parse import quote
import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select
from sqlalchemy.orm import Session
from .db import db_session
from .models import User, PaymentCase, Document, Extraction, RouteAssessment
from .security import current_user, require_mutation_roles
from .finance import owned_case
from .audit import append_event
from .timeutils import iso_utc
from .network_config import REGION_CURRENCIES

# Euro Area is an economic region, NOT a single country. Eligibility is jurisdiction-specific.
REGIONS = {
    'Bangladesh': ('BDT','🇧🇩'),
    'China': ('CNY','🇨🇳'),
    'United Kingdom': ('GBP','🇬🇧'),
    'United States': ('USD','🇺🇸'),
    'Canada': ('CAD','🇨🇦'),
    'Euro Area': ('EUR','🇪🇺'),
    'Australia': ('AUD','🇦🇺'),
    'Singapore': ('SGD','🇸🇬'),
}
CURRENCIES = tuple(v[0] for v in REGIONS.values())
ROUTES = tuple((a,b) for a in REGIONS for b in REGIONS if a != b)
FX_BASE = 'https://api.frankfurter.dev/v2/rate'
router = APIRouter(prefix='/api/v1/network',tags=['cross-border-planning'])

def region_currency(region: str)->str:
    try: return REGIONS[region][0]
    except KeyError: raise HTTPException(422,'Unknown country or economic region')

def money(v:str):
    try: d=Decimal(str(v))
    except (InvalidOperation,ValueError):raise HTTPException(422,'Invalid amount')
    if not d.is_finite() or d<=0 or d>Decimal('1000000') or d.as_tuple().exponent < -2:
        raise HTTPException(422,'Amount must be positive, at most 1,000,000 and at most two decimals')
    return d

def fresh_pair(base:str, target:str, amount:str):
    """Live authenticated-by-TLS public *reference*, NEVER an executable quote.

    HTTP fetch happens only after strict currency validation (no SSRF input).
    """
    if base not in CURRENCIES or target not in CURRENCIES:
        raise HTTPException(422,'Unsupported source or target currency')
    if base==target:raise HTTPException(422,'Choose two distinct currencies')
    quantity=money(amount)
    url=f'{FX_BASE}/{base.lower()}/{target.lower()}'
    try:
        response=httpx.get(url,timeout=9,follow_redirects=False,headers={'Accept':'application/json'})
        response.raise_for_status()
        result=json.loads(response.content,parse_float=Decimal)
        if result['base'].upper()!=base or result['quote'].upper()!=target:
            raise ValueError('Currency mismatch')
        d=date.fromisoformat(result['date']); today=datetime.now(timezone.utc).date()
        if d>today or (today-d).days>7:raise ValueError('Stale financial data')
        raw=Decimal(str(result['rate']))
        if not raw.is_finite() or raw<=0 or raw>Decimal('100000000'):raise ValueError('Bad rate')
    except (httpx.HTTPError,ValueError,KeyError,TypeError,InvalidOperation,OverflowError,ArithmeticError):
        raise HTTPException(503,'Independent FX reference unavailable or stale; no estimated rate supplied')
    return {
        'status':'REFERENCE_ONLY_NOT_AN_EXECUTION_QUOTE',
        'base':base,'quote':target,'source_amount':str(quantity),
        'rate':str(raw),'indicative_target_amount':str((quantity*raw).quantize(Decimal('0.01'),rounding=ROUND_HALF_EVEN)),
        'published_date':str(d),'retrieved_at_utc':datetime.now(timezone.utc).isoformat(),
        'source_url':url,'provider':'Frankfurter v2 / published central-bank and official-source rates (provider varies)',
        'response_sha256':hashlib.sha256(response.content).hexdigest(),
        'fees':None,'provider_quote':False,'provider_available':False,'legal_eligibility':'UNKNOWN',
        'notices':['Reference exchange rates are not executable offers or guaranteed settlement rates',
                   'Bank/FX provider fees, spreads, sanctions and student-payment regulations are unverified'],
    }

@router.get('/corridors')
def corridors(user:User=Depends(current_user)):
    return {'regions':[{'name':k,'currency':v[0],'flag':v[1],'type':'region' if k=='Euro Area' else 'country'} for k,v in REGIONS.items()],
        'currencies':list(CURRENCIES),'directed_route_count':len(ROUTES),
        'routes':[{'origin_country':a,'destination_country':b,'source_currency':region_currency(a),
                   'destination_currency':region_currency(b),'planning_supported':True,
                   'provider_available':False,'legal_eligibility':'UNKNOWN','execution_allowed':False}
                  for a,b in ROUTES],
        'disclaimer':'56 bidirectional planning pairs, zero provider-verified transfer routes. Never a payment availability claim.'}

@router.get('/reference')
def reference(from_currency:str,to_currency:str,amount:str='1.00',user:User=Depends(current_user)):
    return fresh_pair(from_currency,to_currency,amount)

@router.get('/cases/{case_id}/assessment')
def assessment(case_id:str,user:User=Depends(current_user),db:Session=Depends(db_session)):
    c=owned_case(db,case_id,user.id)
    docs=db.scalars(select(Document).where(Document.case_id==c.id,Document.user_id==user.id)).all()
    latest=db.scalar(select(Extraction).where(Extraction.case_id==c.id,Extraction.owner_id==user.id).order_by(Extraction.created_at.desc()))
    conflicts=[];missing=[]; fields={}
    # Every document is part of the case evidence set, not just the latest one.
    # A changed/deleted earlier invoice must never silently pass the network review.
    from .storage import configured_storage
    storage=configured_storage()
    for doc in docs:
        try:
            path=storage.resolve(doc.internal_path)
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=doc.sha256:
                conflicts.append('DOCUMENT_SET_INTEGRITY_FAILED')
                break
        except (ValueError, OSError):
            conflicts.append('DOCUMENT_SET_INTEGRITY_FAILED')
            break
    if latest:
        newest=sorted(docs,key=lambda d:(d.created_at,d.id),reverse=True)[0] if docs else None
        if not newest or newest.id!=latest.document_id:
            conflicts.append('STALE_EXTRACTION_AFTER_DOCUMENT_CHANGE')
        elif latest.document_hash != newest.sha256:
            conflicts.append('EXTRACTION_DOCUMENT_HASH_MISMATCH')
        else:
            try:
                from .finance import read_document
                raw,_=read_document(newest)
                if re.search(r'(?i)(ignore\s+(all\s+)?(previous|system|bank)\s+instructions|bypass\s+(verification|approval|security)|pay\s+to\s+the\s+new\s+account\s+without\s+(checks|verification))',raw):
                    conflicts.append('MALICIOUS_OR_SUSPICIOUS_INVOICE_INSTRUCTIONS')
            except HTTPException:
                conflicts.append('SOURCE_FILE_MISSING_OR_HASH_CHANGED')
        try:
            parsed=json.loads(latest.fields_json)
            if not isinstance(parsed,dict):raise ValueError('Invalid extraction field structure')
            fields={k:v.get('value','') for k,v in parsed.items() if isinstance(v,dict)}
        except (ValueError,AttributeError,TypeError):conflicts.append('UNREADABLE_EXTRACTION')
        # A parser may return the first of several conflicting values. Do not
        # treat that first value as clean evidence when its issue list says otherwise.
        try:
            issues=json.loads(latest.issues_json)
            if not isinstance(issues,list):raise ValueError('Invalid issue structure')
            if any(isinstance(issue,str) and issue.startswith(('CONFLICTING_','INVALID_','DOCUMENT_LINE_LIMIT_'))
                   for issue in issues):
                conflicts.append('EXTRACTION_PARSER_SAFETY_ISSUES')
        except (ValueError,TypeError):conflicts.append('UNREADABLE_EXTRACTION_ISSUES')
        for k,expected in [('institution',c.institution),('currency',c.currency),('amount',c.amount)]:
            if k in fields and str(fields[k]).casefold()!=str(expected).casefold():conflicts.append(k.upper()+'_MISMATCH')
            if k not in fields:missing.append('MISSING_'+k.upper())
        for k in ('beneficiary','account'): 
            if not fields.get(k):missing.append('MISSING_'+k.upper())
    else: missing.append('NO_EXTRACTED_INVOICE')
    if not docs:missing.append('NO_UPLOADED_DOCUMENT')
    source_currency=c.source_currency or 'BDT'
    target_currency=c.destination_currency or region_currency(c.destination_country)
    if c.origin_country==c.destination_country:conflicts.append('NOT_CROSS_BORDER')
    if source_currency!=region_currency(c.origin_country):missing.append('SOURCE_CURRENCY_NOT_NATIVE_REQUIRES_CONFIRMATION')
    if c.currency!=target_currency:missing.append('INVOICE_CURRENCY_DIFFERS_FROM_SETTLEMENT_CURRENCY')
    status='BLOCKED_CONFLICT' if conflicts else 'REVIEW_REQUIRED'
    outcome={'case_id':c.id,'status':status,'origin_country':c.origin_country,
        'destination_country':c.destination_country,'source_currency':source_currency,
        'destination_currency':target_currency,'invoice_currency':c.currency,
        'source_documents':[{'id':d.id,'sha256':d.sha256,'status':d.status} for d in docs],
        'extraction_id':latest.id if latest else None,'extracted_values':fields,
        'conflicts':conflicts,'missing_or_unknown':missing,
        'university_attestation':'NOT_VERIFIED','bank_beneficiary_ownership':'NOT_VERIFIED',
        'legal_corridor_eligibility':'UNKNOWN','provider_rail':'NOT_CONNECTED',
        'execution_allowed':False,'route_decision':'DO_NOT_EXECUTE_REAL_PAYMENT','explanation':'User-supplied documents cannot independently prove university or bank beneficiary authenticity.'}
    return outcome

@router.post('/cases/{case_id}/assessment',status_code=201)
def persist_assessment(case_id:str,user:User=Depends(require_mutation_roles('student')),db:Session=Depends(db_session)):
    result=assessment(case_id,user,db)
    canonical=json.dumps(result,sort_keys=True,ensure_ascii=False,separators=(',',':'))
    item=RouteAssessment(case_id=case_id,owner_id=user.id,result_json=canonical,result_sha256=hashlib.sha256(canonical.encode()).hexdigest())
    db.add(item);db.flush()
    append_event(db,user.id,'NETWORK_EVIDENCE_ASSESSED','case',case_id,{'assessment_id':item.id,'status':result['status'],'result_hash':item.result_sha256})
    db.commit()
    return {'id':item.id,'created_at':iso_utc(item.created_at),'result_sha256':item.result_sha256,**result}

@router.get('/cases/{case_id}/history')
def history(case_id:str,user:User=Depends(current_user),db:Session=Depends(db_session)):
    owned_case(db,case_id,user.id)
    items=db.scalars(select(RouteAssessment).where(RouteAssessment.owner_id==user.id,RouteAssessment.case_id==case_id).order_by(RouteAssessment.created_at.desc())).all()
    return {'items':[{'id':x.id,'case_id':x.case_id,'result_sha256':x.result_sha256,'created_at':iso_utc(x.created_at),**json.loads(x.result_json)} for x in items]}
