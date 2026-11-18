#!/usr/bin/env python3
"""Regression: main controls must visit every original cue, including 念覺支."""
import functools,http.server,importlib.util,io,json,subprocess,tempfile,threading,zipfile
from pathlib import Path
from PIL import Image
from lxml import html
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'docs/previews/seven-sequence';O.mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location('original_check',R/'scripts/check-seven-factors.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old);old.static()
assert (R/'seven-factors/book/book-data.js').read_bytes()==subprocess.check_output(['git','show','fe9c5d9:seven-factors/book/book-data.js'],cwd=R)
root=html.parse(str(R/'seven-factors/index.html'));assert not root.xpath('//a[@download]') and not root.xpath('//a[contains(@href,"13.jpeg")]')
steps=[(i,j,c) for i,p in enumerate(old.BOOK['pages']) for j,c in enumerate(p['cues'])];assert len(steps)==36
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
def verify(page,k):
 i,j,c=steps[k];old.settle(page);assert page.locator('#narration p').all_text_contents()==[c['text']],(k,c['id']);assert page.locator('.page').get_attribute('data-paragraph')==c['id']
 assert page.locator('#verse blockquote').all_text_contents()==[q['text'] for q in c['quotes']]
 assert page.locator('#position-text').inner_text()==f'{k+1} / 37 段 · {i+1}/12 頁'
 assert not page.evaluate('document.documentElement.scrollWidth>innerWidth');old.focus(page,old.BOOK['pages'][i]['scene'],j)
 assert page.locator('#next').get_attribute('aria-label')=='下一頁'
 assert page.locator('#cue-nav').count()==0
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
report={'forward':0,'reverse':0,'offlineForward':0,'viewports':old.SIZES,'errors':[],'physicalSafari':'not tested','data':'all36original cues/times/quotes byte-identical to published version'}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for w,h in old.SIZES:
  page=b.new_page(viewport={'width':w,'height':h},has_touch=True);page.on('pageerror',lambda e:report['errors'].append(str(e)));page.goto(base+'seven-factors/book/?scene=S01&cue=1');page.wait_for_function('typeof showPage==="function"')
  for k,(i,j,c) in enumerate(steps):
   verify(page,k);report['forward']+=1
   if k in [8,29,30,35] and (w,h) in [(768,1024),(1024,768)]:Image.open(io.BytesIO(page.screenshot())).save(O/f'{c["id"]}-{w}x{h}.webp',lossless=True,method=6)
   if k<35:page.locator('#next').tap()
  for k in range(35,-1,-1):
   verify(page,k);report['reverse']+=1
   if k:page.locator('#previous').tap()
  for _ in range(8):page.locator('#next').tap()
  verify(page,8);assert '念覺支' in page.locator('#narration').inner_text()
  page.locator('#art').focus();page.keyboard.press('ArrowRight');verify(page,9);page.keyboard.press('ArrowLeft');verify(page,8)
  page.evaluate('''()=>{const target=document.querySelector('.page');const a=new Touch({identifier:1,target,clientX:250,clientY:240});const b=new Touch({identifier:1,target,clientX:80,clientY:240});target.dispatchEvent(new TouchEvent('touchstart',{touches:[a],bubbles:true}));target.dispatchEvent(new TouchEvent('touchend',{touches:[],changedTouches:[b],bubbles:true}));}''');verify(page,9)
  page.set_viewport_size({'width':h,'height':w});old.settle(page);verify(page,9);page.set_viewport_size({'width':w,'height':h});page.reload();verify(page,9)
  page.evaluate('showPage(11,0)');assert page.locator('#next').get_attribute('aria-label')=='下一頁'
  for _ in range(5):page.locator('#next').tap()
  verify(page,35);page.locator('#next').tap();assert '走入經藏的起點' in page.locator('#summary-text').inner_text();page.locator('#next').tap();verify(page,0)
  page.locator('.top a').click();page.wait_for_load_state();assert page.locator('a[download]').count()==0 and page.locator('a[href="assets/13.jpeg"]').count()==0
  with tempfile.TemporaryDirectory(prefix='seven-sequence-') as tmp:
   with zipfile.ZipFile(R/'downloads/SutraZen-Seven-Factors-Offline.zip') as z:assert z.testzip() is None;z.extractall(tmp)
   local=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=tmp));threading.Thread(target=local.serve_forever,daemon=True).start();lb=f'http://127.0.0.1:{local.server_port}/';context=b.new_context(viewport={'width':w,'height':h},has_touch=True);context.route('**/*',lambda route:route.continue_() if route.request.url.startswith(lb) else route.abort());offline=context.new_page();offline.on('pageerror',lambda e:report['errors'].append(str(e)));offline.goto(lb+'seven-factors/book/');offline.wait_for_function('typeof showPage==="function"')
   for k in range(36):
    verify(offline,k);report['offlineForward']+=1
    if k<35:offline.locator('#next').tap()
   offline.locator('#next').tap();assert '走入經藏的起點' in offline.locator('#summary-text').inner_text();offline.locator('#next').tap();verify(offline,0);context.close();local.shutdown()
  page.close();print(w,h,'all36main-next/main-previous/offline-next and keyboard/swipe/restart passed',flush=True)
 b.close()
server.shutdown();assert not report['errors'];assert report['forward']==report['reverse']==report['offlineForward']==180;(O/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
