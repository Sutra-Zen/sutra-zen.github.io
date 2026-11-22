#!/usr/bin/env python3
"""Independent outer-ocean, safe overview and exact-return UI regressions."""
from pathlib import Path
import functools,http.server,importlib.util,json,re,subprocess,threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/previews/game-ocean-overview'
s=importlib.util.spec_from_file_location('dock_qa',ROOT/'scripts/check-game-fullscreen-dock.py')
d=importlib.util.module_from_spec(s);s.loader.exec_module(d)
d.q.BASE='53e8eee0db9d2465ea5f584a840649d3c73d0f8d'
SIZES=d.SIZES


def exact(before,after):
    assert all(abs(before[k]-after[k])<.000001 for k in ['x','y','scale']),(before,after)


def fit_and_return(page):
    page.locator('[data-wm-overview]').focus();page.locator('[data-wm-overview]').click();d.q.settle(page)


def capture_geometry(page):
    result=page.evaluate('''()=>{const a=document.querySelector('.wm-background').getBoundingClientRect(),dock=document.querySelector('.game-dock').getBoundingClientRect(),w=document.querySelector('.wm-world').getBoundingClientRect(),svg=document.querySelector('.wm-geography').getBoundingClientRect();return{art:{x:a.x,y:a.y,w:a.width,h:a.height,bottom:a.bottom,right:a.right},world:{x:w.x,y:w.y,w:w.width,h:w.height},svg:{x:svg.x,y:svg.y,w:svg.width,h:svg.height},dockTop:dock.y,screen:[innerWidth,innerHeight]}}''')
    for k in ['x','y','w','h']:assert abs(result['art'][k]-result['svg'][k])<1,result
    return result


def overview_checks(browser,base,report):
    cases=[]
    for width,height in SIZES:
        context=d.q.context_for(browser,base,has_touch=True,viewport={'width':width,'height':height})
        page=context.new_page();d.q.observe(page,base,report);page.goto(base+'game/#map');d.map_ready(page);d.full_map_geometry(page)
        # A real gesture and zoom establish a non-default camera before fitting.
        initial=d.camera(page)
        d.touch_drag(page,context,{'x':width*.45,'y':height*.42},65,35)
        moved=d.camera(page);assert abs(initial['x']-moved['x'])+abs(initial['y']-moved['y'])>10
        assert not page.locator('#wm-dialog').is_visible()
        page.locator('[data-wm-zoom-in]').focus();page.locator('[data-wm-zoom-in]').click();d.q.settle(page)
        prior=d.camera(page)
        page.screenshot(path=str(OUT/f'explore-before-{width}x{height}.png'))
        fit_and_return(page)
        fitted=d.camera(page);assert fitted['overview']
        geometry=capture_geometry(page);a=geometry['art']
        assert a['x']>=-1 and a['y']>=-1 and a['right']<=width+1 and a['bottom']<=geometry['dockTop']-3,geometry
        assert page.locator('[data-wm-return]').is_visible()
        page.screenshot(path=str(OUT/f'overview-safe-{width}x{height}.png'))
        page.locator('[data-wm-return]').click();d.q.settle(page)
        restored=d.camera(page);exact(prior,restored)
        assert page.locator('[data-wm-return]').is_hidden()
        page.screenshot(path=str(OUT/f'explore-returned-{width}x{height}.png'))
        # Repeated enter/return operations must not drift or replace the source view.
        fit_and_return(page);fit_and_return(page);exact(prior,d.camera(page))
        # A full-view reload retains an explicit return to the prior exploration.
        fit_and_return(page);page.reload();d.map_ready(page)
        assert d.camera(page)['overview']
        fit_and_return(page);exact(prior,d.camera(page))
        # Reorientation while fitted preserves the saved exploration, not a fitted snapshot.
        fit_and_return(page);page.set_viewport_size({'width':height,'height':width});d.q.settle(page)
        page.set_viewport_size({'width':width,'height':height});d.q.settle(page)
        fit_and_return(page);exact(prior,d.camera(page))
        # Native keyboard focus makes every southern bridge and the station readable above the dock.
        found=[]
        for step in range(70):
            page.keyboard.press('Tab');d.q.settle(page)
            native_scroll=page.locator('.wm-viewport').evaluate('(n)=>[n.scrollLeft,n.scrollTop]')
            assert native_scroll==[0,0],native_scroll
            item=page.evaluate('''()=>{const n=document.activeElement;if(!n?.matches('.wm-landmark'))return null;let r=n.getBoundingClientRect(),dock=document.querySelector('.game-dock').getBoundingClientRect(),a=document.querySelector('.wm-background').getBoundingClientRect(),sx=parseFloat(n.style.getPropertyValue('--x')),sy=parseFloat(n.style.getPropertyValue('--y'));return{id:n.dataset.landmark,x:r.x,y:r.y,right:r.right,bottom:r.bottom,dockTop:dock.y,width:innerWidth,anchorError:[Math.abs((r.x+r.right)/2-(a.x+a.width*sx/1600)),Math.abs((r.y+r.bottom)/2-(a.y+a.height*sy/900))]}}''')
            if item and (item['id'].startswith('path_bridge_') or item['id']=='path_station'):
                assert item['x']>=-1 and item['right']<=item['width']+1 and item['y']>=-1 and item['bottom']<=item['dockTop']+1,item
                assert max(item['anchorError'])<1,item
                found.append(item['id'])
            if len(set(found))==5:break
        assert len(set(found))==5,found
        page.screenshot(path=str(OUT/f'peninsula-keyboard-{width}x{height}.png'))
        assert d.q.snapshot(page) is None or d.q.snapshot(page)['completed']==[]
        cases.append({'viewport':[width,height],'prior':prior,'fitted':fitted,'overviewGeometry':geometry,
            'returnExact':True,'repeatNoDrift':True,'reloadReturnExact':True,'rotationReturnExact':True,
            'nativeFocusScrollStayedZero':True,'sourceAnchorAlignment':True,'southernKeyboardLabels':sorted(set(found))})
        context.close()
    report['overviewChecks']=cases


