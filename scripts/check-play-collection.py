#!/usr/bin/env python3
"""Read all fourteen original books with real controls in opt-in collection mode."""
from pathlib import Path
from urllib.parse import urljoin,urlsplit,unquote
import functools,hashlib,http.server,json,re,subprocess,threading
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'docs/previews/play-collection';BASE='0f0a797';KEY='sutrazen.play.collection.v1';SIZES=[(1280,900),(390,844),(844,390),(768,1024),(1024,768)]

def catalog():
 s=(R/'play/collection/catalog.js').read_text();return json.JSONDecoder().raw_decode(s[s.index('export const CATALOG = ')+len('export const CATALOG = '):])[0]
def normalize(value,base):
 p=urlsplit(urljoin(base,value));return p.path.removesuffix('index.html'),p.fragment

def static_checks():
 books=catalog();assert len(books)==14 and len({b['id'] for b in books})==14 and [b['number'] for b in books]==list(range(1,15))
 inventory=json.loads((R/'docs/play/visual-v2/thumbnail-inventory.json').read_text())['items'];assert [b['id'] for b in books]==[i['id'] for i in inventory]
 original_keys=[]
 for book,entry in zip(books,inventory):
  name=book['id']+'/book/index.html';old=subprocess.check_output(['git','show',BASE+':'+name],cwd=R);new=(R/name).read_bytes();tag=b'<script type="module" src="../../play/collection/reader-bridge.js?v=1"></script>\n';assert new.count(tag)==1 and new.replace(tag,b'')==old,name
  path=urlsplit(urljoin('https://sutra-zen.github.io/play/collection/',book['cover'])).path;assert path==entry['currentCover']['sitePath'];raw=(R/path.lstrip('/')).read_bytes();assert hashlib.sha256(raw).hexdigest()==entry['currentCover']['sha256']
  if book['number']==1:assert book['unreadIcon'] is None
  else:
   icon=urlsplit(urljoin('https://sutra-zen.github.io/play/collection/',book['unreadIcon'])).path.lstrip('/');assert hashlib.sha256((R/icon).read_bytes()).hexdigest()==entry['originalLockedIcon']['assetSha256']
  original_keys.append(name)
 protected=['index.html','sitemap.xml','robots.txt','googlee0c995331ec518ae.html','reader-controls.css','reader-layout.js','reader-restart.js','play/app.js','play/progress.js','play/reader-bridge.js','play/reader-bridge.css','play/i18n.js','play/books.js']
 for name in protected:assert (R/name).read_bytes()==subprocess.check_output(['git','show',BASE+':'+name],cwd=R),name
 changed=subprocess.check_output(['git','diff','--name-only',BASE],cwd=R,text=True).splitlines()
 for name in changed:
  if any(name.startswith(b['id']+'/') for b in books):assert name in original_keys,'unapproved original book change: '+name
 return {'baseline':BASE,'catalogBooks':14,'originalReaderChanges':'Each HTML differs only by one opt-in collection script; old journey module retained','originalCoversAndUnreadIconHashes':'14 covers and 13 old icons match inventory; book1 has no original locked icon','protectedOriginalSiteAndV1':'passed','protectedPaths':protected}

class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
 def copyfile(self,src,dst):
  try:super().copyfile(src,dst)
  except (BrokenPipeError,ConnectionResetError):pass

def check_storage_errors(browser,base):
 results=[]
 for mode in ['corrupt','unavailable']:
  ctx=browser.new_context(reduced_motion='reduce')
  if mode=='corrupt':ctx.add_init_script("if(location.pathname.endsWith('shelf.html'))localStorage.setItem('sutrazen.play.collection.v1','{bad')")
  else:ctx.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Blocked','SecurityError')}})")
  p=ctx.new_page();p.goto(base+'play/visual-v2/shelf.html');p.wait_for_selector('[data-book-card]');assert p.locator('#collection-notice').is_visible();p.locator('[data-collection-read="four-truths"]').click();p.wait_for_function('document.body?.dataset.collectionBook==="four-truths"')
  if p.locator('.collection-reader-storage button').count():p.locator('.collection-reader-storage button').click()
  p.locator('#next').click();p.wait_for_function('document.body?.dataset.collectionIndex==="1"');results.append({'case':mode,'noticeAndReading':'passed'});ctx.close()
 return results

def check_v1_coexistence(browser,base):
 ctx=browser.new_context(reduced_motion='reduce');p=ctx.new_page();p.goto(base+'play/');p.evaluate("localStorage.setItem('sutrazen.play.collection.v1','preserve-collection')");p.locator('[data-action="start"]').click();p.wait_for_function('document.body?.dataset.playBook==="four-truths"');assert not p.locator('.collection-reader-return').count()
 for i in range(28):p.locator('#next').click();p.wait_for_function('(n)=>Number(document.body?.dataset.playIndex)===n',arg=i+1)
 p.locator('#next').click();p.wait_for_url('**/play/**');p.wait_for_selector('[data-action="continue"]');assert p.evaluate("JSON.parse(localStorage.getItem('sutrazen.play.v1')).completed.join()")=='four-truths';assert p.evaluate("localStorage.getItem('sutrazen.play.collection.v1')")=='preserve-collection';ctx.close();return 'Original29-step v1 journey succeeds and leaves collection key unchanged'

