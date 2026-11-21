#!/usr/bin/env python3
"""Read-only visual-v2 smoke tests; never writes v1 progress or publishes."""
from pathlib import Path
import functools,hashlib,http.server,json,subprocess,threading
from urllib.parse import urlsplit,unquote
from playwright.sync_api import sync_playwright
from PIL import Image

R=Path(__file__).resolve().parents[1]
O=R/'docs/previews/play-visual-v2'
BASE='5056201'
SIZES=[(1280,900),(390,844),(844,390),(768,1024),(1024,768)]

class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def copyfile(self,src,dst):
  try:super().copyfile(src,dst)
  except (BrokenPipeError,ConnectionResetError):pass

def static_checks():
 tracked=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],cwd=R,text=True).splitlines()
 protected=[p for p in tracked if p.startswith(('play/','four-truths/','five-aggregates/','six-senses/','docs/seo/')) or p in ['AGENTS.md','index.html','shelf.css','sitemap.xml','robots.txt','googlee0c995331ec518ae.html','reader-controls.css','reader-layout.js','reader-restart.js']]
 for name in protected:
  assert (R/name).read_bytes()==subprocess.check_output(['git','show',BASE+':'+name],cwd=R),name
 inv=json.loads((R/'docs/play/visual-v2/thumbnail-inventory.json').read_text())
 assert len(inv['items'])==14 and [x['number'] for x in inv['items']]==list(range(1,15))
 original=subprocess.check_output(['git','show',inv['originalShelfCommit']+':'+inv['originalShelfSource']],cwd=R).decode()
 cover_report=[]
 for row in inv['items']:
  assert row['originalPublicReader']['available'] is True
  reader_path=row['originalPublicReader']['sitePath'].lstrip('/');assert (R/(reader_path+'index.html' if reader_path.endswith('/') else reader_path)).is_file()
  cover=row['currentCover'];raw=(R/cover['sitePath'].lstrip('/')).read_bytes()
  assert len(raw)==cover['bytes'] and hashlib.sha256(raw).hexdigest()==cover['sha256']
  icon=row['originalLockedIcon']
  if row['number']==1:assert icon['kind']=='absent'
  else:
   assert icon['kind']=='inline-svg';raw=(R/icon['assetPath']).read_bytes();assert len(raw)==icon['bytes'] and hashlib.sha256(raw).hexdigest()==icon['assetSha256']
   fragment=raw.decode().removesuffix('\n').replace(' xmlns="http://www.w3.org/2000/svg"','',1)
   assert fragment in original and hashlib.sha256(fragment.encode()).hexdigest()==icon['sourceFragmentSha256']
  cover_report.append({'number':row['number'],'id':row['id'],'originalIcon':icon['kind'],'coverHash':'passed','originalReader':'available'})
 asset_report=[]
 for path in [R/'play/visual-v2/assets'/name for name in ['archipelago-concept.png','city-concept.png','garden-growth-concept.png','kitten-boat-concept.png']]:
  with Image.open(path) as im:asset_report.append({'file':path.name,'dimensions':list(im.size),'mode':im.mode,'alphaExtrema':list(im.getchannel('A').getextrema()) if 'A' in im.getbands() else None,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
 assert len(asset_report)==4
 return {'assetScope':'Four earlier concepts retained as historical assets; active network/rowboat assets checked by check-play-network.py','conceptImages':asset_report,'protectedFiles':len(protected),'baseline':BASE,'allV1PlayAndFirstThreeBookFiles':'byte-for-byte unchanged','thumbnailInventory':cover_report,'originalFirstBookIcon':'No locked icon existed; any wheel is explicitly a new UI marker'}

def main():
 O.mkdir(parents=True,exist_ok=True);report=static_checks();report.update({'sizes':[],'javascriptErrors':[],'httpErrors':[],'physicalSafari':'not tested','publication':'not published; local HTTP prototype only','assets':'Generated watercolor concepts, not author-approved final artwork'})
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  context=browser.new_context(reduced_motion='reduce');page=context.new_page();page.on('pageerror',lambda e:report['javascriptErrors'].append(str(e)));page.on('response',lambda r:report['httpErrors'].append(r.url) if r.url.startswith(base) and r.status>=400 else None)
  context.add_init_script("""(()=>{const raw=Storage.prototype.setItem;raw.call(localStorage,'sutrazen.play.v1','visual-qa-preserve');raw.call(localStorage,'sutrazen.qa.unrelated','preserve');window.__qaStorageWrites=[];for(const name of ['setItem','removeItem','clear']){const original=Storage.prototype[name];Storage.prototype[name]=function(...args){if(this===localStorage)window.__qaStorageWrites.push({method:name,args});return original.apply(this,args)}}})();""")
  for w,h in SIZES:
   page.set_viewport_size({'width':w,'height':h});page.goto(base+'play/visual-v2/',wait_until='domcontentloaded');page.evaluate('()=>document.fonts.ready');page.locator('[data-view="map"]').click()
   page.wait_for_selector('[data-island="14"]');page.locator('.scene-art').evaluate('e=>e.decode()');page.locator('.map-boat img').evaluate('e=>e.decode()');assert page.locator('.island-pin').count()==14
   config=page.evaluate("async()=>{const d=await import('./data.js');return {islands:d.ISLANDS,spots:d.CITY_SPOTS}}")
   assert [r['id'] for r in config['islands']]==[r['id'] for r in json.loads((R/'docs/play/visual-v2/thumbnail-inventory.json').read_text())['items']]
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
   assert '可左右／上下滑動' in page.locator('#scene-footer').inner_text()
   page.screenshot(path=str(O/f'map-{w}x{h}.png'),full_page=True)
   for n in [1,2,3]:
    page.locator('[data-locate="'+str(n)+'"]').click();page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
    assert page.locator('.island-pin[data-island="'+str(n)+'"]').evaluate('e=>{const a=e.getBoundingClientRect(),b=e.closest(".scene-scroll").getBoundingClientRect();return a.left+a.width/2>b.left&&a.left+a.width/2<b.right&&a.top+a.height/2>b.top&&a.top+a.height/2<b.bottom}')
   # All island labels remain interactive, including the eleven future game routes.
   for row in config['islands']:
    page.locator('.island-pin[data-island="'+str(row['n'])+'"]').click();dialog=page.locator('#inspect-dialog');assert dialog.is_visible();assert dialog.locator('#inspect-title').inner_text()==row['title']
    if row['n']>3:
     assert '已在原網站公開閱讀' in dialog.inner_text() and '不表示它尚未上架' in dialog.inner_text()
    for href in dialog.locator('a').evaluate_all('els=>els.map(e=>e.href)'):
     path=unquote(urlsplit(href).path).lstrip('/');target=R/(path+'index.html' if path.endswith('/') else path);assert target.is_file(),href
    dialog.locator('.close-dialog').click()
   # Toggle the relation overlay without changing the primary route or stored progress.
   page.locator('[data-toggle="relations"]').click();assert page.locator('[data-toggle="relations"]').get_attribute('aria-pressed')=='true'
   page.locator('[data-view="city"]').click();assert page.locator('.city-spot').count()==len(config['spots'])
   for spot in config['spots']:
    page.locator('[data-spot="'+spot['id']+'"]').click();dialog=page.locator('#inspect-dialog');assert dialog.locator('#inspect-title').inner_text()==spot['title'];assert spot['copy'] in dialog.inner_text();assert 'SN 35.245' in dialog.inner_text();assert dialog.locator('a[href="../sources.html"]').count()==1;dialog.locator('.close-dialog').click()
   assert page.locator('a[href="../sources.html"]').count()>=1
   page.locator('[data-toggle="spots"]').click();assert page.locator('.city-spot').count()==0
   page.locator('[data-toggle="spots"]').click();assert page.locator('.city-spot').count()==len(config['spots'])
   states=[]
   for n in [0,1,2,3]:
    page.locator('[data-stage="'+str(n)+'"]').click();assert page.locator('[data-board="city"]').evaluate('(e,n)=>e.classList.contains("stage-"+n)',n)
    growth=float(page.locator('.garden-growth').evaluate('e=>getComputedStyle(e).opacity'));lights=float(page.locator('.gate-light').first.evaluate('e=>getComputedStyle(e).opacity'))
    assert growth==(1 if n>=2 else 0) and lights==(1 if n==3 else 0),(n,growth,lights)
    if w==1280 and n in [1,2]:page.screenshot(path=str(O/f'city-stage-{n}-1280x900.png'),full_page=True)
    states.append(n)
   page.locator('.scene-art').evaluate('e=>e.decode()');page.locator('.garden-growth').evaluate('e=>e.decode()');page.screenshot(path=str(O/f'city-{w}x{h}.png'),full_page=True)
   page.locator('[data-toggle="zoom"]').click();assert page.locator('#scene-host.is-overview').count()==1;assert page.locator('.scene-scroll').evaluate('e=>e.scrollWidth<=e.clientWidth+2&&e.scrollHeight<=e.clientHeight+2');page.locator('[data-toggle="zoom"]').click()
   page.locator('[data-view="celebrate"]').click();assert page.locator('[data-board="city"].is-celebration.stage-3').count()==1;assert '第一段旅程完成' in page.locator('#scene-footer').inner_text()
   page.locator('.return-boat img').evaluate('e=>e.decode()');page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
   assert page.locator('.return-boat').evaluate('e=>{const a=e.getBoundingClientRect(),b=e.closest(".scene-scroll").getBoundingClientRect();return a.left>=b.left-2&&a.right<=b.right+2&&a.top>=b.top-2&&a.bottom<=b.bottom+2}')
   assert page.locator('[data-continue]').is_visible()
   if w in [1280,390]:page.screenshot(path=str(O/f'celebrate-{w}x{h}.png'),full_page=True)
   page.locator('[data-continue]').click();assert page.locator('[data-board="map"]').count()==1
   page.locator('[data-toggle="zoom"]').click();assert page.locator('[data-toggle="zoom"]').get_attribute('aria-pressed')=='true'
   assert page.locator('.scene-scroll').evaluate('e=>e.scrollWidth<=e.clientWidth+2&&e.scrollHeight<=e.clientHeight+2')
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
   assert page.evaluate("localStorage.getItem('sutrazen.play.v1')==='visual-qa-preserve' && localStorage.getItem('sutrazen.qa.unrelated')==='preserve' && window.__qaStorageWrites.length===0")
   report['sizes'].append({'size':[w,h],'islandDialogs':14,'cityHotspots':len(config['spots']),'tabsAndFeedback':'passed','simulationStages':states,'flowerGrowthAndGateLights':'stages0/1 no growth,2 growth,3 growth+lights','locateButtons':3,'overviewFit':'no internal clipping','celebrationBoatAndContinue':'whole boat frame within scene scroll viewport; story and continue visible','storageWrites':0,'overflow':'none outside native scene pan'})
  browser.close()
 server.shutdown();assert not report['javascriptErrors'] and not report['httpErrors'],report
 (O/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
