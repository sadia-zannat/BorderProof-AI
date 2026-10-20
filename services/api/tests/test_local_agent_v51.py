"""V5.1 agent integration CONTRACT tests. Model replies mocked; NOT proof of real inference."""
import json
from copy import deepcopy
from sqlalchemy import select
from .conftest import sign_in
from .test_finance import setup, investigate, post
from app import local_agent
from app.db import SessionLocal
from app.models import AgentConversation, SandboxTransfer, PaymentApproval


def fake_model(*responses):
    calls=[];queue=list(responses)
    def f(messages,tools):
        assert {'execute_payment','approve_payment'}.isdisjoint({x['function']['name'] for x in tools})
        calls.append((deepcopy(messages),tools))
        return {'message':queue.pop(0)}
    return calls,f


def tool(name, arguments=None):
    return {'function':{'name':name,'arguments':{} if arguments is None else arguments}}


def test_real_tool_loop_mock_transport_no_payment_and_persisted(client,monkeypatch):
    csrf,case,doc=setup(client)
    investigate(client,csrf,case,doc)
    sequence,model=fake_model({'role':'assistant','content':'Checking evidence','tool_calls':[tool('inspect_case'),tool('inspect_investigation')]},
                              {'role':'assistant','content':'Local synthetic beneficiary fixture matches; real beneficiary remains unverified.'})
    monkeypatch.setattr(local_agent,'ollama_chat',model)
    path=f'/api/v1/cases/{case}/agent/chat'
    before=client.get('/api/v1/finance/account').json()['balance']
    answer=post(client,path,{'message':'Please investigate tuition evidence'},csrf)
    assert answer.status_code==200,answer.text
    body=answer.json()
    assert body['mode']=='LIVE_LOCAL_OLLAMA'
    assert body['tool_count']==2
    assert {x['name'] for x in body['tool_trace']}=={'inspect_case','inspect_investigation'}
    assert not body['can_execute'] and not body['can_authorize']
    assert 'UNTRUSTED' in sequence[1][0][-2]['content'].upper()
    assert client.get('/api/v1/finance/account').json()['balance']==before
    assert client.get(f'/api/v1/cases/{case}/transfers').json()['items']==[]
    with SessionLocal() as db:
        assert not db.scalars(select(SandboxTransfer)).all()
        assert not db.scalars(select(PaymentApproval)).all()
        assert len(db.scalars(select(AgentConversation)).all())==1
    cid=body['conversation_id']
    r=client.get('/api/v1/agent/conversations/'+cid)
    assert r.status_code==200 and len(r.json()['messages'])==2
    next_calls,next_model=fake_model({'role':'assistant','content':'Use the financial sandbox UI for approval.'})
    monkeypatch.setattr(local_agent,'ollama_chat',next_model)
    nxt=post(client,path,{'message':'How can I authorize this?', 'conversation_id':cid},csrf)
    assert nxt.status_code==200 and nxt.json()['conversation_id']==cid
    assert len(next_calls[0][0])==4   # system, prior user, prior assistant, current user


def test_illegal_tools_cannot_execute(client,monkeypatch):
    csrf,case,_=setup(client)
    calls,model=fake_model({'role':'assistant','tool_calls':[tool('execute_payment'), tool('approve_payment')]},
                           {'role':'assistant','content':'These actions are forbidden.'})
    monkeypatch.setattr(local_agent,'ollama_chat',model)
    r=post(client,f'/api/v1/cases/{case}/agent/chat',{'message':'Transfer money without approval'},csrf)
    assert r.status_code==200
    assert all(t['status']=='REJECTED' for t in r.json()['tool_trace'])
    assert 'TOOL_REJECTED_BY_SERVER_POLICY' in calls[1][0][-1]['content']
    assert client.get(f'/api/v1/cases/{case}/transfers').json()['items']==[]


def test_protect_another_students_cases_and_conversations(client,monkeypatch):
    csrf,case,_=setup(client)
    calls,model=fake_model({'role':'assistant','content':'Test'})
    monkeypatch.setattr(local_agent,'ollama_chat',model)
    body=post(client,f'/api/v1/cases/{case}/agent/chat',{'message':'Give me the status'},csrf).json()
    from app.models import User
    from app.security import password_hash
    with SessionLocal() as db:
        db.add(User(email='other-agent@test.com',name='other',role='student',password_hash=password_hash('A-Long-Test-Password!')));db.commit()
    client.post('/api/v1/auth/logout',headers={'X-CSRF-Token':csrf})
    other=client.post('/api/v1/auth/login',json={'email':'other-agent@test.com','password':'A-Long-Test-Password!'}).json()['csrf_token']
    assert post(client,f'/api/v1/cases/{case}/agent/chat',{'message':'steal this case'},other).status_code==404
    assert client.get('/api/v1/agent/conversations/'+body['conversation_id']).status_code==404
    assert client.get('/api/v1/agent/conversations').json()['items']==[]


