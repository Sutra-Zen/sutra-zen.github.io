#!/usr/bin/env python3
"""Independent fullscreen dock/input regressions, isolated browser profiles."""
from pathlib import Path
import functools
import http.server
import importlib.util
import json
import subprocess
import threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/previews/game-fullscreen-dock'
spec=importlib.util.spec_from_file_location('immersion_qa',ROOT/'scripts/check-game-immersion.py')
q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
q.BASE='ab311d9a2e030cf7e608e3bd9bc83a006445532e'
SIZES=q.SIZES
DOCK='.game-dock'
SCROLL='.game-dock__scroll'


def map_ready(page):
    q.wait_map(page)
    page.locator('.wm-background').evaluate('(image)=>image.decode().catch(()=>{})')
    q.settle(page)


def camera(page):
    return page.evaluate('window.SutraZenWorldmap.getState().camera')


def full_map_geometry(page):
    result=page.evaluate('''()=>{const v=document.querySelector('.wm-viewport').getBoundingClientRect(),c=document.querySelector('#game-content').getBoundingClientRect();return {viewport:{x:v.x,y:v.y,w:v.width,h:v.height},content:{x:c.x,y:c.y,w:c.width,h:c.height},screen:[innerWidth,innerHeight],outer:[document.documentElement.scrollWidth,document.documentElement.scrollHeight],y:scrollY}}''')
    width,height=result['screen']
    for name in ['viewport','content']:
        r=result[name];assert abs(r['x'])<1 and abs(r['y'])<1 and abs(r['w']-width)<1 and abs(r['h']-height)<1,result
    assert result['outer'][0]<=width+1 and result['outer'][1]<=height+1 and result['y']==0,result
    return result


def title_and_controls(browser,base,report):
    samples=[]
    for width,height in SIZES:
        context=q.context_for(browser,base,has_touch=True,viewport={'width':width,'height':height})
        page=context.new_page();q.observe(page,base,report);page.goto(base+'game/')
        page.wait_for_selector('#game-title-screen.is-art-loaded')
        p=page.locator('.game-title-paper').bounding_box()
        assert abs(p['x']+p['width']/2-width/2)<2 and abs(p['y']+p['height']/2-height/2)<2,p
        page.screenshot(path=str(OUT/f'title-centered-{width}x{height}.png'))
        page.locator('[data-title-start]').click();map_ready(page)
        geometry=full_map_geometry(page)
        dock=page.locator(DOCK);assert dock.is_visible()
        page.screenshot(path=str(OUT/f'map-initial-dock-{width}x{height}.png'))
        selectors=['[data-game-nav="map"]','[data-game-nav="city"]','[data-game-nav="shelf"]',
                   '[data-game-progress]','[data-wm-next]','[data-wm-locate]','[data-wm-overview]',
                   '[data-wm-zoom-in]','[data-wm-zoom-out]','[data-wm-tools-open]','[data-game-settings]']
        for selector in selectors:
            assert page.locator(selector).evaluate('(node)=>Boolean(node.closest(".game-dock"))'),selector
        # Offscreen dock actions must be reachable by native focus and scrolling.
        targets=dock.locator('a,button,summary').all()
        positions=[]
        for target in targets:
            if not target.is_visible():continue
            target.focus();q.settle(page)
            r=target.bounding_box();assert r and 0<=r['x']+r['width']/2<=width and r['y']>=0 and r['y']+r['height']<=height+1,r
            assert r['width']>=44 and r['height']>=44,r
            positions.append({'selector':target.get_attribute('data-game-nav') or target.get_attribute('aria-label') or target.inner_text(),'box':r})
        tops=[p['box']['y'] for p in positions];assert max(tops)-min(tops)<12,positions
        translucent=dock.evaluate('''n=>{const s=getComputedStyle(n);return {background:s.backgroundColor,gradient:s.backgroundImage,backdrop:s.backdropFilter,rect:n.getBoundingClientRect().toJSON()}}''')
        assert translucent['backdrop']!='none',translucent
        # The tool dialog is outside the horizontal clip and opens upward.
        tool=page.locator('[data-wm-tools-open]');tool.focus();page.keyboard.press('Enter')
        page.wait_for_selector('#wm-tools-dialog[open]')
        menu=page.locator('#wm-tools-dialog').bounding_box();d=dock.bounding_box()
        assert menu['x']>=0 and menu['x']+menu['width']<=width+1 and menu['y']>=0 and menu['y']+menu['height']<=d['y']-3,(menu,d)
        page.screenshot(path=str(OUT/f'tools-up-{width}x{height}.png'))
        page.keyboard.press('Escape');page.wait_for_function('!document.querySelector("#wm-tools-dialog").open')
        assert tool.evaluate('(n)=>n===document.activeElement')
        settings=page.locator('[data-game-settings]');settings.focus();page.keyboard.press('Enter')
        page.wait_for_selector('#game-settings[open]');page.keyboard.press('Escape')
        assert settings.evaluate('(n)=>n===document.activeElement')
        # Screenshot with the primary action brought into view, not hidden behind the outer page.
        page.locator('[data-wm-next]').focus();q.settle(page)
        page.screenshot(path=str(OUT/f'map-dock-{width}x{height}.png'))
        samples.append({'size':[width,height],'titleCentered':True,'geometry':geometry,'dock':translucent,'oneRowActions':positions,'toolMenuAboveDock':menu,'keyboardDialogAndFocusRestore':True})
        context.close()
    report['viewportChecks']=samples


