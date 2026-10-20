"""Typed persistence entities. Monetary values are decimal strings in V1."""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, ForeignKey, Integer, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

def uid(): return uuid.uuid4().hex
def utcnow(): return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = 'users'
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=uid)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    role: Mapped[str] = mapped_column(String(20), default='student')
    password_hash: Mapped[str] = mapped_column(String(255))
    institution: Mapped[str] = mapped_column(String(160), default='')
    home_country: Mapped[str] = mapped_column(String(64), default='Bangladesh')
    currency: Mapped[str] = mapped_column(String(3), default='BDT')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

class LoginSession(Base):
    __tablename__ = 'login_sessions'
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=uid)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'), index=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    csrf_hash: Mapped[str] = mapped_column(String(64))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

class PaymentCase(Base):
    __tablename__ = 'payment_cases'
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=uid)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'), index=True)
    title: Mapped[str] = mapped_column(String(160))
    institution: Mapped[str] = mapped_column(String(160))
    origin_country: Mapped[str] = mapped_column(String(64), default='Bangladesh')
    source_currency: Mapped[str] = mapped_column(String(3), default='BDT')
    destination_currency: Mapped[str | None] = mapped_column(String(3), nullable=True, default=None)
    destination_country: Mapped[str] = mapped_column(String(64))
    amount: Mapped[str] = mapped_column(String(40))
    currency: Mapped[str] = mapped_column(String(3))
    status: Mapped[str] = mapped_column(String(32), default='DRAFT')
    is_synthetic: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

class Document(Base):
    __tablename__ = 'documents'
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=uid)
    case_id: Mapped[str] = mapped_column(ForeignKey('payment_cases.id'), index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'), index=True)
    filename: Mapped[str] = mapped_column(String(160))
    content_type: Mapped[str] = mapped_column(String(80))
    bytes_size: Mapped[int] = mapped_column(Integer)
    sha256: Mapped[str] = mapped_column(String(64))
    internal_path: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(32), default='STORED_UNVERIFIED')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

class AuditEvent(Base):
    __tablename__ = 'audit_events'
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=uid)
    actor_id: Mapped[str] = mapped_column(String(32), index=True)
    action: Mapped[str] = mapped_column(String(60))
    object_type: Mapped[str] = mapped_column(String(32))
    object_id: Mapped[str] = mapped_column(String(32))
    details: Mapped[str] = mapped_column(Text, default='{}')
    previous_hash: Mapped[str] = mapped_column(String(64))
    event_hash: Mapped[str] = mapped_column(String(64), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

# V2: stored financial investigations and immutable sandbox transaction history.
class Extraction(Base):
    __tablename__ = 'invoice_extractions'
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=uid)
    case_id: Mapped[str] = mapped_column(ForeignKey('payment_cases.id'), index=True)
    document_id: Mapped[str] = mapped_column(ForeignKey('documents.id'), unique=True)
    owner_id: Mapped[str] = mapped_column(ForeignKey('users.id'), index=True)
    engine: Mapped[str] = mapped_column(String(70))
    document_hash: Mapped[str] = mapped_column(String(64))
    fields_json: Mapped[str] = mapped_column(Text)
    issues_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

class Investigation(Base):
    __tablename__ = 'investigations'
    id: Mapped[str] = mapped_column(String(32),primary_key=True,default=uid)
    case_id: Mapped[str] = mapped_column(ForeignKey('payment_cases.id'), index=True)
    owner_id: Mapped[str] = mapped_column(ForeignKey('users.id'),index=True)
    extraction_id: Mapped[str] = mapped_column(ForeignKey('invoice_extractions.id'))
    state: Mapped[str] = mapped_column(String(40))
    result_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=utcnow)

class Quote(Base):
    __tablename__ = 'payment_quotes'
    id: Mapped[str] = mapped_column(String(32),primary_key=True,default=uid)
    case_id: Mapped[str] = mapped_column(ForeignKey('payment_cases.id'),index=True)
    owner_id: Mapped[str] = mapped_column(ForeignKey('users.id'),index=True)
    investigation_id: Mapped[str] = mapped_column(ForeignKey('investigations.id'))
    evidence_hash: Mapped[str] = mapped_column(String(64))
    provider: Mapped[str] = mapped_column(String(90))
    beneficiary_id: Mapped[str] = mapped_column(String(90))
    recipient: Mapped[str] = mapped_column(String(160))
    amount: Mapped[str] = mapped_column(String(32))
    currency: Mapped[str] = mapped_column(String(3))
    source_amount: Mapped[str] = mapped_column(String(32))
    source_currency: Mapped[str] = mapped_column(String(3),default='BDT')
    synthetic_rate: Mapped[str] = mapped_column(String(32))
    synthetic_fee: Mapped[str] = mapped_column(String(32))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=utcnow)

class PaymentApproval(Base):
    __tablename__ = 'payment_approvals'
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=uid)
    case_id: Mapped[str] = mapped_column(ForeignKey('payment_cases.id'),index=True)
    owner_id: Mapped[str] = mapped_column(ForeignKey('users.id'),index=True)
    quote_id: Mapped[str] = mapped_column(ForeignKey('payment_quotes.id'),unique=True)
    fingerprint: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(30),default='ACTIVE')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=utcnow)

class SandboxAccount(Base):
    __tablename__ = 'sandbox_accounts'
    id: Mapped[str] = mapped_column(String(32), primary_key=True,default=uid)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'),index=True)
    currency: Mapped[str] = mapped_column(String(3),default='BDT')
    balance: Mapped[str] = mapped_column(String(32),default='3000000.00')
    is_synthetic: Mapped[bool] = mapped_column(Boolean,default=True)
    __table_args__ = (__import__('sqlalchemy').UniqueConstraint('user_id','currency',name='uq_sandbox_account_owner_currency'),)