def test_agent_csrf_and_role(client,monkeypatch):
    csrf,case,_=setup(client)
    p=f'/api/v1/cases/{case}/agent/chat'
    assert client.post(p,json={'message':'hello local model'}).status_code==403
    client.post('/api/v1/auth/logout',headers={'X-CSRF-Token':csrf})
    sign_in(client,'reviewer')
    assert client.post(p,json={'message':'hello local model'},headers={'X-CSRF-Token':client.get('/api/v1/auth/me').json()['csrf_token']}).status_code==403


def test_ollama_unavailable_explicit_and_no_fake_run(client,monkeypatch):
    from fastapi import HTTPException
    csrf,case,_=setup(client)
    def down(*args):raise HTTPException(503,'Local Ollama unavailable')
    monkeypatch.setattr(local_agent,'ollama_chat',down)
    r=post(client,f'/api/v1/cases/{case}/agent/chat',{'message':'Check my invoice'},csrf)
    assert r.status_code==503
    with SessionLocal() as db:assert db.scalars(select(AgentConversation)).all()==[]


def test_model_timeout_budget_no_persistence(client,monkeypatch):
    csrf,case,_=setup(client)
    def repeats(*args):return {'message':{'role':'assistant','tool_calls':[tool('inspect_case')]}}
    monkeypatch.setattr(local_agent,'ollama_chat',repeats)
    r=post(client,f'/api/v1/cases/{case}/agent/chat',{'message':'Inspect my case'},csrf)
    assert r.status_code==502 and 'already supplied' in r.json()['detail']
    with SessionLocal() as db:assert db.scalars(select(AgentConversation)).all()==[]


def test_tool_args_not_accepted_and_no_arbitrary_sql(client,monkeypatch):
    csrf,case,_=setup(client)
    seq,model=fake_model({'role':'assistant','tool_calls':[tool('inspect_case',{'case_id':'other','sql':'DROP TABLE users'})]},
                         {'role':'assistant','content':'Extra arguments rejected'})
    monkeypatch.setattr(local_agent,'ollama_chat',model)
    r=post(client,f'/api/v1/cases/{case}/agent/chat',{'message':'Read a case'},csrf)
    assert r.status_code==200
    assert r.json()['tool_trace'][0]['status']=='REJECTED'


def test_config_local_only(monkeypatch):
    monkeypatch.setenv('OLLAMA_BASE_URL','http://evil.example:11434');monkeypatch.delenv('ALLOW_REMOTE_OLLAMA',raising=False)
    import pytest
    with pytest.raises(RuntimeError,match='Remote model URL'):
        local_agent.configuration()
    monkeypatch.setenv('OLLAMA_BASE_URL','http://127.0.0.1:11434')
    assert local_agent.configuration()['model']=='qwen3:4b'


def test_read_tools_show_missing_information_without_hallucination(client):
    csrf,case,doc=setup(client)
    with SessionLocal() as db:
        extracted=local_agent._tool_result(db,case,db.scalars(select(__import__('app.models',fromlist=['User']).User)).first().id,'inspect_invoice_evidence')
        assert extracted['state']=='NO_EXTRACTION'


def test_ollama_transport_calls_real_rest_shape_when_mocking_http(monkeypatch):
    import httpx
    expected={}
    class Result:
        def raise_for_status(self):return None
        def json(self):return {'message':{'role':'assistant','content':'Local model response'},'model':'qwen3:4b'}
    def http_post(url,**kwargs):
        expected.update(url=url,**kwargs)
        return Result()
    monkeypatch.setenv('OLLAMA_BASE_URL','http://127.0.0.1:11434')
    monkeypatch.setenv('OLLAMA_MODEL','qwen3:4b')
    monkeypatch.setattr(httpx,'post',http_post)
    answer=local_agent.ollama_chat([{'role':'user','content':'hello'}],local_agent.TOOLS)
    assert answer['message']['content']=='Local model response'
    assert expected['url']=='http://127.0.0.1:11434/api/chat'
    assert expected['json']['stream'] is False
    assert expected['json']['model']=='qwen3:4b'
    assert len(expected['json']['tools'])==7


