#!/usr/bin/env python3
"""Verify S08's four ways while preserving the published Anapana content."""
import functools,http.server,io,json,subprocess,threading
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'docs/previews/anapana-four-ways';O.mkdir(parents=True,exist_ok=True)
def load(path,key):return json.loads((R/path).read_text().split('const '+key+' = ')[1].rstrip(';\n'))
b=load('anapana/book/book-data.js','BOOK');f=load('anapana/book/panel-focus-data.js','PANEL_FOCUS')['scenes']['S08']
assert (R/'anapana/book/book-data.js').read_bytes()==subprocess.check_output(['git','show','b362653:anapana/book/book-data.js'],cwd=R)
assert f['pages']==[None]*5+['p1']*3+['p2']*3+['p3']*2+['p4']*2
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=s.serve_forever,daemon=True).start()
report={'pageStates':0,'zoomStates':0,'errors':[],'viewports':[],'physicalSafari':'not tested'}
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for w,h in [(360,800),(800,360),(768,1024),(1024,768),(1440,900)]:
  page=browser.new_page(viewport={'width':w,'height':h},has_touch=True);page.on('pageerror',lambda e:report['errors'].append(str(e)));page.goto(f'http://127.0.0.1:{s.server_port}/anapana/book/?scene=S08');page.wait_for_function('typeof showPage==="function"')
  for i,item in enumerate(b['pages']):
   if item['scene']!='S08':continue
   page.evaluate('i=>showPage(i)',i);page.wait_for_function('document.querySelector("#art").complete && document.querySelector("#art").naturalWidth>0');page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
   active=f['pages'][item['paragraphNumber']-1];m=page.locator('#art-frame .picture-panel-focus');assert m.is_visible()==bool(active)
   assert page.locator('#narration p').all_text_contents()==item['lines'] and not page.evaluate('document.documentElement.scrollWidth>innerWidth')
   assert page.locator('#verse blockquote').all_text_contents()==[q['text'] for q in item['quotes']]
   if active:assert m.get_attribute('data-active-panel')==active and m.locator('span:not(.active)').count()==3
   report['pageStates']+=1
  for cell in f['panels']:
   local=f['pages'].index(cell['id'])+1;i=71+local-1;page.evaluate('i=>showPage(i)',i)
   if (w,h) in [(768,1024),(1024,768)]:Image.open(io.BytesIO(page.screenshot())).save(O/f'{cell["id"]}-{w}x{h}.webp',lossless=True,method=6)
   page.locator('#art').click();page.wait_for_function('document.querySelector("#zoom-art").complete');assert page.locator('#zoom-frame .picture-panel-focus').get_attribute('data-active-panel')==cell['id'];assert page.locator('#zoom-frame .picture-panel-focus span:not(.active)').count()==3;report['zoomStates']+=1
   page.locator('#image-dialog form button').click();position=page.locator('#position-text').inner_text();page.set_viewport_size({'width':h,'height':w});assert page.locator('#position-text').inner_text()==position;page.set_viewport_size({'width':w,'height':h})
  page.select_option('#page-select','S09');assert page.locator('#art-frame .picture-panel-focus').is_hidden();page.select_option('#page-select','S08');assert page.locator('#art-frame .picture-panel-focus').is_hidden()
  for _ in range(6):page.locator('#next').tap()
  assert page.locator('#position-text').inner_text()=='78 / 119 頁' and page.evaluate('visualViewport.scale')==1 and page.locator('#next').evaluate('e=>getComputedStyle(e).touchAction')=='manipulation'
  page.close();report['viewports'].append([w,h]);print(w,h,'passed',flush=True)
 browser.close()
s.shutdown();assert report['pageStates']==75 and report['zoomStates']==20 and not report['errors'];(O/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
