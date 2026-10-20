"""Chromium V4 research UI (real FastAPI requests, sandboxed browser bridge)."""
import os,subprocess,sys,tempfile,time
from pathlib import Path
from urllib.request import urlopen
import requests
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[2]
PORT=8107

def test_research_preview():
    with tempfile.TemporaryDirectory(prefix='bp-v4-browser-') as temp:
        env=os.environ.copy();env.update({
            'DATABASE_URL':f'sqlite:///{temp}/test.sqlite3',
            'PRIVATE_UPLOAD_DIR':f'{temp}/uploads','APP_ENV':'development',
            'ENABLE_DEMO_SEED':'1','DEMO_SEED_PASSWORD':'V4-Temporary-Browser-Password!',
            'ALLOWED_ORIGINS':f'http://127.0.0.1:{PORT},http://localhost:3000'})
        proc=subprocess.Popen([sys.executable,'-m','uvicorn','app.main:app','--host','127.0.0.1','--port',str(PORT)],cwd=str(ROOT/'services/api'),env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        try:
            for _ in range(100):
                try:
                    if urlopen(f'http://127.0.0.1:{PORT}/api/v1/health',timeout=.3).status==200:break
                except Exception:time.sleep(.1)
            else:raise RuntimeError('Uvicorn startup did not succeed')
            with sync_playwright() as p:
                browser=p.chromium.launch(headless=True,executable_path=os.getenv('BORDERPROOF_CHROMIUM') or None,args=['--no-sandbox','--disable-dev-shm-usage'])
                page=browser.new_page(viewport={'width':1440,'height':960});page.set_default_timeout(10000)
                session=requests.Session();js_errors=[];page.on('pageerror',lambda err:js_errors.append(str(err)))
                def bridge(req):
                    r=session.request(req.get('method','GET'),f'http://127.0.0.1:{PORT}'+req['url'],data=req.get('body'),headers=req.get('headers') or {},timeout=10)
                    return {'status':r.status_code,'body':r.text,'content_type':r.headers.get('Content-Type','application/json')}
                page.expose_function('bridgeRequest',bridge)
                page.evaluate("""(()=>{const store={};Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=String(v)}}});window.history.replaceState=()=>{};window.fetch=async function(url,init={}){const ans=await window.bridgeRequest({url,method:init.method||'GET',headers:init.headers||{},body:init.body||null});return new Response(ans.body,{status:ans.status,headers:{'Content-Type':ans.content_type}})};return true;})()""")
                page.set_content((ROOT/'apps/preview/index.html').read_text(encoding='utf-8'))
                page.get_by_role('button',name='Sign in').click()
                page.get_by_label('Password').fill('V4-Temporary-Browser-Password!')
                page.locator('.login button.btn').click()
                page.get_by_text('Your workspace').wait_for()
                page.get_by_role('button',name='Research & IntegrityBench').click()
                page.get_by_text('Research & IntegrityBench').first.wait_for()
                page.get_by_text('BPCE unsafe acceptance').wait_for()
                page.get_by_text('10.4%').first.wait_for()
                assert len(page.locator('.res-barrow').all())==8
                page.screenshot(path=str(ROOT/'docs/V4_RESEARCH_DESKTOP_SCREENSHOT.png'),full_page=True)
                page.locator('.res-selects select').nth(0).select_option('prompt_injection')
                page.wait_for_function("document.querySelectorAll('.res-selects select')[1]?.value==='PROMPT_INJECTION-000'")
                page.get_by_role('button',name='Replay evidence checks').click()
                page.locator('.res-result').wait_for()
                assert len(page.locator('.res-checks span').all())>=10
                page.screenshot(path=str(ROOT/'docs/V4_RESEARCH_REPLAY_SCREENSHOT.png'),full_page=True)
                page.locator('header select').select_option('bn-BD')
                page.get_by_text('রিসার্চ ও IntegrityBench').first.wait_for()
                page.set_viewport_size({'width':390,'height':844})
                page.screenshot(path=str(ROOT/'docs/V4_RESEARCH_MOBILE_SCREENSHOT.png'),full_page=True)
                page.locator('header select').select_option('zh-CN')
                page.get_by_text('研究与完整性测试').first.wait_for()
                assert not js_errors,js_errors
                browser.close()
            print('PASS V4 Chromium research dashboard: real API, 8 baselines, filtered replay, EN/BN/ZH, mobile')
        finally:
            proc.terminate()
            try:proc.communicate(timeout=6)
            except subprocess.TimeoutExpired:proc.kill();proc.communicate()

if __name__=='__main__':test_research_preview()
