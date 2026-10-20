from io import BytesIO
from .conftest import sign_in

def test_health_and_public_config(client):
    assert client.get('/api/v1/health').json()['execution_mode']=='INTERNAL_SANDBOX_ONLY'
    cfg=client.get('/api/v1/public/config').json()
    assert not cfg['real_payments_enabled']
    assert cfg['supported_locales']==['en','zh-CN','bn-BD']

def test_auth_cookie_me_csrf_logout(client):
    assert client.get('/api/v1/auth/me').status_code==401
    csrf=sign_in(client)
    assert client.get('/api/v1/auth/me').status_code==200
    assert client.post('/api/v1/auth/logout').status_code==403
    # V5.3: GET /me is idempotent. The synchronizer token stays session-bound
    # across tabs; an unrelated token must still be rejected.
    assert client.post('/api/v1/auth/logout',headers={'X-CSRF-Token':'forged-token'}).status_code==403
    csrf=client.get('/api/v1/auth/me').json()['csrf_token']
    assert client.post('/api/v1/auth/logout',headers={'X-CSRF-Token':csrf}).status_code==200
    assert client.get('/api/v1/auth/me').status_code==401

def test_invalid_password(client):
    r=client.post('/api/v1/auth/login',json={'email':'student@test.com','password':'wrong'})
    assert r.status_code==401

def test_cases_created_and_persisted(client):
    csrf=sign_in(client)
    case={'title':'Tuition for year 3','institution':'Example University','destination_country':'United Kingdom','amount':'5000.00','currency':'GBP'}
    assert client.post('/api/v1/cases',json=case).status_code==403
    r=client.post('/api/v1/cases',json=case,headers={'X-CSRF-Token':csrf})
    assert r.status_code==201,r.text
    id=r.json()['id']
    assert r.json()['status']=='DRAFT'
    assert client.get('/api/v1/cases/'+id).status_code==200
    assert len(client.get('/api/v1/cases').json()['items'])==1
    assert client.get('/api/v1/dashboard').json()['cases_total']==1

def test_money_validation_and_corridor(client):
    csrf=sign_in(client)
    base={'title':'Tuition for year 3','institution':'Example University','destination_country':'United Kingdom','currency':'GBP'}
    for amount in ('-3.00','NaN','12.567','1e9999','0','99999999999'):
        r=client.post('/api/v1/cases',json={**base,'amount':amount},headers={'X-CSRF-Token':csrf})
        assert r.status_code==422,(amount,r.text)
    r=client.post('/api/v1/cases',json={**base,'amount':'200','currency':'NZD'},headers={'X-CSRF-Token':csrf})
    assert r.status_code==422

def test_role_separation(client):
    csrf=sign_in(client,'student')
    assert client.get('/api/v1/reviewer/queue').status_code==403
    assert client.get('/api/v1/audit').status_code==403
    assert client.get('/api/v1/admin/summary').status_code==403
    assert client.post('/api/v1/cases',json={'title':'Case One','institution':'Example University','destination_country':'Canada','amount':'12','currency':'CAD'},headers={'X-CSRF-Token':csrf}).status_code==201
    csrf=sign_in(client,'reviewer')
    assert client.get('/api/v1/reviewer/queue').status_code==200
    assert client.get('/api/v1/audit').status_code==403
    assert client.post('/api/v1/cases',json={'title':'Case Two','institution':'Example University','destination_country':'Canada','amount':'12','currency':'CAD'},headers={'X-CSRF-Token':csrf}).status_code==403
    sign_in(client,'auditor')
    assert client.get('/api/v1/audit').status_code==200
    assert client.get('/api/v1/reviewer/queue').status_code==403
    sign_in(client,'admin')
    assert client.get('/api/v1/admin/summary').json()['users']==4

