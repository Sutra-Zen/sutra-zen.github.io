#!/usr/bin/env python3
"""Check twelve pages,36timed cues, center coordinates and downloaded-file offline use."""
import functools,hashlib,http.server,io,json,re,subprocess,tempfile,threading,zipfile,urllib.request
from pathlib import Path
from urllib.parse import urlsplit,unquote
from PIL import Image
from lxml import html
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];D=R/'docs/seven-factors';O=R/'docs/previews/seven-factors';O.mkdir(parents=True,exist_ok=True);BASE='99b1a1d96169917ad682f8df72649b0da1cd8388'
STORY=json.loads((D/'storyboard.json').read_text());CAT=json.loads((D/'scripture-catalog.json').read_text());BOOK=json.loads((R/'seven-factors/book/book-data.js').read_text().split('const BOOK = ')[1].rstrip(';\n'))
LEGACY=['four-truths','five-aggregates','six-senses','twelve-links','eightfold-path','four-fruits-ten-fetters','four-purities-six-recollections','mindfulness','right-effort','anapana','iddhipada','four-jhanas','five-roots-powers']
SIZES=[(360,800),(800,360),(768,1024),(1024,768),(1440,900)]
def old(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=R)
def static():
 subprocess.run(['python3','scripts/build-seven-factors.py','--check'],cwd=R,check=True)
 assert len(BOOK['pages'])==12 and sum(len(s['cues']) for s in BOOK['pages'])==36 and len(CAT)==16
 for scene,page in zip(STORY,BOOK['pages']):
  assert scene['id']==page['scene'] and page['artOverlay']==scene['artOverlay']
  for c,view in zip(scene['cues'],page['cues']):assert view['text']==c['text'] and view['startSeconds']==c['startSeconds'] and view['endSeconds']==c['endSeconds'] and view['quotes']==[CAT[q] for q in c['quoteIds']]
 assert not BOOK['pages'][11]['artOverlay'] and len(BOOK['pages'][10]['artOverlay'])==2
 assert all('猗' in q['text'] for q in CAT.values() if q['quoteId'] in ['Q09'])
 for raw in subprocess.check_output(['git','ls-tree','-rz','--name-only',BASE],cwd=R).split(b'\0'):
  if not raw:continue
  name=raw.decode()
  if any(name.startswith(k+'/') for k in LEGACY) or name.startswith('.github/') or name in ['reader-controls.css','reader-restart.js','picture-panel-focus.js','picture-panel-focus.css','guide-header.css','guide-ui.css','shelf.css','.nojekyll','CNAME']:assert (R/name).read_bytes()==old(name),name
 a,b=[json.loads(re.search(r'const dhammaData = (.*?);\s*\n',s)[1]) for s in [old('index.html').decode(),(R/'index.html').read_text()]];assert a.keys()==b.keys()
 for key in a:
  if key!='七覺支總說':assert a[key]==b[key]
 assert 'seven-factors/index.html' in b['七覺支總說']['content']
 root=html.parse(str(R/'index.html'));assert len(root.xpath('//*[contains(concat(" ",@class," ")," sz-ready ")]'))==14 and not root.xpath('//*[@class="sz-book-lock"]') and root.xpath('//iframe/@src')==html.fromstring(old('index.html')).xpath('//iframe/@src')
 for name in ['seven-factors/index.html','seven-factors/book/index.html']:
  tree=html.parse(str(R/name));assert 'data:image' not in (R/name).read_text()
  for url in tree.xpath('//@src|//@href'):
   u=urlsplit(url)
   if u.scheme or u.netloc:continue
   p=((R/name).parent/unquote(u.path)).resolve()
   if p.is_dir():p/='index.html'
   assert p.is_file(),(name,url)
   if u.fragment:assert html.parse(str(p)).xpath('//*[@id=$id]',id=u.fragment)
 guide=html.parse(str(R/'seven-factors/index.html'))
 for source in json.loads((D/'verified-sources.json').read_text())['sources']:
  assert guide.xpath('//*[@id=$id]//blockquote/p/text()',id=source['id'])==[s['text'] for s in source['sections']]
 print('Source content,36timed cues,13images,14overlays and13legacy books verified',flush=True)
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
def settle(page):
 page.wait_for_function('document.querySelector("#art").complete && document.querySelector("#art").naturalWidth>0');page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
