"""V3 BorderProof Consistency Engine (BPCE).

Deterministic domain-specific safety checks, not a bank KYC/AML engine, not an
implementation of AP2, and not proof of a user's real-world identity.
Document text is *data*, never privileged instructions. All transfers stay internal.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import (PaymentCase, Quote, Document, Extraction, Investigation,
                     EvidenceSeal, ReviewTicket)

CORRIDORS = {'United Kingdom': 'GBP', 'United States': 'USD', 'Canada': 'CAD'}
# Heuristics are deliberately conservative; not a general prompt injection detector.
INJECTION_MARKERS = (
    r'ignore (?:all |any )?(?:previous|prior|system) instructions',
    r'(?:system|developer)\s*(?:prompt|message|instruction)\s*:',
    r'(?:disable|bypass|override)\s+(?:security|approval|policy|safety)',
    r'(?:call|invoke|execute)\s+(?:the\s+)?(?:payment|transfer)\s+tool',
    r'(?:approve|authorize)\s+(?:the\s+)?transfer\s+now',
)

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',',':'))

def hash_of(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()

def assess_injection(text):
    return ['UNTRUSTED_INSTRUCTION_INDICATOR'] if any(re.search(p,text,flags=re.I) for p in INJECTION_MARKERS) else []

def policy_for_case(case:PaymentCase):
    hard=[]
    if case.origin_country!='Bangladesh':hard.append('ORIGIN_NOT_SUPPORTED_IN_DEMO')
    if CORRIDORS.get(case.destination_country)!=case.currency:hard.append('DESTINATION_CURRENCY_NOT_SUPPORTED_IN_DEMO')
    return {'demonstration_corridor':'SUPPORTED_INTERNAL_SIMULATOR_ONLY' if not hard else 'BLOCKED',
            'hard_blocks':hard,'real_world_transfer_eligibility':'UNKNOWN_REQUIRES_LICENSED_PROVIDER',
            'sanctions_screening':'NOT_CONNECTED','bangladesh_bank_policy':'NOT_VERIFIED',
            'policy_version':'DEMO_RULESET_V3_1'}

def snapshot(db:Session,q:Quote):
    """Recompute from stored source; compare regenerated parsing with extraction."""
    from .finance import read_document, extract_fields, BENEFICIARIES, j
    c=db.get(PaymentCase,q.case_id)
    inv=db.get(Investigation,q.investigation_id)
    x=db.get(Extraction,inv.extraction_id) if inv else None
    d=db.get(Document,x.document_id) if x else None
    if not (c and inv and x and d and q.owner_id==c.user_id==inv.owner_id==x.owner_id==d.user_id
            and q.case_id==inv.case_id==x.case_id==d.case_id):
        raise HTTPException(409,'BPCE: evidence relationship/ownership mismatch')
    if inv.state!='SANDBOX_FIXTURE_MATCH':raise HTTPException(409,'BPCE: investigation not cleared for demo')
    raw,engine=read_document(d)
    fields,issues=extract_fields(raw)
    if fields!=json.loads(x.fields_json) or issues!=json.loads(x.issues_json) or x.document_hash!=d.sha256:
        raise HTTPException(409,'BPCE: extracted fields or source evidence no longer match')
    if assess_injection(raw):raise HTTPException(409,'BPCE: untrusted document instruction detected; manual review required')
    if issues:raise HTTPException(409,'BPCE: incomplete invoice')
    value=lambda k:fields.get(k,{}).get('value','')
    if (value('institution').casefold()!=c.institution.casefold() or value('amount')!=c.amount
            or value('currency')!=c.currency):
        raise HTTPException(409,'BPCE: case/invoice mismatch')
    beneficiary=next((b for b in BENEFICIARIES if b['id']==q.beneficiary_id),None)
    if not beneficiary or not (
        beneficiary['institution'].casefold()==c.institution.casefold()
        and beneficiary['beneficiary'].casefold()==value('beneficiary').casefold()
        and beneficiary['account'].casefold()==value('account').casefold()
        and beneficiary['currency']==c.currency and beneficiary['country']==c.destination_country
        and beneficiary['beneficiary']==q.recipient
    ):
        raise HTTPException(409,'BPCE: beneficiary differs from synthetic evidence registry')
    if (q.amount,q.currency,q.evidence_hash)!=(c.amount,c.currency,d.sha256):
        raise HTTPException(409,'BPCE: quote amount/currency/document changed')
    if q.provider not in ('CAMPUS_SIM_A','CAMPUS_SIM_B'):
        raise HTTPException(409,'BPCE: provider is not an internal simulator')
    policy=policy_for_case(c)
    if policy['hard_blocks']:raise HTTPException(409,'BPCE: demo corridor policy blocks execution')
    docs=db.scalars(select(Document).where(Document.case_id==c.id).order_by(Document.id)).all()
    latest=max(docs,key=lambda doc:(doc.created_at,doc.id))
    if latest.id!=d.id:
        raise HTTPException(409,'BPCE: newer document requires a fresh extraction and investigation')
    for document in docs:
        content,_=read_document(document)
        if assess_injection(content):
            raise HTTPException(409,'BPCE: untrusted document instruction detected in evidence set')
        # A conflicting prior invoice cannot be silently hidden by a later one.
        observed,problems=extract_fields(content)
        if any(p.startswith(('CONFLICTING_','INVALID_')) for p in problems):
            raise HTTPException(409,'BPCE: conflicting or invalid evidence-set fields require review')
        for key in ('institution','amount','currency','beneficiary','account'):
            if key in observed and observed[key]['value'].casefold()!=value(key).casefold():
                raise HTTPException(409,'BPCE: conflicting case documents require review')
    # Adding, replacing or deleting *any* case document invalidates old approvals.
    document_set=[{'id':doc.id,'sha256':doc.sha256,'bytes':doc.bytes_size} for doc in docs]
    registry_file=Path(__file__).resolve().parents[3]/'data/fixtures/synthetic_beneficiaries.json'
    if not registry_file.is_file():raise HTTPException(409,'BPCE: beneficiary registry unavailable')
    return {'version':'BPCE_V3_1',
        'case':{'id':c.id,'owner_id':c.user_id,'institution':c.institution,'origin':c.origin_country,
                'destination':c.destination_country,'amount':c.amount,'currency':c.currency},
        'source':{'document_id':d.id,'sha256':d.sha256,'engine':engine,'extraction_id':x.id,
                  'invoice_id':value('invoice_id'),'extracted_fields_sha256':hash_of(fields),
                  'document_set':document_set},
        'beneficiary':{'fixture_id':q.beneficiary_id,'name':q.recipient,
                       'account_sha256':hashlib.sha256(beneficiary['account'].encode()).hexdigest(),
                       'registry_sha256':hashlib.sha256(registry_file.read_bytes()).hexdigest(),
                       'source_class':'SYNTHETIC_FIXTURE_NOT_BANK_VERIFIED'},
        'quote':{'id':q.id,'provider':q.provider,'recipient':q.recipient,
                 'amount':q.amount,'currency':q.currency,'source_amount':q.source_amount,
                 'source_currency':q.source_currency,'synthetic_rate':q.synthetic_rate,
                 'synthetic_fee':q.synthetic_fee,'expires_at':q.expires_at.replace(tzinfo=timezone.utc).isoformat()},
        'policy':policy}

def seal_quote(db:Session,q:Quote):
    snap=snapshot(db,q)
    seal=EvidenceSeal(quote_id=q.id,case_id=q.case_id,owner_id=q.owner_id,
                      snapshot_json=canonical(snap),snapshot_sha256=hash_of(snap),engine_version='BPCE_V3_1')
    db.add(seal);db.flush()
    return seal

def verify_quote(db:Session,q:Quote):
    seal=db.scalar(select(EvidenceSeal).where(EvidenceSeal.quote_id==q.id))
    if not seal:raise HTTPException(409,'BPCE: legacy quote lacks a V3 evidence seal; create a fresh quote')
    try:sealed=json.loads(seal.snapshot_json)
    except Exception:raise HTTPException(409,'BPCE: corrupted evidence seal')
    if hash_of(sealed)!=seal.snapshot_sha256:
        raise HTTPException(409,'BPCE: evidence seal hash changed')
    actual=snapshot(db,q)
    if actual!=sealed or hash_of(actual)!=seal.snapshot_sha256:
        raise HTTPException(409,'BPCE: critical payment dependencies changed; reauthorize a fresh quote')
    return seal

def bound_fingerprint(db:Session,q:Quote,c:PaymentCase):
    from .finance import fingerprint
    seal=verify_quote(db,q)
    return hash_of({'engine':'BPCE_V3_1','v2_approval_scope':fingerprint(q,c),
                    'evidence_seal':seal.snapshot_sha256})

def graph_for_quote(db:Session,q:Quote):
    seal=verify_quote(db,q)
    s=json.loads(seal.snapshot_json)
    nodes=[{'id':'case','kind':'Payment intent','status':'CASE_MATCH'},
           {'id':'invoice','kind':'Invoice document','status':'UNVERIFIED_EXTERNAL_INPUT'},
           {'id':'extraction','kind':'Parsed fields','status':'DETERMINISTIC_REPARSED'},
           {'id':'beneficiary','kind':'Recipient','status':'SYNTHETIC_FIXTURE_MATCH_ONLY'},
           {'id':'policy','kind':'Corridor demo policy','status':'INTERNAL_ONLY_REAL_WORLD_UNKNOWN'},
           {'id':'quote','kind':'Sandbox quote','status':'SYNTHETIC_NON_EXECUTABLE_MARKET_QUOTE'},
           {'id':'approval','kind':'Transaction-specific consent','status':'REQUIRED_BEFORE_EXECUTION'}]
    edges=[{'from':a,'to':b,'rule':r} for a,b,r in (
        ('invoice','extraction','source hash + deterministic reparse'),
        ('extraction','case','invoice fields equal payment case'),
        ('extraction','beneficiary','account and recipient match demo fixture'),
        ('case','policy','supported demo origin, destination and currency'),
        ('beneficiary','quote','quoted recipient bound to fixture'),
        ('policy','quote','synthetic corridor policy prerequisite'),
        ('quote','approval','immutable quote + full snapshot hash'))]
    return {'quote_id':q.id,'seal_sha256':seal.snapshot_sha256,'nodes':nodes,'edges':edges,
        'caveat':'BPCE integrity is local/database based; data is not externally authenticated and no real bank was contacted'}

def case_risk(db:Session,c:PaymentCase):
    from .finance import read_document
    flags=[]
    policy=policy_for_case(c)
    flags.extend(policy['hard_blocks'])
    docs=db.scalars(select(Document).where(Document.case_id==c.id)).all()
    for doc in docs:
        try:
            raw,_=read_document(doc)
            flags.extend(assess_injection(raw))
        except HTTPException:
            flags.append('DOCUMENT_INTEGRITY_OR_EXTRACTION_UNAVAILABLE')
    investigations=db.scalars(select(Investigation).where(Investigation.case_id==c.id)).all()
    for investigation in investigations:
        try:
            if investigation.state in ('BLOCKED','NEEDS_CLARIFICATION'):
                flags.append('EVIDENCE_INVESTIGATION_'+investigation.state)
        except Exception:
            flags.append('EVIDENCE_INVESTIGATION_INVALID')
    flags=sorted(set(flags))
    return {'case_id':c.id,'flags':flags,'requires_review':bool(flags),
            'demo_execution_allowed':not flags and bool(investigations) and any(i.state=='SANDBOX_FIXTURE_MATCH' for i in investigations),
            'policy':policy,'source':'RULE_BASED_LOCAL_ASSESSMENT_NOT_KYC_AML_SCREENING',
            'notice':'No live OFAC, OpenSanctions, provider, beneficiary ownership or Bangladesh Bank compliance verification'}

def attack_probe(text:str):
    return {'input_class':'UNTRUSTED_DOCUMENT_TEXT','detections':assess_injection(text),
            'can_request_tools':False,'can_authorize':False,'can_execute':False,
            'warning':'Heuristic indicator scanner; misses are possible. Normal payment authority never comes from documents.'}
