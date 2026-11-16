#!/usr/bin/env python3
"""Verify book 10 fidelity, image-relative labels and the shared reader interactions."""
import argparse,functools,hashlib,http.server,io,json,re,subprocess,threading,urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import unquote,urlsplit
from PIL import Image
from lxml import html
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]; DOCS=ROOT/'docs/anapana'; OUT=ROOT/'docs/previews/anapana'
BASELINE='0034db754a478bbce76c79b0dbe7479822dfee76'
STORY=json.loads((DOCS/'storyboard.json').read_text()); CAT=json.loads((DOCS/'scripture-catalog.json').read_text()); LABELS=json.loads((DOCS/'overlays.json').read_text())
BOOK=json.loads((ROOT/'anapana/book/book-data.js').read_text().split('const BOOK = ')[1].rstrip(';\n'))
DISPLAY_CAT={q['quoteId']:q for page in BOOK['pages'] for q in page['quotes']}
COMMENTARY_IDS={f'Q{i:02}' for i in range(32,42)}
STOP_TEXT='止爲何等，入息至竟，遍止鼻頭。莫隨。出息至竟，著鼻頭，莫隨。是爲止。何用是止？但欲從是止念。'
SOURCES=json.loads((DOCS/'verified-sources.json').read_text())
SIZES=[(360,800),(800,360),(768,1024),(1024,768),(1440,900)]
LEGACY=['four-truths','five-aggregates','six-senses','twelve-links','eightfold-path','four-fruits-ten-fetters','four-purities-six-recollections','mindfulness','right-effort']
def old(path): return subprocess.check_output(['git','show',BASELINE+':'+path],cwd=ROOT)
def clean(raw):
 r=html.fromstring(raw)
 for a in r.xpath('//a[contains(@class,"ref")]'): a.drop_tree()
 return re.sub(r'\s+','',r.text_content())
