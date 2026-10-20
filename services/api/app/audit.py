"""Hash-linked local audit history (NOT a signed or externally anchored ledger)."""
import hashlib, json
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import AuditEvent

def append_event(db: Session, actor: str, action: str, target_type: str, target_id: str, details: dict|None=None):
    # Flush earlier events/writes before reading the head. SQLite's writer lock
    # serializes this read-and-append across processes, including login events.
    db.flush()
    if db.bind.dialect.name == 'sqlite':
        connection=db.connection()
        if not connection.connection.driver_connection.in_transaction:
            connection.exec_driver_sql('BEGIN IMMEDIATE')
    elif db.bind.dialect.name == 'postgresql':
        from sqlalchemy import text
        db.execute(text('SELECT pg_advisory_xact_lock(53425353)'))
    previous = db.scalar(select(AuditEvent).order_by(AuditEvent.created_at.desc(),AuditEvent.id.desc()).limit(1))
    prevhash = previous.event_hash if previous else 'GENESIS'
    data = json.dumps({'actor':actor,'action':action,'target_type':target_type,'target_id':target_id,'details':details or {},'prev':prevhash},sort_keys=True,separators=(',',':'))
    rec=AuditEvent(actor_id=actor,action=action,object_type=target_type,object_id=target_id,details=json.dumps(details or {}),previous_hash=prevhash,event_hash=hashlib.sha256(data.encode()).hexdigest())
    db.add(rec)
    db.flush()
    return rec


def verify_event_chain(db: Session):
    """Verify all local event hashes, references, fork freedom and chain completeness.

    SHA-256 linking is tamper-evident only while the root database itself is trusted;
    a DB administrator can rebuild or replace an entire chain.
    """
    events=db.scalars(select(AuditEvent)).all()
    by_hash={e.event_hash:e for e in events}
    errors=[]; children={}
    if len(by_hash)!=len(events):errors.append('DUPLICATE_EVENT_HASH')
    for e in events:
        try:
            d=json.loads(e.details)
            value=json.dumps({'actor':e.actor_id,'action':e.action,'target_type':e.object_type,
                              'target_id':e.object_id,'details':d,'prev':e.previous_hash},
                             sort_keys=True,separators=(',',':'))
            expected=hashlib.sha256(value.encode()).hexdigest()
            if expected!=e.event_hash:errors.append('EVENT_HASH_MISMATCH:'+e.id)
        except (ValueError,TypeError):errors.append('INVALID_EVENT_DETAILS:'+e.id)
        if e.previous_hash!='GENESIS' and e.previous_hash not in by_hash:
            errors.append('MISSING_PARENT:'+e.id)
        children.setdefault(e.previous_hash,[]).append(e.event_hash)
    if events and len(children.get('GENESIS',[]))!=1:errors.append('INVALID_GENESIS_COUNT')
    if any(len(v)>1 for v in children.values()):errors.append('CHAIN_FORK')
    if events:
        seen=set();cursor=children.get('GENESIS',[None])[0] if children.get('GENESIS') else None
        while cursor and cursor not in seen:
            seen.add(cursor);cursor=children.get(cursor,[None])[0] if children.get(cursor) else None
        if cursor in seen:errors.append('CHAIN_CYCLE')
        if len(seen)!=len(events):errors.append('UNREACHABLE_EVENTS')
    return {'valid':not errors,'events_checked':len(events),'issues':sorted(set(errors)),
            'integrity_type':'UNANCHORED_LOCAL_SHA256_HASH_CHAIN',
            'caveat':'Not signed and not anchored externally; DB administrator could rewrite the full history.'}