def touch_drag(page,context,point,dx,dy,cancel=False):
    cdp=context.new_cdp_session(page)
    def event(kind,x=0,y=0):
        cdp.send('Input.dispatchTouchEvent',{'type':kind,'touchPoints':[] if kind in ['touchEnd','touchCancel'] else [{'x':x,'y':y,'id':1}]})
    event('touchStart',point['x'],point['y'])
    for step in range(1,7):event('touchMove',point['x']+dx*step/6,point['y']+dy*step/6)
    event('touchCancel' if cancel else 'touchEnd')
    q.settle(page)


def touch_and_resume(browser,base,report):
    context=q.context_for(browser,base,has_touch=True,viewport={'width':390,'height':844})
    page=context.new_page();q.observe(page,base,report);page.goto(base+'game/#map');map_ready(page)
    # The dock has its own explicit arrows and native horizontal swipe; it does not pan the map.
    row=page.locator(SCROLL)
    assert row.evaluate('(n)=>n.scrollWidth>n.clientWidth')
    assert page.locator('[data-dock-scroll="1"]').is_visible()
    dock_camera=camera(page);r=row.bounding_box();left=row.evaluate('(n)=>n.scrollLeft')
    touch_drag(page,context,{'x':r['x']+r['width']*.75,'y':r['y']+r['height']/2},-100,0)
    assert row.evaluate('(n)=>n.scrollLeft')>left
    assert all(abs(camera(page)[k]-dock_camera[k])<.001 for k in ['x','y','scale'])
    assert '/game/' in page.url
    page.locator('[data-dock-scroll="-1"]').click();q.settle(page)
    first=camera(page)
    background=page.evaluate('''()=>{for(let y=150;y<innerHeight-180;y+=70)for(let x=70;x<innerWidth-80;x+=70){const n=document.elementFromPoint(x,y);if(n?.closest('.wm-world')&&!n.closest('button,a'))return{x,y};}throw Error('No exposed map background point')}''')
    touch_drag(page,context,background,75,45)
    changed=camera(page);assert abs(first['x']-changed['x'])+abs(first['y']-changed['y'])>10,(first,changed)
    assert not page.locator('#wm-dialog').is_visible()
    page.locator('[data-wm-locate]').focus();page.locator('[data-wm-locate]').click();q.settle(page)
    label=page.locator('.wm-landmark.is-next').bounding_box();point={'x':label['x']+label['width']/2,'y':label['y']+label['height']/2}
    before=camera(page);touch_drag(page,context,point,65,35)
    after=camera(page);assert abs(before['x']-after['x'])+abs(before['y']-after['y'])>10
    assert not page.locator('#wm-dialog').is_visible() and '/book/' not in page.url
    touch_drag(page,context,{'x':120,'y':250},50,20,cancel=True)
    assert page.locator('.wm-viewport').get_attribute('data-camera-gesture')=='none'
    assert not page.locator('#wm-dialog').is_visible()
    cdp=context.new_cdp_session(page);old=camera(page)['scale']
    for kind,d in [('touchStart',30),('touchMove',60),('touchEnd',0)]:
        cdp.send('Input.dispatchTouchEvent',{'type':kind,'touchPoints':[] if kind=='touchEnd' else [{'x':160-d,'y':300,'id':1},{'x':160+d,'y':300,'id':2}]})
    q.settle(page);assert camera(page)['scale']>old
    assert page.evaluate('visualViewport.scale')==1
    assert not page.locator('#wm-dialog').is_visible()
    # Start the real, still-first book and operate actual controls only.
    page.locator('[data-wm-next]').focus();page.locator('[data-wm-next]').click()
    page.wait_for_selector('body[data-collection-book="four-truths"]')
    for at in range(1,6):q.click_next(page,at)
    page.reload();page.wait_for_selector('body[data-collection-index="5"]')
    page.set_viewport_size({'width':844,'height':390});q.settle(page)
    assert page.locator('body').get_attribute('data-collection-index')=='5'
    assert page.locator(DOCK).count()==0
    page.locator('.collection-reader-return').click();map_ready(page)
    full_map_geometry(page)
    assert '6／29' in page.locator('[data-wm-next]').inner_text()
    assert q.snapshot(page)['completed']==[]
    page.locator('[data-wm-next]').focus();page.locator('[data-wm-next]').click();page.wait_for_selector('body[data-collection-index="5"]')
    page.locator('.collection-reader-return').click();map_ready(page)
    before=q.snapshot(page)
    page.goto(base+'four-jhanas/book/?collection=1&collectionReturn=game&collectionPage=5')
    page.wait_for_url('**/game/?notice=locked#map');map_ready(page)
    assert q.snapshot(page)==before
    page.locator('[data-wm-overview]').focus();page.locator('[data-wm-overview]').click();q.settle(page)
    assert page.locator('[data-harbor-castle]').count()==1
    page.screenshot(path=str(OUT/'map-overview-harbor-844x390.png'))
    page.locator('[data-wm-city-entry]').click();page.wait_for_selector('.city-tactics-board')
    assert q.snapshot(page)==before
    report['nativeRegression']={'singleFingerBackgroundPan':True,'singleFingerLabelPanWithoutOpening':True,
        'touchCancelWithoutOpening':True,'simulatedPinchWithoutDocumentZoom':True,'actualNextSteps':5,
        'reloadAndRotationAt':5,'returnAndMainResumeAt':5,'futureDirectReaderLocked':True,
        'countUnchanged':True,'readerHasNoGameDock':True,'nativeDockSwipeNotMapPan':True,
        'halfCastleNativeCityEntry':True}
    context.close()


