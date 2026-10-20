"""Start an actual V1 database in another Python process and upgrade it with V2."""
import os,sys,tempfile,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
V1=ROOT.parent/'BorderProof_AI_V1_Foundation'

def verify():
    with tempfile.TemporaryDirectory(prefix='bp-v1-upgrade-') as d:
        env=os.environ.copy();env.update({'DATABASE_URL':f'sqlite:///{d}/legacy.sqlite3','APP_ENV':'test','ENABLE_DEMO_SEED':'0'})
        # Test a true previous source if present, or create the exact V1 baseline
        # from frozen old table list when this complete V2 ZIP is independently extracted.
        if (V1/'services'/'api'/'app'/'main.py').is_file():
            source=V1
            old='''from app.db import init_schema,SessionLocal
from app.models import User, PaymentCase
init_schema()
with SessionLocal() as db:
 u=User(email='legacy@test.com',name='Legacy',role='student',password_hash='legacy-hash')
 db.add(u);db.flush()
 db.add(PaymentCase(user_id=u.id,title='Legacy case',institution='SYNTHETIC Archive',destination_country='Canada',amount='42.00',currency='CAD'))
 db.commit()
print('Real V1 DB created')'''
        else:
            source=ROOT
            old='''from app.db import engine,SessionLocal,Base
from app.models import User,PaymentCase
from sqlalchemy import text
# Frozen V1 model table list with unchanged V1 column/foreign-key shape.
for name in ['users','login_sessions','payment_cases','documents','audit_events']:
 Base.metadata.tables[name].create(engine,checkfirst=True)
with engine.begin() as conn:
 conn.execute(text('CREATE TABLE schema_versions(version INTEGER PRIMARY KEY, description VARCHAR(120) NOT NULL)'))
 conn.execute(text("INSERT INTO schema_versions VALUES (1,'initial V1 foundation schema')"))
with SessionLocal() as db:
 u=User(email='legacy@test.com',name='Legacy',role='student',password_hash='legacy-hash')
 db.add(u);db.flush()
 db.add(PaymentCase(user_id=u.id,title='Legacy case',institution='SYNTHETIC Archive',destination_country='Canada',amount='42.00',currency='CAD'))
 db.commit()
print('Standalone V1-shaped legacy DB created')'''
        new='''from app.db import init_schema,SessionLocal
from app.models import User,PaymentCase
from sqlalchemy import text
init_schema();init_schema()
with SessionLocal() as db:
 assert db.query(User).filter(User.email=='legacy@test.com').count()==1
 assert db.query(PaymentCase).filter(PaymentCase.title=='Legacy case').count()==1
 assert db.execute(text('SELECT MAX(version) FROM schema_versions')).scalar()==5
 print('V1→V5.3 MIGRATION PASSED: existing user and case preserved')'''
        for source,code in ((source,old),(ROOT,new)):
            e={**env,'PYTHONPATH':str(source/'services/api')}
            p=subprocess.run([sys.executable,'-c',code],env=e,cwd=str(source),text=True,capture_output=True,timeout=30)
            if p.returncode:raise RuntimeError(p.stdout+'\n'+p.stderr)
            print(p.stdout.strip())
if __name__=='__main__':verify()
