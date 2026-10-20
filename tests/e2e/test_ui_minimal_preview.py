"""V5.2 browser smoke of edited standalone UI, using real FastAPI through a local HTTP bridge.
Runs with /usr/bin/chromium and Playwright, where installed. No external banking/LLM claims.
"""
import os,sys,subprocess,tempfile,time,base64
from pathlib import Path
from urllib.request import urlopen
import requests
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
PORT=8146

def test_ui_minimal_preview():
    with tempfile.TemporaryDirectory(prefix='bp-v52-') as temp:
        env=os.environ.copy()
        env.update({'DATABASE_URL':f'sqlite:///{temp}/db.sqlite3','PRIVATE_UPLOAD_DIR':f'{temp}/uploads','APP_ENV':'development','ENABLE_DEMO_SEED':'1','DEMO_SEED_PASSWORD':'Local-Screenshot-Temporary-2026','ALLOWED_ORIGINS':f'http://127.0.0.1:{PORT}'})
        proc=subprocess.Popen([sys.executable,'-m','uvicorn','app.main:app','--host','127.0.0.1','--port',str(PORT)],cwd=str(ROOT/'services/api'),env=env,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
        try:
            for _ in range(150):
                try:
                    with urlopen(f'http://127.0.0.1:{PORT}/api/v1/health',timeout=.2):break
                except Exception:time.sleep(.1)
            else:raise RuntimeError('Server not ready')
            session=requests.Session()
            with sync_playwright() as p:
                browser=p.chromium.launch(headless=True,executable_path=os.getenv('BORDERPROOF_CHROMIUM') or None,args=['--no-sandbox','--disable-dev-shm-usage'])
                page=browser.new_page(viewport={'width':1440,'height':900},device_scale_factor=1)
                errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
                def bridge(req):
                    args={'timeout':15,'headers':req.get('headers') or {}}
                    if req.get('form'):
                        data,files={},{}
                        for item in req['form']:
                            if item.get('file'):files[item['key']]=(item['name'],base64.b64decode(item['data']),item['mime'])
                            else:data[item['key']]=item['value']
                        args.update(data=data,files=files)
                    else:args['data']=req.get('body')
                    r=session.request(req.get('method','GET'),f'http://127.0.0.1:{PORT}'+req['url'],**args)
                    return {'status':r.status_code,'text':r.text,'content_type':r.headers.get('Content-Type','application/json')}
                page.expose_function('bridgeRequest',bridge)
                page.evaluate(r"""(()=>{const saved={};Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>saved[k]??null,setItem:(k,v)=>saved[k]=String(v)}});window.history.replaceState=()=>{};window.fetch=async function(url,init={}){let form=null,body=init.body||null;if(body instanceof FormData){form=[];for(const [key,value] of body.entries()){if(value instanceof File){let bytes=new Uint8Array(await value.arrayBuffer());let binary='';for(let i=0;i<bytes.length;i+=8192)binary+=String.fromCharCode(...bytes.subarray(i,i+8192));form.push({key,file:true,name:value.name,mime:value.type,data:btoa(binary)});}else form.push({key,value:String(value)})}body=null;}const ans=await window.bridgeRequest({url,method:init.method||'GET',headers:init.headers||{},body,form});return new Response(ans.text,{status:ans.status,headers:{'Content-Type':ans.content_type}})};return true;})()""")
                page.set_content((ROOT/'apps/preview/index.html').read_text(encoding='utf8'))
                page.get_by_role('heading',name='Pay tuition across borders, with clarity.').wait_for(timeout=10000)
                assert 'V3 INTERNAL SANDBOX' not in page.locator('.hero').inner_text()
                page.screenshot(path=str(ROOT/'docs/V5_2_MINIMAL_LANDING_DESKTOP.png'),full_page=True)
                page.set_viewport_size({'width':390,'height':844})
                page.screenshot(path=str(ROOT/'docs/V5_2_MINIMAL_LANDING_MOBILE.png'),full_page=True)
                page.set_viewport_size({'width':1440,'height':900})
                page.get_by_role('button',name='Sign in').click()
                page.locator('h1').get_by_text('Sign in').wait_for()
                assert page.locator('.login p').count()==1
                page.screenshot(path=str(ROOT/'docs/V5_2_MINIMAL_LOGIN_DESKTOP.png'),full_page=True)
                page.set_viewport_size({'width':390,'height':844})
                page.screenshot(path=str(ROOT/'docs/V5_2_MINIMAL_LOGIN_MOBILE.png'),full_page=True)
                page.set_viewport_size({'width':1440,'height':900})
                page.get_by_label('Password').fill('Local-Screenshot-Temporary-2026')
                page.locator('.login button.btn').click()
                page.get_by_role('heading',name='Your workspace').wait_for(timeout=10000)
                page.wait_for_timeout(4650)
                page.screenshot(path=str(ROOT/'docs/V5_2_MINIMAL_DASHBOARD_DESKTOP.png'),full_page=True)
                page.get_by_role('button',name='AI agent').click()
                page.get_by_role('heading',name='AI assistant').wait_for()
                assert 'Tool activity' not in page.locator('main').inner_text() # hidden before an inference
                page.screenshot(path=str(ROOT/'docs/V5_2_MINIMAL_AGENT_DESKTOP.png'),full_page=True)
                page.locator('header select').select_option('bn-BD')
                page.get_by_role('heading',name='AI সহকারী').wait_for()
                page.locator('header select').select_option('en')
                page.set_viewport_size({'width':390,'height':844})
                page.screenshot(path=str(ROOT/'docs/V5_2_MINIMAL_AGENT_MOBILE.png'),full_page=True)
                assert not errors,errors
                browser.close()
        finally:
            proc.terminate()
            try:proc.wait(timeout=6)
            except subprocess.TimeoutExpired:proc.kill();proc.wait()
