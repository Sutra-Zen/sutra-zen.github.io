#!/usr/bin/env python3
"""Targeted art-direction checks; core1192-step coverage remains in prior reports."""
from pathlib import Path
import functools,http.server,json,re,subprocess,threading
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'docs/previews/play-art-directions';BASE='dedc066';SIZES=[(1280,900),(390,844),(844,390),(768,1024),(1024,768)]

class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
 def copyfile(self,s,d):
  try:super().copyfile(s,d)
  except (BrokenPipeError,ConnectionResetError):pass

def unchanged_core():
 tracked=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],cwd=R,text=True).splitlines();protected=[f for f in tracked if f.startswith('play/collection/') or f.endswith('/book/index.html') or f in ['index.html','AGENTS.md','sitemap.xml','robots.txt','googlee0c995331ec518ae.html','play/visual-v2/network-data.js','play/progress.js','play/reader-bridge.js','play/app.js','reader-controls.css','reader-layout.js','reader-restart.js']]
 for f in protected:assert (R/f).read_bytes()==subprocess.check_output(['git','show',BASE+':'+f],cwd=R),f
 old=subprocess.check_output(['git','show',BASE+':play/visual-v2/shelf.js'],cwd=R,text=True);new=(R/'play/visual-v2/shelf.js').read_text();assert old[old.index('function read('):]==new[new.index('function read('):],'shelf behavior handlers changed'
 return {'baseline':BASE,'protectedFiles':len(protected),'coreAndReaderBytes':'unchanged','shelfBehaviorHandlers':'unchanged','priorCompleteReadingCoverage':'docs/previews/play-collection/validation.json (1192 actual reading steps); no full repeat for art-only changes'}

def actual_completion_smoke(browser,base):
 ctx=browser.new_context(viewport={'width':1280,'height':900},reduced_motion='reduce');p=ctx.new_page();p.goto(base+'play/visual-v2/shelf.html');p.wait_for_selector('[data-collection-read="four-truths"]');p.evaluate("localStorage.setItem('sutrazen.play.v1','preserve-v1')");assert p.locator('.earned-cover').count()==0;p.locator('[data-collection-read="four-truths"]').click();p.wait_for_function('document.body?.dataset.collectionBook==="four-truths"')
 for index in range(28):
  p.locator('#next').click();p.wait_for_function('(i)=>document.body?.dataset.collectionIndex===String(i)',arg=index+1)
  if index==4:p.reload(wait_until='domcontentloaded');p.wait_for_function('document.body?.dataset.collectionIndex==="5"')
 assert p.evaluate("JSON.parse(localStorage.getItem('sutrazen.play.collection.v1')).completed.length") == 0
 p.locator('#next').click();p.wait_for_url('**/play/visual-v2/shelf.html**');p.wait_for_selector('.earned-cover');assert p.locator('.earned-cover').count()==1;assert p.locator('[data-book-card="four-truths"]').get_attribute('data-earned')=='true';assert '1／14' in p.locator('#collection-count').inner_text();assert p.evaluate("localStorage.getItem('sutrazen.play.v1')")=='preserve-v1';p.locator('.earned-cover').evaluate('e=>e.decode()');p.screenshot(path=str(O/'shelf-actual-first-completion-1280x900.png'),full_page=True);ctx.close();return 'Actual29-step Four Truths read (reload at step5), explicit finish changes only its real cover and count1/14; old journey key preserved'

