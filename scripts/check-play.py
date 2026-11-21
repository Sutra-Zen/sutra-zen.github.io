#!/usr/bin/env python3
"""Exercise the journey with real page-button navigation and protected-site checks.
Run from any directory: python3 scripts/check-play.py. Requires Playwright + Chromium.
Uses a disposable local server/browser profile, never a public deployment.
"""
from pathlib import Path
from urllib.parse import urlsplit
import functools, hashlib, http.server, json, subprocess, threading
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/previews/play'
KEY = 'sutrazen.play.v1'
BASELINE = 'b9a0dad2c2c34d7e15e6dc5e55d6125de630f57b'
BOOKS = ['four-truths', 'five-aggregates', 'six-senses']
ORIGINAL = {
 'four-truths': {'total': 29, 'scenes': 11, 'pageDataSha256': 'fc4ad2489fd0deb00344206e55131fbdfcda9027da2e255a91df45584bd781d3', 'sceneDataSha256': 'ed9323c4c99b1e46462aba2d126e32968dea1c961b7d5fbf0ecb8b39ff08a00b'},
 'five-aggregates': {'total': 54, 'scenes': 16, 'pageDataSha256': 'cf9cb4d4fb050c793b36b0cb5913d4b8620372a8a60995c6177fd703123d8592', 'sceneDataSha256': '9375b95d87d87ec8c01c2fb4e2344514ae3647067a8e8e64f626e39715a54cfc'},
 'six-senses': {'total': 115, 'scenes': 16, 'pageDataSha256': 'b3d19ecdce3bc379dd9ed0a7805f566470d6bb955eac26d301e1bdea00f357c3', 'sceneDataSha256': '30ef677968d66ced004e1604282df664af8f06e44fd3293b361b16bbc0d84481'},
}

class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self, *args): pass
 def copyfile(self, src, dst):
  try: super().copyfile(src, dst)
  except (BrokenPipeError, ConnectionResetError): pass


def check_original_home(page, base):
 page.goto(base+'index.html#map-heading',wait_until='domcontentloaded')
 page.wait_for_function('typeof openModal==="function"')
 assert page.locator('#map-heading').count()==1
 assert page.locator('.sz-books > li').count()==14
 page.locator('[onclick*="四聖諦總說"]').first.click()
 page.wait_for_function('document.querySelector("#detailModal").getAttribute("aria-hidden")==="false"')
 assert page.locator('.sz-topic-resource strong').all_text_contents()==['專頁說明','翻頁繪本','繪本影片']
 page.locator('#modalContent > div').last.locator('button').click()
 page.wait_for_function('document.querySelector("#detailModal").classList.contains("hidden")')
 page.locator('#books a[href="./four-truths/book/"]').click()
 page.wait_for_function('typeof showPage==="function"')
 assert not page.locator('.sz-journey-return').count()
 assert page.locator('#position-text').inner_text().endswith('/ 29 頁')


def check_progress_transitions(page):
 return page.evaluate('''async()=>{const {store}=await import('./progress.js');const original=store.exportBackup();store.reset();if(!store.finish('four-truths'))throw Error('First completion failed');store.savePosition('four-truths',4,'ordered');if(store.get().replayBook!=='four-truths')throw Error('Replay not tracked');store.savePosition('five-aggregates',7,'ordered');let s=store.get();if(s.replayBook!==null||s.orderedBook!=='five-aggregates')throw Error('Unfinished ordered book failed to supersede replay');store.setActive('six-senses','free');store.savePosition('six-senses',9,'free');s=store.get();if(s.orderedBook!=='five-aggregates'||s.positions['five-aggregates']!==7||s.freePositions['six-senses']!==9||s.completed.join()!=='four-truths')throw Error('Free reading altered ordered progress');if(!store.restoreBackup(original))throw Error('Restore original failed');return true}''')


