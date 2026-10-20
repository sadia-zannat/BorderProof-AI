"""BorderProof AI V2 — evidence-aware internal sandbox, NEVER real money."""
from __future__ import annotations
from .timeutils import iso_utc
import hashlib, os, re, secrets
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, File, Form, HTTPException, Request, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from .db import Base, engine, db_session, init_schema
from .models import User, LoginSession, PaymentCase, Document, AuditEvent, PaymentApproval, utcnow
from .schemas import LoginIn, ProfileUpdate, CaseIn, RegisterIn
from .security import COOKIE, SESSION_HOURS, create_login, get_login, current_user, csrf_user, require_roles, require_mutation_roles, verify_password, sha
from .seed import seed_demo
from .audit import append_event

MAX_DOC_SIZE = 5 * 1024 * 1024
DATA_DIR = Path(os.getenv('PRIVATE_UPLOAD_DIR', str(Path(__file__).resolve().parents[3] / 'runtime' / 'uploads')))
DATA_DIR.mkdir(parents=True,exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv('APP_ENV') == 'production' and os.getenv('ENABLE_DEMO_SEED','0') == '1':
        raise RuntimeError('Production cannot seed demonstration credentials')
    init_schema()
    with next(db_session()) as db: seed_demo(db)
    yield

app=FastAPI(title='BorderProof AI', version='5.5.0', lifespan=lifespan, docs_url='/api/docs',openapi_url='/api/openapi.json')
@app.middleware('http')
async def security_response_headers(request: Request, call_next):
    result=await call_next(request)
    result.headers.setdefault('X-Content-Type-Options','nosniff')
    result.headers.setdefault('X-Frame-Options','DENY')
    result.headers.setdefault('Referrer-Policy','no-referrer')
    result.headers.setdefault('Permissions-Policy','camera=(), microphone=(), geolocation=()')
    if request.url.path.startswith('/api/'):
        result.headers['Cache-Control']='no-store'
    return result

app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in os.getenv('ALLOWED_ORIGINS','http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000,http://127.0.0.1:8000').split(',')], allow_credentials=True, allow_methods=['GET','POST','PATCH'],allow_headers=['Content-Type','X-CSRF-Token'])

FAILED_LOGINS:dict[str,list[float]] = {}  # single-process V1; distributed lockout pending

@app.post('/api/v1/auth/register',status_code=201)
def register(inp:RegisterIn,request:Request,db:Session=Depends(db_session)):
    # Local demo account creation only; no email/identity verification is claimed.
    if os.getenv('APP_ENV')!='development' or os.getenv('ENABLE_LOCAL_SIGNUP')!='1':
        raise HTTPException(403,'Local registration is disabled')
    origin=request.headers.get('origin')
    if origin and origin not in {v.strip() for v in os.getenv('ALLOWED_ORIGINS','http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000,http://127.0.0.1:8000').split(',')}:
        raise HTTPException(403,'Untrusted origin')
    from .security import password_hash
    from sqlalchemy.exc import IntegrityError
    u=User(email=inp.email.lower(),name=inp.name,role='student',password_hash=password_hash(inp.password))
    db.add(u)
    try:
        db.flush();append_event(db,u.id,'LOCAL_STUDENT_REGISTERED','user',u.id,{'identity_verified':False});db.commit()
    except IntegrityError:
        db.rollback();raise HTTPException(409,'Local account already exists')
    return {'id':u.id,'role':'student','identity_verified':False,'mode':'LOCAL_DEMO_ACCOUNT_ONLY'}

def user_out(u: User): return {'id':u.id,'email':u.email,'name':u.name,'role':u.role,'institution':u.institution,'home_country':u.home_country,'currency':u.currency}
def case_out(c: PaymentCase):return {'id':c.id,'title':c.title,'institution':c.institution,'origin_country':c.origin_country,'source_currency':c.source_currency or 'BDT','destination_currency':c.destination_currency or c.currency,'destination_country':c.destination_country,'amount':c.amount,'currency':c.currency,'status':c.status,'is_synthetic':c.is_synthetic,'created_at':iso_utc(c.created_at)}
def doc_out(d: Document): return {'id':d.id,'case_id':d.case_id,'filename':d.filename,'content_type':d.content_type,'bytes_size':d.bytes_size,'sha256':d.sha256,'status':d.status,'created_at':iso_utc(d.created_at)}

