#!/usr/bin/env python3
"""Check book 09 original handoff fidelity, actual-image overlays and existing reader interactions."""
import argparse,functools,hashlib,http.server,io,json,re,subprocess,threading,urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import unquote,urlsplit
from PIL import Image
from lxml import html
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs/right-effort';OUT=ROOT/'docs/previews/right-effort'
BASELINE='cd1cb6f743d773afe9ea22c6c548384c7760ef75'
STORY=json.loads((DOCS/'storyboard.json').read_text());CAT={q['id']:q for q in json.loads((DOCS/'scripture-catalog.json').read_text())}
BOOK=json.loads((ROOT/'right-effort/book/book-data.js').read_text().split('const BOOK = ')[1].rstrip(';\n'))
SOURCES=json.loads((DOCS/'verified-sources.json').read_text())
SIZES=[(360,800),(800,360),(768,1024),(1024,768),(1440,900)]
LEGACY=['four-truths','five-aggregates','six-senses','twelve-links','eightfold-path','four-fruits-ten-fetters','four-purities-six-recollections','mindfulness']
def old(path):return subprocess.check_output(['git','show',BASELINE+':'+path],cwd=ROOT)
def clean(raw):
 r=html.fromstring(raw)
 for a in r.xpath('//a[contains(@class,"ref")]'):a.drop_tree()
 return re.sub(r'\s+','',r.text_content())
def static_checks(network):
 subprocess.run(['python','scripts/build-right-effort.py','--check'],cwd=ROOT,check=True)
 assert len(BOOK['pages'])==81 and len(BOOK['scenes'])==11
 n=0
 for original,scene in zip(STORY,BOOK['scenes']):
  assert scene['image']==original['asset'] and scene['artOverlay']==original['artOverlay']
  assert scene['darkOverlayOpacity']==original.get('darkOverlayOpacity',0)
  for index,text in enumerate(original['narration'],1):
   page=BOOK['pages'][n];assert page['lines']==[text] and page['scene']==scene['id'] and page['paragraphNumber']==index
   expected=[r['quoteId'] for r in original['scriptureRefs'] if index in r['narrationParagraphs']]
   assert [q['quoteId'] for q in page['quotes']]==expected
   for q in page['quotes']:assert q['text']==CAT[q['quoteId']]['quote'] and q['source']==CAT[q['quoteId']]['source']
   n+=1
 assert n==80 and BOOK['pages'][-1]['afterword']
 assert not BOOK['pages'][-2]['quotes'] and BOOK['pages'][-2]['scene']=='S10'
 assert '溫柔' not in ''.join(BOOK['pages'][-1]['lines']) and '解讀仍請以原經文為準' in ''.join(BOOK['pages'][-1]['lines'])
 for row in json.loads((DOCS/'verified-inventory.json').read_text())['images']:
  with Image.open(DOCS/row['path']) as im:assert list(im.size)==row['dimensions'];im.verify()
 for name in subprocess.check_output(['git','ls-tree','-r','--name-only',BASELINE],cwd=ROOT,text=True).splitlines():
  if any(name.startswith(k+'/') for k in LEGACY) or name.startswith('.github/') or name in ['shelf.css','guide-ui.css','guide-header.css','reader-controls.css','reader-restart.js','.nojekyll','CNAME']:
   assert (ROOT/name).read_bytes()==old(name),name
 before=old('index.html').decode();after=(ROOT/'index.html').read_text();r=html.fromstring(after)
 assert len(r.xpath('//ol[@class="sz-books"]/li'))==14
 assert len(r.xpath('//*[contains(concat(" ",@class," ")," sz-ready ")]'))==9
 assert len(r.xpath('//*[@class="sz-book-lock"]'))==5
 assert r.xpath('//iframe/@src')==html.fromstring(before).xpath('//iframe/@src')
 maps=[json.loads(re.search(r'const dhammaData = (.*?);\s*\n',s)[1]) for s in [before,after]];assert maps[0].keys()==maps[1].keys()
 for key in maps[0]:
  if key!='四正勤':assert maps[0][key]==maps[1][key]
  else:assert maps[0][key]['content'][:-6] in maps[1][key]['content']
 guide=html.parse(str(ROOT/'right-effort/index.html'))
 for f in SOURCES['files']:
  raw=(DOCS/f['local']).read_bytes();assert hashlib.sha256(raw).hexdigest()==f['sha256']
  source=next(s for s in SOURCES['sources'] if s['id']==f['id'])
  assert all(t in clean(raw) for t in source['excerpts'])
  card=guide.xpath('//*[@id=$id]',id=f['id'])[0]
  assert card.xpath('.//blockquote/p/text()')==source['excerpts']
  assert card.xpath('.//a[contains(@class,"source-button--annotation")]/@href')==[source.get('annotation',source.get('pali'))]
 for q in CAT:assert guide.xpath('//*[@id=$id]',id=q)
 for path in ['right-effort/index.html','right-effort/book/index.html']:
  for url in html.parse(str(ROOT/path)).xpath('//@src|//@href'):
   u=urlsplit(url)
   if u.scheme or u.netloc:continue
   target=((ROOT/path).parent/unquote(u.path)).resolve()
   if target.is_dir():target/='index.html'
   assert target.is_file(),(path,url)
   if u.fragment:assert html.parse(str(target)).xpath('//*[@id=$id]',id=u.fragment)
 if network:
  def verify(f):assert hashlib.sha256(urllib.request.urlopen(f['url'],timeout=30).read()).hexdigest()==f['sha256'];return f['id']
  print('Official source hashes:',list(ThreadPoolExecutor(max_workers=6).map(verify,SOURCES['files'])),flush=True)
 print('All original files, 80 paragraphs, 13 quotes and paragraph switches; 8 old books preserved: OK',flush=True)
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
def settle(page):
 page.wait_for_function('document.querySelector("#art-frame").hidden || (document.querySelector("#art").complete && document.querySelector("#art").naturalWidth>0)')
 page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
