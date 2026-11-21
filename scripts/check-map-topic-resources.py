"""Verify every map dialog, preserved copy, resource targets and reader round trips."""
from pathlib import Path
import argparse,functools,http.server,io,json,re,subprocess,threading,urllib.request
from urllib.parse import urlparse
from lxml import html
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--live',action='store_true');parser.add_argument('--sizes',default='360x800,390x844,768x1024,1024x768,1280x900');parser.add_argument('--output',type=Path,default=R/'docs/previews/map-topic-resources');args=parser.parse_args();O=args.output;O.mkdir(parents=True,exist_ok=True)
old=subprocess.check_output(['git','show','02843bde:index.html'],cwd=R,text=True);new=(R/'index.html').read_text()
def data(t):return json.loads(re.search(r'const dhammaData = (.*?);\s*\n',t)[1])
a,b=data(old),data(new);assert set(a)==set(b)
for key in a:
 original=re.sub(r'<a\b.*?</a>','',a[key]['content'],flags=re.S)
 original=html.fragment_fromstring(original,create_parent='div').text_content()
 t=html.fragment_fromstring(b[key]['content'],create_parent='div');t.xpath('.//nav')[0].drop_tree()
 assert original==t.text_content(),key
 assert a[key]['title']==b[key]['title']
assert html.fromstring(old).xpath('//iframe/@src')==html.fromstring(new).xpath('//iframe/@src')
assert html.fromstring(old).xpath('//*[@id="books"]//a/@href')==html.fromstring(new).xpath('//*[@id="books"]//a/@href')
for row in json.loads((R/'docs/previews/map-topic-resources/topics.json').read_text()):
 t=html.fragment_fromstring(b[row['key']]['content'],create_parent='div');assert t.xpath('.//a/@href')==row['targets']
 for href in row['targets']:
  if href.startswith('./'):assert (R/href).is_file(),href
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
 def copyfile(self,src,out):
  try:super().copyfile(src,out)
  except (BrokenPipeError,ConnectionResetError):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=s.serve_forever,daemon=True).start()