def shot(page,name):Image.open(io.BytesIO(page.screenshot())).save(O/name,lossless=True,method=6)
def labels(page,selector,frame,plan):
 rows=page.locator(selector).evaluate_all('els=>els.map(e=>({text:e.textContent,r:e.getBoundingClientRect().toJSON(),font:parseFloat(getComputedStyle(e).fontSize),color:getComputedStyle(e).color}))');assert len(rows)==len(plan)
 for a,b in zip(rows,plan):
  assert a['text']==b['text'] and a['color']=='rgb(0, 0, 0)'
  assert abs(a['r']['x']+a['r']['width']/2-frame['x']-frame['width']*b['x']/100)<1 and abs(a['r']['y']+a['r']['height']/2-frame['y']-frame['height']*b['y']/100)<1
  assert abs(a['font']-frame['height']*b['heightPct']/100)<.2
  assert a['r']['x']>=frame['x']-1 and a['r']['right']<=frame['right']+1
def focus(page,scene,cue,zoom=False):
 selector=('#zoom-frame' if zoom else '#art-frame')+' .picture-panel-focus';m=page.locator(selector);active=('left' if cue==3 else 'right' if cue==4 else None) if scene=='S11' else None
 assert m.is_visible()==bool(active),(scene,cue,zoom)
 if active:assert m.get_attribute('data-active-panel')==active and m.locator('span:not(.active)').count()==1 and m.locator('span:not(.active)').evaluate('e=>getComputedStyle(e).backgroundColor')=='rgba(5, 12, 20, 0.76)'
def content(page,i,j):
 scene=BOOK['pages'][i];cue=scene['cues'][j];assert page.locator('#position-text').inner_text()==f'{i+1} / 12 頁';assert page.locator('#narration p').all_text_contents()==[cue['text']]
 assert page.locator('#verse blockquote').all_text_contents()==[q['text'] for q in cue['quotes']]
 assert page.locator('.page').get_attribute('data-paragraph')==cue['id'] and page.locator('.page').get_attribute('data-start-seconds')==str(int(cue['startSeconds']))
 assert not page.evaluate('document.documentElement.scrollWidth>innerWidth');assert page.locator('#next').evaluate('e=>getComputedStyle(e).touchAction')=='manipulation'
 box=page.locator('#art-frame').evaluate('e=>e.getBoundingClientRect().toJSON()');assert abs(box['width']/box['height']-scene['dimensions'][0]/scene['dimensions'][1])<.005
 cap=page.locator('#caption').bounding_box();verse=page.locator('.scripture').bounding_box();assert cap['y']+cap['height']<=box['y']+1
 if cue['quotes']:assert box['bottom']<=verse['y']+1
 labels(page,'#art-overlays .art-overlay',box,scene['artOverlay']);focus(page,scene['scene'],j)
