#!/usr/bin/env python3
"""Inspect the continent/mountain scene while preserving all original reading data."""
from pathlib import Path
import functools,hashlib,http.server,importlib.util,json,re,threading
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'docs/previews/play-continent';SIZES=[(1280,900),(390,844),(844,390),(768,1024),(1024,768)]
def load(name):
 spec=importlib.util.spec_from_file_location(name,str(R/'scripts'/name));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
N=load('check-play-network.py');C=load('check-play-collection.py')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
 def copyfile(self,s,d):
  try:super().copyfile(s,d)
  except (BrokenPipeError,ConnectionResetError):pass

def main():
 O.mkdir(parents=True,exist_ok=True);report={'originalProtection':C.static_checks(),'sourceNetwork':N.static_checks(),'sizes':[],'javascriptErrors':[],'httpErrors':[],'physicalSafari':'not tested','publication':'not published; local HTTP only'}
 assets=[]
 for name in ['continent-concept.png','mountain-atlas-concept.png','library-concept.png']:
  p=R/'play/visual-v2/assets'/name
  with Image.open(p) as im:assets.append({'file':name,'size':list(im.size),'mode':im.mode,'alphaExtrema':list(im.getchannel('A').getextrema()) if 'A' in im.getbands() else None,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 report['newConceptAssets']=assets
 s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=s.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{s.server_port}/'
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);ctx=b.new_context(reduced_motion='reduce');ctx.add_init_script("""(()=>{const native=Storage.prototype.setItem;native.call(localStorage,'sutrazen.play.v1','preserve-v1');native.call(localStorage,'sutrazen.play.collection.v1',JSON.stringify({version:1,activeBook:'four-truths',positions:{},completed:[]}));window.__writes=[];for(const method of ['setItem','removeItem','clear']){const fn=Storage.prototype[method];Storage.prototype[method]=function(...args){if(this===localStorage)window.__writes.push({method,args});return fn.apply(this,args)}}})();""");page=ctx.new_page();page.on('pageerror',lambda e:report['javascriptErrors'].append(str(e)));page.on('response',lambda r:report['httpErrors'].append(r.url) if r.url.startswith(base) and r.status>=400 else None)
  for w,h in SIZES:
   page.set_viewport_size({'width':w,'height':h});page.goto(base+'play/visual-v2/?style=watercolor',wait_until='domcontentloaded');page.wait_for_selector('.continent-art');page.locator('.continent-art').evaluate('e=>e.decode()');page.locator('.network-sea').evaluate('e=>e.decode()');page.evaluate('()=>document.fonts.ready')
   nodes=N.exported('NODES');by_id={n['id']:n for n in nodes};instances=[i for i in N.exported('INSTANCES') if i['nodeId']!='related-overview']
   assert page.locator('.network-island').count()==32 and len(set(page.locator('.network-island').evaluate_all('els=>els.map(e=>e.dataset.node)')))==31
   assert page.locator('[data-node="related-overview"]').count()==0
   assert page.locator('[data-region="related"]').count()==0 and "相關內容大陸" not in page.locator(".network-world").inner_text()
   assert page.locator('.network-mountain[data-terrain="mountain"]').count()==15 and page.locator('.sea-island[data-terrain="island"]').count()==17
   assert page.locator('.continent-art').count()==1
   overlaps=page.locator('.network-island').evaluate_all('els=>{const a=els.map(e=>({id:e.dataset.instance,b:e.getBoundingClientRect()}));return a.flatMap(x=>a.filter(y=>x.id!==y.id&&x.b.x+x.b.width/2>y.b.left&&x.b.x+x.b.width/2<y.b.right&&x.b.y+x.b.height/2>y.b.top&&x.b.y+x.b.height/2<y.b.bottom).map(y=>[x.id,y.id]))}');assert not overlaps,overlaps
   cluster=page.evaluate("async()=>{const d=await import('./network-data.js'),n=await import('./network.js');return ['anapana','iddhipada','four-jhanas'].map(id=>({id,p:n.point(d.INSTANCES.find(i=>i.nodeId===id))}))}");assert max(q['p']['x'] for q in cluster)-min(q['p']['x'] for q in cluster)<9 and max(q['p']['y'] for q in cluster)-min(q['p']['y'] for q in cluster)<14
   for id in ['anapana','iddhipada','four-jhanas']:assert 'mountain-atlas-concept' in page.locator('[data-node="'+id+'"] .island-paint').evaluate('e=>getComputedStyle(e).backgroundImage')
   road=page.locator('.edge-return[data-terrain-road="true"]');assert road.count()==1 and re.search('[CS]',road.get_attribute('d'))
   road_geometry=page.evaluate("async()=>{const d=await import('./network-data.js'),n=await import('./network.js'),e=document.querySelector('[data-terrain-road]');const p=n.point(d.INSTANCES.find(i=>i.id==='eightfold-overview-four-truths-port')),q=n.point(d.INSTANCES.find(i=>i.nodeId==='road-overview')),a=e.getPointAtLength(0),z=e.getPointAtLength(e.getTotalLength());return {start:[a.x,a.y],end:[z.x,z.y],expectedStart:[p.x*18,p.y*13],expectedEnd:[q.x*18,q.y*13],samples:Array.from({length:21},(_,i)=>{const p=e.getPointAtLength(e.getTotalLength()*i/20);return[p.x,p.y]})}}")
   assert all(abs(a-b)<1 for a,b in zip(road_geometry['start'],road_geometry['expectedStart'])) and all(abs(a-b)<1 for a,b in zip(road_geometry['end'],road_geometry['expectedEnd']))
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
   page.screenshot(path=str(O/f'continent-{w}x{h}.png'),full_page=True)
   for i in instances:
    n=by_id[i['nodeId']];page.locator('.network-island[data-instance="'+i['id']+'"]').click();dialog=page.locator('#inspect-dialog');assert dialog.is_visible();assert dialog.locator('#inspect-title').inner_text()==n['label'];assert '?collection=1' in dialog.locator('[data-network-reader]').get_attribute('href') if n['bookId'] else True;dialog.locator('.close-dialog').click()
   for id in ['anapana','iddhipada','four-jhanas']:
    page.locator('.network-island[data-node="'+id+'"]').click();page.locator('#inspect-dialog .close-dialog').click()
   page.locator('[data-net-locate="four-mindfulness"]').click();page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');assert page.locator('.network-island[data-node="four-mindfulness"]').evaluate('e=>{const a=e.getBoundingClientRect(),b=e.closest(".network-scroll").getBoundingClientRect();return a.left+a.width/2>b.left&&a.left+a.width/2<b.right&&a.top+a.height/2>b.top&&a.top+a.height/2<b.bottom}')
   page.locator('[data-toggle="zoom"]').click();assert page.locator('.network-scroll').evaluate('e=>e.scrollWidth<=e.clientWidth+2&&e.scrollHeight<=e.clientHeight+2')
   assert page.evaluate("window.__writes.length===0&&localStorage.getItem('sutrazen.play.v1')==='preserve-v1'")
   report['sizes'].append({'size':[w,h],'visibleInstances':32,'uniqueNodes':31,'mountains':15,'seaIslands':17,'actualDialogs':32,'buttonCenterOverlaps':0,'concentrationCluster':cluster,'road':'curved from right-bottom 道 portal to original 道路 entrance','overviewAndLocate':'passed','localStorageWrites':0})
   if w==1280:
    report['roadGeometry']=road_geometry
    with Image.open(R/'play/visual-v2/assets/continent-concept.png') as art:
     alpha=art.getchannel('A');values=[alpha.getpixel((min(art.width-1,int(x/1800*art.width)),min(art.height-1,int(y/1300*art.height)))) for x,y in road_geometry['samples']]
    assert all(v>=128 for v in values),values
    report['roadOpaqueContinentAlphaSamples']=values
   print(w,h,'continent passed',flush=True)
  b.close()
 s.shutdown();assert not report['javascriptErrors'] and not report['httpErrors'];(O/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