def static_checks(network):
 subprocess.run(['python3','scripts/build-anapana.py','--check'],cwd=ROOT,check=True)
 assert len(BOOK['pages'])==119 and len(BOOK['scenes'])==12 and len(CAT)==41
 n=0; used=set()
 for original,scene in zip(STORY['scenes'],BOOK['scenes']):
  assert scene['image']==original['image'] and scene['artOverlay']==original['overlays']==LABELS[scene['id']]
  for entry in original['narration']:
   item=BOOK['pages'][n]; assert item['lines']==[entry['text']] and item['paragraphId']==entry['id'] and item['scene']==original['sceneId']
   assert item['sourceNote']==entry['sourceNote'] and [q['quoteId'] for q in item['quotes']]==entry['quoteIds']
   for quote in item['quotes']:
    qid=quote['quoteId'];used.add(qid)
    assert all(quote[k]==v for k,v in CAT[qid].items() if qid not in COMMENTARY_IDS or k not in ['source','text','verification'])
    if qid in COMMENTARY_IDS:
     assert quote==DISPLAY_CAT[qid] and quote['relation']=='原文對讀' and '影片摘引' not in quote['source']
   n+=1
 assert n==118 and used==set(CAT) and sum(map(len,LABELS.values()))==12
 assert len(BOOK['pages'][-1]['textSummary'])==5 and len(BOOK['pages'][-1]['textSummary'][-1]['rows'])==4
 assert '覺知心悅 → 覺知心定' in BOOK['pages'][-1]['textSummary'][-1]['rows'][2][1]
 ending=''.join(BOOK['pages'][-1]['editorialNote']); assert '溫柔' not in ending and '解讀仍請以原經文為準' in ending
 assert all(not x['quotes'] for x in BOOK['pages'] if x['scene']=='S09')
 for row in json.loads((DOCS/'receipt.json').read_text())['originalFiles']:
  raw=(DOCS/row['path']).read_bytes(); assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
 for row in json.loads((DOCS/'asset-manifest.json').read_text()):
  raw=(DOCS/row['path']).read_bytes(); assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
  with Image.open(io.BytesIO(raw)) as im: assert list(im.size)==[row['width'],row['height']]; im.verify()
 for row in json.loads((DOCS/'web-assets.json').read_text()):
  with Image.open(ROOT/row['web']) as im: assert list(im.size)==row['dimensions']; im.verify()
 for name in subprocess.check_output(['git','ls-tree','-r','--name-only',BASELINE],cwd=ROOT,text=True).splitlines():
  if any(name.startswith(k+'/') for k in LEGACY) or name.startswith('.github/') or name in ['shelf.css','guide-ui.css','guide-header.css','reader-controls.css','reader-restart.js','.nojekyll','CNAME']:
   assert (ROOT/name).read_bytes()==old(name),name
 before=old('index.html').decode(); after=(ROOT/'index.html').read_text(); root=html.fromstring(after)
 assert len(root.xpath('//ol[@class="sz-books"]/li'))==14
 assert len(root.xpath('//*[contains(concat(" ",@class," ")," sz-ready ")]'))==10
 assert len(root.xpath('//*[@class="sz-book-lock"]'))==4
 assert root.xpath('//iframe/@src')==html.fromstring(before).xpath('//iframe/@src')
 maps=[json.loads(re.search(r'const dhammaData = (.*?);\s*\n',s)[1]) for s in [before,after]]; assert maps[0].keys()==maps[1].keys()
 for key in maps[0]:
  if key!='安那般那與止觀': assert maps[0][key]==maps[1][key]
  else: assert maps[0][key]['content'][:-6] in maps[1][key]['content']
 guide=html.parse(str(ROOT/'anapana/index.html'))
 assert len(guide.xpath('//*[@id="sources"]//article'))==6 and len(guide.xpath('//*[@id="commentary"]//article'))==2
 # Reader cue order remains tied to narration; reconstruct the guide order to catch stale or missing clauses.
 revision={s['id']:s for s in SOURCES['commentarialSources']}
 a=guide.xpath('//*[@id="bhavanakrama"]')[0];b=guide.xpath('//*[@id="anban"]')[0]
 assert a.xpath('./h3/text()')==['蓮花戒大師《修次中編／下編》']
 assert a.xpath('.//*[@class="source-meta"]/text()')==['《菩提道次第廣論》卷十四引述 · 宗喀巴大師造／法尊法師譯']
 assert ''.join(DISPLAY_CAT[q]['text'] for q in ['Q32','Q36','Q33','Q34','Q35','Q37','Q38'])==a.xpath('.//blockquote/p/text()')[0]==revision['bhavanakrama']['excerpts'][0]
 assert '自鼻至臍' in DISPLAY_CAT['Q35']['text']
 assert [DISPLAY_CAT[q]['text'] for q in ['Q39','Q40','Q41']]==b.xpath('.//blockquote/p/text()')==revision['anban']['excerpts']
 assert DISPLAY_CAT['Q41']['text']==STOP_TEXT
 assert '投二' in DISPLAY_CAT['Q39']['text'] and '莫投二' in DISPLAY_CAT['Q40']['text']
 for q in COMMENTARY_IDS:
  expected=revision['bhavanakrama']['readerSourceLabel'] if q<'Q39' else revision['anban']['readerStopSourceLabel' if q=='Q41' else 'readerSourceLabel']
  assert DISPLAY_CAT[q]['source']==expected
 for source in revision.values():
  assert hashlib.sha256((DOCS/source['local']).read_bytes()).hexdigest()==source['sha256']
 for f in SOURCES['files']:
  raw=(DOCS/f['local']).read_bytes(); assert hashlib.sha256(raw).hexdigest()==f['sha256']
  source=next(s for s in SOURCES['sources'] if s['id']==f['id']); assert all(t in clean(raw) for t in source['excerpts'])
  card=guide.xpath('//*[@id=$id]',id=f['id'])[0]; assert card.xpath('.//blockquote/p/text()')==source['excerpts']
  assert card.xpath('.//a[contains(@class,"source-button--annotation")]/@href')==[source.get('annotation',source.get('pali'))]
 for q in CAT: assert guide.xpath('//*[@id=$id]',id=q)
 for path in ['anapana/index.html','anapana/book/index.html']:
  raw=(ROOT/path).read_text(); assert 'SN54.1' not in raw and 'data:image' not in raw
  for url in html.fromstring(raw).xpath('//@src|//@href'):
   u=urlsplit(url)
   if u.scheme or u.netloc: continue
   target=((ROOT/path).parent/unquote(u.path)).resolve()
   if target.is_dir(): target/='index.html'
   assert target.is_file(),(path,url)
   if u.fragment:
    if target.suffix.lower()=='.pdf':
     page=re.fullmatch(r'page=([1-9]\d*)',u.fragment)
     info=subprocess.check_output(['pdfinfo',str(target)],text=True)
     total=int(re.search(r'^Pages:\s+(\d+)',info,re.M)[1])
     assert page and int(page[1])<=total,(path,url,'invalid PDF page')
    else: assert html.parse(str(target)).xpath('//*[@id=$id]',id=u.fragment)
 if network:
  def verify(f):
   assert hashlib.sha256(urllib.request.urlopen(f['url'],timeout=30).read()).hexdigest()==f['sha256']; return f['id']
  print('Official source hashes:',list(ThreadPoolExecutor(max_workers=6).map(verify,SOURCES['files'])),flush=True)
 print('Static fidelity: 11 originals, 27 images, 12 scenes, 118 paragraphs, 41 quotes (10 commentary cues synchronized with guide), 12 labels; all 9 previous books unchanged',flush=True)
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args): pass
def settle(page):
 page.wait_for_function('document.querySelector("#art-frame").hidden || (document.querySelector("#art").complete && document.querySelector("#art").naturalWidth>0)')
 page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
