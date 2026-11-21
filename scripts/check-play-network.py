#!/usr/bin/env python3
"""Validate the mind-map island network without touching journey saves or deployment."""
from pathlib import Path
from urllib.parse import urljoin,urlsplit,unquote
import functools,hashlib,http.server,json,re,subprocess,threading
from lxml import html
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'docs/previews/play-network';BASE='5056201';SIZES=[(1280,900),(390,844),(844,390),(768,1024),(1024,768)]

def exported(name):
 text=(R/'play/visual-v2/network-data.js').read_text();match=re.search(r'export const '+re.escape(name)+r'\s*=\s*',text);assert match,name
 return json.JSONDecoder().raw_decode(text[match.end():])[0]

def normal(href,base):
 p=urlsplit(urljoin(base,href));path=p.path
 if path.endswith('/index.html'):path=path[:-10]
 return p.netloc,path,p.fragment

def static_checks():
 tracked=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],cwd=R,text=True).splitlines();protected=[p for p in tracked if p.startswith(('play/','four-truths/','five-aggregates/','six-senses/','docs/seo/')) or p in ['AGENTS.md','index.html','shelf.css','sitemap.xml','robots.txt','googlee0c995331ec518ae.html','reader-controls.css','reader-layout.js','reader-restart.js']]
 for name in protected:
  current=(R/name).read_bytes()
  if name.endswith('/book/index.html'):current=current.replace(b'<script type="module" src="../../play/collection/reader-bridge.js?v=1"></script>\n',b'')
  assert current==subprocess.check_output(['git','show',BASE+':'+name],cwd=R),name
 source=(R/'index.html').read_text();data=json.loads(re.search(r'const dhammaData = (.*?);\s*\n',source)[1]);tree=html.fromstring(source)
 clicks=[re.search(r"openModal\('([^']+)'\)",e.get('onclick') or '') for e in tree.xpath('//*[@onclick]')];keys=[m[1] for m in clicks if m]
 nodes=exported('NODES');instances=exported('INSTANCES');edges=exported('EDGES');by_id={n['id']:n for n in nodes}
 assert len(nodes)==32 and len(instances)==33 and len({n['key'] for n in nodes})==32
 assert exported('NETWORK_SOURCE')['indexSha256']==hashlib.sha256((R/'index.html').read_bytes()).hexdigest()
 assert sorted(i['sourceInstance'] for i in instances)==list(range(33))
 assert [by_id[i['nodeId']]['key'] for i in sorted(instances,key=lambda i:i['sourceInstance'])]==keys
 assert {n['key'] for n in nodes}==set(data)==set(keys) and len(keys)==33
 assert sum(n['nodeId']=='eightfold-overview' for n in instances)==2 and by_id['eightfold-overview']['bookId']=='eightfold-path'
 checked=[]
 for n in nodes:
  fragment=html.fragment_fromstring(data[n['key']]['content'],create_parent='div');links=fragment.xpath('.//nav//a/@href');assert len(links)==3,n['key']
  for field,old in [('guide',links[0]),('reader',links[1])]:
   assert normal(n[field],'https://sutra-zen.github.io/play/visual-v2/')==normal(old,'https://sutra-zen.github.io/'),(n['id'],field,n[field],old)
   path=unquote(urlsplit(urljoin('https://sutra-zen.github.io/play/visual-v2/',n[field])).path).lstrip('/');assert (R/(path+'index.html' if path.endswith('/') else path)).is_file()
  checked.append({'id':n['id'],'key':n['key'],'bookId':n['bookId'],'guideReaderMatchesOriginal':True})
 assert len(edges)==46 and all(e['from'] in by_id and e['to'] in by_id for e in edges)
 chain=['four-mindfulness','right-mindfulness','mindfulness-awakening','mindfulness-root-power']
 for a,b in zip(chain,chain[1:]):assert any({e['from'],e['to']}=={a,b} for e in edges),(a,b)
 assets=[]
 for name in ['network-sea-concept.png','island-atlas-concept.png','kitten-rowboat-concept.png']:
  path=R/'play/visual-v2/assets'/name
  with Image.open(path) as im:assets.append({'file':name,'dimensions':list(im.size),'mode':im.mode,'alphaExtrema':list(im.getchannel('A').getextrema()) if 'A' in im.getbands() else None,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
 return {'baseline':BASE,'protectedFiles':len(protected),'protectedFilesByteEquality':'passed; v1 and original site untouched, reader HTML only authorized collection-module inclusion','uniqueModalKeys':len(nodes),'visualInstances':len(instances),'sourceEdges':len(edges),'sourceDerivedMapping':checked,'duplicateEightfold':'two visual instances, one stable book ID and same original targets','mindfulnessChain':chain,'conceptAssets':assets}

class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def copyfile(self,src,dst):
  try:super().copyfile(src,dst)
  except (BrokenPipeError,ConnectionResetError):pass

def main():
 O.mkdir(parents=True,exist_ok=True);report=static_checks();report.update({'viewports':[],'javascriptErrors':[],'httpErrors':[],'physicalSafari':'not tested','publication':'not published; local-only visual concept, no first-version progress changes'})
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);context=browser.new_context(reduced_motion='reduce');page=context.new_page();page.on('pageerror',lambda e:report['javascriptErrors'].append(str(e)));page.on('response',lambda r:report['httpErrors'].append(r.url) if r.url.startswith(base) and r.status>=400 else None)
  context.add_init_script("""(()=>{const native=Storage.prototype.setItem;native.call(localStorage,'sutrazen.play.v1','network-qa-preserve');native.call(localStorage,'sutrazen.qa.unrelated','preserve');window.__qaStorageWrites=[];for(const method of ['setItem','removeItem','clear']){const original=Storage.prototype[method];Storage.prototype[method]=function(...args){if(this===localStorage)window.__qaStorageWrites.push({method,args});return original.apply(this,args)}}})();""")
  for w,h in SIZES:
   page.set_viewport_size({'width':w,'height':h});page.goto(base+'play/visual-v2/',wait_until='domcontentloaded');page.evaluate('()=>document.fonts.ready')
   page.wait_for_selector('.network-island[data-node="four-truths"]');page.locator('.network-sea').evaluate('e=>e.decode()');page.locator('.network-footer img').evaluate('e=>e.decode()')
   nodes=exported('NODES');by_id={n['id']:n for n in nodes};instances=[i for i in exported('INSTANCES') if i['nodeId']!='related-overview']
   assert page.locator('.network-island').count()==32 and len(set(page.locator('.network-island').evaluate_all('els=>els.map(e=>e.dataset.node)')))==31
   center_overlaps=page.locator('.network-island').evaluate_all('els=>{const r=els.map(e=>({id:e.dataset.instance,b:e.getBoundingClientRect()}));return r.flatMap(a=>r.filter(b=>a.id!==b.id&&a.b.x+a.b.width/2>b.b.left&&a.b.x+a.b.width/2<b.b.right&&a.b.y+a.b.height/2>b.b.top&&a.b.y+a.b.height/2<b.b.bottom).map(b=>[a.id,b.id]))}')
   assert not center_overlaps,center_overlaps
   assert '閱讀導覽不是修證次第' in page.locator('.network-footer').inner_text()
   assert '閱讀航線仍只是導覽' in page.locator('.network-note').inner_text()
   route_color=page.locator('.network-reading-route').evaluate('e=>getComputedStyle(e).stroke');relation_color=page.locator('.network-edge').first.evaluate('e=>getComputedStyle(e).stroke');assert route_color!=relation_color
   point_info=page.evaluate("async()=>{const d=await import('./network-data.js'),n=await import('./network.js');const p=id=>n.point(d.INSTANCES.find(i=>i.nodeId===id));return {truth:p('four-truths'),roots:p('roots-powers-overview'),eightfoldRoute:n.routeInstance('eightfold-path').id}}")
   assert point_info['truth']['x']>point_info['roots']['x'] and point_info['truth']['y']>point_info['roots']['y']
   assert point_info['eightfoldRoute']=='eightfold-overview-four-truths-port'
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
   page.screenshot(path=str(O/f'network-{w}x{h}.png'),full_page=True)
   # Every visual instance opens the matching original topic links, including duplicated eightfold portals.
   for instance in instances:
    n=by_id[instance['nodeId']];page.locator('.network-island[data-instance="'+instance['id']+'"]').click();dialog=page.locator('#inspect-dialog');assert dialog.is_visible();assert dialog.locator('#inspect-title').inner_text()==n['label']
    assert normal(dialog.locator('[data-network-guide]').get_attribute('href'),'https://sutra-zen.github.io/play/visual-v2/')==normal(n['guide'],'https://sutra-zen.github.io/play/visual-v2/')
    assert normal(dialog.locator('[data-network-reader]').get_attribute('href'),'https://sutra-zen.github.io/play/visual-v2/')==normal(n['reader'],'https://sutra-zen.github.io/play/visual-v2/')
    dialog.locator('.close-dialog').click()
   # Traverse the actual cross-topic buttons rather than manufacturing a selected state.
   chain=report['mindfulnessChain'];page.locator('.network-island[data-node="'+chain[0]+'"]').click()
   for target in chain[1:]:page.locator('#inspect-dialog [data-related-node="'+target+'"]').click();assert page.locator('#inspect-title').inner_text()==by_id[target]['label']
   page.locator('#inspect-dialog .close-dialog').click()
   for node in chain:assert page.locator('.network-island.is-related[data-node="'+node+'"]').count()==1
   for a,b in zip(chain,chain[1:]):
    edges=page.locator('.network-edge.is-highlighted').evaluate_all('els=>els.map(e=>[e.dataset.from,e.dataset.to])');assert any(set(edge)=={a,b} for edge in edges)
   if w in [1280,390]:page.screenshot(path=str(O/f'mindfulness-{w}x{h}.png'),full_page=True)
   page.locator('[data-net-toggle="links"]').click();assert page.locator('.network-edge.is-hidden').count()>0
   page.locator('[data-net-toggle="links"]').click();assert page.locator('.network-edge.is-hidden').count()==0
   page.locator('[data-net-toggle="route"]').click();assert page.locator('.network-reading-route').count()==0
   page.locator('[data-net-toggle="route"]').click();assert page.locator('.network-reading-route').count()==1
   page.locator('[data-net-clear]').click();assert page.locator('.network-island.is-selected').count()==0
   for target in ['four-truths','four-mindfulness','roots-powers-overview']:
    page.locator('[data-net-locate="'+target+'"]').click();page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
    assert page.locator('.network-island[data-node="'+target+'"]').evaluate('e=>{const a=e.getBoundingClientRect(),b=e.closest(".network-scroll").getBoundingClientRect();return a.left+a.width/2>b.left&&a.left+a.width/2<b.right&&a.top+a.height/2>b.top&&a.top+a.height/2<b.bottom}')
   page.locator('[data-toggle="zoom"]').click();assert page.locator('#scene-host.is-overview').count()==1
   assert page.locator('.network-scroll').evaluate('e=>e.scrollWidth<=e.clientWidth+2&&e.scrollHeight<=e.clientHeight+2')
   assert page.locator('img[src*="kitten-boat-concept"]').count()==0
   assert page.locator('.network-footer img').get_attribute('src').endswith('kitten-rowboat-concept.png')
   # The protagonist changed, while the canonical city guardian remains 念.
   page.locator('[data-view="map"]').click();page.locator('.map-boat img').evaluate('e=>e.decode()');assert page.locator('.map-boat>span').count()==0;assert 'rowboat' in page.locator('.map-boat img').get_attribute('src')
   page.locator('[data-view="city"]').click();page.locator('[data-spot="guardian"]').click();assert '守門人譬喻念' in page.locator('#inspect-dialog').inner_text();page.locator('#inspect-dialog .close-dialog').click()
   page.locator('[data-view="celebrate"]').click();page.locator('[data-stage="3"]').click();page.locator('.return-boat img').evaluate('e=>e.decode()');assert page.locator('.return-boat>span').count()==0;assert 'rowboat' in page.locator('.return-boat img').get_attribute('src')
   if w in [1280,390]:page.screenshot(path=str(O/f'hero-without-lantern-{w}x{h}.png'),full_page=True)
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
   assert page.evaluate("localStorage.getItem('sutrazen.play.v1')==='network-qa-preserve'&&localStorage.getItem('sutrazen.qa.unrelated')==='preserve'&&window.__qaStorageWrites.length===0")
   report['viewports'].append({'size':[w,h],'instanceDialogs':32,'visibleUniqueNodes':31,'removedOverview':'related-overview is now a noninteractive continent label','pairwiseButtonCenterOverlaps':0,'mindfulnessChain':'related-button traversal and connected edge highlights passed','routeVsRelations':'different strokes and independent toggles; no required-unlock claim','mirroredLRoute':'lower-right truth to upper-left summaries; eightfold bottom portal retained','locateControls':3,'fullOverview':'no internal crop','activeProtagonist':'new neutral rowboat, no lantern image or HTML 念 prop; city guardian 念 retained','storageWrites':0,'outsideSceneOverflow':False})
   print(w,h,'network passed',flush=True)
  # Follow real source and reader anchors once; all 32 target mappings were checked above.
  page.locator('[data-view="network"]').click();page.locator('.network-island[data-node="four-mindfulness"]').click();page.locator('[data-network-guide]').click();page.wait_for_load_state('domcontentloaded');assert '/mindfulness/' in page.url and page.locator('h1').count()==1
  page.go_back(wait_until='domcontentloaded');page.wait_for_selector('.network-island');page.locator('.network-island[data-node="four-mindfulness"]').click();page.locator('[data-network-reader]').click();page.wait_for_selector('#position-text');assert '/mindfulness/book/' in page.url and page.locator('#next').count()==1
  page.wait_for_function('document.body?.dataset.collectionBook==="mindfulness"');assert page.evaluate("localStorage.getItem('sutrazen.play.v1')==='network-qa-preserve'&&window.__qaStorageWrites.every(w=>w.args[0]==='sutrazen.play.collection.v1')")
  report['actualNavigation']='Four Mindfulness guide and original full reader loaded through native anchors; explicit reader opt-in writes only collection namespace'
  browser.close()
 server.shutdown();assert not report['javascriptErrors'] and not report['httpErrors'],report
 (O/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