base='https://sutra-zen.github.io/' if args.live else f'http://127.0.0.1:{s.server_port}/'
report={'mode':'live' if args.live else 'local','sizes':[],'dialogStates':0,'readerRoundTrips':0,'errors':[],'httpErrors':[],'transport':'live HTTPS responses fetched by TLS-verified urllib and served to Chromium' if args.live else 'local HTTP','cdn':'cached Tailwind/Lucide copies; external CDN not tested','physicalSafari':'not tested','youtubePlayback':'not tested; existing URL and new-tab behavior checked'}
cache={}
def live_route(route):
 url=route.request.url
 try:
  if url not in cache:
   with urllib.request.urlopen(url,timeout=35) as r:cache[url]=(r.status,dict(r.headers),r.read())
  status,headers,body=cache[url];headers={k:v for k,v in headers.items() if k.lower() not in ['content-length','content-encoding','transfer-encoding','connection']}
  route.fulfill(status=status,headers=headers,body=body)
 except Exception as e:report['httpErrors'].append(url+': '+str(e));route.abort()
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for w,h in [tuple(map(int,size.split('x'))) for size in args.sizes.split(',')]:
  context=browser.new_context(viewport={'width':w,'height':h},has_touch=True)
  if args.live:context.route(base+'**',live_route)
  context.route('https://www.youtube.com/**',lambda r:r.abort());context.route('https://cdn.tailwindcss.com/**',lambda r:r.fulfill(content_type='application/javascript',body=Path('/tmp/tailwind-site.js').read_bytes()));context.route('https://unpkg.com/**',lambda r:r.fulfill(content_type='application/javascript',body=Path('/tmp/migration-lucide.min.js').read_bytes()))
  context.route('https://youtu.be/**',lambda r:r.fulfill(content_type='text/html',body='<p>Video link target checked; playback not tested.</p>'))
  page=context.new_page();page.on('pageerror',lambda e:report['errors'].append(str(e)));page.on('response',lambda r:report['httpErrors'].append(r.url) if r.url.startswith(base) and r.status>=400 else None)
  def home():
   page.goto(base,wait_until='domcontentloaded');page.wait_for_function('typeof openModal==="function" && typeof lucide!=="undefined"')
  def open_key(key):
   page.locator('[onclick*='+json.dumps("openModal('"+key+"')",ensure_ascii=False)+']').first.click()
   page.wait_for_function('document.querySelector("#detailModal").getAttribute("aria-hidden")==="false" && !document.querySelector("#modalContent").classList.contains("scale-95")');page.wait_for_timeout(40)
  def close():
   page.locator('#modalContent > div').last.locator('button').click();page.wait_for_function('document.querySelector("#detailModal").classList.contains("hidden")')
  home()
  for key in b:
   open_key(key);links=page.locator('.sz-topic-resource');assert links.count()==3,key
   assert links.locator('strong').all_text_contents()==['專頁說明','翻頁繪本','繪本影片'];assert links.locator('.sz-topic-resource-icon svg').count()==3
   assert len(set(links.evaluate_all('els=>els.map(e=>getComputedStyle(e).backgroundImage)')))==3
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
   assert page.locator('#modalBody').evaluate('e=>e.scrollWidth<=e.clientWidth')
   assert page.locator('#modalContent').bounding_box()['height']<=h*.9+1
   if key in ['五根五力總說','念覺支','四聖諦總說','相關內容總說'] and (w,h) in [(390,844),(768,1024),(1280,900)]:
    page.locator('#modalBody').evaluate('e=>e.scrollTop=0');page.mouse.move(0,0);page.wait_for_timeout(200)
    Image.open(io.BytesIO(page.locator('#modalContent').screenshot())).save(O/f'{key}-{w}x{h}.png')
   for i in range(3):
    links.nth(i).scroll_into_view_if_needed();box=links.nth(i).bounding_box();body=page.locator('#modalBody').bounding_box();assert box['y']>=body['y']-1 and box['y']+box['height']<=body['y']+body['height']+1
   if key not in ['道路總說','相關內容總說']:
    assert links.nth(2).get_attribute('target')=='_blank'
    assert links.nth(2).get_attribute('rel')=='noopener noreferrer'
   close();report['dialogStates']+=1
  print(w,h,"32 modal checks passed",flush=True)
  # Use the cards to navigate every unique guide and book, return to the root map.
  seen=set()
  for row in json.loads((R/'docs/previews/map-topic-resources/topics.json').read_text()):
   if not row['path'] or row['path'] in seen:continue
   seen.add(row['path']);open_key(row['key']);page.locator('.sz-topic-resource').nth(0).click();page.wait_for_url(base+row['path']+'/index.html');assert page.locator('h1').inner_text().strip();home()
   open_key(row['key']);page.locator('.sz-topic-resource').nth(1).click();page.wait_for_url(base+row['path']+'/book/index.html');page.wait_for_timeout(200)
   imgs=page.locator('img');assert imgs.count()>0
   position=page.locator('#position-text');page.wait_for_function('document.querySelector("#position-text").textContent.trim().length>0')
   first=position.inner_text();page.locator('#next').click();page.wait_for_timeout(100);assert position.inner_text()!=first,row['path']
   page.locator('#previous').click();page.wait_for_timeout(100);assert position.inner_text()==first,row['path']
   # The original Five Aggregates / Six Senses readers begin with a text cover.
   advanced=0
   while page.locator('img[src]').count()==0 and advanced<10:
    page.locator('#next').click();advanced+=1;page.wait_for_timeout(50)
   page.wait_for_function('Array.from(document.images).some(i=>i.complete && i.naturalWidth>0)')
   for _ in range(advanced):page.locator('#previous').click()
   assert position.inner_text()==first,row['path']
   print(w,h,row['path'],'guide / book / flips / image passed',flush=True)
   back=page.locator('a').filter(has_text='回修道地圖').first;assert back.count();back.click();page.wait_for_url(re.compile(re.escape(base)+'(index.html)?$'));page.wait_for_function('typeof openModal==="function"');report['readerRoundTrips']+=1
  for key in ['道路總說','相關內容總說']:
   for i,target in [(0,'books'),(1,'books'),(2,'videos')]:
    open_key(key);page.locator('.sz-topic-resource').nth(i).click();page.wait_for_function('document.querySelector("#detailModal").classList.contains("hidden")');assert page.url.endswith('#'+target)
  open_key('五根五力總說')
  with page.expect_popup() as pop:page.locator('.sz-topic-resource').nth(2).click()
  assert pop.value.url.startswith('https://youtu.be/EzZOF8vQS2k');pop.value.close();close()
  report['sizes'].append({'size':[w,h],'dialogs':32,'uniqueGuideBookRoundTrips':14,'overviewActions':6,'videoNewTab':'passed'});print(w,h,'32 dialogs / 14 guide-book-return flows passed',flush=True);context.close()
 browser.close()
s.shutdown();assert not report['errors'] and not report['httpErrors'],report
(O/('live-validation.json' if args.live else 'validation.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False),flush=True)
