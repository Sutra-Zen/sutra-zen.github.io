#!/usr/bin/env python3
"""Check the published Iddhipada reader's paragraph-specific comic focus."""
import functools,http.server,io,json,subprocess,threading
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/previews/iddhipada-focus';OUT.mkdir(parents=True,exist_ok=True)
BASE='7f19874e1380102577eae1a6a34f2bf6a99a7326'
def data(path,key):return json.loads((ROOT/path).read_text().split('const '+key+' = ')[1].rstrip(';\n'))
BOOK=data('iddhipada/book/book-data.js','BOOK');FOCUS=data('iddhipada/book/panel-focus-data.js','PANEL_FOCUS')['scenes']
def old(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
subprocess.run(['python3','scripts/build-iddhipada.py','--check'],cwd=ROOT,check=True)
assert (ROOT/'iddhipada/book/book-data.js').read_bytes()==old('iddhipada/book/book-data.js')
assert len(BOOK['pages'])==82 and len(BOOK['scenes'])==9 and sum(len(s['panels']) for s in FOCUS.values())==8
for sid,f in FOCUS.items():assert f['paragraphIds']==[p['paragraphId'] for p in BOOK['pages'] if p['scene']==sid]
books=['four-truths','five-aggregates','six-senses','twelve-links','eightfold-path','four-fruits-ten-fetters','four-purities-six-recollections','mindfulness','right-effort','anapana','iddhipada','four-jhanas']
for raw in subprocess.check_output(['git','ls-tree','-rz','--name-only',BASE],cwd=ROOT).split(b'\0'):
 if not raw:continue
 name=raw.decode()
 if name in ['iddhipada/book/index.html','iddhipada/book/book.js']:continue
 if any(name.startswith(b+'/') for b in books) or name.startswith('.github/') or name in ['index.html','shelf.css','reader-controls.css','reader-restart.js','picture-panel-focus.js','picture-panel-focus.css','.nojekyll','CNAME']:
  assert (ROOT/name).read_bytes()==old(name),name
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
sizes=[(360,800),(800,360),(768,1024),(1024,768),(1440,900)]
report={'baseline':BASE,'viewports':sizes,'targetPageStates':0,'focusedZoomStates':0,'nonComicStates':0,'javascriptErrors':[],'httpErrors':[],'screenshots':[],'physicalSafari':'未測；以Chromium觸控模擬'}
def settle(page):
 page.wait_for_function('document.querySelector("#art-frame").hidden || (document.querySelector("#art").complete && document.querySelector("#art").naturalWidth>0)');page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
def shot(page,name):Image.open(io.BytesIO(page.screenshot())).save(OUT/name,lossless=True,method=6);report['screenshots'].append(name)
def mask(page,scene,local,zoom=False):
 frame='#zoom-frame' if zoom else '#art-frame';art='#zoom-art' if zoom else '#art';active=FOCUS.get(scene,{}).get('pages',[None]*90)[local-1]
 m=page.locator(frame+' .picture-panel-focus');assert m.count()==1 and m.is_visible()==bool(active),(scene,local,zoom)
 if not active:assert m.locator('span').count()==0;return
 assert m.get_attribute('data-active-panel')==active
 r=page.evaluate('''([f,a])=>{const q=s=>document.querySelector(s),box=e=>e.getBoundingClientRect().toJSON();return {image:box(q(a)),mask:box(q(f+' .picture-panel-focus')),natural:[q(a).naturalWidth,q(a).naturalHeight],cells:[...q(f+' .picture-panel-focus').children].map(e=>({id:e.dataset.panel,r:box(e),color:getComputedStyle(e).backgroundColor}))}}''',[frame,art])
 image=r['image'];scale=min(image['width']/r['natural'][0],image['height']/r['natural'][1]);width=r['natural'][0]*scale;height=r['natural'][1]*scale;m=r['mask']
 assert abs(m['width']-width)<1 and abs(m['height']-height)<1
 assert abs(m['x']-image['x']-(image['width']-width)/2)<1 and abs(m['y']-image['y']-(image['height']-height)/2)<1
 for c,p in zip(r['cells'],FOCUS[scene]['panels']):
  assert c['id']==p['id'] and c['color']==('rgba(0, 0, 0, 0)' if c['id']==active else 'rgba(5, 12, 20, 0.76)')
  assert abs(c['r']['x']-m['x']-m['width']*p['x']/100)<1 and abs(c['r']['y']-m['y']-m['height']*p['y']/100)<1
  assert abs(c['r']['width']-m['width']*p['width']/100)<1 and abs(c['r']['height']-m['height']*p['height']/100)<1
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for w,h in sizes:
  page=browser.new_page(viewport={'width':w,'height':h},has_touch=True);page.on('pageerror',lambda e:report['javascriptErrors'].append(str(e)));page.on('response',lambda r:report['httpErrors'].append(r.url) if r.url.startswith(base) and r.status>=400 else None)
  page.goto(base+'iddhipada/book/');page.wait_for_function('typeof showPage==="function"')
  for i,item in enumerate(BOOK['pages']):
   if item['scene'] not in FOCUS:continue
   scene=next(s for s in BOOK['scenes'] if s['id']==item['scene']);local=i-scene['start']+1
   page.evaluate('i=>showPage(i)',i);settle(page);mask(page,item['scene'],local)
   assert page.locator('#position-text').inner_text()==f'{i+1} / 82 頁' and page.locator('#narration p').all_text_contents()==item['lines']
   assert page.locator('#art-overlays .art-overlay').all_text_contents()==[o['text'] for o in scene['artOverlay']]
   assert page.locator('#verse .scripture-card h3').all_text_contents()==[q['source'] for q in item['quotes']]
   for q in item['quotes']:assert q['originalText'] in page.locator('#verse').text_content() and (not q['translationNote'] or q['translationNote'] in page.locator('#verse').text_content())
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
   assert page.locator('#next').evaluate('e=>getComputedStyle(e).touchAction')=='manipulation'
   r=page.locator('#art-frame').bounding_box();assert abs(r['width']/r['height']-1672/941)<.005
   c=page.locator('#caption').bounding_box();v=page.locator('.scripture').bounding_box();assert c['y']+c['height']<=r['y']+1 and r['y']+r['height']<=v['y']+1
   report['targetPageStates']+=1
  for sid,f in FOCUS.items():
   scene=next(s for s in BOOK['scenes'] if s['id']==sid)
   for cell in f['panels']:
    local=f['pages'].index(cell['id'])+1;i=scene['start']+local-1;page.evaluate('i=>showPage(i)',i);settle(page)
    if (w,h) in [(768,1024),(1024,768)] or (w==360 and cell['id']=='p3'):shot(page,f'{sid}-{cell["id"]}-{w}x{h}.webp')
    page.locator('#art').click();page.wait_for_function('document.querySelector("#zoom-art").complete');page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');mask(page,sid,local,True);report['focusedZoomStates']+=1
    if w==768 and sid=='S06' and cell['id']=='p4':shot(page,'S06-p4-zoom-768x1024.webp')
    page.locator('#image-dialog form button').click();assert page.locator('#position-text').inner_text()==f'{i+1} / 82 頁'
  for scene in BOOK['scenes']:
   if scene['id'] in FOCUS:continue
   page.select_option('#page-select',scene['id']);settle(page);mask(page,scene['id'],1);report['nonComicStates']+=1
  page.evaluate('showPage(49)');settle(page);position=page.locator('#position-text').inner_text();page.set_viewport_size({'width':h,'height':w});settle(page);assert page.locator('#position-text').inner_text()==position;mask(page,'S06',3);page.set_viewport_size({'width':w,'height':h});settle(page)
  page.locator('#open-verse').click();assert BOOK['pages'][49]['quotes'][0]['originalText'] in page.locator('#dialog-verse').text_content();page.locator('.verse-scroll').evaluate('e=>e.scrollTop=e.scrollHeight');page.locator('#verse-dialog form button').click()
  page.evaluate('showPage(0)')
  for _ in range(8):page.locator('#next').tap()
  page.locator('#previous').tap();assert page.locator('#position-text').inner_text()=='8 / 82 頁' and page.evaluate('visualViewport.scale')==1;mask(page,'S01',8)
  page.evaluate('showPage(81)');assert page.locator('#art-frame').is_hidden();page.locator('#next').tap();assert page.locator('#position-text').inner_text()=='1 / 82 頁';mask(page,'S01',1)
  page.locator('.top a').click();assert '/iddhipada/' in page.url and '/book/' not in page.url
  page.close();print(f'{w}x{h}:23 comic paragraphs,8 focused zooms and7 noncomic scenes passed',flush=True)
 browser.close()
server.shutdown();assert not report['javascriptErrors'] and not report['httpErrors'],report
assert report['targetPageStates']==115 and report['focusedZoomStates']==40 and report['nonComicStates']==35
(OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('115 comic-page states,40 focused zooms,35 full-image scene states passed',flush=True)