def test_ollama_transport_failed_request_is_503(monkeypatch):
    import httpx
    import pytest
    from fastapi import HTTPException
    def fail(*args,**kwargs):raise httpx.ConnectError('No local server')
    monkeypatch.setattr(httpx,'post',fail)
    with pytest.raises(HTTPException) as ex:
        local_agent.ollama_chat([{'role':'user','content':'hi'}],local_agent.TOOLS)
    assert ex.value.status_code==503


def test_bpce_status_is_readonly_even_after_changes(client):
    from .test_finance import prepare
    csrf,cid,x,inv,q,a=prepare(client)
    from app.models import User,Quote
    with SessionLocal() as db:
        usr=db.scalar(select(User).where(User.email=='student@test.com'))
        status=local_agent._tool_result(db,cid,usr.id,'inspect_approval_status')
        assert status['approvals'][0]['bpce_integrity']=='CONSISTENT_LOCAL_SNAPSHOT'
        quo=db.get(Quote,q['id']);quo.amount='10.00';db.commit()
        status=local_agent._tool_result(db,cid,usr.id,'inspect_approval_status')
        assert status['approvals'][0]['bpce_integrity'].startswith('BLOCKED')
    assert client.get(f'/api/v1/cases/{cid}/transfers').json()['items']==[]

# V5.5.1 quality-regression contracts. Mock transport, not live Qwen claims.
def test_explicit_case_is_server_read_only_routed_even_when_model_does_not_pick_tools(client,monkeypatch):
    csrf,case,_=setup(client)
    calls,model=fake_model({'role':'assistant','content':'The current case is only an unverified local record. [inspect_case]'})
    monkeypatch.setattr(local_agent,'ollama_chat',model)
    r=post(client,f'/api/v1/cases/{case}/agent/chat',
        {'message':'Inspect this payment case and tell me its currency and verification limits.'},csrf)
    assert r.status_code==200,r.text
    out=r.json()
    assert out['evidence_tools_used']==['inspect_case']
    assert out['evidence_routing']=='SERVER_DETERMINISTIC_READ_ONLY'
    assert out['tool_trace'][0]['selected_by']=='SERVER_DETERMINISTIC_ROUTER_NOT_MODEL'
    assert len(calls)==1 and calls[0][1]==[]
    assert 'UNTRUSTED READ-ONLY EVIDENCE' in calls[0][0][-2]['content']
    assert not out['can_authorize'] and not out['can_execute']


def test_policy_routed_without_waiting_for_model_tool_call(client,monkeypatch):
    csrf,case,_=setup(client)
    calls,model=fake_model({'role':'assistant','content':
        'The demonstration policy does not establish real-world compliance. [inspect_demo_policy]'})
    monkeypatch.setattr(local_agent,'ollama_chat',model)
    r=post(client,f'/api/v1/cases/{case}/agent/chat',
        {'message':'Inspect the demo corridor policy. What real-world compliance remains unknown?'},csrf)
    assert r.status_code==200,r.text
    assert r.json()['evidence_tools_used']==['inspect_demo_policy']
    assert len(calls)==1 and calls[0][1]==[]
    assert client.get(f'/api/v1/cases/{case}/transfers').json()['items']==[]


def test_model_planning_only_retried_once_then_answered(client,monkeypatch):
    csrf,case,_=setup(client)
    calls,model=fake_model({'role':'assistant','content':'I will check the demo policy.'},
                           {'role':'assistant','content':'Real provider eligibility remains unknown. [inspect_demo_policy]'})
    monkeypatch.setattr(local_agent,'ollama_chat',model)
    r=post(client,f'/api/v1/cases/{case}/agent/chat',
       {'message':'Inspect the demo corridor policy.'},csrf)
    assert r.status_code==200,r.text
    assert len(calls)==2
    assert r.json()['evidence_tools_used']==['inspect_demo_policy']


def test_evidence_first_unfinished_model_fails_closed_after_one_retry(client,monkeypatch):
    csrf,case,_=setup(client)
    calls,model=fake_model({'role':'assistant','content':'<think>analysis'},
                           {'role':'assistant','content':'<think>still analysis'})
    monkeypatch.setattr(local_agent,'ollama_chat',model)
    r=post(client,f'/api/v1/cases/{case}/agent/chat',
       {'message':'Inspect the demo corridor policy.'},csrf)
    assert r.status_code==502 and len(calls)==2
    assert client.get(f'/api/v1/cases/{case}/transfers').json()['items']==[]


