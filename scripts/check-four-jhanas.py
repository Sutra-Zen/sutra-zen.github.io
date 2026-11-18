#!/usr/bin/env python3
"""Verify book12 source fidelity, complete-image geometry and existing controls."""
import argparse,functools,hashlib,http.server,io,json,re,subprocess,threading,urllib.request
from pathlib import Path
from urllib.parse import urlsplit,unquote
from PIL import Image
from lxml import html
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'docs/four-jhanas';OUT=ROOT/'docs/previews/four-jhanas';BASE='c4e6670d30416b4203767287cf14cd754dea8dd7'
STORY=json.loads((D/'storyboard.json').read_text());CAT=json.loads((D/'scripture-catalog.json').read_text());PLAN=json.loads((D/'reader-plan.json').read_text());SOURCE=json.loads((D/'verified-sources.json').read_text())
BOOK=json.loads((ROOT/'four-jhanas/book/book-data.js').read_text().split('const BOOK = ')[1].rstrip(';\n'));FOCUS=json.loads((ROOT/'four-jhanas/book/panel-focus-data.js').read_text().split('const PANEL_FOCUS = ')[1].rstrip(';\n'))['scenes']
SIZES=[(360,800),(800,360),(768,1024),(1024,768),(1440,900)]
LEGACY=['four-truths','five-aggregates','six-senses','twelve-links','eightfold-path','four-fruits-ten-fetters','four-purities-six-recollections','mindfulness','right-effort','anapana','iddhipada']
def old(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
def text_source(raw):
 r=html.fromstring(raw)
 for a in r.xpath('//a[contains(@class,"ref")]'):a.drop_tree()
 return re.sub(r'\s+','',r.text_content())
def static_checks():
 subprocess.run(['python3','scripts/build-four-jhanas.py','--check'],cwd=ROOT,check=True)
 assert len(STORY)==len(BOOK['scenes'])==10 and len(BOOK['pages'])==131 and len(CAT)==8
 assert all(not p.get('tableSummary') for p in BOOK['pages'])
 n=0;used=set()
 for scene,display in zip(STORY,BOOK['scenes']):
  assert scene['id']==display['id'] and scene['asset']==display['image'] and display['start']==n
  for local,cue in enumerate(scene['cues'],1):
   item=BOOK['pages'][n];assert item['paragraphId']==cue['id']==f'P{n+1:03}' and item['lines']==[cue['text']]
   assert [item['startTime'],item['endTime']]==[cue['start'],cue['end']] and item['paragraphNumber']==local
   assert item['videoUrl'].endswith('&t='+str(item['startSeconds'])+'s')
   for q in item['quotes']:assert q==CAT[q['quoteId']];used.add(q['quoteId'])
   number=n+1
   for a,b,qid in [(20,35,'Q01'),(36,40,'Q02'),(41,42,'Q01'),(43,58,'Q03'),(59,65,'Q04'),(66,69,'Q03'),(70,86,'Q05'),(87,92,'Q06'),(93,99,'Q05'),(100,116,'Q07'),(117,122,'Q08'),(123,123,'Q07')]:
    if a<=number<=b:assert [q['quoteId'] for q in item['quotes']]==[qid]
   if number<20:assert not item['quotes'] and item['context'].startswith('《長部》第二經') and item['sourceAnchor']
   n+=1
 assert n==130 and used==set(CAT) and BOOK['pages'][-2]['paragraphId']=='P130' and BOOK['pages'][-1]['afterword']
 assert '溫柔' not in str(BOOK['pages'][-1]) and '走入經藏的起點' in str(BOOK['pages'][-1])
 assert sum(len(s['artOverlay']) for s in BOOK['scenes'])==7
 for scene in BOOK['scenes']:
  if scene['id'] not in ['S01','S02','S05']:assert not scene['artOverlay']
 a,b=BOOK['scenes'][0]['artOverlay'][0],BOOK['scenes'][1]['artOverlay'][0]
 assert a['text']=='由戒生定' and a['x']>50 and a['y']>50
 assert b['text']=='守護六根' and b['y']>=45 and b['y']+b['fontSizeCqw']*1536/857*1.15<50
 for row in json.loads((D/'web-assets.json').read_text()):
  with Image.open(ROOT/row['web']) as im:assert list(im.size)==row['dimensions'];im.verify()
  assert hashlib.sha256((ROOT/row['web']).read_bytes()).hexdigest()==row['sha256']
 guide=html.parse(str(ROOT/'four-jhanas/index.html'))
 for source in SOURCE['files']:
  raw=(D/source['local']).read_bytes();assert hashlib.sha256(raw).hexdigest()==source['sha256']
  card=next(s for s in SOURCE['sources'] if s['id']==source['id'])
  for section in card['sections']:
   assert section['text'] in text_source(raw)
   assert guide.xpath('//*[@id=$id]/following-sibling::blockquote[1]/p/text()',id=section['id'])==[section['text']]
 for q in CAT:assert guide.xpath('//*[@id=$id]',id=q)
 for path in ['four-jhanas/index.html','four-jhanas/book/index.html']:
  raw=(ROOT/path).read_text();assert 'data:image' not in raw
  for url in html.fromstring(raw).xpath('//@src|//@href'):
   u=urlsplit(url)
   if u.scheme or u.netloc:continue
   target=((ROOT/path).parent/unquote(u.path)).resolve()
   if target.is_dir():target/='index.html'
   assert target.is_file(),(path,url)
   if u.fragment:assert html.parse(str(target)).xpath('//*[@id=$id]',id=u.fragment)
 for name in subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],cwd=ROOT,text=True).splitlines():
  if any(name.startswith(k+'/') for k in LEGACY) or name.startswith('.github/') or name in ['shelf.css','guide-ui.css','guide-header.css','reader-controls.css','reader-restart.js','picture-panel-focus.css','picture-panel-focus.js','.nojekyll','CNAME']:
   # The author's later Anapana focus change only touches its reader wiring.
   if name not in ['anapana/book/book.js','anapana/book/index.html']:
    assert (ROOT/name).read_bytes()==old(name),name
 before=old('index.html').decode();after=(ROOT/'index.html').read_text();root=html.fromstring(after)
 assert len(root.xpath('//ol[@class="sz-books"]/li'))==14 and len(root.xpath('//*[@class="sz-book-lock"]'))==2
 assert len(root.xpath('//*[contains(concat(" ",@class," ")," sz-ready ")]'))==12
 assert root.xpath('//iframe/@src')==html.fromstring(before).xpath('//iframe/@src')
 maps=[json.loads(re.search(r'const dhammaData = (.*?);\s*\n',s)[1]) for s in [before,after]];assert maps[0].keys()==maps[1].keys()
 for key in maps[0]:
  if key!='四禪':assert maps[0][key]==maps[1][key]
  else:assert maps[0][key]['content'][:-6] in maps[1][key]['content']
 print('Static fidelity passed: 10 scenes, 130 captions, 8 Q cards, 7 overlays, 11 images; legacy data/artwork preserved (Anapana focus wiring allowed)',flush=True)
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
def settle(page):
 page.wait_for_function('document.querySelector("#art-frame").hidden || (document.querySelector("#art").complete && document.querySelector("#art").naturalWidth>0)')
 page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
