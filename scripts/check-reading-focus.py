#!/usr/bin/env python3
"""Verify the two published readers after their 2026-11-18 visual corrections."""
import io
from PIL import Image
import functools,hashlib,http.server,importlib.util,json,subprocess,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/previews/reading-focus';OUT.mkdir(parents=True,exist_ok=True)
BASE='e578c2a85131c646ad4986e8c1367d7d60f8e652'
def jsdata(path,name):return json.loads((ROOT/path).read_text().split('const '+name+' = ')[1].rstrip(';\n'))
A=jsdata('anapana/book/book-data.js','BOOK');J=jsdata('four-jhanas/book/book-data.js','BOOK');F=jsdata('anapana/book/panel-focus-data.js','PANEL_FOCUS')['scenes']
def old(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
subprocess.run(['python3','scripts/build-anapana.py','--check'],cwd=ROOT,check=True)
spec=importlib.util.spec_from_file_location('jcheck',ROOT/'scripts/check-four-jhanas.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);mod.static_checks()
assert len(A['pages'])==119 and len(J['pages'])==131
assert (ROOT/'anapana/book/book-data.js').read_bytes()==old('anapana/book/book-data.js')
previous=json.loads(old('four-jhanas/book/book-data.js').decode().split('const BOOK = ')[1].rstrip(';\n'))
for before,after in zip(previous['pages'],J['pages']):
 if 'tableSummary' in before:before['tableSummary']=None
 assert before==after
for before,after in zip(previous['scenes'],J['scenes']):
 if before['id']=='S05':next(o for o in before['artOverlay'] if o['text']=='瞋恚')['y']=17
 assert before==after
allowed={'anapana/book/book.js','anapana/book/index.html','four-jhanas/book/book.js','four-jhanas/book/book.css','four-jhanas/book/book-data.js','four-jhanas/book/index.html'}
paths=subprocess.check_output(['git','ls-tree','-rz','--name-only',BASE],cwd=ROOT).split(b'\0')
for raw in paths:
 if not raw:continue
 name=raw.decode()
 if (any(name.startswith(k+'/') for k in mod.LEGACY+['four-jhanas']) or name.startswith('.github/') or name in ['index.html','reader-controls.css','reader-restart.js','picture-panel-focus.js','picture-panel-focus.css']) and name not in allowed:
  assert (ROOT/name).read_bytes()==old(name),name
assert len(F)==4 and sum(len(s['panels']) for s in F.values())==16
assert sum(len(s['pages']) for s in F.values())==55
for sid,focus in F.items():assert [p['paragraphId'] for p in A['pages'] if p['scene']==sid]==focus['paragraphIds']
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
report={'baseline':BASE,'viewports':mod.SIZES,'anapanaPageStates':0,'jhanasPageStates':0,'zoomStates':0,'errors':[],'physicalSafari':'未測；以Chromium觸控模擬','screenshots':[]}
def settle(page):
 page.wait_for_function('document.querySelector("#art-frame").hidden || (document.querySelector("#art").complete && document.querySelector("#art").naturalWidth>0)');page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
def shot(page,name):Image.open(io.BytesIO(page.screenshot())).save(OUT/name,lossless=True,method=6);report['screenshots'].append(name)
def check_mask(page,sid,local,zoom=False):
 frame='#zoom-frame' if zoom else '#art-frame';art='#zoom-art' if zoom else '#art';active=F.get(sid,{}).get('pages',[None]*30)[local-1]
 mask=page.locator(frame+' .picture-panel-focus');assert mask.count()==1
 assert mask.is_visible()==bool(active),(sid,local,zoom)
 if not active:assert mask.locator('span').count()==0;return
 assert mask.get_attribute('data-active-panel')==active
 r=page.evaluate('''([f,a])=>{const q=s=>document.querySelector(s),box=e=>e.getBoundingClientRect().toJSON();return {frame:box(q(f)),art:box(q(a)),mask:box(q(f+' .picture-panel-focus')),natural:[q(a).naturalWidth,q(a).naturalHeight],cells:[...q(f+' .picture-panel-focus').children].map(e=>({id:e.dataset.panel,r:box(e),color:getComputedStyle(e).backgroundColor,active:e.classList.contains('active')}))}}''',[frame,art])
 im=r['art'];scale=min(im['width']/r['natural'][0],im['height']/r['natural'][1]);w=scale*r['natural'][0];h=scale*r['natural'][1];m=r['mask']
 assert abs(m['width']-w)<1 and abs(m['height']-h)<1
 assert abs(m['x']-im['x']-(im['width']-w)/2)<1 and abs(m['y']-im['y']-(im['height']-h)/2)<1
 for cell,plan in zip(r['cells'],F[sid]['panels']):
  assert cell['id']==plan['id'] and cell['active']==(cell['id']==active)
  assert cell['color']==('rgba(0, 0, 0, 0)' if cell['active'] else 'rgba(5, 12, 20, 0.76)')
  for edge,coord,whole in [('x','x','width'),('y','y','height')]:assert abs(cell['r'][edge]-m[edge]-m[whole]*plan[coord]/100)<1
  for edge in ['width','height']:assert abs(cell['r'][edge]-m[edge]*plan[edge]/100)<1
def check_content(page,item,index,total):
 assert page.locator('#position-text').inner_text()==f'{index+1} / {total} 頁'
 assert page.locator('#narration p').all_text_contents()==item['lines']
 assert page.locator('#verse .scripture-card blockquote').all_text_contents()==[q['text'] for q in item['quotes']]
 assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
 assert page.locator('#next').evaluate('e=>getComputedStyle(e).touchAction')=='manipulation'
 r=page.locator('#art-frame').bounding_box();assert abs(r['width']/r['height']-item['dimensions'][0]/item['dimensions'][1])<.01
 assert page.locator('#caption').bounding_box()['y']<r['y']
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for w,h in mod.SIZES:
  page=browser.new_page(viewport={'width':w,'height':h},has_touch=True);page.on('pageerror',lambda e:report['errors'].append(str(e)));page.on('response',lambda r:report['errors'].append(str(r.status)+' '+r.url) if r.url.startswith(base) and r.status>=400 else None)
  page.goto(base+'anapana/book/');page.wait_for_function('typeof showPage==="function"')
  for i,item in enumerate(A['pages']):
   if item['scene'] not in F:continue
   page.evaluate('i=>showPage(i)',i);settle(page);check_content(page,item,i,119);check_mask(page,item['scene'],item['paragraphNumber']);report['anapanaPageStates']+=1
  for sid,focus in F.items():
   for panel in focus['panels']:
    local=focus['pages'].index(panel['id'])+1;i=next(i for i,x in enumerate(A['pages']) if x['scene']==sid and x['paragraphNumber']==local)
    page.evaluate('i=>showPage(i)',i);settle(page)
    if panel['id']=='p1' and (w,h) in [(360,800),(768,1024),(1024,768)]:shot(page,f'anapana-{sid}-{w}x{h}.webp')
    page.locator('#art').click();page.wait_for_function('document.querySelector("#zoom-art").complete');page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');check_mask(page,sid,local,True);report['zoomStates']+=1
    if panel['id']=='p2' and sid=='S06' and w==768:shot(page,'anapana-zoom-768x1024.webp')
    page.locator('#image-dialog form button').click();assert page.locator('#position-text').inner_text()==f'{i+1} / 119 頁'
  page.select_option('#page-select','S03');settle(page);check_mask(page,'S03',1)
  page.select_option('#page-select','S08');settle(page);check_mask(page,'S08',1)
  page.evaluate('showPage(45)');settle(page);position=page.locator('#position-text').inner_text();page.set_viewport_size({'width':h,'height':w});settle(page);assert page.locator('#position-text').inner_text()==position;check_mask(page,'S06',3);page.set_viewport_size({'width':w,'height':h});settle(page)
  page.locator('#open-verse').click();assert A['pages'][45]['quotes'][0]['text'] in page.locator('#dialog-verse').inner_text();page.locator('#verse-dialog form button').click()
  page.evaluate('showPage(0)')
  for _ in range(8):page.locator('#next').tap()
  page.locator('#previous').tap();assert page.locator('#position-text').inner_text()=='8 / 119 頁' and page.evaluate('visualViewport.scale')==1
  page.evaluate('showPage(118)');assert page.locator('#art-frame').is_hidden();page.locator('#next').tap();assert page.locator('#position-text').inner_text()=='1 / 119 頁'
  page.locator('.top a').click();assert '/anapana/' in page.url and '/book/' not in page.url
  page.goto(base+'four-jhanas/book/');page.wait_for_function('typeof showPage==="function"')
  for i,item in enumerate(J['pages']):
   if item['scene'] not in ['S05','S10'] or not item.get('paragraphId'):continue
   page.evaluate('i=>showPage(i)',i);settle(page);check_content(page,item,i,131);assert page.locator('#verse table').count()==0;report['jhanasPageStates']+=1
   if item['scene']=='S05':
    label=page.locator('#art-overlays .art-overlay').filter(has_text='瞋恚');r=label.bounding_box();f=page.locator('#art-frame').bounding_box();assert abs(r['y']-f['y']-.17*f['height'])<1;assert r['y']+r['height']<f['y']+.26*f['height']
   if i in [13,128] and (w,h) in [(360,800),(768,1024),(1024,768)]:shot(page,f'jhanas-{item["scene"]}-{w}x{h}.webp')
  page.evaluate('showPage(128)');settle(page);page.locator('#open-verse').click();text=page.locator('#dialog-verse').inner_text();assert all(q['text'] in text for q in J['pages'][128]['quotes']);assert '四禪比較' not in text;page.locator('#verse-dialog form button').click()
  page.locator('.verse-body').evaluate('e=>e.scrollTop=e.scrollHeight');assert page.locator('.verse-body').evaluate('e=>e.scrollTop>0');page.locator('#next').tap();assert page.locator('#position-text').inner_text()=='130 / 131 頁'
  page.select_option('#page-select','S05');settle(page);page.locator('#art').click();page.wait_for_function('document.querySelector("#zoom-art").complete');r=page.locator('#zoom-overlays .art-overlay').filter(has_text='瞋恚').bounding_box();f=page.locator('#zoom-frame').bounding_box();assert abs(r['y']-f['y']-.17*f['height'])<1;page.locator('#image-dialog form button').click()
  page.close();print(f'{w}x{h}: 55 Anapana +13 Jhanas states,16 focused zooms and controls passed',flush=True)
 browser.close()
server.shutdown();assert not report['errors'],report['errors']
assert report['anapanaPageStates']==275 and report['jhanasPageStates']==65 and report['zoomStates']==80
report['preserved']='130 Jhanas captions/times/quotes unchanged; Anapana119page data unchanged; original art and other10books/shared/Pages unchanged'
(OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('340 targeted page states and80 focused zooms passed',flush=True)
