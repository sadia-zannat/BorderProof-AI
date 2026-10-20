"""Browser integration test using a real Chromium instance and real Uvicorn."""
import os, subprocess, sys, tempfile, time, base64
import requests
from pathlib import Path
from urllib.request import urlopen
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
PORT=int(os.getenv('BP_E2E_PORT','8097'))

def wait_ready(timeout=15):
    end=time.time()+timeout
    while time.time()<end:
        try:
            with urlopen(f'http://127.0.0.1:{PORT}/api/v1/health',timeout=.4) as r:
                if r.status==200:return
        except Exception:time.sleep(.1)
    raise RuntimeError('Uvicorn did not start')

def test_preview():
    with tempfile.TemporaryDirectory(prefix='bp-e2e-') as temp:
        env=os.environ.copy()
        env.update({'DATABASE_URL':f'sqlite:///{temp}/test.sqlite3','PRIVATE_UPLOAD_DIR':f'{temp}/uploads','APP_ENV':'development','ENABLE_DEMO_SEED':'1','DEMO_SEED_PASSWORD':'Demo-Preview-Strong-2026','ALLOWED_ORIGINS':f'http://127.0.0.1:{PORT},http://localhost:3000'})
        proc=subprocess.Popen([sys.executable,'-m','uvicorn','app.main:app','--host','127.0.0.1','--port',str(PORT)],cwd=str(ROOT/'services/api'),env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        try:
            wait_ready()
            with sync_playwright() as p:
                browser=p.chromium.launch(headless=True,executable_path=os.getenv('BORDERPROOF_CHROMIUM') or None,args=['--no-sandbox','--disable-dev-shm-usage'])
                context=browser.new_context(viewport={'width':1440,'height':960})
                page=context.new_page()
                # This sandbox blocks Chromium network navigation. Exercise REAL server
                # requests through a Python HTTP session while rendering REAL page JS.
                session=requests.Session()
                def bridge(req):
                    target=f'http://127.0.0.1:{PORT}'+str(req.get('url') or '')
                    opts={'timeout':10,'headers':req.get('headers') or {}}
                    if req.get('form'):
                        data,files={},{}
                        for item in req['form']:
                            if item.get('file'):
                                files[item['key']] = (item['name'],base64.b64decode(item['data']),item['mime'])
                            else:data[item['key']]=item['value']
                        opts.update({'data':data,'files':files})
                    else:
                        opts['data']=req.get('body')
                    r=session.request(req.get('method','GET'),target,**opts)
                    return {'status':r.status_code,'text':r.text,'content_type':r.headers.get('Content-Type','application/json')}
                page.expose_function('bridgeRequest',bridge)
                page.evaluate(r"""(()=>{ const store={};Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=String(v)}}});window.history.replaceState=()=>{};window.fetch=async function(url,init={}){
                  let form=null,body=init.body||null;
                  if(body instanceof FormData){form=[];for(const [key,value] of body.entries()){
                     if(value instanceof File){let bytes=new Uint8Array(await value.arrayBuffer());let binary='';
                       for(let i=0;i<bytes.length;i+=8192)binary+=String.fromCharCode(...bytes.subarray(i,i+8192));
                       form.push({key,file:true,name:value.name,mime:value.type,data:btoa(binary)});
                     }else form.push({key,value:String(value)});
                  }body=null;}
                  const ans=await window.bridgeRequest({url,method:init.method||'GET',headers:init.headers||{},body,form});
                  return new Response(ans.text,{status:ans.status,headers:{'Content-Type':ans.content_type}});
                };return true;})()""")
                page.on('pageerror',lambda err:print('PAGEERROR',err));page.set_content((ROOT/'apps/preview/index.html').read_text(encoding='utf8'))
                page.locator('.hero h1').wait_for()
                assert 'tuition' in page.locator('.hero h1').inner_text().lower()
                page.get_by_role('button',name='Sign in').click()
                page.get_by_label('Password').fill('Demo-Preview-Strong-2026')
                page.locator('.login button.btn').click()
                page.get_by_text('Your workspace').wait_for()
                page.get_by_role('button',name='Payment cases').click()
                page.get_by_role('button',name='New case').click()
                page.locator('input[name=title]').fill('Browser E2E tuition 2026')
                page.locator('input[name=institution]').fill('E2E Sample University')
                page.locator('input[name=amount]').fill('1850.50')
                page.locator('#newcase button[type=submit]').click()
                page.get_by_text('Browser E2E tuition 2026').wait_for()
                assert page.get_by_text('Browser E2E tuition 2026').count()==1
                page.get_by_role('button',name='Document vault').click()
                page.locator('input[type=file]').set_input_files({'name':'synthetic-invoice.txt','mimeType':'text/plain','buffer':b'SYNTHETIC NOT REAL invoice 1850.50 GBP'})
                page.locator('form button.btn').click()
                page.get_by_text('synthetic-invoice.txt').wait_for()
                page.locator('header select').select_option('bn-BD')
                page.get_by_text('ডকুমেন্ট ভল্ট').first.wait_for()
                page.locator('header select').select_option('en')
                page.get_by_role('button',name='Dashboard').click()
                assert page.locator('.tile').count()==3
                page.screenshot(path=str(ROOT/'docs'/'V2_BROWSER_BASIC_SCREENSHOT.png'),full_page=True)
                page.set_viewport_size({'width':390,'height':844})
                assert page.locator('.mobile-menu').is_visible()
                page.locator('.mobile-menu').click()
                assert page.locator('.side').evaluate('(x)=>x.classList.contains("open")')
                page.evaluate("document.querySelector('.side').classList.remove('open')")
                page.wait_for_timeout(300)
                page.screenshot(path=str(ROOT/'docs'/'V2_MOBILE_BASIC_SCREENSHOT.png'),full_page=True)
                page.set_viewport_size({'width':1440,'height':960})
                page.get_by_title('Sign out').click()
                page.get_by_role('button',name='Sign in').wait_for()
                browser.close()
            print('PASS: Chromium DOM/JS + real bridged Uvicorn requests: landing -> login -> draft case -> upload -> locale -> desktop/mobile -> logout')
        finally:
            proc.terminate()
            try:proc.communicate(timeout=5)
            except subprocess.TimeoutExpired:proc.kill();proc.communicate()

if __name__=='__main__':test_preview()
