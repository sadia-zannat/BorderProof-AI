import os,sys,tempfile
from pathlib import Path
p=Path(tempfile.mkdtemp(prefix='bp-test-'))
os.environ['DATABASE_URL']=f'sqlite:///{p}/test.sqlite3'
os.environ['PRIVATE_UPLOAD_DIR']=str(p/'uploads')
os.environ['APP_ENV']='test'
os.environ['ENABLE_DEMO_SEED']='0'
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pytest
from fastapi.testclient import TestClient
from app.db import Base,engine,SessionLocal
from app.models import User
from app.security import password_hash
from app.main import app

@pytest.fixture(autouse=True)
def reset():
    Base.metadata.drop_all(engine);Base.metadata.create_all(engine)
    with SessionLocal() as db:
        for role in ('student','reviewer','auditor','admin'):
            db.add(User(email=f'{role}@test.com',name=role,role=role,password_hash=password_hash('A-Long-Test-Password!')))
        db.commit()
    yield

@pytest.fixture
def client():
    with TestClient(app) as c:yield c

def sign_in(client, role='student'):
    r=client.post('/api/v1/auth/login',json={'email':f'{role}@test.com','password':'A-Long-Test-Password!'})
    assert r.status_code==200, r.text
    return r.json()['csrf_token']