@app.get('/api/v1/health')
def health():return {'ok':True,'version':'5.5.0','execution_mode':'INTERNAL_SANDBOX_ONLY','financial_data':'SYNTHETIC_DEMO_ONLY'}

@app.get('/api/v1/public/config')
def public_config():return {'brand':'BorderProof AI','version':'V5.5','local_signup_enabled':os.getenv('ENABLE_LOCAL_SIGNUP')=='1' and os.getenv('APP_ENV')=='development','real_payments_enabled':False,'supported_locales':['en','zh-CN','bn-BD'],'corridors':[], 'network_endpoint':'/api/v1/network/corridors','notice':'Corridor listings are demo coverage, NOT transfer availability or legal eligibility.'}

@app.post('/api/v1/auth/login')
def login(inp: LoginIn, response: Response, request: Request, db:Session=Depends(db_session)):
    import time
    origin=request.headers.get('origin')
    if origin and origin not in {x.strip() for x in os.getenv('ALLOWED_ORIGINS','http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000,http://127.0.0.1:8000').split(',')}:raise HTTPException(403,'Untrusted origin')
    key=hashlib.sha256((inp.email.lower()+'|'+(request.client.host if request.client else '')).encode()).hexdigest()
    now=time.monotonic(); attempts=[v for v in FAILED_LOGINS.get(key,[]) if now-v < 300]; FAILED_LOGINS[key]=attempts
    if len(attempts)>=5:raise HTTPException(429,'Too many failed attempts. Retry later.')
    user=db.scalar(select(User).where(User.email == inp.email.strip().lower()))
    if not user or not verify_password(user.password_hash,inp.password):
        attempts.append(now); raise HTTPException(401,'Invalid email or password')
    FAILED_LOGINS.pop(key,None)
    token,csrf=create_login(db,user)
    response.set_cookie(COOKIE,token,httponly=True,secure=(os.getenv('COOKIE_SECURE','0')=='1' or os.getenv('APP_ENV')=='production'),samesite='lax',max_age=SESSION_HOURS*3600,path='/')
    append_event(db,user.id,'AUTH_LOGIN','user',user.id)
    db.commit()
    return {'user':user_out(user),'csrf_token':csrf}

@app.get('/api/v1/auth/me')
def me(request: Request, db:Session=Depends(db_session)):
    user,sess=get_login(request,db)
    csrf=sha('csrf:'+request.cookies[COOKIE])
    if sess.csrf_hash!=sha(csrf):
        sess.csrf_hash=sha(csrf);db.commit()
    return {'user':user_out(user),'csrf_token':csrf}

@app.post('/api/v1/auth/logout')
def logout(response: Response,request:Request, user:User=Depends(csrf_user),db:Session=Depends(db_session)):
    raw=request.cookies.get(COOKIE)
    sess=db.scalar(select(LoginSession).where(LoginSession.token_hash==sha(raw)))
    if sess: db.delete(sess)
    append_event(db,user.id,'AUTH_LOGOUT','user',user.id);db.commit()
    response.delete_cookie(COOKIE,path='/')
    return {'ok':True}

@app.patch('/api/v1/me/profile')
def update_profile(inp:ProfileUpdate,user:User=Depends(csrf_user),db:Session=Depends(db_session)):
    obj=db.get(User,user.id)
    for field,value in inp.model_dump().items():setattr(obj,field,value.strip() if isinstance(value,str) else value)
    append_event(db,user.id,'PROFILE_UPDATE','user',user.id)
    db.commit();return user_out(obj)

@app.get('/api/v1/dashboard')
def dashboard(user:User=Depends(current_user),db:Session=Depends(db_session)):
    cases=db.scalars(select(PaymentCase).where(PaymentCase.user_id==user.id).order_by(PaymentCase.created_at.desc()).limit(10)).all() if user.role=='student' else []
    docs=db.scalar(select(func.count(Document.id)).where(Document.user_id==user.id))
    total=db.scalar(select(func.count(PaymentCase.id)).where(PaymentCase.user_id==user.id))
    return {'role':user.role,'cases_total':total,'documents_total':docs,'cases':[case_out(x) for x in cases], 'payment_execution':'INTERNAL_SANDBOX_ONLY', 'amounts_are':'USER_ENTERED_OR_SYNTHETIC_NOT_PROCESSED'}

