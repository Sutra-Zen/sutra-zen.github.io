#!/usr/bin/env python3
"""Original-map cover bounds, real overview and compact city-entry regression."""
from pathlib import Path
import functools,http.server,importlib.util,json,subprocess,threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/previews/game-original-frame'
s=importlib.util.spec_from_file_location('ocean_qa',ROOT/'scripts/check-game-ocean-overview.py');o=importlib.util.module_from_spec(s);s.loader.exec_module(o)
d=o.d;d.q.BASE='0971b459e5c1eab99460ba4ad3cdb75ec6ce2685';SIZES=d.SIZES


def geometry(page):
    return page.evaluate('''()=>{let i=document.querySelector('.wm-background'),r=i.getBoundingClientRect(),v=document.querySelector('.wm-viewport'),dock=document.querySelector('.game-dock').getBoundingClientRect(),s=getComputedStyle(i);return {art:{x:r.x,y:r.y,right:r.right,bottom:r.bottom,w:r.width,h:r.height},screen:[innerWidth,innerHeight],dockTop:dock.y,mask:s.maskImage,opacity:s.opacity,filter:s.filter,matte:getComputedStyle(v).backgroundColor,overflow:[document.documentElement.scrollWidth,document.documentElement.scrollHeight],nativeScroll:[v.scrollLeft,v.scrollTop]}}''')


def cover_safe(page):
    g=geometry(page);a=g['art'];w,h=g['screen'];state=d.camera(page)
    assert not state['overview'] and not state['overviewExplicit'],state
    assert a['x']<=.6 and a['y']<=.6 and a['right']>=w-.6 and a['bottom']>=g['dockTop']-.6,g
    assert g['mask']=='none' and g['opacity']=='1' and g['filter']=='none',g
    assert g['nativeScroll']==[0,0] and g['overflow'][0]<=w+1 and g['overflow'][1]<=h+1,g
    assert state['scale']>=state['coverScale']-.000001,state
    return g


def native_edge(page,context,axis,direction):
    width=page.viewport_size['width'];bottom=page.locator('.game-dock').bounding_box()['y']
    if axis=='x':point={'x':width*(.15 if direction>0 else .85),'y':bottom*.45};dx=direction*width*.7;dy=0
    else:point={'x':width*.5,'y':bottom*(.2 if direction>0 else .8)};dx=0;dy=direction*bottom*.6
    trace=[]
    for _ in range(12):
        before=d.camera(page);d.touch_drag(page,context,point,dx,dy);after=d.camera(page)
        cover_safe(page);assert not page.locator('#wm-dialog').is_visible()
        trace.append({k:after[k] for k in ['x','y','scale']})
        if all(abs(before[k]-after[k])<.000001 for k in ['x','y']):break
    else:raise AssertionError('Did not reach original-image edge')
    a=geometry(page)['art'];limit=geometry(page)['dockTop'] if axis=='y' and direction<0 else width
    edge=a['x'] if axis=='x' and direction>0 else a['right']-width if axis=='x' else a['y'] if direction>0 else a['bottom']-limit
    assert abs(edge)<1,(axis,direction,edge,a)
    return trace


def frame_checks(browser,base,report):
    cases=[]
    for width,height in SIZES:
        c=d.q.context_for(browser,base,has_touch=True,viewport={'width':width,'height':height});p=c.new_page();d.q.observe(p,base,report)
        requests=[];p.on('request',lambda request:requests.append(request.url));p.goto(base+'game/#map');d.map_ready(p);d.full_map_geometry(p)
        assert p.locator('.wm-outer-ocean').count()==0
        assert not any('/ocean-frame.js' in url for url in requests)
        assert p.locator('[data-harbor-castle] image,[data-harbor-castle] img').count()==0
        initial=cover_safe(p);p.screenshot(path=str(OUT/f'original-explore-{width}x{height}.png'))
        edges={}
        for axis,direction,name in [('x',1,'left'),('x',-1,'right'),('y',1,'top'),('y',-1,'bottom')]:
            edges[name]=native_edge(p,c,axis,direction)
            p.screenshot(path=str(OUT/f'edge-{name}-{width}x{height}.png'))
        p.locator('[data-wm-zoom-out]').focus()
        for _ in range(8):p.locator('[data-wm-zoom-out]').click();d.q.settle(p)
        cover_safe(p)
        p.locator('[data-wm-zoom-in]').click();d.q.settle(p)
        prior=d.camera(p);o.fit_and_return(p);state=d.camera(p);g=geometry(p);a=g['art']
        expected=min(width/1600,g['dockTop']/900)
        assert state['overview'] and state['overviewExplicit'] and abs(state['scale']-expected)<.000001,(state,expected)
        assert a['x']>=-1 and a['y']>=-1 and a['right']<=width+1 and a['bottom']<=g['dockTop']+1,g
        assert abs(max(a['w']/width,a['h']/g['dockTop'])-1)<.001,g
        assert g['mask']=='none' and p.locator('.wm-outer-ocean').count()==0
        badge=p.locator('[data-wm-city-entry]').bounding_box();assert badge['width']>=48-.1 and badge['height']>=48-.1,badge
        assert badge['x']>=-1 and badge['y']>=-1 and badge['x']+badge['width']<=width+1 and badge['y']+badge['height']<=g['dockTop']+1,badge
        p.screenshot(path=str(OUT/f'original-overview-{width}x{height}.png'))
        p.locator('[data-wm-return]').click();d.q.settle(p);o.exact(prior,d.camera(p));cover_safe(p)
        p.screenshot(path=str(OUT/f'original-returned-{width}x{height}.png'))
        o.fit_and_return(p);p.reload();d.map_ready(p);p.set_viewport_size({'width':height,'height':width});d.q.settle(p);p.set_viewport_size({'width':width,'height':height});d.q.settle(p);p.locator('[data-wm-return]').click();d.q.settle(p);o.exact(prior,d.camera(p));cover_safe(p)
        o.fit_and_return(p);p.locator('[data-wm-city-entry]').click();p.wait_for_selector('.city-tactics-board')
        assert d.q.snapshot(p) is None
        cases.append({'viewport':[width,height],'initial':initial,'hardEdgeNativeTraces':edges,'fitOriginalScale':expected,'overview':g,'compactBadge':badge,'returnExact':True,'reloadRotationReturnExact':True,'nativeCityEntry':True})
        c.close()
    report['frameChecks']=cases