def keyboard_landmarks(browser,base,report):
    context=q.context_for(browser,base);page=context.new_page();q.observe(page,base,report)
    page.goto(base+'game/#map');map_ready(page)
    reached=[]
    for step in range(60):
        page.keyboard.press('Tab');q.settle(page)
        item=page.evaluate('''()=>{const n=document.activeElement;if(!n?.matches('.wm-landmark,.wm-harbor-castle__entry'))return null;const r=n.getBoundingClientRect(),d=document.querySelector('.game-dock').getBoundingClientRect();return {id:n.dataset.landmark||'harbor-city',visibleFocus:n.matches(':focus-visible'),x:r.x,y:r.y,w:r.width,h:r.height,dockTop:d.y,screenWidth:innerWidth}}''')
        if item:
            assert item['visibleFocus'] and item['x']>=-1 and item['y']>=-1 and item['x']+item['w']<=item['screenWidth']+1 and item['y']+item['h']<=item['dockTop']+1,item
            reached.append(item)
            if len(reached)==1:page.screenshot(path=str(OUT/'keyboard-landmark-focus-1280x900.png'))
        if len({x['id'] for x in reached})==33:break
    assert len({x['id'] for x in reached})==33,len(reached)
    # Switch to genuine pointer input before checking that a visible marker tap
    # and dialog-close focus do not recenter the world.
    point=page.evaluate('''()=>{const d=document.querySelector('.game-dock').getBoundingClientRect();for(const n of document.querySelectorAll('.wm-landmark')){let r=n.getBoundingClientRect();if(r.x>5&&r.y>5&&r.right<innerWidth-5&&r.bottom<d.y-5)return {x:r.x+r.width/2,y:r.y+r.height/2};}throw Error('No exposed marker')}''')
    before=camera(page);page.mouse.click(point['x'],point['y']);page.wait_for_selector('#wm-dialog[open]');after=camera(page)
    assert all(abs(before[k]-after[k])<.001 for k in ['x','y','scale']),(before,after)
    page.locator('[data-wm-close]').click();q.settle(page)
    assert all(abs(before[k]-camera(page)[k])<.001 for k in ['x','y','scale'])
    report['keyboardWorldFocus']={'actualTabReached':len(reached),'uniqueLandmarksAndHarbor':33,
        'allFocusVisibleAboveDock':True,'visiblePointerTapDoesNotMoveCamera':True,'dialogCloseDoesNotMovePointerCamera':True}
    context.close()


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    report=q.protect_originals();report.update({'phase':'Local review only; not published',
        'javascriptErrors':[],'httpErrors':[],'physicalSafari':'Not tested; Chromium CDP input and viewport emulation only'})
    policy=['play/collection/store.js','play/collection/reader-bridge.js','play/collection/catalog.js',
            'play/route/eligibility.js','play/route/data.js','play/route/selectors.js','play/route/metadata.js',
            'play/worldmap-v4/data.js']
    changed=subprocess.check_output(['git','diff','--name-only',q.BASE,'--',*policy],cwd=ROOT,text=True).splitlines()
    assert not changed,{'unexpectedPolicyOrContentChange':changed}
    report['unchangedGamePolicyAndContentFiles']=policy
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(q.Quiet,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
            title_and_controls(browser,base,report)
            touch_and_resume(browser,base,report)
            keyboard_landmarks(browser,base,report)
            browser.close()
    finally:server.shutdown()
    assert not report['javascriptErrors'],report['javascriptErrors'];assert not report['httpErrors'],report['httpErrors']
    report['result']='passed';(OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'result':'passed','report':str((OUT/'validation.json').relative_to(ROOT))},ensure_ascii=False))


if __name__=='__main__':main()
