#!/usr/bin/env python3
"""Check book 08's complete source text, shared reader UI, scripture cards and touch controls."""
import argparse
import functools
import hashlib
import http.server
import io
import json
import re
import subprocess
import threading
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import unquote,urlsplit
from lxml import html
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs/mindfulness'
OUT=ROOT/'docs/previews/mindfulness'
BASELINE='1d964bbd8d6c9d0c05aa725f36da1b44d8ffb078'
STORY=json.loads((DOCS/'storyboard.json').read_text())
CATALOG={q['id']:q for q in json.loads((DOCS/'scripture-catalog.json').read_text())['quotes']}
BOOK=json.loads((ROOT/'mindfulness/book/book-data.js').read_text().split('const BOOK = ')[1].rstrip(';\n'))
SOURCES=json.loads((DOCS/'verified-sources.json').read_text())
SIZES=[(360,800),(800,360),(768,1024),(1024,768),(1440,900)]
LEGACY=['four-truths','five-aggregates','six-senses','twelve-links','eightfold-path','four-fruits-ten-fetters','four-purities-six-recollections']
def old(path):return subprocess.check_output(['git','show',BASELINE+':'+path],cwd=ROOT)
def source_text(raw):
 doc=html.fromstring(raw)
 for a in doc.xpath('//a[contains(@class,"ref")]'):a.drop_tree()
 return re.sub(r'\s+','',doc.text_content())
def static_checks(network):
 subprocess.run(['python','scripts/build-mindfulness.py','--check'],cwd=ROOT,check=True)
 assert len(BOOK['pages'])==111 and len(BOOK['scenes'])==25
 count=0
 for scene in STORY['scenes'][:24]:
  for number,p in enumerate(scene['narrationParagraphs'],1):
   pages=[x for x in BOOK['pages'] if x.get('paragraphId')==p['id']]
   assert ''.join(''.join(x['lines']) for x in pages)==p['text']
   expected=[r['quoteId'] for r in scene['scriptureRefs'] if number in r['narrationParagraphs']]
   for page in pages:
    assert [q['quoteId'] for q in page['quotes']]==expected
    for q in page['quotes']:
     assert q['text']==CATALOG[q['quoteId']]['videoText']
     assert q['source']==CATALOG[q['quoteId']]['sourceLabelAsVideo']
   count+=1
 assert count==92
 assert BOOK['pages'][-2]['summary'] and BOOK['pages'][-1]['afterword']
 ending=BOOK['pages'][-1]['lines']
 assert '《中阿含經》' in ending[0] and '《增壹阿含經》' in ending[0]
 assert '解讀仍請以原經文為準。' in ''.join(ending) and '溫柔' not in ''.join(ending)
 for name in subprocess.check_output(['git','ls-tree','-r','--name-only',BASELINE],cwd=ROOT,text=True).splitlines():
  if any(name.startswith(k+'/') for k in LEGACY) or name.startswith('.github/') or name in ['index.html','shelf.css','reader-controls.css','reader-restart.js','guide-ui.css','guide-header.css','.nojekyll','CNAME']:
   assert (ROOT/name).read_bytes()==old(name),name
 guide=html.parse(str(ROOT/'mindfulness/index.html'))
 for s in SOURCES['sources']:
  card=guide.xpath('//*[@id=$id]',id=s['id'])[0]
  assert len(card.xpath('.//*[contains(@class,"source-button")]'))==2
  assert len(card.xpath('.//*[contains(@class,"source-providers")]/p'))==2
  assert [p.text_content() for p in card.xpath('.//blockquote/p')]==s['excerpts']
  assert card.xpath('.//a[contains(@class,"source-button--original")]/@href')==[s['original']]
  for q in s['quoteIds']:assert guide.xpath('//*[@id=$id]',id=q)
 for file in SOURCES['files']:
  raw=(DOCS/file['local']).read_bytes();assert hashlib.sha256(raw).hexdigest()==file['sha256']
  for s in SOURCES['sources']:
   if s['id']==file['id']:
    assert all(t in source_text(raw) for t in s['excerpts'])
 if network:
  def verify(row):
   raw=urllib.request.urlopen(row['url'],timeout=30).read();assert hashlib.sha256(raw).hexdigest()==row['sha256'];return row['id']
  print('Official frozen source files:',list(ThreadPoolExecutor(max_workers=7).map(verify,SOURCES['files'])),flush=True)
 for path in ['mindfulness/index.html','mindfulness/book/index.html']:
  for url in html.parse(str(ROOT/path)).xpath('//@href|//@src'):
   parsed=urlsplit(url)
   if parsed.scheme or parsed.netloc:continue
   target=((ROOT/path).parent/unquote(parsed.path)).resolve()
   if target.is_dir():target/='index.html'
   assert target.is_file(),(path,url)
   if parsed.fragment:assert html.parse(str(target)).xpath('//*[@id=$id]',id=parsed.fragment)
 print('92 original paragraphs, 27 source mappings, seven canonical sources, footer and legacy preservation: OK',flush=True)
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
def settle(page):
 page.wait_for_function('document.querySelector("#art-frame").hidden || (document.querySelector("#art").complete && document.querySelector("#art").naturalWidth>0)')
 page.evaluate('()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))')
