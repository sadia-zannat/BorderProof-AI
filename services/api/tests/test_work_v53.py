"""New independent technical regression cases. Synthetic inputs; no live model mocks here."""
import json
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from sqlalchemy import select
from fastapi.testclient import TestClient
from .conftest import sign_in
from .test_finance import setup, investigate, prepare, post, pay, SAMPLE
from app.main import app
from app.db import SessionLocal
from app.models import Quote, LedgerEntry, SandboxTransfer, User
from app.finance import extract_fields
from app.audit import append_event, verify_event_chain
import pytest


@pytest.mark.parametrize('label,value', [('Amount','900.00'),('Currency','USD'),
    ('Account','ATTACKER-ACCOUNT'),('Institution','Conflicting University')])
def test_contradictory_duplicate_labels_are_issues(label,value):
    fields, issues = extract_fields(SAMPLE.decode()+f'\n{label}: {value}\n')
    assert 'CONFLICTING_'+label.upper() in issues


@pytest.mark.parametrize('value',['1,2,500.00','12500.001','-12500','NaN'])
def test_malformed_amount_never_silently_normalizes(value):
    _, issues=extract_fields(SAMPLE.decode().replace('12500.00',value))
    assert 'INVALID_AMOUNT' in issues


def test_lowercase_currency_normalized():
    fields,issues=extract_fields(SAMPLE.decode().replace('GBP','gbp'))
    assert fields['currency']['value']=='GBP'
    assert not issues


def test_impossible_calendar_date_asks_clarification():
    import re
    _,issues=extract_fields(re.sub(r'\d{4}-\d\d-\d\d','2026-02-30',SAMPLE.decode()))
    assert 'INVALID_DEADLINE' in issues


def test_conflicting_invoice_investigation_cannot_clear(client):
    token,c,d=setup(client,txt=SAMPLE+b'\nAccount: ATTACKER-ACCOUNT\n')
    x,i=investigate(client,token,c,d)
    assert i['state']!='SANDBOX_FIXTURE_MATCH'
    assert i['clarification_questions']
    assert post(client,f'/api/v1/cases/{c}/quotes',{'investigation_id':i['id']},token).status_code==409


def test_old_invoice_cannot_be_requoted_after_new_document(client):
    token,c,x,i,q,a=prepare(client)
    r=client.post('/api/v1/documents',data={'case_id':c},files={'file':('new.txt',SAMPLE+b'\nAccount: EVIL\n','text/plain')},headers={'X-CSRF-Token':token})
    assert r.status_code==201
    assert post(client,f'/api/v1/cases/{c}/quotes',{'investigation_id':i['id']},token).status_code==409


def test_safe_plan_points_at_latest_document(client):
    token,c,x,i,q,a=prepare(client)
    r=client.post('/api/v1/documents',data={'case_id':c},files={'file':('latest.txt',SAMPLE,'text/plain')},headers={'X-CSRF-Token':token})
    assert r.status_code==201
    result=client.get(f'/api/v1/cases/{c}/safe-plan').json()
    assert result['recommended_next_step']=='EXTRACT_LATEST_DOCUMENT'


def test_idempotency_key_rejects_changed_outcome(client):
    token,c,x,i,q,a=prepare(client)
    assert pay(client,token,c,a,outcome='TIMEOUT').json()['status']=='UNKNOWN'
    assert pay(client,token,c,a,outcome='SUCCESS').status_code==409


def test_reconciliation_uses_immutable_transfer_debit(client):
    token,c,x,i,q,a=prepare(client)
    t=pay(client,token,c,a,outcome='TIMEOUT').json()
    with SessionLocal() as db:
        db.get(Quote,q['id']).source_amount='0.01';db.commit()
    r=post(client,f"/api/v1/transfers/{t['id']}/reconcile",{'simulated_confirmation':'CONFIRMED_SUCCESS'},token)
    assert r.status_code==200
    assert Decimal(client.get('/api/v1/finance/account').json()['balance'])==Decimal('3000000')-Decimal(t['source_debit'])


def test_concurrent_reconciliation_debits_once(client):
    token,c,x,i,q,a=prepare(client)
    t=pay(client,token,c,a,outcome='TIMEOUT').json()
    cookie=client.cookies.get('bp_session')
    def worker(_):
        with TestClient(app) as other:
            other.cookies.set('bp_session',cookie)
            return post(other,f"/api/v1/transfers/{t['id']}/reconcile",{'simulated_confirmation':'CONFIRMED_SUCCESS'},token).status_code
    with ThreadPoolExecutor(max_workers=4) as pool:
        statuses=list(pool.map(worker,range(4)))
    assert statuses.count(200)==1 and statuses.count(409)==3, statuses
    with SessionLocal() as db:
        assert len(db.scalars(select(LedgerEntry).where(LedgerEntry.transfer_id==t['id'])).all())==2


def test_audit_multiple_events_in_same_transaction_do_not_fork(client):
    with SessionLocal() as db:
        append_event(db,'local','ONE','test','one')
        append_event(db,'local','TWO','test','two')
        db.commit()
        assert verify_event_chain(db)['valid']


def test_refreshing_session_does_not_break_other_tab_csrf(client):
    token=sign_in(client)
    assert client.get('/api/v1/auth/me').status_code==200
    assert post(client,'/api/v1/cases',{'title':'Fresh other tab','institution':'Fresh University','destination_country':'Canada','amount':'123.45','currency':'CAD'},token).status_code==201


def test_malformed_model_envelope_fails_safely(client,monkeypatch):
    from app import local_agent
    token,c,d=setup(client)
    monkeypatch.setattr(local_agent,'ollama_chat',lambda *_:{'message':None})
    result=post(client,f'/api/v1/cases/{c}/agent/chat',{'message':'Inspect this new case.'},token)
    assert result.status_code==502


