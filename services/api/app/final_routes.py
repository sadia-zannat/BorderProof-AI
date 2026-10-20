"""V5: audited, tenant-scoped evidence export, deterministic next-step planner,
and synthetic-only dispute assistance. NO real refund or provider invocation."""
from __future__ import annotations
from .timeutils import iso_utc
import hashlib
import json
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from .db import db_session
from .models import (User, PaymentCase, Document, Extraction, Investigation, Quote,
                     PaymentApproval, EvidenceSeal, SandboxTransfer, LedgerEntry,
                     DisputeCase)
from .security import current_user, require_mutation_roles
from .finance import owned_case, quote_out, transfer_out, parse_dt, utcnow
from .audit import append_event, verify_event_chain
from .bpce import policy_for_case

router = APIRouter(prefix='/api/v1', tags=['V5 Evidence and Recovery'])

class DisputeInput(BaseModel):
    transfer_id: str = Field(min_length=32,max_length=32)
    category: str = Field(pattern=r'^(STATUS_QUERY|PAYMENT_ERROR|REFUND_GUIDANCE|OTHER)$')
    message: str = Field(min_length=12,max_length=1000)

class PlanInput(BaseModel):
    case_id: str = Field(min_length=32,max_length=32)


def dispute_out(d: DisputeCase) -> dict:
    return dict(id=d.id,case_id=d.case_id,transfer_id=d.transfer_id,status=d.status,
                category=d.category,message=d.message,created_at=iso_utc(d.created_at),
                mode='GUIDANCE_CASE_ONLY_NO_BANK_DISPUTE_OR_REFUND')

@router.post('/support/disputes',status_code=201)
def create_dispute(inp:DisputeInput, user:User=Depends(require_mutation_roles('student')),
                   db:Session=Depends(db_session)):
    t=db.get(SandboxTransfer,inp.transfer_id)
    if not t or t.owner_id!=user.id: raise HTTPException(404,'Transfer not found')
    case=owned_case(db,t.case_id,user.id)
    active=db.scalar(select(DisputeCase).where(DisputeCase.transfer_id==t.id,
                  DisputeCase.owner_id==user.id,DisputeCase.status=='OPEN'))
    if active:raise HTTPException(409,'An open support case already exists for this transfer')
    d=DisputeCase(owner_id=user.id,case_id=case.id,transfer_id=t.id,category=inp.category,
                  message=inp.message.strip(),status='OPEN')
    db.add(d); db.flush()
    append_event(db,user.id,'SYNTHETIC_SUPPORT_CASE_OPENED','support_case',d.id,
                 {'transfer_id':t.id,'category':d.category,'no_bank_action':True})
    db.commit()
    return dispute_out(d)

@router.get('/support/disputes')
def list_disputes(user:User=Depends(current_user),db:Session=Depends(db_session)):
    if user.role!='student': raise HTTPException(403,'Student only')
    items=db.scalars(select(DisputeCase).where(DisputeCase.owner_id==user.id)
                     .order_by(DisputeCase.created_at.desc()).limit(100)).all()
    return {'items':[dispute_out(d) for d in items],
            'notice':'Local demonstration records only. They do not contact banks or initiate refunds.'}

@router.get('/cases/{case_id}/safe-plan')
def safe_plan(case_id:str,user:User=Depends(current_user),db:Session=Depends(db_session)):
    """Reads state, chooses one of bounded *recommended* steps. Never invokes payment tools."""
    if user.role!='student':raise HTTPException(403,'Student only')
    c=owned_case(db,case_id,user.id)
    docs=db.scalars(select(Document).where(Document.case_id==c.id).order_by(Document.created_at.desc())).all()
    extra=db.scalars(select(Extraction).where(Extraction.case_id==c.id).order_by(Extraction.created_at.desc())).all()
    inv=db.scalars(select(Investigation).where(Investigation.case_id==c.id).order_by(Investigation.created_at.desc())).all()
    quotes=db.scalars(select(Quote).where(Quote.case_id==c.id).order_by(Quote.created_at.desc())).all()
    approvals=db.scalars(select(PaymentApproval).where(PaymentApproval.case_id==c.id).order_by(PaymentApproval.created_at.desc())).all()
    transfers=db.scalars(select(SandboxTransfer).where(SandboxTransfer.case_id==c.id).order_by(SandboxTransfer.created_at.desc())).all()
    issues=[]
    if policy_for_case(c)['hard_blocks']:
        step='REVIEW_DEMO_CORRIDOR';issues=['UNSUPPORTED_DEMO_CORRIDOR']
    elif not docs:step='UPLOAD_INVOICE'
    elif not extra or not any(x.document_id==docs[0].id for x in extra):step='EXTRACT_LATEST_DOCUMENT'
    elif not inv or inv[0].extraction_id!=extra[0].id:step='INVESTIGATE_EVIDENCE'
    elif inv[0].state!='SANDBOX_FIXTURE_MATCH':
        step='RESOLVE_EVIDENCE_CONFLICT';issues=[inv[0].state]
    elif not quotes or quotes[0].investigation_id!=inv[0].id:step='COMPARE_SYNTHETIC_QUOTES'
    elif parse_dt(quotes[0].expires_at)<=utcnow():step='RENEW_EXPIRED_QUOTE';issues=['QUOTE_EXPIRED']
    elif transfers:
        step={'UNKNOWN':'REQUEST_SIMULATOR_RECONCILIATION','FAILED':'REVIEW_FAILURE_AND_REPLAN',
              'COMPLETED':'DOWNLOAD_SIMULATION_EVIDENCE'}.get(transfers[0].status,'INSPECT_SANDBOX_STATUS')
    elif not approvals or not any(a.quote_id==quotes[0].id and a.status=='ACTIVE' for a in approvals):
        step='REVIEW_AND_APPROVE_EXACT_QUOTE'
    else:step='EXPLICITLY_CHOOSE_INTERNAL_SIMULATION'
    return {'mode':'READ_ONLY_DETERMINISTIC_PLANNER_NOT_AUTONOMOUS_AGENT',
            'case_id':c.id,'recommended_next_step':step,'issues':issues,
            'observed':{'documents':len(docs),'extractions':len(extra),'investigations':len(inv),
                        'quotes':len(quotes),'approvals':len(approvals),'transfers':len(transfers)},
            'allowed_tool_names':['read_uploaded_evidence','compare_synthetic_beneficiary',
                                  'inspect_synthetic_quote','inspect_authorization','inspect_simulation_receipt'],
            'requested_authorization':False,'executed_actions':[],
            'real_world_eligibility':'UNKNOWN_REQUIRES_LICENSED_PROVIDER',
            'notice':'This endpoint gives guidance only. It neither approves nor executes any financial task.'}