@app.get('/api/v1/cases')
def cases(user:User=Depends(current_user),db:Session=Depends(db_session)):
    stmt=select(PaymentCase).order_by(PaymentCase.created_at.desc())
    if user.role=='student':stmt=stmt.where(PaymentCase.user_id==user.id)
    elif user.role not in {'reviewer','auditor','admin'}:raise HTTPException(403,'Insufficient role')
    return {'items':[case_out(x) for x in db.scalars(stmt.limit(100)).all()]}

@app.post('/api/v1/cases',status_code=201)
def create_case(inp:CaseIn,user:User=Depends(require_mutation_roles('student')),db:Session=Depends(db_session)):
    c=PaymentCase(user_id=user.id,title=inp.title.strip(),institution=inp.institution.strip(),origin_country=inp.origin_country,source_currency=inp.source_currency,destination_country=inp.destination_country,destination_currency=inp.destination_currency,amount=inp.amount,currency=inp.currency,status='DRAFT')
    db.add(c); db.flush();append_event(db,user.id,'CASE_CREATE','case',c.id,{'currency':c.currency,'status':'DRAFT'})
    db.commit();return case_out(c)

@app.get('/api/v1/cases/{case_id}')
def one_case(case_id:str,user:User=Depends(current_user),db:Session=Depends(db_session)):
    c=db.get(PaymentCase,case_id)
    if not c or (user.role=='student' and c.user_id!=user.id):raise HTTPException(404,'Case not found')
    return case_out(c)

@app.get('/api/v1/documents')
def documents(user:User=Depends(current_user),db:Session=Depends(db_session)):
    q=select(Document).order_by(Document.created_at.desc()).limit(100)
    if user.role=='student':q=q.where(Document.user_id==user.id)
    elif user.role not in {'reviewer','auditor','admin'}:raise HTTPException(403,'Insufficient role')
    return {'items':[doc_out(x) for x in db.scalars(q).all()]}

@app.post('/api/v1/documents',status_code=201)
async def upload_document(case_id:str=Form(...),file:UploadFile=File(...),user:User=Depends(require_mutation_roles('student')),db:Session=Depends(db_session)):
    from .finance import financial_write_lock
    financial_write_lock(db,user.id)
    c=db.get(PaymentCase,case_id)
    if not c or c.user_id!=user.id:raise HTTPException(404,'Case not found')
    if c.status not in ('DRAFT','SIMULATED_FAILED'):raise HTTPException(409,'Case not editable')
    name=Path(file.filename or 'document').name[:160]
    ext=Path(name).suffix.lower()
    allowed={'.pdf':'application/pdf','.txt':'text/plain','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg'}
    if ext not in allowed:raise HTTPException(415,'Only PDF, PNG, JPEG and TXT files are supported')
    data=await file.read(MAX_DOC_SIZE+1)
    if len(data)>MAX_DOC_SIZE:raise HTTPException(413,'File exceeds 5MB size limit')
    if not data:raise HTTPException(422,'Empty file')
    if ext=='.pdf' and not data.startswith(b'%PDF-'):raise HTTPException(422,'Invalid PDF signature')
    if ext=='.png' and not data.startswith(b'\x89PNG\r\n\x1a\n'):raise HTTPException(422,'Invalid PNG signature')
    if ext in ('.jpg','.jpeg') and not data.startswith(b'\xff\xd8\xff'):raise HTTPException(422,'Invalid JPEG signature')
    if ext=='.txt':
        try:data.decode('utf-8')
        except UnicodeDecodeError:raise HTTPException(422,'Text must be UTF-8')
    from .storage import configured_storage
    destination=configured_storage().save(data,ext)
    record=Document(user_id=user.id,case_id=c.id,filename=name,content_type=allowed[ext],bytes_size=len(data),sha256=hashlib.sha256(data).hexdigest(),internal_path=str(destination))
    db.add(record);db.flush()
    # V3: any newly added document changes the evidence-set version. Previously
    # active approvals must be explicitly renewed with a newly sealed quote.
    active=db.scalars(select(PaymentApproval).where(PaymentApproval.case_id==c.id,PaymentApproval.status=='ACTIVE')).all()
    for approval in active:
        approval.status='INVALIDATED'
        append_event(db,user.id,'APPROVAL_INVALIDATED_BY_NEW_DOCUMENT','approval',approval.id,
                     {'case_id':c.id,'new_document_id':record.id})
    append_event(db,user.id,'DOCUMENT_UPLOADED','document',record.id,{'case_id':case_id,'sha256':record.sha256})
    db.commit();return doc_out(record)

