"""Actual Chromium V5 support journey using FastAPI backend via browser bridge."""
import os,subprocess,sys,tempfile,time
from pathlib import Path
from urllib.request import urlopen
import requests
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
PORT=8115

def test_v5_support_preview():
 with tempfile.TemporaryDirectory(prefix='bp-v5-browser-') as temp:
  env=os.environ.copy();env.update({'DATABASE_URL':f'sqlite:///{temp}/test.sqlite3',
   'PRIVATE_UPLOAD_DIR':f'{temp}/uploads','APP_ENV':'development','ENABLE_DEMO_SEED':'1',
   'DEMO_SEED_PASSWORD':'V5-Temporary-Browser-Password!',
   'ALLOWED_ORIGINS':f'http://127.0.0.1:{PORT},http://localhost:3000'})
  process=subprocess.Popen([sys.executable,'-m','uvicorn','app.main:app','--host','127.0.0.1','--port',str(PORT)],
      cwd=str(ROOT/'services/api'),env=env,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
  try:
   for _ in range(120):
    try:
     if urlopen(f'http://127.0.0.1:{PORT}/api/v1/health',timeout=.3).status==200:break
    except Exception:time.sleep(.1)
   else:raise RuntimeError('FastAPI server failed')
   session=requests.Session();url=f'http://127.0.0.1:{PORT}/api/v1'
   r=session.post(url+'/auth/login',json={'email':'student@borderproof.test','password':'V5-Temporary-Browser-Password!'});r.raise_for_status()
   csrf=r.json()['csrf_token'];hdr={'X-CSRF-Token':csrf}
   cases=session.get(url+'/cases').json()['items'];case=cases[0]['id']
   d=session.post(url+'/cases/'+case+'/synthetic-invoice',headers=hdr).json();assert 'id' in d,d
   ex=session.post(url+f'/cases/{case}/documents/{d["id"]}/extract',headers=hdr).json()
   inv=session.post(url+f'/cases/{case}/investigations',json={'extraction_id':ex['id']},headers=hdr).json()
   qt=session.post(url+f'/cases/{case}/quotes',json={'investigation_id':inv['id']},headers=hdr).json()
   ap=session.post(url+f'/cases/{case}/approvals',json={'quote_id':qt['id'],'confirmation':'I AUTHORIZE THIS INTERNAL SANDBOX PAYMENT'},headers=hdr).json()
   transfer=session.post(url+f'/cases/{case}/transfers',json={'approval_id':ap['id'],'idempotency_key':'v5-demo-unique-key-001','simulated_outcome':'SUCCESS'},headers=hdr).json();assert transfer['status']=='COMPLETED'
   with sync_playwright() as p:
    b=p.chromium.launch(headless=True,executable_path=os.getenv('BORDERPROOF_CHROMIUM') or None,args=['--no-sandbox','--disable-dev-shm-usage'])
    page=b.new_page(viewport={'width':1400,'height':920},accept_downloads=True);page.set_default_timeout(12000)
    errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
    def bridge(req):
     answer=session.request(req.get('method','GET'),url.replace('/api/v1','')+req['url'],
       data=req.get('body'),headers=req.get('headers') or {},timeout=10)
     return {'status':answer.status_code,'body':answer.text,'content_type':answer.headers.get('Content-Type','application/json')}
    page.expose_function('bridgeRequest',bridge)
    page.evaluate("""(()=>{const store={};Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=String(v)}}});window.history.replaceState=()=>{};window.fetch=async function(url,init={}){const ans=await window.bridgeRequest({url,method:init.method||'GET',headers:init.headers||{},body:init.body||null});return new Response(ans.body,{status:ans.status,headers:{'Content-Type':ans.content_type}})};return true;})()""")
    page.set_content((ROOT/'apps/preview/index.html').read_text(encoding='utf-8'))
    page.get_by_role('button',name='Evidence & support').click()
    page.get_by_role('heading',name='Evidence & recovery').wait_for()
    page.get_by_role('button',name='Inspect safe next step').click()
    page.get_by_text('DOWNLOAD_SIMULATION_EVIDENCE').wait_for()
    page.locator('#su-transfer').select_option(transfer['id'])
    with page.expect_download() as future:
     page.get_by_role('button',name='Export evidence JSON').click()
    download=future.value
    assert download.suggested_filename.endswith('.json')
    page.locator('#su-category').select_option('REFUND_GUIDANCE')
    page.locator('#su-message').fill('Please explain what simulated refund guidance is available.')
    page.get_by_role('button',name='Create support case').click()
    page.get_by_text('REFUND_GUIDANCE · OPEN').wait_for()
    page.screenshot(path=str(ROOT/'docs/V5_SUPPORT_DESKTOP_SCREENSHOT.png'),full_page=True)
    page.locator('header select').select_option('bn-BD')
    page.get_by_role('heading',name='প্রমাণ ও সহায়তা').wait_for()
    page.set_viewport_size({'width':390,'height':844})
    page.screenshot(path=str(ROOT/'docs/V5_SUPPORT_MOBILE_SCREENSHOT.png'),full_page=True)
    page.locator('header select').select_option('zh-CN')
    page.get_by_role('heading',name='证据与恢复').wait_for()
    assert not errors,errors
    assert len(session.get(url+'/support/disputes').json()['items'])==1
    assert session.get(url+f'/transfers/{transfer["id"]}/receipt').json()['transfer']['status']=='COMPLETED'
    b.close()
   print('PASS V5 browser: API-backed plan, export, support case, desktop/mobile, EN/BN/ZH')
  finally:
   process.terminate()
   try:process.wait(timeout=6)
   except subprocess.TimeoutExpired:process.kill();process.wait()
if __name__=='__main__':test_v5_support_preview()