@router.get('/transfers/{transfer_id}/evidence-export')
def evidence_export(transfer_id:str, response:Response,
                    user:User=Depends(current_user),db:Session=Depends(db_session)):
    """Deterministic JSON evidence envelope with SHA-256, not a signed or bank-attested receipt."""
    if user.role!='student':raise HTTPException(403,'Student only')
    t=db.get(SandboxTransfer,transfer_id)
    if not t or t.owner_id!=user.id:raise HTTPException(404,'Transfer not found')
    q=db.get(Quote,t.quote_id)
    a=db.get(PaymentApproval,t.approval_id)
    seal=db.scalar(select(EvidenceSeal).where(EvidenceSeal.quote_id==q.id))
    entries=db.scalars(select(LedgerEntry).where(LedgerEntry.transfer_id==t.id)).all()
    document=db.scalars(select(Document).where(Document.case_id==t.case_id)).all()
    chain=verify_event_chain(db)
    evidence={'schema_version':'BORDERPROOF_SYNTHETIC_EXPORT_V5',
              'generated_at':datetime.now(timezone.utc).isoformat(),
              'transfer':transfer_out(t),'quote':quote_out(q),
              'approval':{'id':a.id,'status':a.status,'scope_fingerprint_sha256':a.fingerprint},
              'evidence_seal_sha256':seal.snapshot_sha256 if seal else None,
              'document_sha256':[{'id':d.id,'sha256':d.sha256} for d in document],
              'ledger':[{'currency':v.currency,'signed_amount':v.signed_amount,'account_id':v.account_id} for v in entries],
              'local_audit_chain_valid':chain['valid'],
              'provenance':{'source':'LOCAL_SYNTHETIC_DEMONSTRATION',
                  'provider_settlement_verified':False,'real_payment':False,
                  'real_beneficiary_verified':False,'bank_compliance_verified':False},
              'limitations':['The local SHA-256 digest is not a digital signature',
                  'Local database administrators can modify/replace records',
                  'No real financial institution confirms settlement']}
    payload=json.dumps(evidence,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
    response.headers['Cache-Control']='no-store'
    response.headers['Content-Disposition']=f'attachment; filename="borderproof-synthetic-{t.id}.json"'
    return {'evidence':evidence,'evidence_sha256':hashlib.sha256(payload).hexdigest(),
            'canonicalization':'UTF-8 JSON sort_keys compact separators, no ASCII escaping',
            'proof_class':'SELF_HASHED_LOCAL_DATA_NOT_SIGNED_NOT_BANK_VERIFIED'}

@router.get('/release/capabilities')
def release_capabilities(user:User=Depends(current_user)):
    return {'release':'V5','execution':'INTERNAL_SANDBOX_ONLY','real_money_enabled':False,
            'safe_plan':'DETERMINISTIC_READ_ONLY',
            'evidence_export':'SELF_HASHED_LOCAL_JSON_NOT_DIGITALLY_SIGNED',
            'support':'LOCAL_GUIDANCE_CASE_ONLY',
            'externals':{'real_provider_credential_present':False,'real_beneficiary_attestation':False,
                         'verified_legal_compliance':False},
            'production_readiness':'NOT_SUITABLE_FOR_REAL_FINANCIAL_OPERATIONS'}
