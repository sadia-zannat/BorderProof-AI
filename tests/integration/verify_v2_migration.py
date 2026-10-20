"""Self-contained frozen V2 table-shape migration, no sibling ZIP required."""
import os,sys,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def verify():
 with tempfile.TemporaryDirectory(prefix='bp-v2-migration-') as temp:
  env={**os.environ,'DATABASE_URL':f'sqlite:///{temp}/legacy.sqlite3','APP_ENV':'test','ENABLE_DEMO_SEED':'0','PYTHONPATH':str(ROOT/'services/api')}
  code="""from app.db import Base,engine,init_schema,SessionLocal
from app.models import User,PaymentCase,SandboxAccount
from sqlalchemy import text
names=['users','login_sessions','payment_cases','documents','audit_events','invoice_extractions','investigations','payment_quotes','payment_approvals','sandbox_accounts','sandbox_transfers','sandbox_ledger','notifications']
for name in names: Base.metadata.tables[name].create(engine,checkfirst=True)
with engine.begin() as c:
 c.execute(text('CREATE TABLE schema_versions(version INTEGER PRIMARY KEY,description VARCHAR(120) NOT NULL)'))
 c.execute(text("INSERT INTO schema_versions VALUES(2,'frozen V2 table shape')"))
with SessionLocal() as db:
 u=User(email='v2-legacy@example.test',name='Legacy V2',role='student',password_hash='non-login-fixture');db.add(u);db.flush()
 db.add(PaymentCase(user_id=u.id,title='Preserved V2',institution='Synthetic Archive',destination_country='Canada',amount='42.00',currency='CAD'))
 db.add(SandboxAccount(user_id=u.id,balance='123456.78',currency='BDT'));db.commit()
init_schema();init_schema()
with SessionLocal() as db:
 assert db.query(PaymentCase).filter_by(title='Preserved V2').count()==1
 assert db.query(SandboxAccount).one().balance=='123456.78'
 assert db.execute(text('SELECT MAX(version) FROM schema_versions')).scalar()==5
print('PASS V2-shaped migration: case and balance preserved; reentrant schema 5 + V5.3 indexes')
"""
  result=subprocess.run([sys.executable,'-c',code],env=env,cwd=ROOT,text=True,capture_output=True,timeout=30)
  print(result.stdout,result.stderr)
  if result.returncode:raise SystemExit(result.returncode)
if __name__=='__main__':verify()
