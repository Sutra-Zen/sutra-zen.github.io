#!/usr/bin/env python3
"""Verify book13's complete content, image-space overlays and shared reader UI."""
import functools,hashlib,http.server,io,json,re,subprocess,threading,urllib.request
from pathlib import Path
from urllib.parse import unquote,urlsplit
from PIL import Image
from lxml import html
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];D=R/'docs/five-roots-powers';O=R/'docs/previews/five-roots-powers';O.mkdir(parents=True,exist_ok=True);BASE='2376c9cafb4b59e5eeba6aaa2833ec3c900497fc'
def load(path):return json.loads(path.read_text())
B=json.loads((R/'five-roots-powers/book/book-data.js').read_text().split('const BOOK = ')[1].rstrip(';\n'));STORY=load(D/'storyboard.json');CAT=load(D/'scripture-catalog.json');PLAN=load(D/'reader-plan.json');SOURCES=load(D/'verified-sources.json');LABELS=load(D/'overlay-layout.json')['overlays']
SIZES=[(360,800),(800,360),(768,1024),(1024,768),(1440,900)]
LEGACY=['four-truths','five-aggregates','six-senses','twelve-links','eightfold-path','four-fruits-ten-fetters','four-purities-six-recollections','mindfulness','right-effort','anapana','iddhipada','four-jhanas']
def old(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=R)
def static():
 subprocess.run(['python3','scripts/build-five-roots-powers.py','--check'],cwd=R,check=True)
 assert len(B['scenes'])==10 and len(B['pages'])==76 and len(CAT)==14 and sum(len(s['artOverlay']) for s in B['scenes'])==5
 n=0;markdown=(D/'storyboard.md').read_text()
 for s,scene in zip(STORY,B['scenes']):
  assert scene['image']==s['asset'] and scene['artOverlay']==LABELS[scene['id']] and scene['start']==n
  for cue,mapping in zip(s['cues'],PLAN[scene['id']]):
   p=B['pages'][n];assert p['lines']==[cue['text']] and p['paragraphId']==mapping['paragraphId']==f'P{n+1:03}'
   assert [p['startTime'],p['endTime']]==[cue['start'],cue['end']] and cue['text'] in markdown
   assert p['quotes']==[CAT[q] for q in mapping['quoteIds']];n+=1
 assert n==74 and B['pages'][74]['credits'] and B['pages'][75]['afterword']
 for q in CAT.values():assert any(q['text'] in s['scripture'] for s in STORY)
 assert '樹根站穩與抗風是影片的教學譬喻' in B['pages'][12]['sourceNote']
 assert (R/'five-roots-powers/assets/sources.png').read_bytes()==(D/'assets/sources.png').read_bytes()
 assert all(not s['artOverlay'] for s in B['scenes'] if s['id'] not in ['S04','S05','S06','S07','S08'])
 for row in load(D/'web-assets.json'):
  assert hashlib.sha256((R/row['web']).read_bytes()).hexdigest()==row['sha256']
  with Image.open(R/row['web']) as im:assert list(im.size)==row['dimensions'];im.verify()
 for raw in subprocess.check_output(['git','ls-tree','-rz','--name-only',BASE],cwd=R).split(b'\0'):
  if not raw:continue
  name=raw.decode()
  if any(name.startswith(k+'/') for k in LEGACY) or name.startswith('.github/') or name in ['reader-controls.css','reader-restart.js','guide-header.css','guide-ui.css','shelf.css','picture-panel-focus.js','picture-panel-focus.css','.nojekyll','CNAME']:assert (R/name).read_bytes()==old(name),name
 root=html.parse(str(R/'index.html'));before=html.fromstring(old('index.html'));assert root.xpath('//iframe/@src')==before.xpath('//iframe/@src')
 assert len(root.xpath('//ol[@class="sz-books"]/li'))==14 and len(root.xpath('//*[@class="sz-book-lock"]'))==1 and len(root.xpath('//*[contains(concat(" ",@class," ")," sz-ready ")]'))==13
 a,b=[json.loads(re.search(r'const dhammaData = (.*?);\s*\n',s)[1]) for s in [old('index.html').decode(),(R/'index.html').read_text()]];assert a.keys()==b.keys()
 for key in a:
  if key!='五根五力總說':assert a[key]==b[key],key
 assert 'five-roots-powers/index.html' in b['五根五力總說']['content']
 guide=html.parse(str(R/'five-roots-powers/index.html'));assert not guide.xpath('//details') and len(guide.xpath('//*[@id="sources"]/article'))==5
 for source in SOURCES['sources']:
  assert guide.xpath('//*[@id=$id]//blockquote/p/text()',id=source['id'])==source['excerpts']
  for q in source['quoteIds']:assert guide.xpath('//*[@id=$id]',id=q)
 for name in ['five-roots-powers/index.html','five-roots-powers/book/index.html']:
  text=(R/name).read_text();assert 'data:image' not in text
  for url in html.fromstring(text).xpath('//@href|//@src'):
   u=urlsplit(url)
   if u.scheme or u.netloc:continue
   target=((R/name).parent/unquote(u.path)).resolve()
   if target.is_dir():target/='index.html'
   assert target.is_file(),(name,url)
   if u.fragment:assert html.parse(str(target)).xpath('//*[@id=$id]',id=u.fragment)
 print('Static fidelity:74timed cues,14original quote cards,5overlays,11images; all12existing readers unchanged',flush=True)
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
def settle(page):
 page.wait_for_function('document.querySelector("#art-frame").hidden || (document.querySelector("#art").complete && document.querySelector("#art").naturalWidth>0)');page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
