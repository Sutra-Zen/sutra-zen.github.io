#!/usr/bin/env python3
"""Focused dark narration/vertical Heart Sutra geometry, not a full-book reread."""
from pathlib import Path
import functools,hashlib,http.server,importlib.util,io,json,re,subprocess,sys,threading,zipfile
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/previews/reader-dark-heart';BASELINE='47e4b6ef5c7f51c9aba4766c6bc25eaa790cc239';VERSION='dark-heart-1'
s=importlib.util.spec_from_file_location('stable_reader',ROOT/'scripts/check-reader-stable-artwork.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h);h.VERSION=VERSION
CANDIDATES=json.loads((OUT/'candidates.json').read_text())['books'];SIZES=h.SIZES;ORDER=h.q.ORDER
SHOTS={('four-truths','public',23,1280,900):'heart-fit-four-1280x900.png',('four-truths','public',23,360,800):'heart-overflow-four-360x800.png',('five-aggregates','review',51,2048,1115):'heart-fit-five-review-2048x1115.png',('six-senses','review',110,1024,768):'heart-six-review-1024x768.png',('twelve-links','public',74,844,390):'heart-overflow-twelve-844x390.png',('twelve-links','public',0,1280,900):'dark-former-cream-twelve-1280x900.png',('four-purities-six-recollections','ordered',0,360,800):'dark-former-black-purities-360x800.png',('mindfulness','public',109,844,390):'dark-summary-band-844x390.png'}
def normalize(x):return re.sub(r'\?v=[A-Za-z0-9-]+','?v=CACHE',x)
def guard():
 old=lambda p:subprocess.check_output(['git','show',BASELINE+':'+p],cwd=ROOT)
 prefixes=ORDER+['docs/'+b for b in ORDER]+['index.html','shelf.css','sitemap.xml','robots.txt','googlee0c995331ec518ae.html','reader-controls.css','reader-layout.js','reader-restart.js','picture-panel-focus.js','picture-panel-focus.css','docs/seo','map-topic-resources.css','scripts/site_seo.py','scripts/build-seo.py','scripts/check-seo.py']
 allowed={b+'/book/index.html' for b in ORDER}|{'reader-controls.css','reader-layout.js','docs/seven-factors/offline-manifest.json'}
 changed=set(subprocess.check_output(['git','diff','--name-only',BASELINE,'--',*prefixes],cwd=ROOT,text=True).splitlines());assert changed<=allowed,changed-allowed
 for b in ORDER:assert normalize((ROOT/b/'book/index.html').read_text())==normalize(old(b+'/book/index.html').decode()),b
 strict=['play/collection/store.js','play/collection/catalog.js','play/collection/reader.css','play/route','play/story','play/city/modules/store.js','play/journey-save.js','play/reader-bridge.js','play/visual-v2/assets','play/worldmap-v4/assets','play/assets']
 assert not subprocess.check_output(['git','diff','--name-only',BASELINE,'--',*strict],cwd=ROOT,text=True).splitlines()
 assert normalize((ROOT/'play/collection/reader-bridge.js').read_text())==normalize(old('play/collection/reader-bridge.js').decode())
 count=len([p for p in subprocess.check_output(['git','ls-tree','-rz','--name-only',BASELINE,'--',*prefixes],cwd=ROOT,text=True).split('\0') if p])
 return {'baseline':BASELINE,'auditedOriginalFiles':count,'originalNarrationScriptureImagesInlineBookDataAndBookRenderers':'unchanged; fourteen HTML cache query normalization only','authorizedPresentation':'Shared reader-controls CSS/reader-layout JS plus cache-only reader bridge; no completion/eligibility/storage changes','homepageSeoGoogleOriginalOverlayAndPanelFocus':'byte-for-byte unchanged'}
def save(r):OUT.mkdir(parents=True,exist_ok=True);(OUT/'validation.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
def shot(p,b,mode,index,size):
 name=SHOTS.get((b,mode,index,*size))
 if name:p.screenshot(path=str(OUT/name))
def show(p,b,index):h.show_row(p,h.BOOKS[b]['allRows'][index])
def row_ids(b):
 c=CANDIDATES[b];ids={c['normalCaptionCandidates'][0]['index'],max(c['normalCaptionCandidates'],key=lambda r:r['captionChars'])['index'],c['steps']-1}
 for values in c['normalIllustratedInkFlagRanges'].values():
  if values:ids.add(values[0]['first'])
 ids.update(c['illustratedSummaryIndices'][:1]);return sorted(ids)
THEME=r'''()=>{
 const shown=n=>n&&!n.hidden&&n.checkVisibility()&&n.getBoundingClientRect().width>0;
 function rgb(s){const m=s.match(/[\d.]+/g)?.map(Number)||[0,0,0];return [...m.slice(0,3),m.length>3?m[3]:1]}
 function background(n){const a=[];for(let p=n;p;p=p.parentElement)a.push(p);let out=[255,255,255];for(const p of a.reverse()){const c=rgb(getComputedStyle(p).backgroundColor);out=out.map((v,i)=>c[i]*c[3]+v*(1-c[3]))}return out}
 const region=[],ending=document.querySelector('.page').classList.contains('reader-framed-ending');
 for(const sel of ['#caption','#reader-summary-caption',...(ending?['.scene']:[])]){const n=document.querySelector(sel);if(!shown(n))continue;const colors=new Set(),walk=document.createTreeWalker(n,NodeFilter.SHOW_TEXT);let t;while(t=walk.nextNode()){const e=t.parentElement;if(!t.textContent.trim()||!shown(e)||e.closest('[aria-hidden="true"],.caption-sizer,#caption-sizer,[hidden]'))continue;colors.add(getComputedStyle(e).color)}region.push({selector:sel,background:getComputedStyle(n).backgroundColor,effectiveBackground:background(n),color:getComputedStyle(n).color,textColors:[...colors],textLength:n.innerText.length,rect:n.getBoundingClientRect().toJSON()})}
 const top=document.querySelector('.top');return {regions:region,header:{background:getComputedStyle(top).backgroundColor,effectiveBackground:background(top),color:getComputedStyle(top).color,childColors:[...new Set([...top.querySelectorAll('*')].filter(shown).map(n=>getComputedStyle(n).color))]},classes:document.querySelector('.page').className,overlays:[...document.querySelectorAll('.art-overlay,.window-label')].filter(shown).map(n=>({text:n.textContent,color:getComputedStyle(n).color})),artFilter:getComputedStyle(document.querySelector('#art')).filter}
}'''
def parse_color(s):
 a=list(map(float,re.findall(r'[\d.]+',s)));return a[:3]
def luminance(c):
 v=[x/255 for x in c];v=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in v];return .2126*v[0]+.7152*v[1]+.0722*v[2]
def contrast(a,b):x,y=sorted([luminance(a),luminance(b)]);return (y+.05)/(x+.05)
def theme(p,b,index):
 t=p.evaluate(THEME);assert t['artFilter']=='none',('art accidentally dimmed',b,index,t)
 assert max(t['header']['effectiveBackground'])<90,(b,index,'header not dark',t)
 for region in t['regions']:
  assert max(abs(x-30) for x in region['effectiveBackground'])<.1,(b,index,'caption/end effective bg differs',region)
  if region['selector']!='.scene':assert parse_color(region['color'])==[255,253,248],(b,index,'caption not white',region)
  region['minimumContrast']=min([contrast(parse_color(c),region['effectiveBackground']) for c in region['textColors']] or [99])
  assert region['minimumContrast']>=4.5,(b,index,'unreadable child text',region)
 return t
HEART=r'''r=>{
 const $=s=>document.querySelector(s),body=$('.verse-body'),title=$('#page-title'),verse=$('#verse'),rect=n=>n.getBoundingClientRect().toJSON(),union=boxes=>{const left=Math.min(...boxes.map(b=>b.left)),right=Math.max(...boxes.map(b=>b.right)),top=Math.min(...boxes.map(b=>b.top)),bottom=Math.max(...boxes.map(b=>b.bottom));return {left,right,top,bottom,width:right-left,height:bottom-top,xCenter:(left+right)/2,yCenter:(top+bottom)/2}};
 const boxes=[rect(title),rect(verse)],glyphs=[];for(const host of [title,verse]){const w=document.createTreeWalker(host,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode())if(n.textContent.trim()){const a=document.createRange();a.selectNodeContents(n);glyphs.push(...[...a.getClientRects()].map(x=>x.toJSON()))}}
 const item=typeof currentItem==='function'?currentItem():pages[r.pageArg],source=Number.isInteger(item.sceneIndex)&&typeof scenes!=='undefined'?scenes[item.sceneIndex]:item,expected=typeof source.heart==='string'?source.heart:(source.verse||item.verse||'');
 const highlighted=verse.querySelector('strong'),expectedHighlight=source.highlight||(typeof BOOK!=='undefined'?BOOK.heartHighlight:'')||'';
 return {fits:$('.page').classList.contains('reader-heart-fits'),body:rect(body),title:boxes[0],verse:boxes[1],union:union(boxes),glyphUnion:union(glyphs),clientWidth:body.clientWidth,scrollWidth:body.scrollWidth,scrollLeft:body.scrollLeft,flex:getComputedStyle(verse).flex,writing:getComputedStyle(verse).writingMode,textExact:verse.textContent===expected,textLength:verse.textContent.length,highlight:highlighted?.textContent,expectedHighlight}
}'''
def heart_measure(p,b,index):
 d=p.evaluate(HEART,h.BOOKS[b]['allRows'][index]);assert d['textExact'] and d['textLength']>300 and d['highlight']==d['expectedHighlight'] and d['writing']=='vertical-rl',(b,index,d)
 center=(d['body']['left']+d['body']['right'])/2;d['boxCenterError']=abs(d['union']['xCenter']-center);d['glyphCenterError']=abs(d['glyphUnion']['xCenter']-center)
 if d['fits']:
  assert d['union']['width']<=d['clientWidth']+1 and d['boxCenterError']<=1,(b,index,'content boxes not centered',d)
  assert abs(d['union']['yCenter']-(d['body']['top']+d['body']['bottom'])/2)<=1,(b,index,'content box vertical frame alignment',d)
  assert d['glyphCenterError']<=4,(b,index,'actual text still off center',d)
 else:
  assert d['scrollWidth']>d['clientWidth']+1 and abs(d['scrollLeft'])<1,(b,index,'overflow not initial RTL right',d)
  assert abs(d['title']['right']-d['body']['right'])<1,(b,index,'title not reachable at right start',d)
  body=p.locator('.verse-body');box=body.bounding_box();before=h.step_index(p);p.mouse.move(box['x']+box['width']/2,box['y']+box['height']/2);p.mouse.wheel(-100000,0);p.wait_for_timeout(80)
  assert body.evaluate('(n)=>n.scrollLeft')<0 and h.step_index(p)==before
  tail=p.locator('#verse').evaluate('''n=>{const w=document.createTreeWalker(n,NodeFilter.SHOW_TEXT);let t,last;while(t=w.nextNode())if(t.textContent.trim())last=t;const r=document.createRange();r.setStart(last,Math.max(0,last.length-10));r.setEnd(last,last.length);return r.getBoundingClientRect().toJSON()}''')
  assert tail['right']>d['body']['left'] and tail['left']<d['body']['right'],(b,index,'tail not reachable',tail,d)
  d['nativeRtlToEnd']={'scrollLeft':body.evaluate('(n)=>n.scrollLeft'),'tail':tail,'stepUnchanged':True};body.evaluate('(n)=>n.scrollLeft=0')
 return d

def hearts(browser,base,r):
 existing={(x['book'],x['mode'],tuple(x['viewport'])) for x in r['heartCases']}
 for mode in ['public','review']:
  for b in ORDER[:4]:
   ctx=h.context(browser,base,b,mode,SIZES[0]);p=ctx.new_page();h.q.observe(p,base,r);p.goto(h.uri(base,b,mode));h.settle(p);indices=h.BOOKS[b]['specialIndices']['heart']
   if mode!='public':p.wait_for_selector('body[data-collection-book]')
   for size in SIZES:
    if (b,mode,tuple(size)) in existing:continue
    previous=h.step_index(p);p.set_viewport_size({'width':size[0],'height':size[1]});h.settle(p);assert h.step_index(p)==previous
    show(p,b,indices[0]-1);before=p.evaluate(h.GEOMETRY);p.locator('#next').click();h.settle(p);assert h.step_index(p)==indices[0];trace=[]
    for index in indices:
     if index!=indices[0]:p.locator('#next').click();h.settle(p);assert h.step_index(p)==index
     g=p.evaluate(h.GEOMETRY)
     for key in ['width','height']:assert abs(g['scripture'][key]-before['frame'][key])<1,(b,mode,size,'frame changed',g,before)
     if before['caption']:assert abs(g['caption']['top']-before['caption']['top'])<1
     data=heart_measure(p,b,index);theme(p,b,index);shot(p,b,mode,index,size);trace.append({'index':index,**data})
    saved=len(h.q.snapshot(p)['completed']) if mode!='public' else None
    if size==SIZES[0]:p.reload();h.settle(p);assert h.step_index(p)==indices[-1];heart_measure(p,b,indices[-1])
    assert (len(h.q.snapshot(p)['completed']) if mode!='public' else None)==saved
    r['heartCases'].append({'book':b,'mode':mode,'viewport':list(size),'nativeTrace':[indices[0]-1]+indices,'cues':trace,'rotationStepPreserved':True,'reloadAtFirstViewport':size==SIZES[0],'noCompletion':True});save(r)
   ctx.close();print('hearts',mode,b,'six sizes passed',flush=True)

def captions(browser,base,r):
 existing={(x['book'],x['mode'],tuple(x['viewport'])) for x in r['captionCases']}
 for mode in ['public','ordered']:
  for b in ORDER:
   ctx=h.context(browser,base,b,mode,SIZES[0]);p=ctx.new_page();h.q.observe(p,base,r);p.goto(h.uri(base,b,mode));h.settle(p)
   if mode!='public':p.wait_for_selector('body[data-collection-book]')
   p.locator('#next').click();h.settle(p);assert h.step_index(p)==1
   for size in SIZES:
    if (b,mode,tuple(size)) in existing:continue
    p.set_viewport_size({'width':size[0],'height':size[1]});h.settle(p);samples=[]
    for index in row_ids(b):
     show(p,b,index);t=theme(p,b,index);g=h.measure(p,b,h.BOOKS[b]['allRows'][index],mode,size);shot(p,b,mode,index,size)
     samples.append({'index':index,'classes':t['classes'],'regions':t['regions'],'header':t['header'],'overlays':t['overlays'],'paint':g['paint']})
    r['captionCases'].append({'book':b,'mode':mode,'viewport':list(size),'sampleIndices':row_ids(b),'samples':samples,'nativeInitial0to1':True});save(r)
   assert (len(h.q.snapshot(p)['completed']) if mode!='public' else None)==(ORDER.index(b) if mode!='public' else None);ctx.close();print('captions',mode,b,'six sizes passed',flush=True)

def offline_guard(r):
 path='downloads/SutraZen-Seven-Factors-Offline.zip';old=zipfile.ZipFile(io.BytesIO(subprocess.check_output(['git','show',BASELINE+':'+path],cwd=ROOT)))
 with zipfile.ZipFile(ROOT/path) as z:
  assert z.testzip() is None and len(z.namelist())==30
  for name in ['reader-controls.css','reader-layout.js']:assert z.read(name)==(ROOT/name).read_bytes()
  names=[n for n in old.namelist() if n.endswith(('.png','.jpg','.webp','.jpeg','book-data.js','book.js'))];assert all(z.read(n)==old.read(n) for n in names)
  r['offline']={'members':30,'bytes':(ROOT/path).stat().st_size,'crc':'passed','sharedReaderFilesMatch':True,'originalImagesNarrationScriptureAndBookJsEqualBaselineZip':True,'sha256':hashlib.sha256((ROOT/path).read_bytes()).hexdigest()}

def summarize(r):
 cues=[c for group in r['heartCases'] for c in group['cues']];fitting=[c for c in cues if c['fits']];overflow=[c for c in cues if not c['fits']]
 regions=[reg for g in r['captionCases'] for sample in g['samples'] for reg in sample['regions']]
 r['summary']={'heartBookModeViewportGroups':len(r['heartCases']),'nativeHeartCueMeasuresAndNextClicks':len(cues),'fittingCueMeasures':len(fitting),'rtlOverflowCueMeasures':len(overflow),'maximumFitBoxHorizontalCenterErrorPx':max(c['boxCenterError'] for c in fitting),'maximumFitBoxVerticalCenterErrorPx':max(abs(c['union']['yCenter']-(c['body']['top']+c['body']['bottom'])/2) for c in fitting),'maximumFitGlyphCenterErrorPx':max(c['glyphCenterError'] for c in fitting),'ordinaryBookModeViewportGroups':len(r['captionCases']),'captionSummaryEndingSampleStates':sum(len(g['samples']) for g in r['captionCases']),'minimumChildTextContrast':min(reg['minimumContrast'] for reg in regions),'screenshots':len(list(OUT.glob('*.png')))}
 assert len(r['heartCases'])==48 and len(r['captionCases'])==168
 assert r['summary']['maximumFitBoxVerticalCenterErrorPx']<=1


def main():
 OUT.mkdir(exist_ok=True);r=guard();r.update({'result':'running','heartCases':[],'captionCases':[],'javascriptErrors':[],'httpErrors':[],'physicalSafari':'Not tested; Chromium viewport, native pointer/wheel/Next simulation','nativeVsFixture':'Heart all thirteen cues use actual Next from previous image, repeated in six dimensions/public+review; ordinary later indices are geometry probes. Game histories isolated, no reading completion granted.'})
 if '--resume' in sys.argv:
  previous=json.loads((OUT/'validation.json').read_text());r['heartCases']=previous.get('heartCases',[]);r['captionCases']=previous.get('captionCases',[]);r['runScope']='Completed geometry groups retained; last targeted fixes/probes continue using frozen runtime.'
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(h.q.Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
 try:
  with sync_playwright() as p:
   b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);hearts(b,base,r);captions(b,base,r);b.close()
  offline_guard(r);assert not r['javascriptErrors'] and not r['httpErrors']
  summarize(r);r['result']='passed'
 except Exception as e:r['result']='failed';r['error']=repr(e);raise
 finally:server.shutdown();save(r)
 print(json.dumps({'result':r['result'],'heartGroups':len(r['heartCases']),'captionGroups':len(r['captionCases'])},ensure_ascii=False))
if __name__=='__main__':main()