def screenshot(page,name):
 Image.open(io.BytesIO(page.screenshot(type='png'))).save(OUT/name,lossless=True,method=6)
def browser_checks(capture):
 OUT.mkdir(parents=True,exist_ok=True)
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
 threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
 report={'baseline':BASELINE,'pages':111,'scenes':25,'paragraphs':92,'quoteMappings':27,'quoteIds':18,'pageStates':0,'viewports':[],'javascriptErrors':[],'httpErrors':[],'realIPadSafari':'not tested'}
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for width,height in SIZES:
   page=browser.new_page(viewport={'width':width,'height':height},has_touch=True)
   page.on('pageerror',lambda e:report['javascriptErrors'].append(str(e)))
   page.on('response',lambda r:report['httpErrors'].append(r.url) if r.url.startswith(base) and r.status>=400 else None)
   page.goto(base+'mindfulness/book/');page.wait_for_function('typeof showPage==="function"')
   for index,item in enumerate(BOOK['pages']):
    page.evaluate('i=>showPage(i)',index);settle(page)
    result=page.evaluate('''()=>{
      const $=s=>document.querySelector(s),r=s=>$(s).getBoundingClientRect().toJSON();
      return {lines:[...$('#narration').children].map(p=>p.textContent),verse:$('#verse').textContent,number:$('#position-text').textContent,
       overflow:document.documentElement.scrollWidth>innerWidth,touch:getComputedStyle($('#next')).touchAction,
       art:r('#art-frame'),caption:r('#caption'),scripture:r('.scripture'),image:$('#art').getAttribute('src'),natural:[$('#art').naturalWidth,$('#art').naturalHeight],
       labels:[...$('#art-overlays').children].map(l=>({text:l.textContent,r:l.getBoundingClientRect().toJSON(),font:parseFloat(getComputedStyle(l).fontSize)}))};}''')
    assert result['lines']==item['lines'] and result['number']==f'{index+1} / 111 頁'
    assert not result['overflow'] and result['touch']=='manipulation'
    for q in item['quotes']:
     assert q['text'] in result['verse'] and q['source'] in result['verse']
     if q['relation']!='原片下方引文對應':assert q['relation'] in result['verse']
    if item['image']:
     assert result['image']==item['image'] and result['natural']==item['dimensions']
     art=result['art'];assert art['width']>100 and art['height']>90
     assert abs(art['width']/art['height']-item['dimensions'][0]/item['dimensions'][1])<.005
     plan=next(s for s in BOOK['scenes'] if s['id']==item['scene'])
     for actual,expected in zip(result['labels'],plan['artOverlay']):
      assert actual['text']==expected['text']
      assert abs(actual['r']['x']-art['x']-art['width']*expected['x']/100)<1
      assert abs(actual['r']['y']-art['y']-art['height']*expected['y']/100)<1
      assert abs(actual['font']-art['width']*expected['fontSizeCqw']/100)<.1
     if not item.get('summary'):
      assert result['caption']['bottom']<=art['top']+1
      if item['quotes']:assert art['bottom']<=result['scripture']['top']+1
    report['pageStates']+=1
    if capture and (width,height) in [(768,1024),(1024,768)]:
     plan=next((s for s in BOOK['scenes'] if s['id']==item['scene']),None)
     if (plan and plan['start']==index and item['scene'] in ['S03','S10','S18','S19','S21','S25']) or item.get('afterword'):
      screenshot(page,f'{item["scene"]}-{width}x{height}.webp')
    if capture and width==1440 and item.get('summary'):screenshot(page,'S25-1440x900.webp')
   page.locator('#next').tap();assert page.locator('#position-text').inner_text()=='1 / 111 頁'
   for _ in range(8):page.locator('#next').tap()
   assert page.locator('#position-text').inner_text()=='9 / 111 頁' and page.evaluate('visualViewport.scale')==1
   # The shared menu and controls occupy the same places as the existing book 07.
   controls=page.locator('#next').bounding_box();menu=page.locator('.position').bounding_box()
   reference=browser.new_page(viewport={'width':width,'height':height});reference.goto(base+'four-purities-six-recollections/book/')
   reference.wait_for_function('typeof showPage==="function"')
   for actual,selector in [(controls,'#next'),(menu,'.position')]:
    expected=reference.locator(selector).bounding_box()
    assert abs(actual['x']-expected['x'])<1 and abs(actual['y']-expected['y'])<1
   reference.close()
   page.select_option('#page-select','S10');start=BOOK['scenes'][9]['start'];q6=next(i for i,x in enumerate(BOOK['pages']) if x.get('paragraphId')=='S10-P03')
   assert 'Q06' not in [q['quoteId'] for q in BOOK['pages'][start]['quotes']]
   page.evaluate('i=>showPage(i)',q6);settle(page)
   page.locator('#open-verse').click();assert page.locator('#verse-dialog').evaluate('e=>e.open')
   assert CATALOG['Q06']['videoText'] in page.locator('#dialog-verse').inner_text()
   before=page.locator('#position-text').inner_text();page.locator('.verse-scroll').focus();page.keyboard.press('ArrowRight');assert page.locator('#position-text').inner_text()==before
   page.locator('.verse-scroll').evaluate('e=>e.scrollTop=e.scrollHeight');page.locator('#dialog-source').click()
   assert page.url.endswith('/mindfulness/#Q06') and page.locator('#ma98').is_visible()
   page.go_back();page.wait_for_function('typeof showPage==="function"');assert page.locator('#position-text').inner_text()==before
   page.reload();page.wait_for_function('typeof showPage==="function"');assert page.locator('#position-text').inner_text()==before
   page.set_viewport_size({'width':height,'height':width});settle(page);assert page.locator('#position-text').inner_text()==before
   page.set_viewport_size({'width':width,'height':height})
   page.select_option('#page-select','S19');settle(page);page.locator('#art').click()
   assert page.locator('#image-dialog').evaluate('e=>e.open') and page.locator('#zoom-overlays .art-overlay').count()==5
   page.locator('.image-scroll').evaluate('e=>{e.scrollLeft=150;e.scrollTop=50}')
   page.locator('#image-dialog form button').click()
   page.goto(base+'mindfulness/');assert page.locator('#sources .source-entry').count()==7
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
   for href,scene in [('S05','S05'),('S12','S12'),('S17','S17'),('S19','S19')]:
    page.goto(base+'mindfulness/book/?scene='+href);page.wait_for_function('typeof showPage==="function"')
    assert page.locator('.page').get_attribute('data-scene')==scene
   if capture and width==768:
    page.goto(base+'mindfulness/#sources');page.locator('#ma98').scroll_into_view_if_needed();screenshot(page,'sources-768x1024.webp')
   page.close();report['viewports'].append({'width':width,'height':height,'pages':111,'controls':'same as book 07; passed'})
   print(f'{width}x{height}: 111 pages, shared control positions, full text, sources, dialog, image labels, rotation and restart passed',flush=True)
  page=browser.new_page(viewport={'width':1024,'height':768})
  for name in LEGACY:
   page.goto(base+name+'/book/');page.locator('#next').wait_for(state='visible');before=page.locator('#position-text').inner_text()
   page.locator('#next').click();assert page.locator('#position-text').inner_text()!=before
   page.locator('.top a').click();assert urlsplit(page.url).path=='/'+name+'/'
  browser.close()
 server.shutdown()
 assert not report['javascriptErrors'] and not report['httpErrors'],report
 report['legacyReaders']='all seven open/next/return passed'
 (OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print('555 page states passed; source cards and reading controls match existing books.',flush=True)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--screenshots',action='store_true');parser.add_argument('--verify-sources',action='store_true');args=parser.parse_args()
 static_checks(args.verify_sources);browser_checks(args.screenshots)
