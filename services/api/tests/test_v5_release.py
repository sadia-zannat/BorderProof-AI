"""V5 new functionality: never initiates a provider payment/refund."""
import hashlib, json
from sqlalchemy import select
from .conftest import sign_in
from .test_finance import setup, investigate, prepare, pay, post
from app.db import SessionLocal
from app.models import DisputeCase, AuditEvent, SandboxTransfer

def test_release_capabilities(client):
    sign_in(client)
    d=client.get('/api/v1/release/capabilities').json()
    assert not d['real_money_enabled']
    assert 'NOT_SUITABLE' in d['production_readiness']

def test_safe_plan_increments_without_executing(client):
    csrf,case,doc=setup(client)
    path=f'/api/v1/cases/{case}/safe-plan'
    plan=client.get(path).json()
    assert plan['recommended_next_step']=='EXTRACT_LATEST_DOCUMENT'
    assert not plan['executed_actions'] and not plan['requested_authorization']
    x,i=investigate(client,csrf,case,doc)
    plan=client.get(path).json()
    assert plan['recommended_next_step']=='COMPARE_SYNTHETIC_QUOTES'
    assert client.get(f'/api/v1/cases/{case}/transfers').json()['items']==[]

def test_safe_plan_unsupported_demo_corridor_blocked(client):
    csrf=sign_in(client)
    c=post(client,'/api/v1/cases',{'title':'Test','institution':'Synthetic University',
        'destination_country':'United Kingdom','amount':'300.00','currency':'USD'},csrf)
    assert c.status_code==201
    plan=client.get(f"/api/v1/cases/{c.json()['id']}/safe-plan").json()
    assert plan['recommended_next_step']=='REVIEW_DEMO_CORRIDOR'

def test_export_sha256_exact_and_local_no_provider(client):
    csrf,case,x,i,q,a=prepare(client)
    t=pay(client,csrf,case,a).json()
    response=client.get(f"/api/v1/transfers/{t['id']}/evidence-export")
    assert response.status_code==200
    assert response.headers['Cache-Control']=='no-store'
    assert 'attachment' in response.headers['Content-Disposition']
    item=response.json();raw=json.dumps(item['evidence'],sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
    assert hashlib.sha256(raw).hexdigest()==item['evidence_sha256']
    assert not item['evidence']['provenance']['provider_settlement_verified']
    assert not item['evidence']['provenance']['real_payment']
    assert item['evidence']['local_audit_chain_valid']
    assert len(item['evidence']['ledger'])==2

def test_export_failed_never_fabricates_settlement(client):
    csrf,case,x,i,q,a=prepare(client)
    t=pay(client,csrf,case,a,outcome='TIMEOUT').json()
    d=client.get(f"/api/v1/transfers/{t['id']}/evidence-export").json()['evidence']
    assert d['transfer']['status']=='UNKNOWN'
    assert d['ledger']==[]
    assert d['provenance']['real_payment'] is False

def test_export_tenant_auth_and_role(client):
    csrf,case,x,i,q,a=prepare(client)
    t=pay(client,csrf,case,a).json()
    path=f"/api/v1/transfers/{t['id']}/evidence-export"
    assert client.get(path).status_code==200
    client.post('/api/v1/auth/logout',headers={'X-CSRF-Token':csrf})
    assert client.get(path).status_code==401
    sign_in(client,'reviewer')
    assert client.get(path).status_code==403

def test_dispute_create_listing_no_transfer_state_change(client):
    csrf,case,x,i,q,a=prepare(client)
    t=pay(client,csrf,case,a).json()
    r=post(client,'/api/v1/support/disputes',{
        'transfer_id':t['id'],'category':'REFUND_GUIDANCE',
        'message':'Please explain the synthetic receipt and possible recovery steps.'},csrf)
    assert r.status_code==201, r.text
    assert r.json()['status']=='OPEN'
    assert 'NO_BANK_DISPUTE' in r.json()['mode']
    assert len(client.get('/api/v1/support/disputes').json()['items'])==1
    assert client.get(f"/api/v1/transfers/{t['id']}/receipt").json()['transfer']['status']=='COMPLETED'
    with SessionLocal() as db:
        assert len(db.scalars(select(DisputeCase)).all())==1

def test_dispute_duplicate_and_cross_tenant_protected(client):
    csrf,case,x,i,q,a=prepare(client)
    t=pay(client,csrf,case,a).json()
    payload={'transfer_id':t['id'],'category':'OTHER','message':'This is a synthetic payment status question.'}
    assert post(client,'/api/v1/support/disputes',payload,csrf).status_code==201
    assert post(client,'/api/v1/support/disputes',payload,csrf).status_code==409
    client.post('/api/v1/auth/logout',headers={'X-CSRF-Token':csrf})
    sign_in(client,'reviewer')
    assert client.get('/api/v1/support/disputes').status_code==403
    client.post('/api/v1/auth/logout',headers={'X-CSRF-Token':client.get('/api/v1/auth/me').json()['csrf_token']})
    from app.models import User
    from app.security import password_hash
    with SessionLocal() as db:
        db.add(User(email='other@test.com',name='Another',role='student',password_hash=password_hash('A-Long-Test-Password!')));db.commit()
    csrf2=client.post('/api/v1/auth/login',json={'email':'other@test.com','password':'A-Long-Test-Password!'}).json()['csrf_token']
    assert client.get(f"/api/v1/transfers/{t['id']}/evidence-export").status_code==404
    assert post(client,'/api/v1/support/disputes',payload,csrf2).status_code==404
    assert client.get('/api/v1/support/disputes').json()['items']==[]

def test_support_input_constraints_and_csrf(client):
    csrf,case,x,i,q,a=prepare(client)
    t=pay(client,csrf,case,a).json()
    payload={'transfer_id':t['id'],'category':'REFUND_GUIDANCE','message':'Can you help me check the simulation?'}
    assert client.post('/api/v1/support/disputes',json=payload).status_code==403
    assert post(client,'/api/v1/support/disputes',{**payload,'category':'ISSUE_REAL_BANK_REFUND'},csrf).status_code==422
    assert post(client,'/api/v1/support/disputes',{**payload,'message':'a'},csrf).status_code==422

def test_v5_sensitive_headers_are_present(client):
    sign_in(client)
    response=client.get('/api/v1/release/capabilities')
    assert response.status_code==200
    assert response.headers.get('Cache-Control')=='no-store'
    assert response.headers.get('X-Content-Type-Options')=='nosniff'
    assert response.headers.get('X-Frame-Options')=='DENY'
    assert response.headers.get('Referrer-Policy')=='no-referrer'

def test_production_rejects_seeded_demo_credentials(monkeypatch):
    import pytest
    from fastapi.testclient import TestClient
    from app.main import app
    monkeypatch.setenv('APP_ENV','production')
    monkeypatch.setenv('ENABLE_DEMO_SEED','1')
    with pytest.raises(RuntimeError,match='Production cannot seed demonstration credentials'):
        with TestClient(app):pass
