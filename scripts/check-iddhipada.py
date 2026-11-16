#!/usr/bin/env python3
"""Check handoff fidelity, image-space labels and existing reader interactions."""
import argparse,functools,hashlib,http.server,io,json,re,subprocess,threading,urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import unquote,urlsplit
from PIL import Image
from lxml import html
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]; DOCS=ROOT/'docs/iddhipada'; OUT=ROOT/'docs/previews/iddhipada'
BASELINE='140f62221726485916f3992d8ea6f5782e7507b5'
STORY=json.loads((DOCS/'storyboard.json').read_text());CAT=json.loads((DOCS/'scripture-catalog.json').read_text())
for qid,changes in json.loads((DOCS/'reader-edits.json').read_text()).items():CAT[qid].update(changes)
LABELS=json.loads((DOCS/'overlay-layout.json').read_text())['overlays']; SOURCES=json.loads((DOCS/'verified-sources.json').read_text())
BOOK=json.loads((ROOT/'iddhipada/book/book-data.js').read_text().split('const BOOK = ')[1].rstrip(';\n'))
SIZES=[(360,800),(800,360),(768,1024),(1024,768),(1440,900)]
LEGACY=['four-truths','five-aggregates','six-senses','twelve-links','eightfold-path','four-fruits-ten-fetters','four-purities-six-recollections','mindfulness','right-effort','anapana']
def old(path):return subprocess.check_output(['git','show',BASELINE+':'+path],cwd=ROOT)
def clean(raw):
 r=html.fromstring(raw)
 for a in r.xpath('//a[contains(@class,"ref")]'):a.drop_tree()
 return re.sub(r'\s+','',r.text_content())
def static_checks(network):
 subprocess.run(['python3','scripts/build-iddhipada.py','--check'],cwd=ROOT,check=True)
 assert len(BOOK['scenes'])==9 and len(BOOK['pages'])==82 and len(CAT)==11 and sum(map(len,LABELS.values()))==13
 n=0;used=set()
 for original,scene in zip(STORY['scenes'],BOOK['scenes']):
  assert scene['image']==original['image'] and scene['artOverlay']==LABELS[scene['id']]
  assert scene['bakedText']==original['bakedText'] and scene['start']==n
  for entry in original['narration']:
   item=BOOK['pages'][n];assert item['scene']==original['sceneId'] and item['lines']==[entry['text']]
   assert item['paragraphId']==entry['id']==f'P{n+1:02}'
   assert all(item[k]==entry[k] for k in ['startSeconds','endSeconds'])
   assert [q['quoteId'] for q in item['quotes']]==entry['quoteIds']
   for q in item['quotes']:
    qid=q['quoteId'];used.add(qid);assert q==dict(CAT[qid],quoteId=qid)
   n+=1
 assert n==81 and used==set(CAT) and BOOK['timingAccuracy']==STORY['timingAccuracy']
 assert not CAT['Q09']['translationNote'] and CAT['Q09']['originalText'] in clean((DOCS/'canonical/sn51.11.html').read_bytes())
 assert CAT['Q09']['sourceType']=='modern_chinese_translation' and '莊春江' in CAT['Q09']['source']
 assert all('Q03' not in q['translationNote'] for q in CAT.values())
 assert BOOK['scenes'][5]['image']=='assets/S06.png'
 assert all(s['artOverlay']==[] for s in [BOOK['scenes'][0],BOOK['scenes'][-1]])
 ending=BOOK['pages'][-1];assert ending['afterword'] and not ending['lines'] and not ending['quotes']
 assert '走入經藏的起點' in str(ending) and '溫柔' not in str(ending)
 receipt=json.loads((DOCS/'receipt.json').read_text());assert len(receipt)==30
 images=0
 for name,row in receipt.items():
  raw=(DOCS/name).read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],name
  if name.endswith('.png'):
   with Image.open(io.BytesIO(raw)) as im:im.verify()
   images+=1
 assert images==19
 for row in json.loads((DOCS/'web-assets.json').read_text()):
  with Image.open(ROOT/row['web']) as im:assert list(im.size)==row['dimensions']==[1672,941];im.verify()
 for name in subprocess.check_output(['git','ls-tree','-r','--name-only',BASELINE],cwd=ROOT,text=True).splitlines():
  if any(name.startswith(k+'/') for k in LEGACY) or name.startswith('.github/') or name in ['shelf.css','guide-ui.css','guide-header.css','reader-controls.css','reader-restart.js','.nojekyll','CNAME']:
   assert (ROOT/name).read_bytes()==old(name),name
 before=old('index.html').decode();after=(ROOT/'index.html').read_text();root=html.fromstring(after)
 assert len(root.xpath('//ol[@class="sz-books"]/li'))==14
 assert len(root.xpath('//*[contains(concat(" ",@class," ")," sz-ready ")]'))==11
 assert len(root.xpath('//*[@class="sz-book-lock"]'))==3
 assert root.xpath('//iframe/@src')==html.fromstring(before).xpath('//iframe/@src')
 maps=[json.loads(re.search(r'const dhammaData = (.*?);\s*\n',s)[1]) for s in [before,after]];assert maps[0].keys()==maps[1].keys()
 for key in maps[0]:
  if key!='四如意足':assert maps[0][key]==maps[1][key]
  else:assert maps[0][key]['content'][:-6] in maps[1][key]['content']
 guide=html.parse(str(ROOT/'iddhipada/index.html'));assert len(guide.xpath('//*[@id="sources"]//article'))==5
 for f in SOURCES['files']+SOURCES['paliFiles']:
  raw=(DOCS/f['local']).read_bytes();assert hashlib.sha256(raw).hexdigest()==f['sha256']
  if f in SOURCES['files']:
   source=next(s for s in SOURCES['sources'] if s['id']==f['id'])
   assert all(re.sub(r'\s+','',t) in clean(raw) for t in source['excerpts']),f['id']
   card=guide.xpath('//*[@id=$id]',id=f['id'])[0];assert card.xpath('.//blockquote/p/text()')==source['excerpts']
 for q in CAT:assert guide.xpath('//*[@id=$id]',id=q)
 for path in ['iddhipada/index.html','iddhipada/book/index.html']:
  raw=(ROOT/path).read_text();assert 'data:image' not in raw
  for url in html.fromstring(raw).xpath('//@src|//@href'):
   u=urlsplit(url)
   if u.scheme or u.netloc:continue
   target=((ROOT/path).parent/unquote(u.path)).resolve()
   if target.is_dir():target/='index.html'
   assert target.is_file(),(path,url)
   if u.fragment:assert html.parse(str(target)).xpath('//*[@id=$id]',id=u.fragment),(path,url)
 if network:
  def verify(f):
   with urllib.request.urlopen(f['url'],timeout=45) as r:assert hashlib.sha256(r.read()).hexdigest()==f['sha256']
   return f['id']
  print('Official source hashes:',list(ThreadPoolExecutor(max_workers=5).map(verify,SOURCES['files']+SOURCES['paliFiles'])),flush=True)
 print('Static fidelity passed: 30 original files, 19 images, 9 formal scenes, 81 paragraphs, 11 Q cards, 13 labels; all 10 previous books unchanged',flush=True)
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
def settle(page):
 page.wait_for_function('document.querySelector("#art-frame").hidden || (document.querySelector("#art").complete && document.querySelector("#art").naturalWidth>0)')
 page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