class SandboxTransfer(Base):
    __tablename__ = 'sandbox_transfers'
    id: Mapped[str] = mapped_column(String(32),primary_key=True,default=uid)
    owner_id: Mapped[str] = mapped_column(ForeignKey('users.id'),index=True)
    case_id: Mapped[str] = mapped_column(ForeignKey('payment_cases.id'),index=True)
    quote_id: Mapped[str] = mapped_column(ForeignKey('payment_quotes.id'),index=True)
    approval_id: Mapped[str] = mapped_column(ForeignKey('payment_approvals.id'))
    idempotency_key: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(30))
    requested_outcome: Mapped[str] = mapped_column(String(24))
    debit_amount: Mapped[str] = mapped_column(String(32))
    paid_amount: Mapped[str] = mapped_column(String(32))
    paid_currency: Mapped[str] = mapped_column(String(3))
    provider_reference: Mapped[str] = mapped_column(String(80),unique=True)
    result_json: Mapped[str] = mapped_column(Text, default='{}')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=utcnow,onupdate=utcnow)
    __table_args__ = (__import__('sqlalchemy').UniqueConstraint('owner_id','idempotency_key',name='uq_sandbox_owner_idempotency'),
                      __import__('sqlalchemy').UniqueConstraint('approval_id',name='uq_sandbox_approval_once'))

class LedgerEntry(Base):
    __tablename__ = 'sandbox_ledger'
    id: Mapped[str] = mapped_column(String(32), primary_key=True,default=uid)
    transfer_id: Mapped[str] = mapped_column(ForeignKey('sandbox_transfers.id'),index=True)
    account_id: Mapped[str] = mapped_column(String(60))
    currency: Mapped[str] = mapped_column(String(3))
    signed_amount: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=utcnow)

class Notification(Base):
    __tablename__ = 'notifications'
    id: Mapped[str] = mapped_column(String(32),primary_key=True,default=uid)
    owner_id: Mapped[str] = mapped_column(ForeignKey('users.id'),index=True)
    case_id: Mapped[str] = mapped_column(ForeignKey('payment_cases.id'),index=True)
    message: Mapped[str] = mapped_column(String(255))
    code: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=utcnow)


# V3 additive tables. Existing V2 payment/approval rows are retained but
# cannot execute without a V3 evidence seal and freshly bound authorization.
class EvidenceSeal(Base):
    __tablename__='bpce_evidence_seals'
    id: Mapped[str] = mapped_column(String(32),primary_key=True,default=uid)
    quote_id: Mapped[str] = mapped_column(ForeignKey('payment_quotes.id'),unique=True,index=True)
    case_id: Mapped[str] = mapped_column(ForeignKey('payment_cases.id'),index=True)
    owner_id: Mapped[str] = mapped_column(ForeignKey('users.id'),index=True)
    snapshot_json: Mapped[str] = mapped_column(Text)
    snapshot_sha256: Mapped[str] = mapped_column(String(64),index=True)
    engine_version: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=utcnow)

class ReviewTicket(Base):
    __tablename__='bpce_review_tickets'
    id: Mapped[str] = mapped_column(String(32),primary_key=True,default=uid)
    case_id: Mapped[str] = mapped_column(ForeignKey('payment_cases.id'),index=True)
    owner_id: Mapped[str] = mapped_column(ForeignKey('users.id'),index=True)
    status: Mapped[str] = mapped_column(String(24),default='PENDING')
    reason: Mapped[str] = mapped_column(String(240))
    reviewer_id: Mapped[str | None] = mapped_column(String(32),nullable=True)
    decision_note: Mapped[str] = mapped_column(Text,default='')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=utcnow,onupdate=utcnow)


class DisputeCase(Base):
    """Student synthetic support case, never a provider dispute/refund."""
    __tablename__ = 'synthetic_support_cases'
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=uid)
    owner_id: Mapped[str] = mapped_column(ForeignKey('users.id'), index=True)
    case_id: Mapped[str] = mapped_column(ForeignKey('payment_cases.id'), index=True)
    transfer_id: Mapped[str] = mapped_column(ForeignKey('sandbox_transfers.id'), index=True)
    category: Mapped[str] = mapped_column(String(40))
    message: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default='OPEN')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

# V5.1: persistent conversation records, tenant-scoped; no bank secrets are stored.
class AgentConversation(Base):
    __tablename__ = 'agent_conversations'
    id: Mapped[str] = mapped_column(String(32),primary_key=True,default=uid)
    owner_id: Mapped[str] = mapped_column(ForeignKey('users.id'),index=True)
    case_id: Mapped[str] = mapped_column(ForeignKey('payment_cases.id'),index=True)
    messages_json: Mapped[str] = mapped_column(Text,default='[]')
    last_tool_trace_json: Mapped[str] = mapped_column(Text,default='[]')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=utcnow)


class RouteAssessment(Base):
    """Persisted evidence diagnostics. Never a payment approval or attestation."""
    __tablename__='route_assessments'
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=uid)
    case_id: Mapped[str] = mapped_column(ForeignKey('payment_cases.id'),index=True)
    owner_id: Mapped[str] = mapped_column(ForeignKey('users.id'),index=True)
    result_json: Mapped[str] = mapped_column(Text)
    result_sha256: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=utcnow)