def old_camera_clamps(browser,base,report):
    saved=d.q.fixture([d.q.ORDER[0]],{d.q.ORDER[1]:3,d.q.ORDER[10]:5},d.q.ORDER[10]);results=[]
    for kind,camera in [('legacy-v1-low-scale',{'version':1,'x':-200,'y':1040,'scale':.4}),('old-padded-return',{'version':1,'x':800,'y':490,'scale':.164,'overviewExplicit':True,'returnView':{'x':1700,'y':1040,'scale':1.1}})]:
        c=d.q.context_for(browser,base,saved,viewport={'width':360,'height':800});c.add_init_script('if(!sessionStorage.getItem("qa.camera.seeded")){sessionStorage.setItem("sutrazen.play.camera.v1",'+json.dumps(json.dumps(camera))+');sessionStorage.setItem("qa.camera.seeded","yes")}')
        p=c.new_page();d.q.observe(p,base,report);p.goto(base+'game/#map');d.map_ready(p)
        if kind=='old-padded-return':assert d.camera(p)['overview'];p.locator('[data-wm-return]').click();d.q.settle(p)
        g=cover_safe(p);assert d.q.snapshot(p)==saved
        p.screenshot(path=str(OUT/f'{kind}-safe.png'));results.append({'case':kind,'safeOriginalCover':g,'readingSaveUnchanged':True});c.close()
    report['oldCameraClamps']=results


def reader_and_pinch(browser,base,report):
    c=d.q.context_for(browser,base,has_touch=True,viewport={'width':360,'height':800});p=c.new_page();d.q.observe(p,base,report);p.goto(base+'game/#map');d.map_ready(p)
    native_edge(p,c,'x',1);p.locator('[data-wm-city-entry]').click();p.wait_for_selector('.city-tactics-board')
    assert d.q.snapshot(p) is None
    p.locator('[data-game-nav="map"]').click();d.map_ready(p);cover_safe(p)
    session=c.new_cdp_session(p)
    for kind,distance in [('touchStart',70),('touchMove',15),('touchEnd',0)]:
        session.send('Input.dispatchTouchEvent',{'type':kind,'touchPoints':[] if kind=='touchEnd' else [{'x':180-distance,'y':300,'id':1},{'x':180+distance,'y':300,'id':2}]})
    d.q.settle(p);cover_safe(p);assert p.evaluate('visualViewport.scale')==1
    p.locator('[data-wm-next]').focus();p.locator('[data-wm-next]').click();p.wait_for_selector('body[data-collection-book="four-truths"]')
    for at in [1,2]:d.q.click_next(p,at)
    p.reload();p.wait_for_selector('body[data-collection-index="2"]');p.set_viewport_size({'width':844,'height':390});d.q.settle(p)
    assert p.locator('body').get_attribute('data-collection-index')=='2'
    p.locator('.collection-reader-return').click();d.map_ready(p);cover_safe(p)
    assert '3／29' in p.locator('[data-wm-next]').inner_text() and d.q.snapshot(p)['completed']==[]
    saved=d.q.snapshot(p);p.goto(base+'four-jhanas/book/?collection=1&collectionReturn=game');p.wait_for_url('**/game/?notice=locked#map');d.map_ready(p);cover_safe(p);assert d.q.snapshot(p)==saved
    report['readerAndPinch']={'normalViewBadgeNativeCityRoundTrip':True,'nativePinchOutStopsAtCover':True,'documentScaleUnchanged':True,'actualNextClicks':2,'reloadRotationAndReturnAtPage3':True,'completionStillZero':True,'futureDirectBookLocked':True};c.close()


def main():
    OUT.mkdir(parents=True,exist_ok=True);report=d.q.protect_originals();report.update({'phase':'Local review only','javascriptErrors':[],'httpErrors':[],'physicalSafari':'Not tested; Chromium CDP viewport/input simulation only'})
    paths=['play/collection/store.js','play/collection/reader-bridge.js','play/reader-bridge.js','play/route','play/worldmap-v4/data.js','play/visual-v2/network-data.js','play/title-screen.js','play/title-screen.css','play/game-ui-text.js','play/assets/CC1A7C32-0620-4DB2-BCD2-A9457A83C259.jpeg']
    changes=subprocess.check_output(['git','diff','--name-only',d.q.BASE,'--',*paths],cwd=ROOT,text=True).splitlines();assert not changes,changes;report['protectedGameData']=paths
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(d.q.Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
    try:
        with sync_playwright() as p:
            b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);frame_checks(b,base,report);old_camera_clamps(b,base,report);reader_and_pinch(b,base,report);b.close()
    finally:server.shutdown()
    assert not report['javascriptErrors'],report['javascriptErrors'];assert not report['httpErrors'],report['httpErrors'];report['result']='passed';(OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'result':'passed','report':str((OUT/'validation.json').relative_to(ROOT))},ensure_ascii=False))


if __name__=='__main__':main()