def main():
 O.mkdir(parents=True,exist_ok=True);report=static_checks();original=json.loads((O/'baseline-reader-data.json').read_text())['books'];books=catalog();ids=[b['id'] for b in books]
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/';report.update({'checks':[],'readers':[],'viewports':[],'javascriptErrors':[],'httpErrors':[],'physicalSafari':'not tested','publication':'not published; local HTTP only'})
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);context=browser.new_context(viewport={'width':1280,'height':900},reduced_motion='reduce');page=context.new_page();page.on('pageerror',lambda e:report['javascriptErrors'].append(str(e)));page.on('response',lambda r:report['httpErrors'].append(r.url) if r.url.startswith(base) and r.status>=400 else None);page.route('https://www.youtube.com/**',lambda r:r.abort())
  def go(path):page.goto(base+path,wait_until='domcontentloaded')
  def state():return page.evaluate('(key)=>JSON.parse(localStorage.getItem(key))',KEY)
  def reader_ready(book):
   page.wait_for_function('(book)=>document.body?.dataset.collectionBook===book',arg=book);assert int(page.locator('body').get_attribute('data-collection-total'))==original[book]['total']
  def pos():return int(page.locator('body').get_attribute('data-collection-index'))
  def next_step():
   before=pos();page.locator('#next').click();page.wait_for_function('(n)=>Number(document.body?.dataset.collectionIndex)!==n',arg=before)
  def snapshot(book):
   data=page.evaluate("()=>({kind:typeof BOOK!=='undefined'?'BOOK':'pages/scenes',raw:typeof BOOK!=='undefined'?JSON.stringify(BOOK):JSON.stringify({pages,scenes})})");assert data['kind']==original[book]['kind'] and hashlib.sha256(data['raw'].encode()).hexdigest()==original[book]['originalDataSha256'],book
  def no_overflow():
   page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),{'url':page.url,'viewport':page.viewport_size}
  def screen(name):page.screenshot(path=str(O/name),full_page=True)
  # Standalone source books have no collection UI or new save side effects.
  for book in ids:
   go(book+'/book/');page.wait_for_function('typeof window.showPage==="function"');assert page.locator('.collection-reader-return').count()==0;snapshot(book);first=page.locator('#position-text').inner_text();page.locator('#next').click();assert page.locator('#position-text').inner_text()!=first;page.locator('#previous').click();assert page.locator('#position-text').inner_text()==first;assert state() is None
  report['checks'].append('All14 standalone readers preserve original runtime content hashes and next/previous behavior; no collection save without opt-in')
  go('play/visual-v2/shelf.html');page.evaluate("localStorage.setItem('sutrazen.play.v1','qa-preserve-v1');localStorage.setItem('sutrazen.unrelated.qa','preserve')")
  page.wait_for_selector('[data-book-card="seven-factors"]');assert page.locator('[data-book-card]').count()==14;assert '0／14' in page.locator('#collection-count').inner_text();assert page.locator('.earned-cover').count()==0;assert page.locator('.achievement-lock').count()==14;screen('01-unearned-shelf-desktop.png')
  order=['seven-factors']+[id for id in ids if id!='seven-factors'];completed=[]
  assert all(book['totalSteps']==original[book['id']]['total'] for book in books)
  for number,book in enumerate(order):
   page.locator('[data-collection-read="'+book+'"]').click();reader_ready(book);snapshot(book);assert state()['completed']==completed
   initial=pos();assert initial==0
   if number==0:
    for _ in range(5):next_step()
    page.reload(wait_until='domcontentloaded');reader_ready(book);assert pos()==5
    page.locator('.reading-links a').first.click();page.wait_for_load_state('domcontentloaded');page.go_back(wait_until='domcontentloaded');reader_ready(book);assert pos()==5
    page.locator('.collection-reader-return').click();page.wait_for_selector('[data-book-card="'+book+'"]');assert page.locator('[data-book-card="'+book+'"]').get_attribute('data-earned')=='false';assert state()['completed']==[]
    page.locator('[data-collection-read="'+book+'"]').click();reader_ready(book);assert pos()==5;screen('02-reader-resume-desktop.png')
   total=original[book]['total']
   while pos()<total-1:next_step()
   assert state()['completed']==completed
   assert '完成這本' in page.locator('#next').inner_text();assert page.locator('#next').evaluate('e=>getComputedStyle(e).touchAction')=='manipulation'
   page.locator('#next').click();page.wait_for_url('**/play/visual-v2/shelf.html**');page.wait_for_selector('[data-book-card="'+book+'"]');completed.append(book);assert state()['completed']==completed
   assert page.locator('[data-book-card="'+book+'"]').get_attribute('data-earned')=='true';assert page.locator('[data-book-card="'+book+'"] .earned-cover').count()==1
   assert page.locator('.earned-cover').count()==number+1;assert f'{number+1}／14' in page.locator('#collection-count').inner_text()
   report['readers'].append({'id':book,'totalOriginalSteps':total,'actualForwardClicks':total-1,'completedByExplicitLastAction':True,'originalRuntimeDataHash':'unchanged'})
   if number==0:screen('03-first-collected-seven-factors.png')
   print(book,total,'real steps and explicit finish passed',flush=True)
  assert len(state()['completed'])==14 and page.locator('.earned-cover').count()==14;assert page.locator('.achievement-lock').count()==0;screen('04-all-fourteen-collected.png')
  report['checks'].append('1192 original reading steps traversed by actual Next buttons, starting with book14 proves arbitrary collection order; no book completes before explicit last action; each cover appears only afterwards')
  # An interrupted re-read resumes; explicit re-completion never increments fourteen.
  page.locator('[data-collection-read="seven-factors"]').click();reader_ready('seven-factors');assert pos()==0
  for _ in range(6):next_step()
  page.locator('.collection-reader-return').click();page.wait_for_selector('[data-book-card="seven-factors"]');page.locator('[data-collection-read="seven-factors"]').click();reader_ready('seven-factors');assert pos()==6
  page.reload(wait_until='domcontentloaded');reader_ready('seven-factors');assert pos()==6
  while pos()<original['seven-factors']['total']-1:next_step()
  page.locator('#next').click();page.wait_for_url('**/play/visual-v2/shelf.html**');assert len(state()['completed'])==14
  report['checks'].append('Completed-book re-read returns through shelf to reading step6 and reload preserves it; re-finishing does not double-count or create extra covers')
  # Every new reader header/control works in all required orientations.
  for w,h in SIZES:
   page.set_viewport_size({'width':w,'height':h});go('play/visual-v2/shelf.html');page.wait_for_selector('[data-book-card]');no_overflow()
   if w in [390,768]:screen(f'05-shelf-{w}x{h}.png')
   for book in ids:
    go(book+'/book/?collection=1&collectionPage=0');reader_ready(book);next_step();assert pos()==1
    page.set_viewport_size({'width':h,'height':w});assert pos()==1;no_overflow();assert page.locator('.collection-reader-return').is_visible()
    page.set_viewport_size({'width':w,'height':h});page.locator('#previous').click();assert pos()==0
   report['viewports'].append({'size':[w,h],'allFourteenReaderControlsAndRotation':'passed','shelfOverflow':'none'})
  go('play/visual-v2/shelf.html');assert page.evaluate("localStorage.getItem('sutrazen.play.v1')==='qa-preserve-v1'&&localStorage.getItem('sutrazen.unrelated.qa')==='preserve'")
  # Actual backup/reset/restore UI affects only the collection namespace.
  page.locator('details.collection-options summary').click();page.locator('[data-collection-reset]').click();page.locator('#collection-cancel').click();assert len(state()['completed'])==14
  with page.expect_download() as info:page.locator('[data-collection-backup]').click()
  backup=O/'test-progress-backup.json';info.value.save_as(str(backup));assert len(json.loads(backup.read_text())['completed'])==14
  page.locator('[data-collection-reset]').click();page.locator('#collection-confirm').click();assert state() is None or not state()['completed'];assert page.locator('.earned-cover').count()==0
  assert page.evaluate("localStorage.getItem('sutrazen.play.v1')==='qa-preserve-v1'&&localStorage.getItem('sutrazen.unrelated.qa')==='preserve'")
  page.locator('details.collection-options summary').click();page.locator('#collection-import').set_input_files(str(backup));page.locator('#collection-confirm').click();assert len(state()['completed'])==14 and page.locator('.earned-cover').count()==14
  report['checks'].append('Confirmed reset/cancel and real JSON backup/restore preserve v1 and unrelated storage; restored fourteen covers are derived from the same IDs')
  # Merely using a chapter menu to reach the last step never earns a fresh book.
  fresh=browser.new_context(reduced_motion='reduce');q=fresh.new_page();q.goto(base+'four-truths/book/?collection=1');q.wait_for_function('document.body?.dataset.collectionBook==="four-truths"');q.locator('#page-select').select_option(index=q.locator('#page-select option').count()-1);assert '完成這本' in q.locator('#next').inner_text();assert q.evaluate('(key)=>JSON.parse(localStorage.getItem(key)).completed.length',KEY)==0
  q.reload(wait_until='domcontentloaded');q.wait_for_function('document.body?.dataset.collectionBook==="four-truths"');assert q.evaluate('(key)=>JSON.parse(localStorage.getItem(key)).completed.length',KEY)==0;q.locator('.collection-reader-return').click();q.wait_for_selector('[data-book-card]');assert q.locator('.earned-cover').count()==0;fresh.close()
  report['checks'].append('Menu jump, arrival at last page, reload and return-to-shelf do not earn a book')
  report['storageErrors']=check_storage_errors(browser,base)
  report['v1Coexistence']=check_v1_coexistence(browser,base)
  browser.close()
 server.shutdown();assert not report['javascriptErrors'] and not report['httpErrors'],report
 (O/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