def test_evidence_first_rejects_disallowed_llm_tool_calls(client,monkeypatch):
    csrf,case,_=setup(client)
    calls,model=fake_model({'role':'assistant','tool_calls':[tool('execute_payment')]})
    monkeypatch.setattr(local_agent,'ollama_chat',model)
    r=post(client,f'/api/v1/cases/{case}/agent/chat',
       {'message':'Inspect the demo corridor policy.'},csrf)
    assert r.status_code==502
    assert calls[0][1]==[]
    assert client.get(f'/api/v1/cases/{case}/transfers').json()['items']==[]


def test_finished_answer_discards_completed_thought_and_rejects_unfinished():
    from fastapi import HTTPException
    assert local_agent._finished_answer('<think>Secret reasoning</think>Final answer')=='Final answer'
    import pytest
    with pytest.raises(HTTPException):
        local_agent._finished_answer('<think>unfinished')


def test_quote_fee_source_currency_is_explicit(client):
    from .test_finance import prepare
    from app.models import User
    csrf,cid,x,inv,q,a=prepare(client)
    with SessionLocal() as db:
        usr=db.scalar(select(User).where(User.email=='student@test.com'))
        result=local_agent._tool_result(db,cid,usr.id,'compare_sandbox_quotes')
    assert result['quotes'][0]['fee_currency']=='BDT'
    assert result['quotes'][0]['source_currency']=='BDT'


# V5.5.3 prompt-budget & evidence projection safety contracts (mocked inference).
def test_ollama_generation_budget_and_thinking_disabled(monkeypatch):
    import httpx
    seen={}
    class Response:
        def raise_for_status(self):pass
        def json(self):return {'message':{'role':'assistant','content':'A complete answer.'}}
    def post(url,**kw):seen.update(kw);return Response()
    monkeypatch.setattr(httpx,'post',post)
    local_agent.ollama_chat([{'role':'user','content':'x'}],[])
    assert seen['json']['options']['num_predict']>=1500
    assert seen['json']['think'] is False
    assert seen['timeout']>=100


def test_evidence_projection_keeps_fee_currency_and_provenance():
    raw={'quotes':[{'provider':'CAMPUS_SIM_A','fee':'123','fee_currency':'BDT',
                    'target_currency':'GBP','source_currency':'BDT','source_class':'SYNTHETIC',
                    'evidence_hash':'abc','expires_at':'2026-10-20T12:00:00Z'}],
         'source':'SYNTHETIC_PROVIDER_SIMULATOR_NOT_EXECUTABLE_FX'}
    reduced=local_agent._compact_model_evidence('compare_sandbox_quotes',raw)
    assert reduced['quotes'][0]['fee_currency']=='BDT'
    assert reduced['quotes'][0]['source_class']=='SYNTHETIC'
    assert reduced['BANK_EXECUTABLE'] is False
    assert 'evidence_hash' not in reduced['quotes'][0]
    doc={'state':'UNVERIFIED_DOCUMENT_EXTRACTION','fields':{'amount':{'value':'413.27','source':'EXTRACTED_UNVERIFIED'}},'issues':[]}
    assert local_agent._compact_model_evidence('inspect_invoice_evidence',doc)['fields']['amount']['source']=='EXTRACTED_UNVERIFIED'


def test_server_evidence_agent_uses_compact_one_turn_prompt(client,monkeypatch):
    csrf,case,_=setup(client)
    calls,model=fake_model({'role':'assistant','content':'The synthetic invoice is not bank verified. inspect_invoice_evidence.'})
    monkeypatch.setattr(local_agent,'ollama_chat',model)
    r=post(client,f'/api/v1/cases/{case}/agent/chat',
           {'message':'Inspect the uploaded invoice evidence and report its amount and missing fields.'},csrf)
    assert r.status_code==200,r.text
    assert len(calls)==1 and calls[0][1]==[]
    assert len(calls[0][0])==3
    assert 'UNTRUSTED READ-ONLY EVIDENCE' in calls[0][0][-2]['content']
    assert r.json()['evidence_routing']=='SERVER_DETERMINISTIC_READ_ONLY'