def browser():
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/';report={'baseline':BASE,'viewports':SIZES,'onlineCueStates':0,'offlineCueStates':0,'zoomLabels':0,'errors':[],'physicalSafari':'not tested','publication':'review only,not merged or deployed'}
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);cache={}
  for url in ['https://cdn.tailwindcss.com/','https://unpkg.com/lucide@latest']:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40) as response:cache[url]=(response.read(),response.headers.get('Content-Type','application/javascript'))
  for w,h in SIZES:
   page=b.new_page(viewport={'width':w,'height':h},has_touch=True);page.on('pageerror',lambda e:report['errors'].append(str(e)));page.on('response',lambda r:report['errors'].append(r.url) if r.url.startswith(base) and r.status>=400 else None);page.route('https://www.youtube.com/**',lambda r:r.abort());page.goto(base+'seven-factors/book/');page.wait_for_function('typeof showPage==="function"')
   for i,scene in enumerate(BOOK['pages']):
    page.select_option('#page-select',scene['id']);settle(page)
    for j,cue in enumerate(scene['cues']):
     page.select_option('#cue-select',str(j));settle(page);content(page,i,j);report['onlineCueStates']+=1
     if (w,h) in [(768,1024),(1024,768)] and (j==0 or (i==10 and j in [3,4,5])):shot(page,f'{scene["scene"]}-cue{j+1}-{w}x{h}.webp')
     if w==360 and i in [2,7,10] and j==0:shot(page,f'{scene["scene"]}-360x800.webp')
     if scene['artOverlay'] and (j==0 or i==10):
      page.locator('#art').click();page.wait_for_function('document.querySelector("#zoom-art").complete');labels(page,'#zoom-overlays .art-overlay',page.locator('#zoom-frame').evaluate('e=>e.getBoundingClientRect().toJSON()'),scene['artOverlay']);focus(page,scene['id'],j,True);report['zoomLabels']+=len(scene['artOverlay']);page.locator('#image-dialog form button').click()
   page.evaluate('showPage(10,4)');settle(page);page.set_viewport_size({'width':h,'height':w});settle(page);content(page,10,4);page.set_viewport_size({'width':w,'height':h});page.reload();settle(page);content(page,10,4)
   page.locator('#open-verse').click();assert CAT['Q14']['text'] in page.locator('#dialog-verse').inner_text();page.locator('#verse-dialog form button').click()
   page.evaluate('showPage(0)')
   for _ in range(3):page.locator('#next').tap()
   page.locator('#previous').tap();assert page.locator('#position-text').inner_text()=='3 / 12 頁' and page.evaluate('visualViewport.scale')==1
   page.evaluate('showPage(11,5)');assert page.locator('#reader-note').is_visible();page.locator('#next').tap();content(page,0,0)
   page.locator('.top a').click();page.wait_for_load_state();assert page.locator('h1').inner_text()=='七覺支' and not page.evaluate('document.documentElement.scrollWidth>innerWidth')
   if w in [768,1024]:shot(page,f'guide-{w}x{h}.webp');page.locator('#sources').scroll_into_view_if_needed();shot(page,f'sources-{w}x{h}.webp')
   with page.expect_download() as info:page.locator('a[download]').click()
   download=info.value
   with tempfile.TemporaryDirectory(prefix='seven-offline-') as tmp:
    archive=Path(tmp)/'download.zip';download.save_as(archive);assert archive.read_bytes()==(R/'downloads/SutraZen-Seven-Factors-Offline.zip').read_bytes()
    with zipfile.ZipFile(archive) as z:assert z.testzip() is None;z.extractall(Path(tmp)/'extracted')
    local=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(Path(tmp)/'extracted')));threading.Thread(target=local.serve_forever,daemon=True).start();localbase=f'http://127.0.0.1:{local.server_port}/'
    context=b.new_context(viewport={'width':w,'height':h},has_touch=True)
    context.route('**/*',lambda route:route.continue_() if route.request.url.startswith(localbase) else route.abort())
    offline=context.new_page();offline.on('pageerror',lambda e:report['errors'].append('offline:'+str(e)));offline.goto(localbase+'seven-factors/book/index.html');offline.wait_for_function('typeof showPage==="function"')
    for i,scene in enumerate(BOOK['pages']):
     offline.select_option('#page-select',scene['id']);settle(offline)
     for j in range(len(scene['cues'])):offline.select_option('#cue-select',str(j));settle(offline);content(offline,i,j);report['offlineCueStates']+=1
     if i<11:offline.locator('#next').tap();assert offline.locator('#position-text').inner_text()==f'{i+2} / 12 頁'
    offline.locator('#next').tap();content(offline,0,0);offline.evaluate('showPage(10,3)');settle(offline);offline.locator('#art').click();offline.wait_for_function('document.querySelector("#zoom-art").complete');focus(offline,'S11',3,True);offline.locator('#image-dialog form button').click();offline.locator('.top a').click();offline.wait_for_load_state();assert offline.locator('#sources article').count()==5;context.close();local.shutdown()
   page.close();print(w,h,'36online +36downloaded-file offline cues,controls and centered overlays passed',flush=True)
  page=b.new_page(viewport={'width':1024,'height':768});page.route('https://www.youtube.com/**',lambda r:r.abort())
  for url in cache:
   page.route(url+'**' if 'tailwind' in url else url,lambda route:route.fulfill(status=200,body=cache[route.request.url][0],content_type=cache[route.request.url][1]))
  page.goto(base);page.locator('.sz-book[href="./seven-factors/book/index.html"]').click();settle(page);page.goto(base);page.evaluate('openModal("七覺支總說")');page.locator('#modalBody a[href="./seven-factors/index.html"]').click();assert page.locator('h1').inner_text()=='七覺支'
  for name in LEGACY:
   page.goto(base+name+'/book/');page.locator('#next').wait_for(state='visible');before=page.locator('#position-text').inner_text();page.locator('#next').click();assert page.locator('#position-text').inner_text()!=before;page.locator('.top a').click();assert urlsplit(page.url).path in ['/'+name+'/','/'+name+'/index.html']
  b.close()
 server.shutdown();assert not report['errors'],report;assert report['onlineCueStates']==180 and report['offlineCueStates']==180
 report['offlineMethod']='Actual guide-button ZIP downloaded,CRC checked,extracted;local HTTP serving extracted files with all other origins blocked;36cues and12pages each viewport';report['fileUrl']='Not verified: managed Chromium blocks file:// with ERR_BLOCKED_BY_ADMINISTRATOR';report['legacyReaders']='13open/next/return passed';(O/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':static();browser()