def capture(page,name):Image.open(io.BytesIO(page.screenshot(type='png'))).save(OUT/name,lossless=True,method=6)
def browser_checks(shots):
 OUT.mkdir(parents=True,exist_ok=True);server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
 report={'baseline':BASELINE,'pages':81,'scenes':11,'narrationParagraphs':80,'quotes':13,'pageStates':0,'viewports':[],'javascriptErrors':[],'httpErrors':[],'physicalIPadSafari':'not tested'}
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for w,h in SIZES:
   page=browser.new_page(viewport={'width':w,'height':h},has_touch=True)
   page.on('pageerror',lambda e:report['javascriptErrors'].append(str(e)))
   page.on('response',lambda r:report['httpErrors'].append(r.url) if r.url.startswith(base) and r.status>=400 else None)
   page.route('https://www.youtube.com/**',lambda route:route.abort())
   page.goto(base+'right-effort/book/');page.wait_for_function('typeof showPage==="function"')
   for i,item in enumerate(BOOK['pages']):
    page.evaluate('i=>showPage(i)',i);settle(page)
    r=page.evaluate('''()=>{const $=s=>document.querySelector(s),rect=s=>$(s).getBoundingClientRect().toJSON();return {
      lines:[...$('#narration').children].map(x=>x.textContent),verse:$('#verse').textContent,number:$('#position-text').textContent,
      overflow:document.documentElement.scrollWidth>innerWidth,touch:getComputedStyle($('#next')).touchAction,art:rect('#art-frame'),caption:rect('#caption'),scripture:rect('.scripture'),image:$('#art').getAttribute('src'),natural:[$('#art').naturalWidth,$('#art').naturalHeight],
      maskHidden:$('#closing-shade').hidden,maskOpacity:getComputedStyle($('#closing-shade')).opacity,
      labels:[...$('#art-overlays').children].map(l=>({text:l.textContent,r:l.getBoundingClientRect().toJSON(),font:parseFloat(getComputedStyle(l).fontSize),color:getComputedStyle(l).color,transform:getComputedStyle(l).transform,align:getComputedStyle(l).textAlign}))};}''')
    assert r['lines']==item['lines'] and r['number']==f'{i+1} / 81 頁'
    assert not r['overflow'] and r['touch']=='manipulation'
    for q in item['quotes']:assert q['text'] in r['verse'] and q['source'] in r['verse']
    if item['image']:
     plan=next(s for s in BOOK['scenes'] if s['id']==item['scene']);art=r['art']
     assert r['image']==item['image'] and r['natural']==item['dimensions'] and art['height']>90 and art['width']>160
     assert abs(art['width']/art['height']-item['dimensions'][0]/item['dimensions'][1])<.005
     assert r['caption']['bottom']<=art['top']+1
     if item['quotes']:assert art['bottom']<=r['scripture']['top']+1
     assert len(r['labels'])==len(plan['artOverlay'])
     assert r['maskHidden']==(plan['darkOverlayOpacity']==0)
     if not r['maskHidden']:assert float(r['maskOpacity'])==.6
     for actual,expected in zip(r['labels'],plan['artOverlay']):
      assert actual['text']==expected['text'] and actual['transform']=='none' and actual['align']=='center'
      for metric,key in [('x','leftPct'),('y','topPct')]:assert abs(actual['r'][metric]-art[metric]-art['width' if metric=='x' else 'height']*expected[key]/100)<1
      assert abs(actual['r']['width']-art['width']*expected['widthPct']/100)<1
      assert abs(actual['font']-art['width']*expected['fontSizeCqw']/100)<.1
      assert actual['r']['bottom']<=art['bottom']+1 and actual['r']['right']<=art['right']+1
     if shots and (w,h) in [(768,1024),(1024,768)] and i==plan['start']:capture(page,f'{item["scene"]}-{w}x{h}.webp')
    elif shots and (w,h) in [(768,1024),(1024,768)]:capture(page,f'S11-{w}x{h}.webp')
    report['pageStates']+=1
   page.locator('#next').tap();assert page.locator('#position-text').inner_text()=='1 / 81 頁'
   for _ in range(8):page.locator('#next').tap()
   assert page.locator('#position-text').inner_text()=='9 / 81 頁' and page.evaluate('visualViewport.scale')==1
   # Shared control coordinates match book 08 in each orientation.
   next_rect=page.locator('#next').bounding_box();menu_rect=page.locator('.position').bounding_box()
   other=browser.new_page(viewport={'width':w,'height':h});other.goto(base+'mindfulness/book/');other.wait_for_function('typeof showPage==="function"')
   for actual,selector in [(next_rect,'#next'),(menu_rect,'.position')]:
    expected=other.locator(selector).bounding_box();assert abs(actual['x']-expected['x'])<1 and abs(actual['y']-expected['y'])<1
   other.close()
   page.select_option('#page-select','S04');settle(page);page.locator('#art').click();assert page.locator('#image-dialog').evaluate('e=>e.open')
   assert page.locator('#zoom-overlays .art-overlay').inner_text()=='未生惡令不起'
   page.locator('.image-scroll').evaluate('e=>{e.scrollLeft=300;e.scrollTop=100}');page.locator('#image-dialog form button').click()
   page.select_option('#page-select','S05');index=next(i for i,x in enumerate(BOOK['pages']) if x.get('paragraphId')=='S05-P04');page.evaluate('i=>showPage(i)',index)
   assert CAT['Q08']['quote'] in page.locator('#verse').inner_text();position=page.locator('#position-text').inner_text()
   page.locator('#open-verse').click();assert CAT['Q08']['quote'] in page.locator('#dialog-verse').inner_text()
   page.locator('.verse-scroll').focus();page.keyboard.press('ArrowRight');assert page.locator('#position-text').inner_text()==position
   page.locator('.verse-scroll').evaluate('e=>e.scrollTop=e.scrollHeight');page.locator('#dialog-source').click();assert page.url.endswith('#Q08') and page.locator('#sa879').is_visible()
   page.go_back();page.wait_for_function('typeof showPage==="function"');assert page.locator('#position-text').inner_text()==position
   page.reload();page.wait_for_function('typeof showPage==="function"');assert page.locator('#position-text').inner_text()==position
   page.set_viewport_size({'width':h,'height':w});settle(page);assert page.locator('#position-text').inner_text()==position
   page.set_viewport_size({'width':w,'height':h});page.locator('.top a').click();page.locator('.book-cover').click();page.wait_for_function('typeof showPage==="function"');assert page.locator('#position-text').inner_text()==position
   page.goto(base+'right-effort/');assert page.locator('#sources .source-entry').count()==6 and not page.evaluate('document.documentElement.scrollWidth>innerWidth')
   for scene in ['S02','S04','S05','S06']:
    page.goto(base+'right-effort/book/?scene='+scene);page.wait_for_function('typeof showPage==="function"');assert page.locator('.page').get_attribute('data-scene')==scene
   page.close();report['viewports'].append({'width':w,'height':h,'pages':81,'controls':'passed'})
   print(f'{w}x{h}: 81 pages, full narration, exact switches, image labels/mask, caption above and scripture below, controls, dialog, rotation, restart passed',flush=True)
  page=browser.new_page(viewport={'width':1024,'height':768});cache={}
  for url in ['https://cdn.tailwindcss.com/','https://unpkg.com/lucide@latest']:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as r:cache[url]=(r.read(),r.headers.get('Content-Type','application/javascript'))
  def cdn(route):
   raw,mime=cache[route.request.url];route.fulfill(status=200,body=raw,content_type=mime)
  page.route('https://cdn.tailwindcss.com/**',cdn);page.route('https://unpkg.com/lucide@latest',cdn)
  page.goto(base);page.locator('.sz-book[href="./right-effort/book/"]').click();page.wait_for_function('typeof showPage==="function"');assert page.locator('#position-text').inner_text().endswith('/ 81 頁')
  page.goto(base);page.evaluate('openModal("四正勤")');page.locator('#modalBody a[href="./right-effort/"]').click();assert page.locator('h1').inner_text()=='四正勤'
  for name in LEGACY:
   page.goto(base+name+'/book/');page.locator('#next').wait_for(state='visible');before=page.locator('#position-text').inner_text();page.locator('#next').click();assert page.locator('#position-text').inner_text()!=before;page.locator('.top a').click();assert urlsplit(page.url).path=='/'+name+'/'
  browser.close()
 server.shutdown();assert not report['javascriptErrors'] and not report['httpErrors'],report
 report['legacyReaders']='all 8 open/next/return passed';(OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('405 page states and all 8 old readers passed',flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--screenshots',action='store_true');p.add_argument('--verify-sources',action='store_true');args=p.parse_args();static_checks(args.verify_sources);browser_checks(args.screenshots)
