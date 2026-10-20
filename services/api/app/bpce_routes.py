"""V3 strictly scoped security, human review, decision receipt and attack-probe APIs."""
from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from .db import db_session
from .models import User, Quote, PaymentCase, PaymentApproval, EvidenceSeal, ReviewTicket, SandboxTransfer, LedgerEntry
from .security import current_user, require_mutation_roles, require_roles
from .finance import owned_case, transfer_out, quote_out
from .bpce import (graph_for_quote, verify_quote, case_risk, attack_probe, policy_for_case)
from .audit import append_event, verify_event_chain

router=APIRouter(prefix='/api/v1',tags=['V3 Security and Consistency'])

class AttackProbe(BaseModel):
    untrusted_text:str=Field(min_length=1,max_length=2000)

class ReviewRequest(BaseModel):
    reason:str=Field(min_length=10,max_length=240)

class ReviewDecision(BaseModel):
    decision:str
    explanation:str=Field(min_length=10,max_length=800)

class ToolClaim(BaseModel):
    claimed_reference:str=Field(min_length=1,max_length=100)
    claimed_status:str=Field(min_length=1,max_length=32)

@router.get('/cases/{case_id}/bpce/policy')
def corridor_policy(case_id:str,user:User=Depends(current_user),db:Session=Depends(db_session)):
    c=owned_case(db,case_id,user.id)
    return policy_for_case(c)

@router.get('/cases/{case_id}/bpce/risk')
def risk_inspection(case_id:str,user:User=Depends(current_user),db:Session=Depends(db_session)):
    c=owned_case(db,case_id,user.id)
    return case_risk(db,c)

@router.get('/cases/{case_id}/bpce/quotes/{quote_id}')
def quote_decision(case_id:str,quote_id:str,user:User=Depends(current_user),db:Session=Depends(db_session)):
    owned_case(db,case_id,user.id)
    q=db.get(Quote,quote_id)
    if not q or q.case_id!=case_id or q.owner_id!=user.id:raise HTTPException(404,'Quote not found')
    from .finance import parse_dt,utcnow
    reasons=[];graph=None
    try:graph=graph_for_quote(db,q)
    except HTTPException as exc:reasons.append(str(exc.detail))
    if parse_dt(q.expires_at)<=utcnow():reasons.append('QUOTE_EXPIRED')
    approvals=db.scalars(select(PaymentApproval).where(PaymentApproval.quote_id==quote_id)).all()
    return {'quote_id':q.id,'can_proceed_to_approval':not reasons,'integrity':'CONSISTENT_LOCAL_SNAPSHOT' if not reasons else 'BLOCKED',
            'reasons':reasons,'graph':graph,'approvals':[{'id':a.id,'status':a.status} for a in approvals],
            'real_world_compliance':'NOT_VERIFIED','source_authentication':'SYNTHETIC_ONLY'}

@router.get('/transfers/{transfer_id}/decision-receipt')
def decision_receipt(transfer_id:str,user:User=Depends(current_user),db:Session=Depends(db_session)):
    t=db.get(SandboxTransfer,transfer_id)
    if not t or t.owner_id!=user.id:raise HTTPException(404,'Transfer not found')
    q=db.get(Quote,t.quote_id);seal=db.scalar(select(EvidenceSeal).where(EvidenceSeal.quote_id==q.id))
    a=db.get(PaymentApproval,t.approval_id)
    entries=db.scalars(select(LedgerEntry).where(LedgerEntry.transfer_id==t.id)).all()
    return {'title':'BORDERPROOF_V3_INTERNAL_SANDBOX_DECISION_RECEIPT',
        'transfer':transfer_out(t),'quote':quote_out(q),'approval':{'id':a.id,'status':a.status,'fingerprint':a.fingerprint},
        'bpce_evidence_seal':seal.snapshot_sha256 if seal else None,
        'ledger':[{'account_id':x.account_id,'currency':x.currency,'signed_amount':x.signed_amount} for x in entries],
        'verified':{'authorization_recorded':True,'execution_recorded_in_database':True,
                    'real_beneficiary_ownership':False,'live_provider_contact':False,'bank_compliance':False},
        'status_interpretation':'COMPLETED_SIMULATION' if t.status=='COMPLETED' else 'NOT_CONFIRMED_COMPLETED',
        'warning':'Test-only evidence, not a bank receipt, real provider confirmation or permission to transfer funds.'}