def shot(page,name):Image.open(io.BytesIO(page.screenshot())).save(O/name,lossless=True,method=6)
def overlays(page,selector,frame,plan):
 actual=page.locator(selector).evaluate_all('els=>els.map(e=>({text:e.textContent,r:e.getBoundingClientRect().toJSON(),font:parseFloat(getComputedStyle(e).fontSize),transform:getComputedStyle(e).transform,color:getComputedStyle(e).color}))');assert len(actual)==len(plan)
 for a,p in zip(actual,plan):
  assert a['text']==p['text'] and a['transform']=='none' and a['color']=='rgb(0, 0, 0)'
  assert abs(a['r']['x']-frame['x']-frame['width']*p['x']/100)<1 and abs(a['r']['y']-frame['y']-frame['height']*p['y']/100)<1
  assert abs(a['r']['width']-frame['width']*p['width']/100)<1 and abs(a['font']-frame['width']*p['fontSizeCqw']/100)<.1
  assert a['r']['right']<=frame['right']+1 and a['r']['bottom']<=frame['bottom']+1
def browser():
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
 report={'baseline':BASE,'scenes':10,'originalParagraphs':74,'pages':76,'quotes':14,'overlays':5,'pageStates':0,'zoomOverlayStates':0,'creditsZoomStates':0,'viewports':SIZES,'javascriptErrors':[],'httpErrors':[],'physicalSafari':'not tested','publication':'review branch only; not merged or deployed'}
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  cache={}
  for url in ['https://cdn.tailwindcss.com/','https://unpkg.com/lucide@latest']:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40) as r:cache[url]=(r.read(),r.headers.get('Content-Type','application/javascript'))
  for w,h in SIZES:
   page=b.new_page(viewport={'width':w,'height':h},has_touch=True);page.on('pageerror',lambda e:report['javascriptErrors'].append(str(e)));page.on('response',lambda r:report['httpErrors'].append(r.url) if r.url.startswith(base) and r.status>=400 else None);page.route('https://www.youtube.com/**',lambda route:route.abort());page.goto(base+'five-roots-powers/book/');page.wait_for_function('typeof showPage==="function"')
   for i,item in enumerate(B['pages']):
    page.evaluate('i=>showPage(i)',i);settle(page);assert page.locator('#position-text').inner_text()==f'{i+1} / 76 頁' and page.locator('#narration p').all_text_contents()==item['lines']
    assert page.locator('#verse .scripture-card blockquote').all_text_contents()==[q['text'] for q in item['quotes']]
    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth') and page.locator('#next').evaluate('e=>getComputedStyle(e).touchAction')=='manipulation'
    if item['image']:
     frame=page.locator('#art-frame').evaluate('e=>e.getBoundingClientRect().toJSON()');assert abs(frame['width']/frame['height']-item['dimensions'][0]/item['dimensions'][1])<.005
     caption=page.locator('#caption').bounding_box();assert caption['y']+caption['height']<=frame['y']+1
     if item['quotes'] or item['sourceNote']:assert frame['bottom']<=page.locator('.scripture').bounding_box()['y']+1
     scene=next(s for s in B['scenes'] if s['id']==item['scene']);overlays(page,'#art-overlays .art-overlay',frame,scene['artOverlay'])
     if (w,h) in [(768,1024),(1024,768)] and (i==scene['start'] or item.get('credits')):shot(page,f'{item["scene"]}-page{i+1}-{w}x{h}.webp')
     if w==360 and item.get('paragraphId') in ['P028','P034','P056']:shot(page,f'{item["scene"]}-360x800.webp')
    else:assert '走入經藏的起點' in page.locator('#summary-text').inner_text()
    report['pageStates']+=1
   page.locator('#next').tap();assert page.locator('#position-text').inner_text()=='1 / 76 頁'
   for _ in range(8):page.locator('#next').tap()
   page.locator('#previous').tap();assert page.locator('#position-text').inner_text()=='8 / 76 頁' and page.evaluate('visualViewport.scale')==1
   for scene in B['scenes']:
    page.select_option('#page-select',scene['id']);settle(page);assert page.locator('.page').get_attribute('data-scene')==scene['id']
    if scene['artOverlay']:
     page.locator('#art').click();page.wait_for_function('document.querySelector("#zoom-art").complete');frame=page.locator('#zoom-frame').evaluate('e=>e.getBoundingClientRect().toJSON()');overlays(page,'#zoom-overlays .art-overlay',frame,scene['artOverlay']);report['zoomOverlayStates']+=1;page.locator('#image-dialog form button').click()
   page.evaluate('showPage(74)');settle(page);page.locator('#art').click();page.wait_for_function('document.querySelector("#zoom-art").complete');assert page.locator('#zoom-art').get_attribute('src')=='../assets/sources.png';assert page.locator('#zoom-overlays .art-overlay').count()==0;report['creditsZoomStates']+=1
   if w==768:shot(page,'credits-zoom-768x1024.webp')
   page.locator('#image-dialog form button').click()
   page.evaluate('showPage(28)');settle(page);position=page.locator('#position-text').inner_text();page.set_viewport_size({'width':h,'height':w});settle(page);assert page.locator('#position-text').inner_text()==position;page.set_viewport_size({'width':w,'height':h});page.reload();settle(page);assert page.locator('#position-text').inner_text()==position
   page.locator('#open-verse').click();text=page.locator('#dialog-verse').inner_text();assert 'undefined' not in text and all(q['text'] in text for q in B['pages'][28]['quotes']);page.locator('.verse-scroll').evaluate('e=>e.scrollTop=e.scrollHeight');page.locator('#dialog-source').click();assert '#Q03' in page.url;page.go_back();settle(page);assert page.locator('#position-text').inner_text()==position
   page.locator('.top a').click();page.wait_for_load_state();page.evaluate('()=>document.fonts.ready');assert urlsplit(page.url).path=='/five-roots-powers/index.html';assert not page.evaluate('document.documentElement.scrollWidth>innerWidth');page.locator('.book-cover').click();settle(page);assert page.locator('#position-text').inner_text()==position
   page.locator('.reading-links a').last.click();assert urlsplit(page.url).path=='/index.html';page.goto(base+'five-roots-powers/');page.locator('#sources').scroll_into_view_if_needed()
   if w in [768,1024]:shot(page,f'sources-{w}x{h}.webp');page.evaluate('window.scrollTo(0,0)');shot(page,f'guide-{w}x{h}.webp')
   page.close();print(f'{w}x{h}:76pages,5overlay zooms,credits zoom and controls passed',flush=True)
  page=b.new_page(viewport={'width':1024,'height':768})
  page.route('https://cdn.tailwindcss.com/**',lambda route:route.fulfill(status=200,body=cache['https://cdn.tailwindcss.com/'][0],content_type=cache['https://cdn.tailwindcss.com/'][1]));page.route('https://unpkg.com/lucide@latest',lambda route:route.fulfill(status=200,body=cache['https://unpkg.com/lucide@latest'][0],content_type=cache['https://unpkg.com/lucide@latest'][1]));page.route('https://www.youtube.com/**',lambda route:route.abort());page.goto(base);page.locator('.sz-book[href="./five-roots-powers/book/index.html"]').click();settle(page);page.goto(base);page.evaluate('openModal("五根五力總說")');page.locator('#modalBody a[href="./five-roots-powers/index.html"]').click();assert page.locator('h1').inner_text()=='五根五力'
  for name in LEGACY:
   page.goto(base+name+'/book/');page.locator('#next').wait_for(state='visible');before=page.locator('#position-text').inner_text();page.locator('#next').click();assert page.locator('#position-text').inner_text()!=before;page.locator('.top a').click();assert urlsplit(page.url).path in ['/'+name+'/','/'+name+'/index.html']
  b.close()
 server.shutdown();assert not report['javascriptErrors'] and not report['httpErrors'],report;assert report['pageStates']==380 and report['zoomOverlayStates']==25 and report['creditsZoomStates']==5
 report['entrances']='shelf13 and existing map node passed;12legacy readers open/next/return passed';(O/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':static();browser()