def test_model_tool_name_must_be_string(client,monkeypatch):
    from app import local_agent
    token,c,d=setup(client)
    outputs=iter([{'message':{'tool_calls':[{'function':{'name':{},'arguments':{}}}]}}, {'message':{'content':'No authority.'}}])
    monkeypatch.setattr(local_agent,'ollama_chat',lambda *_:next(outputs))
    result=post(client,f'/api/v1/cases/{c}/agent/chat',{'message':'Inspect this new case.'},token)
    assert result.status_code==200 and result.json()['tool_trace'][0]['status']=='REJECTED'


def test_signup_cannot_choose_privileged_role(client,monkeypatch):
    monkeypatch.setenv('ENABLE_LOCAL_SIGNUP','1')
    monkeypatch.setenv('APP_ENV','development')
    r=client.post('/api/v1/auth/register',json={'email':'new-student@example.test','name':'Local Student','password':'Only-For-Local-Tests-2026!','role':'admin'})
    assert r.status_code==422


def test_signup_creates_only_local_student(client,monkeypatch):
    monkeypatch.setenv('ENABLE_LOCAL_SIGNUP','1')
    monkeypatch.setenv('APP_ENV','development')
    r=client.post('/api/v1/auth/register',json={'email':'new-student@example.test','name':'Local Student','password':'Only-For-Local-Tests-2026!'})
    assert r.status_code==201 and r.json()['role']=='student'
    assert client.post('/api/v1/auth/login',json={'email':'new-student@example.test','password':'Only-For-Local-Tests-2026!'}).status_code==200


def test_production_registration_is_disabled(client,monkeypatch):
    monkeypatch.setenv('ENABLE_LOCAL_SIGNUP','1');monkeypatch.setenv('APP_ENV','production')
    assert client.post('/api/v1/auth/register',json={'email':'new@example.test','name':'New Student','password':'Local-Long-Password-Only!'}).status_code==403


def test_concurrent_execute_same_idempotency_debits_once(client):
    token,c,x,i,q,a=prepare(client);cookie=client.cookies.get('bp_session')
    def worker(_):
        with TestClient(app) as other:
            other.cookies.set('bp_session',cookie)
            result=pay(other,token,c,a,key='concurrent-native-equivalent')
            assert result.status_code==200,result.text
            return result.json()['id']
    with ThreadPoolExecutor(max_workers=6) as pool:ids=list(pool.map(worker,range(6)))
    assert len(set(ids))==1
    with SessionLocal() as db:
        assert len(db.scalars(select(SandboxTransfer)).all())==1
        assert len(db.scalars(select(LedgerEntry)).all())==2
        assert verify_event_chain(db)['valid']


def test_session_csrf_cannot_be_reused_after_new_login(client):
    old=sign_in(client);new=sign_in(client)
    assert old!=new
    assert client.post('/api/v1/auth/logout',headers={'X-CSRF-Token':old}).status_code==403
    assert client.post('/api/v1/auth/logout',headers={'X-CSRF-Token':new}).status_code==200


def test_external_provider_adapters_fail_without_network():
    from app.provider_adapters import WISE_SANDBOX,AIRWALLEX_SANDBOX,ExternalSandboxBlocked
    for adapter in (WISE_SANDBOX,AIRWALLEX_SANDBOX):
        assert adapter.capabilities()['connected'] is False
        with pytest.raises(ExternalSandboxBlocked):adapter.read_transfer('invented-reference')


def test_reference_fx_validated_as_read_only(monkeypatch):
    from app.references import fetch_reference_fx
    import httpx
    body=b'{"base":"EUR","date":"2026-10-01","rates":{"GBP":0.84205}}'
    monkeypatch.setattr(httpx,'get',lambda *a,**k:httpx.Response(200,content=body,request=httpx.Request('GET','https://api.frankfurter.dev/v1/latest')))
    value=fetch_reference_fx()
    assert value['rates']['GBP']=='0.84205' and value['retrieved_at_utc']
    assert value['verified_execution_quote'] is False and value['fallback_used'] is False


def test_reference_fx_rejects_injected_response(monkeypatch):
    from app.references import fetch_reference_fx
    from fastapi import HTTPException
    import httpx
    monkeypatch.setattr(httpx,'get',lambda *a,**k:httpx.Response(200,json={'base':'EUR','date':'2026-10-01','rates':{'GBP':-1}},request=httpx.Request('GET','https://api.frankfurter.dev/v1/latest')))
    with pytest.raises(HTTPException) as e:fetch_reference_fx()
    assert e.value.status_code==503


def test_private_document_path_cannot_escape_root(client):
    from app.storage import configured_storage
    with pytest.raises(ValueError):configured_storage().resolve('/etc/passwd')


def test_persisted_quote_expiry_has_explicit_utc_offset(client):
    token,c,x,i,q,a=prepare(client)
    read=client.get(f'/api/v1/cases/{c}/quotes').json()['items'][0]
    assert read['expires_at'].endswith('+00:00')
    assert read['expires_at']==q['expires_at']


def test_reference_transport_configuration_error_stays_unavailable(monkeypatch):
    from app.references import fetch_reference_fx
    from fastapi import HTTPException
    import httpx
    def missing_proxy(*args,**kwargs):raise ImportError('SOCKS transport unavailable')
    monkeypatch.setattr(httpx,'get',missing_proxy)
    with pytest.raises(HTTPException) as e:fetch_reference_fx()
    assert e.value.status_code==503