def main():
 O.mkdir(parents=True,exist_ok=True);report=unchanged_core();report.update({'maps':[],'cities':[],'shelves':[],'javascriptErrors':[],'httpErrors':[],'physicalSafari':'not tested','publication':'not published; art-direction local previews only','shelfVisualFixtures':'Valid disposable browser backup states are used to render unread/one/all14; these are QA fixtures, not fake achievement controls in product'})
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);ctx=b.new_context(reduced_motion='reduce');page=ctx.new_page();page.on('pageerror',lambda e:report['javascriptErrors'].append(str(e)));page.on('response',lambda r:report['httpErrors'].append(r.url) if r.url.startswith(base) and r.status>=400 else None)
  ctx.add_init_script("localStorage.setItem('sutrazen.play.v1','art-qa-preserve-v1')")
  for w,h in SIZES:
   page.set_viewport_size({'width':w,'height':h});page.goto(base+'play/visual-v2/',wait_until='domcontentloaded');page.wait_for_selector('.network-island')
   assert page.locator('.network-island').count()==32
   assert '相關內容大陸' not in page.locator('#scene-host').inner_text()
   nodes=page.evaluate("async()=>{const d=await import('./network-data.js');return Object.fromEntries(d.NODES.map(n=>[n.id,n]))}")
   for style in ['terrain','world']:
    page.locator('button[data-map-style="'+style+'"]').click();page.wait_for_selector('.network-world[data-map-style="'+style+'"]');page.locator('[data-net-clear]').click();page.locator('#scene-host img').evaluate_all('els=>Promise.all(els.map(i=>i.decode()))')
    assert page.locator('.network-island').count()==32 and page.locator('[data-node="related-overview"]').count()==0
    edge_ids=page.locator('.network-edge').evaluate_all('els=>els.map(e=>e.dataset.edge)');assert len(edge_ids)==46 and len(set(edge_ids))==46
    overlaps=page.locator('.network-island').evaluate_all('els=>{const a=els.map(e=>({id:e.dataset.instance,b:e.getBoundingClientRect()}));return a.flatMap(x=>a.filter(y=>x.id!==y.id&&x.b.x+x.b.width/2>y.b.left&&x.b.x+x.b.width/2<y.b.right&&x.b.y+x.b.height/2>y.b.top&&x.b.y+x.b.height/2<y.b.bottom).map(y=>[x.id,y.id]))}');assert not overlaps,overlaps
    assert '相關內容大陸' not in page.locator('#scene-host').inner_text()
    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
    page.screenshot(path=str(O/f'map-{style}-{w}x{h}.png'),full_page=True)
    instances=page.locator('.network-island').evaluate_all('els=>els.map(e=>({id:e.dataset.instance,node:e.dataset.node}))')
    for instance in instances:
     page.locator('.network-island[data-instance="'+instance['id']+'"]').click();dialog=page.locator('#inspect-dialog');assert dialog.locator('#inspect-title').inner_text()==nodes[instance['node']]['label'];assert dialog.locator('[data-network-guide]').get_attribute('href')==nodes[instance['node']]['guide'];assert dialog.locator('[data-network-reader]').get_attribute('href').startswith(nodes[instance['node']]['reader']);dialog.locator('.close-dialog').click();assert page.locator('.network-world').get_attribute('data-map-style')==style
    report['maps'].append({'size':[w,h],'style':style,'nativeNodeDialogs':32,'originalEdgeIds':46,'centerOverlaps':0,'linksAndStyleRetention':'passed','removedLiteralContinentLabel':True})
   # New top-down castle keeps the exact source roles and six gates; no grid overlay.
   page.locator('[data-view="city"]').click();page.wait_for_selector('.city-tactics-board[data-city-view="top-down"]');page.locator('#scene-host img').evaluate_all('els=>Promise.all(els.map(i=>i.decode()))')
   assert page.locator('.tactics-gate-hotspot').count()==6 and page.locator('.city-spot').count()==13
   assert page.locator('.tactics-grid,.city-grid,[data-tactical-grid]').count()==0
   spot_ids=page.locator('.city-spot').evaluate_all('els=>els.map(e=>e.dataset.spot)')
   for spot in spot_ids:
    page.locator('.city-spot[data-spot="'+spot+'"]').click();dialog=page.locator('#inspect-dialog');assert 'SN 35.245' in dialog.inner_text();assert dialog.locator('a[href="../sources.html"]').count()==1;dialog.locator('.close-dialog').click()
   for stage in [0,1,2,3]:
    page.locator('[data-stage="'+str(stage)+'"]').click();assert page.locator('.city-tactics-board').get_attribute('data-city-stage')==str(stage)
    assert (float(page.locator('.tactics-road-light').evaluate('e=>getComputedStyle(e).opacity'))==0) if stage==0 else (float(page.locator('.tactics-road-light').evaluate('e=>getComputedStyle(e).opacity'))>0)
    assert float(page.locator('.tactics-plaza-light').evaluate('e=>getComputedStyle(e).opacity'))==(0 if stage<2 else 1)
    assert page.locator('.tactics-gate-light').evaluate_all('(els,n)=>els.every(e=>Number(getComputedStyle(e).opacity)===(n===3?1:0))',stage)
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
   if w in [1280,390,1024]:page.screenshot(path=str(O/f'city-topdown-{w}x{h}.png'),full_page=True)
   assert page.evaluate("localStorage.getItem('sutrazen.play.v1')==='art-qa-preserve-v1'&&localStorage.getItem('sutrazen.play.collection.v1')===null")
   report['cities'].append({'size':[w,h],'gates':6,'nativeSourceHotspots':13,'progressStages':[0,1,2,3],'noGridOverlay':'DOM and visual screenshot checked','progressStorage':'unchanged'})
  report['actualCompletionSmoke']=actual_completion_smoke(b,base)
  # Shelf visual states use valid backup fixtures in this disposable browser only.
  catalog=page.evaluate("async()=>{const d=await import('../collection/catalog.js');return d.CATALOG}")
  for w,h in SIZES:
   page.set_viewport_size({'width':w,'height':h});page.goto(base+'play/visual-v2/shelf.html',wait_until='domcontentloaded');page.wait_for_selector('[data-book-card]')
   for name,completed in [('unearned',[]),('one-earned',[catalog[0]['id']]),('all-earned',[x['id'] for x in catalog])]:
    state={'version':1,'activeBook':catalog[0]['id'],'positions':{catalog[0]['id']:6} if completed else {},'completed':completed}
    assert page.evaluate("async(state)=>{const {store}=await import('../collection/store.js');return store.restoreBackup(JSON.stringify(state))}",state)
    assert page.locator('[data-book-card]').count()==14 and page.locator('.earned-cover').count()==len(completed) and page.locator('.achievement-lock').count()==14-len(completed)
    assert page.locator('.collection-book-art').evaluate_all('els=>els.every(e=>{const r=e.getBoundingClientRect();return r.height/r.width>1.3})')
    assert page.locator('.collection-book-title').evaluate_all('els=>els.every(e=>{const a=e.getBoundingClientRect(),b=e.closest(".collection-book-art").getBoundingClientRect();return a.left>=b.left-1&&a.right<=b.right+1&&a.top>=b.top-1&&a.bottom<=b.bottom+1})')
    assert page.locator('.collection-book-status').evaluate_all('els=>els.every(e=>getComputedStyle(e).backgroundColor!=="rgba(0, 0, 0, 0)"&&getComputedStyle(e).textShadow==="none")')
    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
    page.locator('.earned-cover').evaluate_all('els=>Promise.all(els.map(i=>i.decode()))')
    if w in [1280,390,768]:page.screenshot(path=str(O/f'shelf-{name}-{w}x{h}.png'),full_page=True)
    report['shelves'].append({'size':[w,h],'fixture':name,'completedCovers':len(completed),'portraitCoverAspect':'height/width >1.3','titlesInsideCover':True,'overflow':'none'})
  # The same native reading action must still resume the valid bookmark after the restyle.
  page.set_viewport_size({'width':390,'height':844});state={'version':1,'activeBook':'four-truths','positions':{'four-truths':6},'completed':['four-truths']};assert page.evaluate("async(s)=>{const {store}=await import('../collection/store.js');return store.restoreBackup(JSON.stringify(s))}",state)
  page.locator('[data-collection-read="four-truths"]').click();page.wait_for_function('document.body?.dataset.collectionBook==="four-truths"');assert page.locator('body').get_attribute('data-collection-index')=='6';page.locator('#next').click();page.wait_for_function('document.body?.dataset.collectionIndex==="7"');page.reload(wait_until='domcontentloaded');page.wait_for_function('document.body?.dataset.collectionIndex==="7"');page.locator('.collection-reader-return').click();page.wait_for_selector('[data-book-card]');assert page.locator('.earned-cover').count()==1
  assert page.evaluate("localStorage.getItem('sutrazen.play.v1')==='art-qa-preserve-v1'")
  report['shelfResume']='Native cover opens completed-book bookmark6, Next7 and reload7; return retains1earned cover and leaves old journey key unchanged'
  b.close()
 server.shutdown();assert not report['javascriptErrors'] and not report['httpErrors'];(O/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