def capture(page,name):Image.open(io.BytesIO(page.screenshot())).save(OUT/name,lossless=True,method=6)
def labels(page,selector,frame,plan):
 actual=page.locator(selector).evaluate_all('els=>els.map(l=>({text:l.textContent,r:l.getBoundingClientRect().toJSON(),font:parseFloat(getComputedStyle(l).fontSize),transform:getComputedStyle(l).transform}))');assert len(actual)==len(plan)
 for a,e in zip(actual,plan):
  assert a['text']==e['text'] and a['transform']=='none'
  assert abs(a['r']['x']-frame['x']-frame['width']*e['x']/100)<1 and abs(a['r']['y']-frame['y']-frame['height']*e['y']/100)<1
  assert abs(a['r']['width']-frame['width']*e['width']/100)<1 and abs(a['font']-frame['width']*e['fontSizeCqw']/100)<.1
  assert a['r']['right']<=frame['right']+1 and a['r']['bottom']<=frame['bottom']+1
def browser_checks(shots):
 OUT.mkdir(parents=True,exist_ok=True);server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
 report={'baseline':BASE,'scenes':10,'originalCaptions':130,'pages':131,'scriptures':8,'overlays':7,'pageStates':0,'enlargedLabelStates':0,'focusZoomStates':0,'viewports':[],'javascriptErrors':[],'httpErrors':[],'physicalSafari':'not tested','publication':'review implementation; not merged or deployed'}
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for w,h in SIZES:
   page=browser.new_page(viewport={'width':w,'height':h},has_touch=True);page.on('pageerror',lambda e:report['javascriptErrors'].append(str(e)));page.on('response',lambda r:report['httpErrors'].append(r.url) if r.url.startswith(base) and r.status>=400 else None);page.route('https://www.youtube.com/**',lambda route:route.abort());page.goto(base+'four-jhanas/book/');page.wait_for_function('typeof showPage==="function" && document.querySelector("#position-text").textContent.includes("131")')
   for i,item in enumerate(BOOK['pages']):
    page.evaluate('i=>showPage(i)',i);settle(page)
    r=page.evaluate('''()=>{const $=s=>document.querySelector(s),rect=s=>$(s).getBoundingClientRect().toJSON();return {lines:[...$('#narration').children].map(x=>x.textContent),position:$('#position-text').textContent,paragraph:$('.page').dataset.paragraph,start:$('.page').dataset.startSeconds,end:$('.page').dataset.endSeconds,overflow:document.documentElement.scrollWidth>innerWidth,touch:getComputedStyle($('#next')).touchAction,art:rect('#art-frame'),caption:rect('#caption'),scripture:rect('.scripture'),source:$('#source-link').getAttribute('href'),natural:[$('#art').naturalWidth,$('#art').naturalHeight],quotes:[...$('#verse').querySelectorAll('.scripture-card')].map(x=>({id:x.dataset.quoteId,source:x.querySelector('h3').textContent,text:x.querySelector('blockquote').textContent})),context:$('#verse .source-context')?.textContent||null,focus:$('#art-frame .picture-panel-focus:not([hidden])')?.dataset.activePanel||null};}''')
    assert r['lines']==item['lines'] and r['position']==f'{i+1} / 131 頁' and r['paragraph']==item.get('paragraphId','')
    assert r['start']==str(item.get('startSeconds','')) and r['end']==str(item.get('endSeconds',''))
    assert not r['overflow'] and r['touch']=='manipulation',(w,h,i,'overflow/touch')
    assert r['quotes']==[{'id':q['quoteId'],'source':q['source'],'text':q['text']} for q in item['quotes']] and r['context']==item['context']
    if item['image']:
     art=r['art'];plan=next(s for s in BOOK['scenes'] if s['id']==item['scene'])
     assert r['natural']==item['dimensions'] and abs(art['width']/art['height']-item['dimensions'][0]/item['dimensions'][1])<.005
     assert art['height']>65 and art['width']>115,(w,h,i,art)
     if item['lines']:assert r['caption']['bottom']<=art['top']+1
     if item['quotes'] or item['context']:assert art['bottom']<=r['scripture']['top']+1
     labels(page,'#art-overlays .art-overlay',art,plan['artOverlay'])
     if item['scene'] in FOCUS:
      active=FOCUS[item['scene']]['pages'][item['paragraphNumber']-1];assert r['focus']==active
      if active:assert page.locator('#art-frame .picture-panel-focus > span:not(.active)').count()==3
     else:assert r['focus'] is None
     if item['scene']=='S10':assert page.locator('#verse table').count()==0
     if shots and (w,h) in [(768,1024),(1024,768)] and (i==plan['start'] or i in [21,50,77,111,130]):capture(page,f'{item["scene"]}-page{i+1}-{w}x{h}.webp')
     if shots and w==360 and i in [6,111,123]:capture(page,f'{item["scene"]}-{w}x{h}.webp')
    else:
     assert page.locator('#summary-text').inner_text().endswith('走入經藏的起點。')
     if shots and w==768:capture(page,'ending-768x1024.webp')
    report['pageStates']+=1
   page.locator('#next').tap();assert page.locator('#position-text').inner_text()=='1 / 131 頁'
   for _ in range(8):page.locator('#next').tap()
   page.locator('#previous').tap();assert page.locator('#position-text').inner_text()=='8 / 131 頁' and page.evaluate('visualViewport.scale')==1
   other=browser.new_page(viewport={'width':w,'height':h});other.goto(base+'anapana/book/');other.wait_for_function('typeof showPage==="function"')
   for selector in ['#next','.position']:
    actual=page.locator(selector).bounding_box();expected=other.locator(selector).bounding_box();assert abs(actual['x']-expected['x'])<1 and abs(actual['y']-expected['y'])<1
   other.close()
   for plan in BOOK['scenes']:
    page.select_option('#page-select',plan['id']);settle(page);assert page.locator('.page').get_attribute('data-scene')==plan['id']
    if plan['artOverlay']:
     page.locator('#art').click();page.wait_for_function('document.querySelector("#zoom-art").complete');frame=page.locator('#zoom-frame').evaluate('e=>e.getBoundingClientRect().toJSON()');labels(page,'#zoom-overlays .art-overlay',frame,plan['artOverlay']);report['enlargedLabelStates']+=len(plan['artOverlay']);page.locator('#image-dialog form button').click()
   for sid in FOCUS:
    index=next(i for i,x in enumerate(BOOK['pages']) if x['scene']==sid and PLAN[sid][x['paragraphNumber']-1]['panel']=='p3');page.evaluate('i=>showPage(i)',index);settle(page);page.locator('#art').click();assert page.locator('#zoom-frame .picture-panel-focus:not([hidden])').get_attribute('data-active-panel')=='p3';report['focusZoomStates']+=1
    if shots and sid=='S09' and w==1024:
     page.locator('.image-scroll').evaluate('e=>{e.scrollLeft=e.scrollWidth*.625-e.clientWidth/2;e.scrollTop=e.scrollHeight}');capture(page,'fourth-third-panel-zoom.webp')
    page.locator('#image-dialog form button').click()
   page.select_option('#page-select','S02');settle(page);page.locator('.reading-links a').first.click();assert page.url.endswith('#dn2-senses');page.go_back();page.wait_for_function('typeof showPage==="function"')
   page.evaluate('showPage(123)');settle(page);page.locator('.verse-body').evaluate('e=>e.scrollTop=e.scrollHeight');assert page.locator('.verse-body').evaluate('e=>e.scrollTop>0');page.evaluate('showPage(117)');settle(page);position=page.locator('#position-text').inner_text();page.locator('#open-verse').click();assert CAT['Q08']['text'] in page.locator('#dialog-verse').text_content();page.locator('.verse-scroll').focus();page.keyboard.press('ArrowRight');assert page.locator('#position-text').inner_text()==position
   page.locator('#dialog-source').click();assert page.url.endswith('#Q08');page.go_back();page.wait_for_function('typeof showPage==="function"');assert page.locator('#position-text').inner_text()==position;page.reload();page.wait_for_function('typeof showPage==="function"');assert page.locator('#position-text').inner_text()==position
   page.set_viewport_size({'width':h,'height':w});settle(page);assert page.locator('#position-text').inner_text()==position;page.set_viewport_size({'width':w,'height':h});page.locator('.top a').click();page.locator('.book-cover').click();page.wait_for_function('typeof showPage==="function"');assert page.locator('#position-text').inner_text()==position
   page.locator('.reading-links a').last.click();assert page.url==base+'index.html';page.goto(base+'four-jhanas/');assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
   if shots and (w,h) in [(768,1024),(1024,768)]:capture(page,f'guide-{w}x{h}.webp');page.locator('#sources').scroll_into_view_if_needed();capture(page,f'sources-{w}x{h}.webp')
   page.close();report['viewports'].append({'width':w,'height':h,'pages':131});print(f'{w}x{h}: 131 pages and reader interactions passed',flush=True)
  page=browser.new_page(viewport={'width':1024,'height':768});cache={}
  for url in ['https://cdn.tailwindcss.com/','https://unpkg.com/lucide@latest']:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40) as r:cache[url]=(r.read(),r.headers.get('Content-Type','application/javascript'))
  def cdn(route):
   raw,mime=cache[route.request.url];route.fulfill(status=200,body=raw,content_type=mime)
  page.route('https://cdn.tailwindcss.com/**',cdn);page.route('https://unpkg.com/lucide@latest',cdn);page.route('https://www.youtube.com/**',lambda r:r.abort())
  page.goto(base);page.locator('.sz-book[href="./four-jhanas/book/index.html"]').click();page.wait_for_function('typeof showPage==="function"');page.goto(base);page.evaluate('openModal("四禪")');page.locator('#modalBody a[href="./four-jhanas/index.html"]').click();assert page.locator('h1').inner_text()=='四禪'
  for name in LEGACY:
   page.goto(base+name+'/book/');page.locator('#next').wait_for(state='visible');before=page.locator('#position-text').inner_text();page.locator('#next').click();assert page.locator('#position-text').inner_text()!=before;page.locator('.top a').click();assert urlsplit(page.url).path in ['/'+name+'/','/'+name+'/index.html']
  report['rootEntrances']='shelf #12 and existing 四禪 map node passed';report['legacyReaders']='11 open/next/return passed';browser.close()
 server.shutdown();assert not report['javascriptErrors'] and not report['httpErrors'],report
 (OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('655 page states, 35 enlarged overlay states and 20 comic focus zoom states passed',flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--screenshots',action='store_true');args=p.parse_args();static_checks();browser_checks(args.screenshots)