@router.post('/transfers/{transfer_id}/verify-tool-claim')
def verify_tool_claim(transfer_id:str,claim:ToolClaim,user:User=Depends(require_mutation_roles('student')),db:Session=Depends(db_session)):
    """Compare an UNTRUSTED presented simulator response with stored readback; never mutates status."""
    t=db.get(SandboxTransfer,transfer_id)
    if not t or t.owner_id!=user.id:raise HTTPException(404,'Transfer not found')
    if (claim.claimed_reference,claim.claimed_status)!=(t.provider_reference,t.status):
        raise HTTPException(409,'Tool result is inconsistent with persisted simulator readback')
    return {'matches_persisted_simulator':True,'status':t.status,'real_provider_verified':False,
            'notice':'An internal status match does not establish real payment settlement.'}

@router.post('/cases/{case_id}/bpce/review-request',status_code=201)
def request_review(case_id:str,inp:ReviewRequest,user:User=Depends(require_mutation_roles('student')),db:Session=Depends(db_session)):
    c=owned_case(db,case_id,user.id)
    prev=db.scalar(select(ReviewTicket).where(ReviewTicket.case_id==c.id,ReviewTicket.status=='PENDING'))
    if prev:raise HTTPException(409,'A review request is already pending')
    ticket=ReviewTicket(case_id=c.id,owner_id=user.id,reason=inp.reason.strip(),status='PENDING')
    db.add(ticket);db.flush();append_event(db,user.id,'REVIEW_REQUESTED','review',ticket.id,{'case_id':c.id})
    db.commit()
    return {'id':ticket.id,'status':ticket.status,'reason':ticket.reason,'note':'Review cannot bypass mandatory BPCE execution blocks.'}

@router.get('/cases/{case_id}/bpce/review-requests')
def case_reviews(case_id:str,user:User=Depends(current_user),db:Session=Depends(db_session)):
    owned_case(db,case_id,user.id)
    tickets=db.scalars(select(ReviewTicket).where(ReviewTicket.case_id==case_id).order_by(ReviewTicket.created_at.desc())).all()
    return {'items':[{'id':r.id,'status':r.status,'reason':r.reason,'decision_note':r.decision_note} for r in tickets]}

@router.get('/review/bpce-queue')
def review_queue(user:User=Depends(require_roles('reviewer','admin')),db:Session=Depends(db_session)):
    tickets=db.scalars(select(ReviewTicket).order_by(ReviewTicket.created_at.desc()).limit(100)).all()
    return {'items':[{'id':r.id,'case_id':r.case_id,'status':r.status,'reason':r.reason,'reviewer_id':r.reviewer_id}
                     for r in tickets], 'notice':'Acknowledgment cannot override immutable financial controls.'}

@router.post('/review/bpce-tickets/{ticket_id}/decide')
def decide_review(ticket_id:str,inp:ReviewDecision,user:User=Depends(require_mutation_roles('reviewer','admin')),db:Session=Depends(db_session)):
    r=db.get(ReviewTicket,ticket_id)
    if not r:raise HTTPException(404,'Review ticket not found')
    if r.status!='PENDING':raise HTTPException(409,'Ticket already resolved')
    if inp.decision not in ('ACKNOWLEDGED','REJECTED'):raise HTTPException(422,'Only ACKNOWLEDGED or REJECTED decisions are allowed')
    r.status=inp.decision;r.reviewer_id=user.id;r.decision_note=inp.explanation.strip()
    append_event(db,user.id,'REVIEW_DECISION','review',r.id,{'decision':r.status})
    db.commit()
    return {'id':r.id,'status':r.status,'note':'No reviewer override of payment-consistency checks exists.'}

@router.get('/security/audit-integrity')
def audit_integrity(user:User=Depends(require_roles('auditor','admin')),db:Session=Depends(db_session)):
    return verify_event_chain(db)

@router.post('/security/attack-probe')
def attack_lab(inp:AttackProbe,user:User=Depends(require_mutation_roles('reviewer','auditor','admin')),db:Session=Depends(db_session)):
    return attack_probe(inp.untrusted_text)

@router.get('/security/capabilities')
def v3_security_capabilities(user:User=Depends(current_user)):
    return {'bpce_version':'BPCE_V3_1','real_payments_enabled':False,'real_kyc_aml_enabled':False,
        'offered':['tamper-checked quote evidence seal','reparsed invoice binding','document-set change detection',
                   'hard fail on stale approval','cross-tenant access checks','audit chain verification',
                   'student human-review request','untrusted tool-claim verification',
                   'heuristic document-instruction filter','fail-closed demo corridor policy'],
        'not_offered':['trusted legal policy database','real provider settlement verification',
                       'complete anti-prompt-injection guarantee','signed externally anchored audit',
                       'real sanctions screening','production-grade KYC','production payment rails']}