def capture(page,name): Image.open(io.BytesIO(page.screenshot(type='png'))).save(OUT/name,lossless=True,method=6)
def enlarged_checks(browser,base,report,shots):
 count=0
 for w,h in [(360,800),(1024,768)]:
  page=browser.new_page(viewport={'width':w,'height':h});page.goto(base+'anapana/book/index.html');page.wait_for_function('typeof showPage==="function"')
  for plan in BOOK['scenes']:
   if not plan['artOverlay']:continue
   page.select_option('#page-select',plan['id']);settle(page);page.locator('#art').click();page.wait_for_function('document.querySelector("#zoom-art").complete')
   r=page.evaluate('''()=>{const f=document.querySelector('#zoom-frame').getBoundingClientRect();return {f:f.toJSON(),labels:[...document.querySelectorAll('#zoom-overlays .art-overlay')].map(l=>({text:l.textContent,r:l.getBoundingClientRect().toJSON(),font:parseFloat(getComputedStyle(l).fontSize),display:getComputedStyle(l).display}))}}''')
   for a,e in zip(r['labels'],plan['artOverlay']):
    assert a['text']==e['text'] and a['display']!='none'
    for key,dim in [('x','width'),('y','height')]:assert abs(a['r'][key]-r['f'][key]-r['f'][dim]*e[key]/100)<1
    assert abs(a['r']['width']-r['f']['width']*e['width']/100)<1 and abs(a['font']-r['f']['width']*e['fontSizeCqw']/100)<.1
    count+=1
   if shots and plan['id']=='S10' and w==1024:
    page.locator('.image-scroll').evaluate('e=>{e.scrollLeft=350;e.scrollTop=300}');capture(page,'S10-zoom-1024x768.webp')
   page.locator('#image-dialog form button').click()
  if shots and w==360:
   page.select_option('#page-select','S10');settle(page);capture(page,'S10-360x800.webp')
  page.locator('.reading-links a').last.click();assert page.url==base+'index.html';page.close()
 report["enlargedOverlayStates"]=count; report["backToMap"]="passed at phone and iPad landscape"
 print(count,"enlarged image label coordinates/font sizes and return-map passed",flush=True)