def test_documents_upload_access_and_signature(client):
    csrf=sign_in(client)
    case=client.post('/api/v1/cases',json={'title':'Invoice upload','institution':'Example University','destination_country':'Canada','amount':'123','currency':'CAD'},headers={'X-CSRF-Token':csrf}).json()
    wrong=client.post('/api/v1/documents',data={'case_id':case['id']},files={'file':('x.pdf',b'not-a-pdf','application/pdf')},headers={'X-CSRF-Token':csrf})
    assert wrong.status_code==422
    ok=client.post('/api/v1/documents',data={'case_id':case['id']},files={'file':('invoice.txt',b'SYNTHETIC DEMO INVOICE','text/plain')},headers={'X-CSRF-Token':csrf})
    assert ok.status_code==201,ok.text
    doc=ok.json()
    assert doc['status']=='STORED_UNVERIFIED'
    assert client.get('/api/v1/documents/'+doc['id']+'/download').content==b'SYNTHETIC DEMO INVOICE'
    assert client.get('/api/v1/documents').json()['items'][0]['id']==doc['id']

def test_student_cannot_access_other_student_case(client):
    from app.db import SessionLocal
    from app.models import User, PaymentCase
    from app.security import password_hash
    with SessionLocal() as db:
        other=User(email='other@test.com',name='Other',role='student',password_hash=password_hash('A-Long-Test-Password!'))
        db.add(other); db.flush()
        c=PaymentCase(user_id=other.id,title='Private tuition',institution='Example University',destination_country='Canada',amount='400.00',currency='CAD')
        db.add(c);db.commit();identifier=c.id
    sign_in(client)
    assert client.get('/api/v1/cases/'+identifier).status_code==404
    assert client.get('/api/v1/cases').json()['items']==[]

def test_origin_rejection(client):
    csrf=sign_in(client)
    response=client.post('/api/v1/auth/logout',headers={'X-CSRF-Token':csrf,'Origin':'https://attacker.example'})
    assert response.status_code==403

def test_no_execution_route(client):
    sign_in(client)
    assert client.post('/api/v1/payments/execute',json={}).status_code==404

def test_profile_update_persists(client):
    csrf=sign_in(client)
    profile={'name':'Student Updated','institution':'SYNTHETIC Test Institute','home_country':'Bangladesh','currency':'GBP'}
    r=client.patch('/api/v1/me/profile',json=profile,headers={'X-CSRF-Token':csrf})
    assert r.status_code==200
    assert r.json()['name']=='Student Updated'
    assert client.get('/api/v1/auth/me').json()['user']['currency']=='GBP'

def test_html_preview_is_really_served(client):
    r=client.get('/demo')
    assert r.status_code==200
    assert 'text/html' in r.headers['content-type']
    assert 'BorderProof AI' in r.text
    assert 'function createCase(e)' in r.text

def test_upload_rejects_excess_size(client):
    csrf=sign_in(client)
    case=client.post('/api/v1/cases',json={'title':'Large attachment','institution':'SYNTHETIC Institute','destination_country':'Canada','amount':'123','currency':'CAD'},headers={'X-CSRF-Token':csrf}).json()
    huge=b'x'*(5*1024*1024+1)
    r=client.post('/api/v1/documents',data={'case_id':case['id']},files={'file':('huge.txt',huge,'text/plain')},headers={'X-CSRF-Token':csrf})
    assert r.status_code==413

def test_upload_isolation_for_another_student(client):
    csrf=sign_in(client)
    case=client.post('/api/v1/cases',json={'title':'Case private doc','institution':'SYNTHETIC Institute','destination_country':'Canada','amount':'99','currency':'CAD'},headers={'X-CSRF-Token':csrf}).json()
    d=client.post('/api/v1/documents',data={'case_id':case['id']},files={'file':('synthetic.txt',b'SYNTHETIC','text/plain')},headers={'X-CSRF-Token':csrf}).json()
    from app.db import SessionLocal
    from app.models import User
    from app.security import password_hash
    with SessionLocal() as db:
        db.add(User(email='other@test.com',name='Other User',role='student',password_hash=password_hash('A-Long-Test-Password!')));db.commit()
    r=client.post('/api/v1/auth/login',json={'email':'other@test.com','password':'A-Long-Test-Password!'})
    assert r.status_code==200
    assert client.get('/api/v1/documents/'+d['id']+'/download').status_code==404
    assert client.get('/api/v1/documents').json()['items']==[]

def test_schema_baseline_exists(client):
    from sqlalchemy import text
    from app.db import engine
    from app.db import init_schema
    init_schema()
    with engine.connect() as conn:
        assert conn.execute(text('SELECT MAX(version) FROM schema_versions')).scalar()==6
