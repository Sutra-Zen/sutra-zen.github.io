from pathlib import Path
import json,subprocess,re,functools,http.server,threading
from playwright.sync_api import sync_playwright
import os
ROOT=Path(__file__).resolve().parents[1];os.chdir(ROOT);OLD='也希望這本繪本能成為您走入經藏的溫柔起點。';NEW='也希望這本繪本能成為您走入經藏的起點。'
books=['four-truths','five-aggregates','six-senses','twelve-links','eightfold-path','four-fruits-ten-fetters','four-purities-six-recollections']
def before(path):return subprocess.check_output(['git','show','3bb3c263f2cbe11f7368c395216d93b74c7eca66:'+path],text=True)
def variable(t,key):return json.JSONDecoder().raw_decode(t[t.index('const '+key+' = ')+len('const '+key+' = '):])[0]
for name in books:
 for p in (Path(name)/'book').glob('*'):
  if p.suffix not in ['.html','.js']:continue
  t=p.read_text();assert OLD not in t
  if p.name=='index.html':
   unversion=lambda s:re.sub(r'(src="(?:scenes|book-data|book)\.js)(?:\?[^" ]*)?"',r'\1"',s)
   assert unversion(t)==unversion(before(str(p)).replace(OLD,NEW)),name
  elif name!='four-purities-six-recollections':assert t==before(str(p)).replace(OLD,NEW),str(p)
p='four-purities-six-recollections/book/book-data.js';a=variable(before(p),'BOOK');b=variable(Path(p).read_text(),'BOOK')
for x,y in zip(a['pages'],b['pages']):
 expected=json.loads(json.dumps(x,ensure_ascii=False).replace(OLD,NEW))
 if x['scene']=='S06':expected['image']='../../docs/four-purities-six-recollections/assets/IMG_0400.jpeg'
 if x['scene']=='S07':expected['image']='../../docs/four-purities-six-recollections/assets/IMG_0401.jpeg'
 assert y==expected
assert a['scenes']==b['scenes']
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=s.serve_forever,daemon=True).start()
out=Path('docs/previews/book-copy-fix');out.mkdir(parents=True,exist_ok=True)
report={'closingStates':0,'imageStates':0,'errors':[]}
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for name in books:
  for w,h in [(390,844),(844,390),(768,1024),(1024,768)]:
   page=browser.new_page(viewport={'width':w,'height':h},has_touch=True);page.on('pageerror',lambda e:report['errors'].append(str(e)));page.goto(f'http://127.0.0.1:{s.server_port}/{name}/book/');page.wait_for_function('typeof showPage==="function"')
   total=int(page.locator('#position-text').inner_text().split('/')[1].split()[0]);page.evaluate('n=>showPage(n-1)',total);page.wait_for_function('document.querySelector("#next").getAttribute("aria-label")==="回到第一頁"')
   assert NEW in page.locator('.page').inner_text(),name;assert OLD not in page.locator('.page').inner_text();assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
   page.locator('#next').tap();assert page.locator('#position-text').inner_text().startswith('1 /');report['closingStates']+=1
   if name=='four-purities-six-recollections':
    for i,item in enumerate(b['pages']):
     if item['scene'] not in ['S06','S07']:continue
     page.evaluate('showPage',i);page.wait_for_function('document.querySelector("#art").complete&&document.querySelector("#art").naturalWidth>0');page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
     assert page.locator('#art').get_attribute('src')==item['image'];assert page.locator('.art-overlay').inner_text()==('僧不壞淨' if item['scene']=='S06' else '聖戒成就')
     assert page.locator('#art').evaluate('el=>[el.naturalWidth,el.naturalHeight]')==item['dimensions']
     assert page.locator('#narration').inner_text()==item['lines'][0];report['imageStates']+=1
     if w>=768 and h>=768 and item['subtitle']==1:page.screenshot(path=str(out/f'{item["scene"]}-{w}x{h}.png'))
   page.close()
  print(name,'closing text + restart in four sizes passed',flush=True)
 page=browser.new_page();page.goto(f'http://127.0.0.1:{s.server_port}/four-purities-six-recollections/');assert '「四入流分」與「四不壞淨」在同一經中分別說明' not in page.locator('main').inner_text();assert page.locator('.source-entry').count()==4;browser.close()
s.shutdown();assert not report['errors'];(out/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(report)