@app.get('/api/v1/documents/{document_id}/download')
def download_document(document_id:str,user:User=Depends(current_user),db:Session=Depends(db_session)):
    d=db.get(Document,document_id)
    if not d or (user.role=='student' and d.user_id!=user.id): raise HTTPException(404,'Document not found')
    from .storage import configured_storage
    try:path=configured_storage().resolve(d.internal_path)
    except ValueError:raise HTTPException(404,'File unavailable')
    if not path.is_file():raise HTTPException(404,'File unavailable')
    return FileResponse(path,media_type='application/octet-stream',filename=d.filename,headers={'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'})

@app.get('/api/v1/reviewer/queue')
def review_queue(user:User=Depends(require_roles('reviewer','admin')),db:Session=Depends(db_session)):
    items=db.scalars(select(PaymentCase).order_by(PaymentCase.created_at.desc()).limit(100)).all()
    return {'mode':'SYNTHETIC_SANDBOX_V2','items':[case_out(x) for x in items],'notice':'Reviewer interface is still read-only; sandbox verification is deterministic.'}

@app.get('/api/v1/audit')
def audit(user:User=Depends(require_roles('auditor','admin')),db:Session=Depends(db_session)):
    events=db.scalars(select(AuditEvent).order_by(AuditEvent.created_at.desc()).limit(100)).all()
    return {'events':[{'id':x.id,'actor_id':x.actor_id,'action':x.action,'object_type':x.object_type,'object_id':x.object_id,'previous_hash':x.previous_hash,'event_hash':x.event_hash,'created_at':iso_utc(x.created_at)} for x in events],'notice':'V1 hash-linked events are not digitally signed or externally anchored.'}

@app.get('/api/v1/admin/summary')
def admin_summary(user:User=Depends(require_roles('admin')),db:Session=Depends(db_session)):
    return {'users':db.scalar(select(func.count(User.id))), 'cases':db.scalar(select(func.count(PaymentCase.id))),'documents':db.scalar(select(func.count(Document.id))), 'external_execution_enabled':False}

@app.get('/')
def root():return {'service':'BorderProof AI V5 API','docs':'/api/docs','health':'/api/v1/health'}

@app.get('/demo', include_in_schema=False)
def standalone_preview():
    """No-npm standalone fallback, backed by the SAME live API and database."""
    index = Path(__file__).resolve().parents[3] / 'apps' / 'preview' / 'index.html'
    if not index.is_file():
        raise HTTPException(404, 'Standalone preview unavailable (copy apps/preview with the repo)')
    return FileResponse(index, media_type='text/html',headers={'Cache-Control':'no-store','Content-Security-Policy':"default-src 'self'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'"})

@app.get('/assets/fonts/{name}',include_in_schema=False)
def locale_font(name:str):
    if name not in ('borderproof-cjk.woff2','borderproof-bengali.woff2'):raise HTTPException(404,'Font not found')
    path=Path(__file__).resolve().parents[3]/'apps/preview/fonts'/name
    if not path.is_file():raise HTTPException(404,'Font unavailable')
    return FileResponse(path,media_type='font/woff2',headers={'Cache-Control':'public, max-age=86400'})

from .finance_routes import router as finance_router
from .bpce_routes import router as bpce_router
app.include_router(finance_router)
app.include_router(bpce_router)

from .research_routes import router as research_router
app.include_router(research_router)

from .final_routes import router as final_router
app.include_router(final_router)

from .agent_routes import router as agent_router
app.include_router(agent_router)

from .network import router as network_router
app.include_router(network_router)