def check_sailing(browser, base):
 result=[]
 for skip in [True,False]:
  context=browser.new_context(viewport={'width':768,'height':1024},reduced_motion='no-preference');page=context.new_page();page.goto(base+'play/');page.wait_for_selector('[data-action="start"]');page.locator('[data-action="start"]').click();page.wait_for_selector('#journey-dialog[open] #skip-sailing')
  if skip:
   page.screenshot(path=str(OUT/'07-sailing.png'),full_page=True);page.locator('#skip-sailing').click()
  page.wait_for_function('document.body?.dataset.playBook==="four-truths"');assert page.locator('body').get_attribute('data-play-index')=='0'
  assert json.loads(page.evaluate('(key)=>localStorage.getItem(key)',KEY))['completed']==[]
  result.append({'normalMotion':True,'skip':skip,'landsOnFirstReaderPage':'passed'});context.close()
 return result


def main():
 OUT.mkdir(parents=True, exist_ok=True)
 server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
 threading.Thread(target=server.serve_forever, daemon=True).start()
 base = f'http://127.0.0.1:{server.server_port}/'
 report = {'baseline': BASELINE, 'originalReaders': ORIGINAL, 'checks': [], 'responsive': [], 'javascriptErrors': [], 'httpErrors': [], 'physicalSafari': 'not tested', 'videoPlayback': 'not tested', 'homepageCDN': 'Existing cached Tailwind/Lucide copies; external CDN availability not tested', 'publication': 'not published; disposable local HTTP and Chromium only'}
 protected = ['index.html', 'shelf.css', 'sitemap.xml', 'robots.txt', 'googlee0c995331ec518ae.html', 'reader-controls.css', 'reader-layout.js', 'reader-restart.js']
 for name in protected:
  original = subprocess.check_output(['git', 'show', BASELINE + ':' + name], cwd=ROOT)
  assert original == (ROOT/name).read_bytes(), 'protected file changed: ' + name
 report['protectedFiles'] = protected
 for book in BOOKS:
  path=book+'/book/index.html';original=subprocess.check_output(['git','show',BASELINE+':'+path],cwd=ROOT);current=(ROOT/path).read_bytes().replace(b'<script type="module" src="../../play/collection/reader-bridge.js?v=1"></script>\n',b'');tag=b'<script type="module" src="../../play/reader-bridge.js?v=1"></script>\n';assert current.count(tag)==1 and current.replace(tag,b'')==original,path
 report['readerHTMLChanges']='Each original HTML retains v1 opt-in script; newer authorized collection inclusion is inert without collection=1; all original bytes unchanged'
 with sync_playwright() as p:
  browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
  context = browser.new_context(viewport={'width':1280, 'height':900}, reduced_motion='reduce')
  page = context.new_page()
  page.on('pageerror', lambda e: report['javascriptErrors'].append(str(e)))
  page.on('response', lambda r: report['httpErrors'].append(r.url) if r.url.startswith(base) and r.status >= 400 else None)
  page.route('https://www.youtube.com/**', lambda r:r.abort())
  for pattern, cache in [('https://cdn.tailwindcss.com/**', '/tmp/tailwind-site.js'), ('https://unpkg.com/**', '/tmp/migration-lucide.min.js')]:
   if Path(cache).exists(): page.route(pattern, lambda r, request=None, cache=cache:r.fulfill(content_type='application/javascript', body=Path(cache).read_bytes()))
  def go(path='play/'):
   page.goto(base + path, wait_until='domcontentloaded')
  def saved():
   return page.evaluate('(key)=>JSON.parse(localStorage.getItem(key))', KEY)
  def reader_ready(book):
   page.wait_for_function('(book)=>document.body?.dataset.playBook===book', arg=book)
   assert int(page.locator('body').get_attribute('data-play-total')) == ORIGINAL[book]['total']
  def pos():
   return int(page.locator('body').get_attribute('data-play-index'))
  def click_next():
   old = pos(); page.locator('#next').click(); page.wait_for_function('(old)=>Number(document.body?.dataset.playIndex)!==old', arg=old)
  def content_snapshot(book):
   data = page.evaluate('()=>({total:pages.length,scenes:scenes.length,pageData:JSON.stringify(pages),sceneData:JSON.stringify(scenes)})')
   for key in ['pageData','sceneData']:
    data[key+'Sha256'] = hashlib.sha256(data.pop(key).encode()).hexdigest()
   assert data == ORIGINAL[book], ('original narration/source/image data changed', book, data)
  def assert_no_overflow():
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'), page.url
  def screenshot(name):
   page.screenshot(path=str(OUT/name), full_page=True)

  print('Testing original readers and protected bytes',flush=True)
  # Standalone original readers must retain content, restart and source/map actions.
  for book in BOOKS:
   go(book+'/book/');page.wait_for_function('typeof showPage==="function"')
   assert not page.locator('.sz-journey-return').count();content_snapshot(book)
   first=page.locator('#position-text').inner_text();page.locator('#next').click();assert page.locator('#position-text').inner_text()!=first
   page.locator('#previous').click();assert page.locator('#position-text').inner_text()==first
   assert page.locator('.reading-links a').count() >= 2
   assert page.locator('#next').evaluate('e=>getComputedStyle(e).touchAction') == 'manipulation'
   assert_no_overflow()
  report['checks'].append('Three standalone readers preserve exact page/scene data, first/next/previous, source/map pair and touch-action')
  check_original_home(page,base)
  report['checks'].append('Original homepage map heading, 14-book shelf, real Four Truths map dialog and shelf-to-original-reader route pass')

  go();page.wait_for_selector('[data-action="start"]');screenshot('01-islands-desktop.png')
  page.evaluate('localStorage.setItem("sutrazen.unrelated.qa", "preserve")')
  page.locator('[data-action="start"]').click();reader_ready(BOOKS[0]);assert pos()==0
  content_snapshot(BOOKS[0])
  for _ in range(4):click_next()
  midway=pos();page.reload(wait_until='domcontentloaded');reader_ready(BOOKS[0]);assert pos()==midway
  assert saved()['completed']==[]
  page.locator('.reading-links a').first.click();assert '#sources' in page.url or page.locator('#sources').count()
  page.go_back(wait_until='domcontentloaded');reader_ready(BOOKS[0]);assert pos()==midway
  page.locator('.sz-journey-return').click();page.wait_for_selector('[data-action="start"]')
  assert '繼續' in page.locator('[data-action="start"]').inner_text()
  page.locator('[data-action="start"]').click();reader_ready(BOOKS[0]);assert pos()==midway
  screenshot('02-reader-desktop.png')
  report['checks'].append('Start, autosave, reload and Continue resume the same original page; opening/return/reload do not complete a book')

  print('Testing sequential full journey',flush=True)
  # Read every remaining original page with actual Next actions, then explicitly finish.
  walked=[]
  for i, book in enumerate(BOOKS):
   reader_ready(book);content_snapshot(book);total=ORIGINAL[book]['total'];initial=pos()
   while pos()<total-1:click_next()
   assert saved()['completed']==BOOKS[:i]
   assert '完成這本' in page.locator('#next').inner_text()
   screenshot(f'03-last-{book}.png')
   page.locator('#next').click();page.wait_for_url('**/play/**')
   assert saved()['completed']==BOOKS[:i+1]
   page.wait_for_selector('[data-action="continue"]');assert page.locator(f'.sz-city[data-city-stage="{i+1}"]',).count()==1;screenshot(f'04-feedback-{i+1}.png')
   walked.append({'book':book,'total':total,'actualForwardClicks':total-1-initial,'explicitFinish':True})
   if i<2:page.locator('[data-action="continue"]').click();reader_ready(BOOKS[i+1]);assert pos()==0
  assert '第一段旅程完成' in page.locator('body').inner_text()
  report['walkedReadingSteps']=walked
  report['checks'].append('All 198 original pages reachable in ordered journey; actual Next clicks and explicit finish produce three distinct city feedback stages and final first-journey completion')

  # Completed journeys still resume an in-progress re-read instead of restarting it.
  page.locator('[data-action="reread"]').click();reader_ready(BOOKS[0]);assert pos()==0
  for _ in range(5):click_next()
  assert pos()==5 and saved()['completed']==BOOKS
  page.locator('.sz-journey-return').click();page.wait_for_selector('[data-action="start"]')
  assert '繼續閱讀' in page.locator('[data-action="start"]').inner_text()
  page.locator('[data-action="start"]').click();reader_ready(BOOKS[0]);assert pos()==5
  page.reload(wait_until='domcontentloaded');reader_ready(BOOKS[0]);assert pos()==5
  while pos()<ORIGINAL[BOOKS[0]]['total']-1:click_next()
  page.locator('#next').click();page.wait_for_url('**/play/**');assert saved()['completed']==BOOKS
  report['checks'].append('After all three complete, a five-step re-read resumes from page index5 via main button and reload; finishing still counts only three')

  print('Testing five sizes and rotation',flush=True)
  # Responsive app + real reader controls and direction changes.
  for w,h in [(360,800),(844,390),(768,1024),(1024,768),(1280,900)]:
   page.set_viewport_size({'width':w,'height':h});go();assert_no_overflow()
   page.locator('[data-action="city"]').first.click();assert_no_overflow();screenshot(f'05-city-{w}x{h}.png')
   go('five-aggregates/book/?journey=ordered');reader_ready(BOOKS[1]);before=pos()
   if before:page.locator('#previous').click()
   previous=pos();page.locator('#next').click();assert pos()==previous+1
   page.set_viewport_size({'width':h,'height':w});assert pos()==previous+1;assert_no_overflow()
   assert page.locator('.sz-journey-return').is_visible()
   report['responsive'].append({'size':[w,h],'appCityReaderAndRotation':'passed'})
  page.set_viewport_size({'width':390,'height':844});go();screenshot('06-islands-mobile.png')

  print('Testing free full third-book reading',flush=True)
  # New profile: free reading has separate access and no completion/lock side effects.
  free_context=browser.new_context(viewport={'width':768,'height':1024},reduced_motion='reduce');free=free_context.new_page()
  free.goto(base+'play/');free.wait_for_selector('[data-action="free"]');free.locator('[data-action="free"]').click()
  free.locator('[data-action="read"][data-book="six-senses"]').click();free.wait_for_function('document.body?.dataset.playBook==="six-senses"')
  assert json.loads(free.evaluate('(key)=>localStorage.getItem(key)',KEY))['completed']==[]
  free.reload(wait_until='domcontentloaded');free.wait_for_function('document.body?.dataset.playBook==="six-senses"')
  while int(free.locator('body').get_attribute('data-play-index'))<ORIGINAL['six-senses']['total']-1:
   before=int(free.locator('body').get_attribute('data-play-index'));free.locator('#next').click();free.wait_for_function('(old)=>Number(document.body?.dataset.playIndex)!==old',arg=before)
  free.locator('#next').click();free.wait_for_url('**/play/**')
  assert json.loads(free.evaluate('(key)=>localStorage.getItem(key)',KEY))['completed']==[]
  free.wait_for_selector('[data-action="continue"]');free.locator('[data-action="continue"]').click()
  assert json.loads(free.evaluate('(key)=>localStorage.getItem(key)',KEY))['completed']==[]
  free.goto(base+'six-senses/book/?journey=ordered');free.wait_for_url('**/play/**');assert 'notice=locked' in free.url
  free_context.close();report['checks'].append('Free third-book full read/explicit finish does not fill progress; ordered third-book direct URL stays locked')

  print('Testing backup/reset and error states',flush=True)
  # Destructive UI asks first; actual download/upload round-trip restores only game data.
  page.locator('.sz-options summary').click()
  page.locator('[data-action="clear"]').click();assert page.locator('#journey-dialog').is_visible();page.locator('#cancel-action').click();assert saved()['completed']==BOOKS
  with page.expect_download() as download_info:page.locator('[data-action="backup"]').click()
  backup_path=OUT/'progress-backup.json';download_info.value.save_as(str(backup_path));backup_state=json.loads(backup_path.read_text());assert backup_state['completed']==BOOKS
  page.locator('[data-action="clear"]').click();page.locator('#confirm-action').click();assert saved() is None
  assert page.evaluate('localStorage.getItem("sutrazen.unrelated.qa")')=='preserve'
  page.locator('.sz-options summary').click();page.locator('#backup-file').set_input_files(str(backup_path));page.locator('#confirm-action').click();assert saved()['completed']==BOOKS
  page.locator('.sz-options summary').click();page.locator('#backup-file').set_input_files({'name':'invalid.json','mimeType':'application/json','buffer':b'{bad'});page.locator('#confirm-action').click();assert saved()['completed']==BOOKS;assert '無法讀取' in page.locator('#journey-notice').inner_text()
  report['checks'].append('Clear requires confirmation/cancel; progress download and confirmed restore work; invalid restore preserves state and unrelated localStorage survives reset')

  assert check_progress_transitions(page)
  report['checks'].append('Completed replay yields to unfinished ordered book; free positions preserve the ordered book/page and completion prefix')

  # Storage module: backup validation and reset are constrained to its own namespace.
  state_checks=page.evaluate('''async()=>{const {store}=await import('./progress.js');const before=store.get();const invalid=store.restoreBackup('{bad');if(invalid||JSON.stringify(before)!==JSON.stringify(store.get()))throw Error('Invalid restore altered state');const raw=JSON.parse(store.exportBackup());raw.settings.locale='ja';if(!store.restoreBackup(JSON.stringify(raw)))throw Error('Locale restore rejected');if(JSON.stringify(before.completed)!==JSON.stringify(store.get().completed))throw Error('Language reset progress');store.reset();if(localStorage.getItem('sutrazen.unrelated.qa')!=='preserve')throw Error('Reset cleared other namespace');return true}''')
  assert state_checks;report['checks'].append('Invalid backup preserves state, locale change preserves completion and reset affects only journey key')

  corrupt_context=browser.new_context();corrupt_context.add_init_script("if(location.pathname.startsWith('/play'))localStorage.setItem('sutrazen.play.v1','{broken')")
  corrupt=corrupt_context.new_page();corrupt.goto(base+'play/');corrupt.wait_for_selector('[data-action=\"start\"]');assert corrupt.locator('#journey-notice').is_visible();assert '無法讀取' in corrupt.locator('#journey-notice').inner_text();corrupt.locator('[data-action=\"start\"]').click();corrupt.wait_for_function('Boolean(document.body?.dataset.playBook)');
  if corrupt.locator('.play-reader-storage button').count():corrupt.locator('.play-reader-storage button').click()
  corrupt.locator('#next').click();corrupt_context.close()
  blocked_context=browser.new_context();blocked_context.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Blocked','SecurityError')}})")
  blocked=blocked_context.new_page();blocked.goto(base+'play/');blocked.wait_for_selector('[data-action=\"start\"]');assert blocked.locator('#journey-notice').is_visible();assert '無法儲存' in blocked.locator('#journey-notice').inner_text();blocked.locator('[data-action=\"start\"]').click();blocked.wait_for_function('Boolean(document.body?.dataset.playBook)');blocked.locator('.play-reader-storage button').click();blocked.locator('#next').click();blocked_context.close()
  report['checks'].append('Malformed and unavailable localStorage display an explanation and still permit reading')

  report['sailing']=check_sailing(browser,base)
  browser.close()
 assert not report['javascriptErrors'] and not report['httpErrors'], report
 (OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 server.shutdown();print(json.dumps({k:v for k,v in report.items() if k!='originalReaders'},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