def capture(page,name):Image.open(io.BytesIO(page.screenshot())).save(OUT/name,lossless=True,method=6)
def label_checks(actual,expected,frame):
 assert len(actual)==len(expected)
 for a,e in zip(actual,expected):
  assert a['text']==e['text'] and a['transform']=='none' and a['align']=='center'
  assert abs(a['r']['x']-frame['x']-frame['width']*e['x']/100)<1
  assert abs(a['r']['y']-frame['y']-frame['height']*e['y']/100)<1
  assert abs(a['r']['width']-frame['width']*e['width']/100)<1
  assert abs(a['font']-frame['width']*e['fontSizeCqw']/100)<.1
  assert a['r']['bottom']<=frame['bottom']+1 and a['r']['right']<=frame['right']+1
  # CJK ink can extend below a 1.15 line box; labels deliberately keep overflow visible.
  assert a['scrollWidth']<=a['r']['width']+1,(a,e,frame)
def browser_checks(shots):
 OUT.mkdir(parents=True,exist_ok=True)
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
 report={'baseline':BASELINE,'scenes':9,'pages':82,'narrationParagraphs':81,'quotes':11,'overlays':13,'originalImages':9,'pageStates':0,'enlargedOverlayStates':0,'viewports':[],'javascriptErrors':[],'httpErrors':[],'physicalIPadSafari':'not tested','production':'review branch only; not merged or deployed'}
 labels_js='''l=>({text:l.textContent,r:l.getBoundingClientRect().toJSON(),font:parseFloat(getComputedStyle(l).fontSize),transform:getComputedStyle(l).transform,align:getComputedStyle(l).textAlign,scrollWidth:l.scrollWidth,scrollHeight:l.scrollHeight})'''
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for w,h in SIZES:
   page=browser.new_page(viewport={'width':w,'height':h},has_touch=True)
   page.on('pageerror',lambda e:report['javascriptErrors'].append(str(e)))
   page.on('response',lambda r:report['httpErrors'].append(r.url) if r.url.startswith(base) and r.status>=400 else None)
   page.route('https://www.youtube.com/**',lambda route:route.abort())
   page.goto(base+'iddhipada/book/');page.wait_for_function('typeof showPage==="function"')
   for i,item in enumerate(BOOK['pages']):
    page.evaluate('i=>showPage(i)',i);settle(page)
    r=page.evaluate('''()=>{const $=s=>document.querySelector(s),rect=s=>$(s).getBoundingClientRect().toJSON();return {lines:[...$('#narration').children].map(x=>x.textContent),number:$('#position-text').textContent,paragraph:$('.page').dataset.paragraph,start:$('.page').dataset.startSeconds,end:$('.page').dataset.endSeconds,overflow:document.documentElement.scrollWidth>innerWidth,touch:getComputedStyle($('#next')).touchAction,art:rect('#art-frame'),caption:rect('#caption'),scripture:rect('.scripture'),image:$('#art').getAttribute('src'),natural:[$('#art').naturalWidth,$('#art').naturalHeight],quotes:[...$('#verse').querySelectorAll('.scripture-card')].map(x=>({id:x.dataset.quoteId,type:x.dataset.sourceType,source:x.querySelector('h3').textContent,original:x.querySelector('blockquote').textContent,chinese:x.querySelector('.chinese-paraphrase')?.textContent||null,note:x.querySelector('.source-note')?.textContent||null})),hintHidden:$('#outside-labels').hidden};}''')
    assert r['lines']==item['lines'] and r['number']==f'{i+1} / 82 頁'
    assert not r['overflow'] and r['touch']=='manipulation',(w,h,i,'overflow/touch')
    assert r['paragraph']==item.get('paragraphId','') and r['start']==str(item.get('startSeconds','')) and r['end']==str(item.get('endSeconds',''))
    assert r['quotes']==[{'id':q['quoteId'],'type':q['sourceType'],'source':q['source'],'original':q['originalText'],'chinese':q['translationNote'] if q['sourceType']=='pali_with_editorial_chinese_paraphrase' else None,'note':None if q['sourceType']=='pali_with_editorial_chinese_paraphrase' else q['translationNote'] or None} for q in item['quotes']]
    if item['image']:
     plan=next(s for s in BOOK['scenes'] if s['id']==item['scene']);art=r['art']
     assert r['image']==item['image'] and r['natural']==item['dimensions'] and art['height']>65 and art['width']>115,(w,h,i,art)
     assert abs(art['width']/art['height']-1672/941)<.005 and r['caption']['bottom']<=art['top']+1,(w,h,i,'caption/art ratio')
     assert art['bottom']<=r['scripture']['top']+1 and r['hintHidden'],(w,h,i,'scripture/hint')
     label_checks(page.locator('#art-overlays .art-overlay').evaluate_all('(els)=>els.map('+labels_js+')'),plan['artOverlay'],art)
     if shots and (w,h) in [(768,1024),(1024,768)] and i==plan['start']:capture(page,f'{item["scene"]}-{w}x{h}.webp')
     if shots and w==360 and i in [15,47,55]:capture(page,f'{item["scene"]}-{w}x{h}.webp')
    else:
     assert page.locator('#summary-text section').count()==1
     if shots and w==768:capture(page,'ending-768x1024.webp')
    report['pageStates']+=1
   page.locator('#next').tap();assert page.locator('#position-text').inner_text()=='1 / 82 頁'
   for _ in range(8):page.locator('#next').tap()
   assert page.locator('#position-text').inner_text()=='9 / 82 頁' and page.evaluate('visualViewport.scale')==1
   page.locator('#previous').tap();assert page.locator('#position-text').inner_text()=='8 / 82 頁'
   next_rect=page.locator('#next').bounding_box();menu_rect=page.locator('.position').bounding_box()
   other=browser.new_page(viewport={'width':w,'height':h});other.goto(base+'anapana/book/');other.wait_for_function('typeof showPage==="function"')
   for actual,selector in [(next_rect,'#next'),(menu_rect,'.position')]:
    expected=other.locator(selector).bounding_box();assert abs(actual['x']-expected['x'])<1 and abs(actual['y']-expected['y'])<1,(w,h,selector)
   other.close()
   for plan in BOOK['scenes']:
    page.select_option('#page-select',plan['id']);settle(page);assert page.locator('.page').get_attribute('data-scene')==plan['id']
    if plan['artOverlay']:
     page.locator('#art').click();page.wait_for_function('document.querySelector("#zoom-art").complete')
     frame=page.locator('#zoom-frame').evaluate('e=>e.getBoundingClientRect().toJSON()')
     label_checks(page.locator('#zoom-overlays .art-overlay').evaluate_all('(els)=>els.map('+labels_js+')'),plan['artOverlay'],frame)
     report['enlargedOverlayStates']+=len(plan['artOverlay']);page.locator('#image-dialog form button').click()
     assert not page.locator('#image-dialog').evaluate('e=>e.open')
   assert page.locator('#art-overlays').inner_text()==''
   index=next(i for i,x in enumerate(BOOK['pages']) if len(x['quotes'])==2)
   page.evaluate('i=>showPage(i)',index);settle(page)
   page.locator('.verse-body').evaluate('e=>e.scrollTop=e.scrollHeight');assert page.locator('.verse-body').evaluate('e=>e.scrollTop>0')
   position=page.locator('#position-text').inner_text();page.locator('#open-verse').click()
   for q in BOOK['pages'][index]['quotes']:
    assert q['originalText'] in page.locator('#dialog-verse').text_content() and q['translationNote'] in page.locator('#dialog-verse').text_content()
   assert page.locator('.additional-source').count()==1
   page.locator('.verse-scroll').focus();page.keyboard.press('ArrowRight');assert page.locator('#position-text').inner_text()==position
   page.locator('#dialog-source').click();assert page.url.endswith('#'+BOOK['pages'][index]['quotes'][0]['quoteId'])
   page.go_back();page.wait_for_function('typeof showPage==="function"');assert page.locator('#position-text').inner_text()==position
   page.reload();page.wait_for_function('typeof showPage==="function"');assert page.locator('#position-text').inner_text()==position
   page.set_viewport_size({'width':h,'height':w});settle(page);assert page.locator('#position-text').inner_text()==position
   page.set_viewport_size({'width':w,'height':h});page.locator('.top a').click();page.locator('.book-cover').click();page.wait_for_function('typeof showPage==="function"');assert page.locator('#position-text').inner_text()==position
   page.locator('.reading-links a').last.click();assert page.url==base+'index.html'
   page.goto(base+'iddhipada/');assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
   if shots and (w,h) in [(768,1024),(1024,768)]:
    capture(page,f'guide-{w}x{h}.webp');page.locator('[id="sn51.13"]').scroll_into_view_if_needed();capture(page,f'sources-{w}x{h}.webp')
   page.close();report['viewports'].append({'width':w,'height':h,'pages':82,'controls':'passed'})
   print(f'{w}x{h}: 82 page states, exact captions/quotes, image labels and interactions passed',flush=True)
  # Root map requires its real CDN scripts; fulfill them from verified HTTPS fetches.
  page=browser.new_page(viewport={'width':1024,'height':768});cache={}
  for url in ['https://cdn.tailwindcss.com/','https://unpkg.com/lucide@latest']:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=45) as r:cache[url]=(r.read(),r.headers.get('Content-Type','application/javascript'))
  def cdn(route):
   raw,mime=cache[route.request.url];route.fulfill(status=200,body=raw,content_type=mime)
  page.route('https://cdn.tailwindcss.com/**',cdn);page.route('https://unpkg.com/lucide@latest',cdn)
  page.route('https://www.youtube.com/**',lambda route:route.abort())
  page.goto(base);page.locator('.sz-book[href="./iddhipada/book/index.html"]').click();page.wait_for_function('typeof showPage==="function"')
  page.goto(base);page.evaluate('openModal("四如意足")');page.locator('#modalBody a[href="./iddhipada/index.html"]').click();assert page.locator('h1').inner_text()=='四如意足'
  for name in LEGACY:
   page.goto(base+name+'/book/');page.locator('#next').wait_for(state='visible');before=page.locator('#position-text').inner_text();page.locator('#next').click();assert page.locator('#position-text').inner_text()!=before;page.locator('.top a').click();assert urlsplit(page.url).path in ['/'+name+'/','/'+name+'/index.html'],(name,page.url)
  report['legacyReaders']='all 10 open/next/return passed';report['rootEntrances']='shelf #11 and existing map node passed';report['localHTTPPreview']='guide/reader/menu/navigation/quotes/enlargement/return/restart passed';browser.close()
 server.shutdown();assert not report['javascriptErrors'] and not report['httpErrors'],report
 (OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('410 page states and 65 enlarged-label states passed; no local HTTP or JavaScript errors',flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--screenshots',action='store_true');p.add_argument('--verify-sources',action='store_true');a=p.parse_args();static_checks(a.verify_sources);browser_checks(a.screenshots)