def browser_checks(shots):
 OUT.mkdir(parents=True,exist_ok=True)
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT))); threading.Thread(target=server.serve_forever,daemon=True).start(); base=f'http://127.0.0.1:{server.server_port}/'
 report={'baseline':BASELINE,'pages':119,'scenes':12,'originalImages':11,'narrationParagraphs':118,'quotes':41,'updatedCommentaryQuoteIds':sorted(COMMENTARY_IDS),'overlays':12,'pageStates':0,'viewports':[],'javascriptErrors':[],'httpErrors':[],'physicalIPadSafari':'not tested','production':'local verification; deployment verified separately'}
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for w,h in SIZES:
   page=browser.new_page(viewport={'width':w,'height':h},has_touch=True)
   page.on('pageerror',lambda e:report['javascriptErrors'].append(str(e)))
   page.on('response',lambda r:report['httpErrors'].append(r.url) if r.url.startswith(base) and r.status>=400 else None)
   page.route('https://www.youtube.com/**',lambda route:route.abort())
   page.goto(base+'anapana/book/index.html'); page.wait_for_function('typeof showPage==="function"')
   for i,item in enumerate(BOOK['pages']):
    page.evaluate('i=>showPage(i)',i); settle(page)
    r=page.evaluate('''()=>{const $=s=>document.querySelector(s),rect=s=>$(s).getBoundingClientRect().toJSON();return {
     lines:[...$('#narration').children].map(x=>x.textContent),number:$('#position-text').textContent,
     overflow:document.documentElement.scrollWidth>innerWidth,touch:getComputedStyle($('#next')).touchAction,
     art:rect('#art-frame'),caption:rect('#caption'),scripture:rect('.scripture'),image:$('#art').getAttribute('src'),natural:[$('#art').naturalWidth,$('#art').naturalHeight],
     quotes:[...$('#verse').querySelectorAll('.scripture-card')].map(x=>({id:x.dataset.quoteId,source:x.querySelector('h3').textContent,text:x.querySelector('blockquote').textContent})),
     note:$('#verse .source-note')?.textContent||null,hintHidden:$('#outside-labels').hidden,hint:$('#outside-labels').textContent,
     labels:[...$('#art-overlays').children].map(l=>({text:l.textContent,r:l.getBoundingClientRect().toJSON(),font:parseFloat(getComputedStyle(l).fontSize),color:getComputedStyle(l).color,transform:getComputedStyle(l).transform,display:getComputedStyle(l).display,align:getComputedStyle(l).textAlign}))};}''')
    assert r['lines']==item['lines'] and r['number']==f'{i+1} / 119 頁',(w,h,i,r)
    assert not r['overflow'] and r['touch']=='manipulation',(w,h,i,'overflow/touch')
    assert r['quotes']==[{'id':q['quoteId'],'source':q['source'],'text':q['text']} for q in item['quotes']]
    assert r['note']==('補充說明：'+item['sourceNote'] if item['sourceNote'] else None)
    if item['image']:
     plan=next(s for s in BOOK['scenes'] if s['id']==item['scene']); art=r['art']
     assert r['image']==item['image'] and r['natural']==item['dimensions'] and art['height']>65 and art['width']>115,(w,h,i,art)
     assert abs(art['width']/art['height']-item['dimensions'][0]/item['dimensions'][1])<.005
     assert r['caption']['bottom']<=art['top']+1,(w,h,i,'caption',r['caption'],art)
     if item['quotes'] or item['sourceNote'] or item['context']: assert art['bottom']<=r['scripture']['top']+1,(w,h,i,'scripture')
     assert len(r['labels'])==len(plan['artOverlay'])
     outside=item['scene']=='S10' and art['width']<600
     assert r['hintHidden']==(not outside)
     if outside: assert r['hint']=='由左到右：眼微開／齒唇自然合／舌抵上顎'
     for actual,expected in zip(r['labels'],plan['artOverlay']):
      assert actual['text']==expected['text'] and actual['transform']=='none' and actual['align']==expected['textAlign']
      if outside: assert actual['display']=='none'; continue
      assert actual['display']!='none'
      for metric,key in [('x','x'),('y','y')]: assert abs(actual['r'][metric]-art[metric]-art['width' if metric=='x' else 'height']*expected[key]/100)<1
      assert abs(actual['r']['width']-art['width']*expected['width']/100)<1
      assert abs(actual['font']-art['width']*expected['fontSizeCqw']/100)<.1
      assert actual['r']['bottom']<=art['bottom']+1 and actual['r']['right']<=art['right']+1
     if shots and (w,h) in [(768,1024),(1024,768)] and i==plan['start']: capture(page,f'{item["scene"]}-{w}x{h}.webp')
    else:
     assert page.locator('#summary-text section').count()==6 and page.locator('#summary-text tr').count()==4
     assert '覺知心悅 → 覺知心定' in page.locator('#summary-text').inner_text()
     if shots and (w,h) in [(768,1024),(1024,768)]:
      capture(page,f'S12-{w}x{h}.webp'); page.locator('#summary-text').evaluate('e=>e.closest(".scene").scrollTop=e.closest(".scene").scrollHeight')
      if h>w: page.locator('#summary-text section').last.scroll_into_view_if_needed()
      capture(page,f'S12-end-{w}x{h}.webp')
    report['pageStates']+=1
   page.locator('#next').tap(); assert page.locator('#position-text').inner_text()=='1 / 119 頁'
   for _ in range(8): page.locator('#next').tap()
   assert page.locator('#position-text').inner_text()=='9 / 119 頁' and page.evaluate('visualViewport.scale')==1
   # Shared controls retain the existing book 09 coordinates.
   next_rect=page.locator('#next').bounding_box(); menu_rect=page.locator('.position').bounding_box()
   other=browser.new_page(viewport={'width':w,'height':h}); other.goto(base+'right-effort/book/'); other.wait_for_function('typeof showPage==="function"')
   for actual,selector in [(next_rect,'#next'),(menu_rect,'.position')]:
    expected=other.locator(selector).bounding_box(); assert abs(actual['x']-expected['x'])<1 and abs(actual['y']-expected['y'])<1,(w,h,'controls',selector,actual,expected)
   other.close()
   # Actual menu selection and image enlargement: all 3 tiny hints return inside the enlarged image.
   for plan in BOOK['scenes']:
    page.select_option('#page-select',plan['id']); settle(page); assert page.locator('.page').get_attribute('data-scene')==plan['id']
   page.select_option('#page-select','S10'); settle(page); page.locator('#art').click()
   assert page.locator('#image-dialog').evaluate('e=>e.open') and page.locator('#zoom-frame').bounding_box()['width']>=1400
   assert page.locator('#zoom-overlays .art-overlay:visible').count()==3
   assert page.locator('#zoom-overlays').inner_text().splitlines()==['眼微開','齒唇自然合','舌抵上顎']
   page.locator('.image-scroll').evaluate('e=>{e.scrollLeft=450;e.scrollTop=100}'); page.locator('#image-dialog form button').click()
   assert not page.locator('#image-dialog').evaluate('e=>e.open')
   # Long scripture is directly visible and scrolls; dialog/source/rotation retain exact paragraph.
   index=next(i for i,x in enumerate(BOOK['pages']) if any(q['quoteId']=='Q39' for q in x['quotes']))
   page.evaluate('i=>showPage(i)',index); settle(page)
   page.locator('.verse-body').evaluate('e=>e.scrollTop=e.scrollHeight'); assert page.locator('.scripture-card blockquote').text_content()==DISPLAY_CAT['Q39']['text']
   position=page.locator('#position-text').inner_text(); page.locator('#open-verse').click(); assert DISPLAY_CAT['Q39']['text'] in page.locator('#dialog-verse').inner_text()
   page.locator('.verse-scroll').focus(); page.keyboard.press('ArrowRight'); assert page.locator('#position-text').inner_text()==position
   page.locator('#dialog-source').click(); assert page.url.endswith('#Q39')
   page.go_back(); page.wait_for_function('typeof showPage==="function"'); assert page.locator('#position-text').inner_text()==position
   page.reload(); page.wait_for_function('typeof showPage==="function"'); assert page.locator('#position-text').inner_text()==position
   page.set_viewport_size({'width':h,'height':w}); settle(page); assert page.locator('#position-text').inner_text()==position
   page.set_viewport_size({'width':w,'height':h}); page.locator('.top a').click(); page.locator('.book-cover').click(); page.wait_for_function('typeof showPage==="function"'); assert page.locator('#position-text').inner_text()==position
   # S10 actual image width can change across rotation without stale labels.
   page.select_option('#page-select','S10'); settle(page)
   page.set_viewport_size({'width':h,'height':w}); settle(page)
   assert page.locator('#outside-labels').evaluate('(e)=>e.hidden')==(page.locator('#art-frame').bounding_box()['width']>=600)
   page.select_option('#page-select','S01'); settle(page); assert page.locator('#art-overlays').inner_text()=='' and page.locator('#outside-labels').evaluate('e=>e.hidden')
   page.set_viewport_size({'width':w,'height':h}); page.goto(base+'anapana/index.html'); assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
   if shots and (w,h) in [(768,1024),(1024,768)]:
    capture(page,f'guide-{w}x{h}.webp'); page.locator('#sa803').scroll_into_view_if_needed(); capture(page,f'sources-{w}x{h}.webp'); page.locator('#commentary-heading').scroll_into_view_if_needed(); capture(page,f'commentary-{w}x{h}.webp')
   page.close(); report['viewports'].append({'width':w,'height':h,'pages':119,'controls':'passed'})
   print(f'{w}x{h}: 119 pages, exact text/quotes, full image/labels, caption above, scripture below, interactions passed',flush=True)
  # Actual root map and shelf links, keeping CDN certificate verification enabled.
  page=browser.new_page(viewport={'width':1024,'height':768}); cache={}
  for url in ['https://cdn.tailwindcss.com/','https://unpkg.com/lucide@latest']:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as r: cache[url]=(r.read(),r.headers.get('Content-Type','application/javascript'))
  def cdn(route):
   raw,mime=cache[route.request.url]; route.fulfill(status=200,body=raw,content_type=mime)
  page.route('https://cdn.tailwindcss.com/**',cdn); page.route('https://unpkg.com/lucide@latest',cdn)
  page.goto(base); page.locator('.sz-book[href="./anapana/book/index.html"]').click(); page.wait_for_function('typeof showPage==="function"'); assert page.locator('#position-text').inner_text().endswith('/ 119 頁')
  page.goto(base); page.evaluate('openModal("安那般那與止觀")'); page.locator('#modalBody a[href="./anapana/index.html"]').click(); assert page.locator('h1').inner_text()=='安那般那與止觀'
  for name in LEGACY:
   page.goto(base+name+'/book/'); page.locator('#next').wait_for(state='visible'); before=page.locator('#position-text').inner_text(); page.locator('#next').click(); assert page.locator('#position-text').inner_text()!=before; page.locator('.top a').click(); assert urlsplit(page.url).path=='/'+name+'/'
  enlarged_checks(browser,base,report,shots)
  # Managed Chromium forbids file:// navigation. Verify the identical entry over local HTTP;
  # do not bypass that policy or claim that physical iPad Files executes HTML/JavaScript.
  page.goto(base+'anapana/index.html'); page.locator('.book-cover').click(); page.wait_for_function('typeof showPage==="function"'); settle(page)
  page.locator('#next').click(); before=page.locator('#position-text').inner_text(); page.reload(); page.wait_for_function('typeof showPage==="function"'); assert page.locator('#position-text').inner_text()==before
  page.locator('.top a').click(); assert page.url==base+'anapana/index.html'
  report['offlineFilePreview']='file:// blocked by managed-browser policy; use documented local HTTP server'
  report['localHTTPPreview']='guide/reader/next/reload/return passed'; report['legacyReaders']='all 9 open/next/return passed'; browser.close()
 server.shutdown(); assert not report['javascriptErrors'] and not report['httpErrors'],report
 (OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n'); print('595 page states, local HTTP preview, map/shelf and all 9 old readers passed',flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser(); p.add_argument('--screenshots',action='store_true'); p.add_argument('--verify-sources',action='store_true'); args=p.parse_args(); static_checks(args.verify_sources); browser_checks(args.screenshots)