def legacy_overview_escape(browser,base,report):
    results=[]
    for kind in ['legacy-v1-no-snapshot','manual-zoom-out']:
        context=d.q.context_for(browser,base)
        if kind.startswith('legacy'):
            context.add_init_script('''if(!sessionStorage.getItem('qa.legacy.seeded')){sessionStorage.setItem('sutrazen.play.camera.v1',JSON.stringify({version:1,x:800,y:450,scale:.5}));sessionStorage.setItem('qa.legacy.seeded','yes')}''')
        page=context.new_page();d.q.observe(page,base,report);page.goto(base+'game/#map');d.map_ready(page)
        if kind=='manual-zoom-out':
            for _ in range(8):
                if d.camera(page)['overview']:break
                page.locator('[data-wm-zoom-out]').focus();page.locator('[data-wm-zoom-out]').click();d.q.settle(page)
        previous=d.camera(page)
        assert previous['overview'] and not previous['canReturn'],previous
        assert page.locator('[data-wm-return]').is_visible()
        page.screenshot(path=str(OUT/f'{kind}-before.png'))
        page.locator('[data-wm-return]').click();d.q.settle(page)
        returned=d.camera(page)
        assert not returned['overview'] and not returned['canReturn'],returned
        assert page.locator('[data-wm-return]').is_hidden()
        box=page.locator('.wm-landmark.is-next').bounding_box();dock=page.locator('.game-dock').bounding_box()
        assert box['x']>=-1 and box['x']+box['width']<=1281 and box['y']>=-1 and box['y']+box['height']<=dock['y']+1,box
        assert d.q.snapshot(page) is None
        page.screenshot(path=str(OUT/f'{kind}-after.png'))
        results.append({'case':kind,'noPriorSnapshotFabricated':True,'explicitArrowVisible':True,'fallbackToCurrentAtNormalZoom':True,'before':previous,'after':returned})
        context.close()
    report['overviewWithoutPriorView']=results


def old_copy_cache_probe(browser,base,report):
    old=subprocess.check_output(['git','show',d.q.BASE+':play/worldmap-v4/text.js'],cwd=ROOT)
    context=d.q.context_for(browser,base);page=context.new_page();d.q.observe(page,base,report)
    urls=[];stale=[]
    def route_text(route):
        urls.append(route.request.url)
        if '?' not in route.request.url:
            stale.append(route.request.url);route.fulfill(status=200,content_type='text/javascript',body=old)
        else:route.continue_()
    page.route('**/play/worldmap-v4/text.js*',route_text)
    page.goto(base+'game/#map');d.map_ready(page);fit_and_return(page)
    assert page.locator('[data-wm-return]').is_visible()
    assert '返回' in page.locator('[data-wm-return]').inner_text()
    assert 'undefined' not in page.locator('body').inner_text()
    assert any('?v=ocean-return-1' in url for url in urls),urls
    page.locator('[data-wm-return]').click();d.q.settle(page)
    assert page.locator('[data-wm-return]').is_hidden()
    report['oldUnversionedTextProbe']={'unversionedBaselineProvidedIfRequested':True,'staleUnversionedRequestsServed':len(stale),'versionedMainUiLoaded':True,'actualTextRequests':urls,'returnLabelsDefined':True}
    context.close()


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    report=d.q.protect_originals();report.update({'phase':'Local review only','javascriptErrors':[],'httpErrors':[],
        'physicalSafari':'Not tested; Chromium CDP and viewport emulation only'})
    core=['play/collection/store.js','play/collection/reader-bridge.js','play/reader-bridge.js','play/collection/catalog.js',
          'play/route','play/worldmap-v4/data.js','play/visual-v2/network-data.js',
          'play/title-screen.js','play/title-screen.css','play/game-ui-text.js',
          'play/assets/CC1A7C32-0620-4DB2-BCD2-A9457A83C259.jpeg']
    changed=subprocess.check_output(['git','diff','--name-only',d.q.BASE,'--',*core],cwd=ROOT,text=True).splitlines();assert not changed,changed
    report['protectedGameCore']=core
    original_entry=subprocess.check_output(['git','show',d.q.BASE+':game/index.html'],cwd=ROOT,text=True)
    extract=lambda html:re.search(r'<section id="game-title-screen".*?</section>',html,re.S).group()
    assert extract(original_entry)==extract((ROOT/'game/index.html').read_text())
    report['entryTitleMarkupUnchanged']=True
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(d.q.Quiet,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
    try:
        with sync_playwright() as p:
            b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
            overview_checks(b,base,report)
            legacy_overview_escape(b,base,report)
            old_copy_cache_probe(b,base,report)
            d.OUT=OUT;d.touch_and_resume(b,base,report)
            b.close()
    finally:server.shutdown()
    assert not report['javascriptErrors'],report['javascriptErrors'];assert not report['httpErrors'],report['httpErrors']
    report['result']='passed';(OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'result':'passed','report':str((OUT/'validation.json').relative_to(ROOT))},ensure_ascii=False))


if __name__=='__main__':main()
