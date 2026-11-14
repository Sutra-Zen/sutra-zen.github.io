import json,subprocess,threading,http.server,functools
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1];folder=root/'docs/previews/book06-afterword';folder.mkdir(parents=True,exist_ok=True)
def data(t):return json.loads(t.split('const BOOK = ')[1].rstrip(';\n'))
a=data(subprocess.check_output(['git','show','482e2fa280f6e01c18244dad14b28f0ae200c0b2:four-fruits-ten-fetters/book/book-data.js'],text=True));b=data(Path('four-fruits-ten-fetters/book/book-data.js').read_text());assert b['pages'][:74]==a['pages'];assert len(b['pages'])==75
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root)));threading.Thread(target=s.serve_forever,daemon=True).start()
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for w,h in [(390,844),(844,390),(768,1024),(1024,768)]:
  page=browser.new_page(viewport={'width':w,'height':h},has_touch=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{s.server_port}/four-fruits-ten-fetters/book/');page.evaluate('showPage(74)');page.wait_for_timeout(100)
  assert '溫柔起點' in page.locator('#narration').inner_text();assert page.locator('#next').get_attribute('aria-label')=='回到第一頁';assert page.locator('#next').is_visible()
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
  page.screenshot(path=str(folder/f'closing-{w}x{h}.png'))
  page.locator('#next').tap();assert page.locator('#position-text').inner_text()=='1 / 75 頁';assert page.locator('#previous').is_disabled();assert page.locator('#next').get_attribute('aria-label')=='下一頁'
  page.locator('#next').tap();assert page.locator('#position-text').inner_text()=='2 / 75 頁'
  page.select_option('#page-select','afterword');page.set_viewport_size({'width':h,'height':w});assert page.locator('#position-text').inner_text()=='75 / 75 頁';page.locator('#next').tap();assert page.locator('#position-text').inner_text()=='1 / 75 頁';assert not errors
  page.close();print(w,h,'closing, restart, next, menu, rotation OK')
 browser.close()
s.shutdown()
print('Original 74 pages byte-equivalent as data; 75th editorial page only. Guide disclaimer removed.')
