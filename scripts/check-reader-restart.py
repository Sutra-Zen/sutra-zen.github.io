from pathlib import Path
import functools,http.server,threading
from playwright.sync_api import sync_playwright
import os
os.chdir(Path(__file__).resolve().parents[1])
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(Path.cwd())));threading.Thread(target=s.serve_forever,daemon=True).start()
out=Path('docs/previews/all-readers-restart');out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for name in ['four-truths','five-aggregates','six-senses','twelve-links','eightfold-path','four-fruits-ten-fetters']:
  for w,h in [(390,844),(844,390),(768,1024),(1024,768)]:
   page=b.new_page(viewport={'width':w,'height':h},has_touch=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   page.goto(f'http://127.0.0.1:{s.server_port}/{name}/book/');page.wait_for_function('typeof showPage === "function"');total=int(page.locator('#position-text').inner_text().split('/')[1].split()[0]);page.evaluate('n=>showPage(n-1)',total);page.wait_for_function('document.querySelector("#next").getAttribute("aria-label")==="回到第一頁"')
   assert page.locator('#next').is_enabled();assert page.locator('#next').evaluate('el=>getComputedStyle(el).touchAction')=='manipulation'
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
   if w==1024:page.screenshot(path=str(out/(name+'.png')))
   page.locator('#next').tap();assert page.locator('#position-text').inner_text().startswith('1 /');assert page.locator('#previous').is_disabled();assert page.locator('#next').get_attribute('aria-label')=='下一頁'
   page.locator('#next').tap();assert page.locator('#position-text').inner_text().startswith('2 /')
   page.evaluate('n=>showPage(n-1)',total);page.set_viewport_size({'width':h,'height':w});page.locator('#next').tap();assert page.locator('#position-text').inner_text().startswith('1 /');assert not errors
   page.close()
  print(name,'four viewports: restart, next, rotation, touch action OK',flush=True)
 b.close()
s.shutdown()
