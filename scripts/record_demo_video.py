"""Record a genuine API-backed Chromium internal payment-simulator demonstration (silent)."""
import os, subprocess, sys, tempfile, time, base64
from pathlib import Path
from urllib.request import urlopen
import requests
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
PORT=int(os.getenv('BP_V5_RECORD_PORT','8118'))

def record_finance_demo():
    with tempfile.TemporaryDirectory(prefix='bp-v2-e2e-') as temp:
        env=os.environ.copy()
        env.update({'DATABASE_URL':f'sqlite:///{temp}/test.sqlite3','PRIVATE_UPLOAD_DIR':f'{temp}/uploads','APP_ENV':'development','ENABLE_DEMO_SEED':'1','DEMO_SEED_PASSWORD':'Demo-Preview-Strong-2026','ALLOWED_ORIGINS':f'http://127.0.0.1:{PORT},http://localhost:3000'})
        proc=subprocess.Popen([sys.executable,'-m','uvicorn','app.main:app','--host','127.0.0.1','--port',str(PORT)],cwd=str(ROOT/'services/api'),env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        try:
            for k in range(100):
                try:
                    with urlopen(f'http://127.0.0.1:{PORT}/api/v1/health',timeout=.4) as r:
                        if r.status==200:break
                except Exception:time.sleep(.1)
            with sync_playwright() as p:
                browser=p.chromium.launch(headless=True,slow_mo=160,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
                video_dir=ROOT/'submissions'/'video_raw';video_dir.mkdir(parents=True,exist_ok=True)
                context=browser.new_context(viewport={'width':1280,'height':720},record_video_dir=str(video_dir),record_video_size={'width':1280,'height':720},accept_downloads=True)
                page=context.new_page();page.set_default_timeout(6500)
                session=requests.Session()
                def bridge(req):
                    opts={'timeout':10,'headers':req.get('headers') or {}}
                    if req.get('form'):
                        data,files={},{}
                        for item in req['form']:
                            if item.get('file'):files[item['key']]=(item['name'],base64.b64decode(item['data']),item['mime'])
                            else:data[item['key']]=item['value']
                        opts.update({'data':data,'files':files})
                    else:opts['data']=req.get('body')
                    r=session.request(req.get('method','GET'),f'http://127.0.0.1:{PORT}'+req['url'],**opts)
                    return {'status':r.status_code,'text':r.text,'content_type':r.headers.get('Content-Type','application/json')}
                page.expose_function('bridgeRequest',bridge)
                page.evaluate(r"""(()=>{const store={};Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>store[k]??null,setItem:(k,v)=>{store[k]=String(v)}}});window.history.replaceState=()=>{};window.fetch=async function(url,init={}){
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
                page.on('pageerror',lambda err:print('PAGEERROR',err))
                errors=[]
                page.on('pageerror',lambda err:errors.append(str(err)))
                page.set_content((ROOT/'apps/preview/index.html').read_text(encoding='utf8'))
                page.wait_for_timeout(2200)
                page.get_by_role('button',name='Sign in').click()
                page.get_by_label('Password').fill('Demo-Preview-Strong-2026')
                page.locator('.login button.btn').click()
                page.get_by_text('Your international financial mission').wait_for()
                page.wait_for_timeout(1500)
                page.get_by_role('button',name='Payment lab').click()
                page.get_by_text('Financial execution lab').wait_for()
                page.get_by_text('Synthetic BDT account').wait_for()
                page.wait_for_timeout(1900)
                page.get_by_role('button',name='Attach synthetic example invoice').click()
                page.wait_for_function("Array.from(document.querySelectorAll('option')).some(o=>o.textContent.includes('SYNTHETIC-Northbridge-invoice.txt'))")
                page.get_by_role('button',name='Extract fields').click()
                page.get_by_text('DEMO-2026-0042').wait_for()
                page.wait_for_timeout(1700)
                page.get_by_role('button',name='Investigate evidence').click()
                page.get_by_text('SANDBOX_FIXTURE_MATCH',exact=True).first.wait_for()
                page.wait_for_timeout(1700)
                page.get_by_role('button',name='CAMPUS_SIM_A').click()
                page.get_by_text('2024350.00 BDT').first.wait_for()
                page.wait_for_timeout(1500)
                page.once('dialog',lambda dialog:dialog.accept())
                page.get_by_role('button',name='Authorize this simulation').click()
                page.get_by_text('ACTIVE',exact=True).first.wait_for()
                page.wait_for_timeout(1700)
                page.once('dialog',lambda dialog:dialog.accept())
                page.get_by_role('button',name='Execute simulated transfer').click()
                page.get_by_text('COMPLETED').first.wait_for()
                page.get_by_text('975650.00 BDT').wait_for()
                page.wait_for_timeout(1800)
                page.get_by_role('button',name='Decision receipt').last.click()
                page.locator('.fin-receipt p').filter(has_text='NOT A BANK RECEIPT').wait_for()
                page.wait_for_timeout(2800)
                assert not errors,errors
                page.screenshot(path=str(ROOT/'docs/V2_FINANCE_BROWSER_SCREENSHOT.png'),full_page=True)
                page.get_by_role('button',name='Evidence & support').click()
                page.get_by_role('heading',name='Evidence & recovery').wait_for()
                page.wait_for_timeout(1400)
                page.get_by_role('button',name='Inspect safe next step').click()
                page.wait_for_timeout(1600)
                page.get_by_role('button',name='Research & IntegrityBench').click()
                page.get_by_text('BPCE unsafe acceptance').wait_for()
                page.wait_for_timeout(2700)
                page.get_by_role('button',name='Payment lab').click()
                page.get_by_text('Financial execution lab').wait_for()
                page.wait_for_timeout(900)
                page.locator('header select').select_option('bn-BD')
                page.get_by_text('ফাইন্যান্স এক্সিকিউশন ল্যাব').first.wait_for()
                page.screenshot(path=str(ROOT/'docs/V2_FINANCE_BANGLA_SCREENSHOT.png'),full_page=True)
                page.locator('header select').select_option('zh-CN')
                page.get_by_text('金融执行实验室').first.wait_for()
                page.set_viewport_size({'width':390,'height':844})
                page.screenshot(path=str(ROOT/'docs/V2_FINANCE_MOBILE_SCREENSHOT.png'),full_page=True)
                page.wait_for_timeout(1000)
                context.close()
                video_path=page.video.path()
                from shutil import copyfile
                dest=ROOT/'submissions'/'BorderProof_AI_V5_Actual_Browser_Capture_SILENT.webm'
                copyfile(video_path,dest)
                print('RECORDED',dest,dest.stat().st_size)
                browser.close()
            print('PASS: V2 Chromium UI + real FastAPI requests: demo invoice → extract → investigate → quote → approve → execute → receipt → 3 locales + mobile')
        finally:
            proc.terminate()
            try:proc.communicate(timeout=5)
            except subprocess.TimeoutExpired:proc.kill();proc.communicate()

if __name__=='__main__':record_finance_demo()
