#!/usr/bin/env python3
"""Independent UI regressions for immersion + strict sequence, not old free mode.

Historical release reports remain unchanged. Valid save fixtures are explicitly
separate from the native29-step current-book completion below.
"""
from pathlib import Path
import functools
import http.server
import json
import subprocess
import threading
import re
import hashlib
from PIL import Image

from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/previews/game-immersion'
BASE='7e39f04a383ab98d3b747365ea3e513ad7140a0e'
SIZES=[(1280,900),(360,800),(844,390),(768,1024),(1024,768)]
ORDER=['four-truths','five-aggregates','six-senses','twelve-links','eightfold-path',
       'four-purities-six-recollections','mindfulness','right-effort','anapana',
       'iddhipada','four-jhanas','five-roots-powers','seven-factors','four-fruits-ten-fetters']
KEY='sutrazen.play.collection.v1'


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*_):pass
    def copyfile(self,source,target):
        try:super().copyfile(source,target)
        except (BrokenPipeError,ConnectionResetError):pass


def protect_originals():
    paths=ORDER+['docs/'+book for book in ORDER]+[
        'index.html','shelf.css','sitemap.xml','robots.txt','googlee0c995331ec518ae.html',
        'reader-controls.css','reader-layout.js','reader-restart.js',
        'picture-panel-focus.js','picture-panel-focus.css','docs/seo',
        'map-topic-resources.css','scripts/site_seo.py','scripts/build-seo.py','scripts/check-seo.py',
    ]
    changed=subprocess.check_output(['git','diff','--name-only',BASE,'--',*paths],cwd=ROOT,text=True).splitlines()
    assert not changed,{'protectedChanges':changed}
    files=[p for p in subprocess.check_output(['git','ls-tree','-rz','--name-only',BASE,'--',*paths],cwd=ROOT,text=True).split('\0') if p]
    return {'baseline':BASE,'protectedTrackedFiles':len(files),
            'originalFourteenReadersIncludingHtml':'byte-for-byte unchanged',
            'originalNarrationScripturePicturesAndSourceArchives':'byte-for-byte unchanged',
            'rootHomepageSeoGoogleAndSharedReaderControls':'byte-for-byte unchanged'}


def fixture(completed=(),positions=None,active=None):
    return {'version':1,'completed':list(completed),'positions':positions or {},'activeBook':active or ORDER[0]}


def settle(page):
    page.evaluate('()=>new Promise(done=>requestAnimationFrame(()=>requestAnimationFrame(done)))')


def observe(page,base,report):
    page.on('pageerror',lambda error:report['javascriptErrors'].append(str(error)))
    page.on('response',lambda response:report['httpErrors'].append({'url':response.url,'status':response.status}) if response.url.startswith(base) and response.status>=400 else None)


def context_for(browser,base,saved=None,**kwargs):
    options={'viewport':{'width':1280,'height':900},'reduced_motion':'reduce',**kwargs}
    if saved is not None:
        options['storage_state']={'cookies':[],'origins':[{'origin':base.rstrip('/'),'localStorage':[{'name':KEY,'value':json.dumps(saved)}]}]}
    return browser.new_context(**options)


def snapshot(page):
    return page.evaluate('(key)=>JSON.parse(localStorage.getItem(key)||"null")',KEY)


def wait_map(page):
    page.wait_for_selector('.wm-viewport')
    page.wait_for_function('window.SutraZenWorldmap?.getState().camera?.scale > 0')
    settle(page)


def click_next(page,target):
    page.locator('#next').click()
    page.wait_for_function('(target)=>Number(document.body.dataset.collectionIndex)===target',arg=target)


def assert_shell(page):
    assert page.locator('.sz-game-nav [data-game-nav]').evaluate_all('(nodes)=>nodes.map(n=>n.dataset.gameNav)')==['map','city','shelf']
    bounds=page.evaluate('''()=>({w:innerWidth,h:innerHeight,sw:document.documentElement.scrollWidth,
        sh:document.documentElement.scrollHeight,y:scrollY,nav:[...document.querySelectorAll('.sz-game-nav a')].map(n=>{let r=n.getBoundingClientRect();return {w:r.width,h:r.height,b:r.bottom}})})''')
    assert bounds['sw']<=bounds['w']+1 and bounds['sh']<=bounds['h']+1 and bounds['y']==0,bounds
    assert all(n['w']>=48 and n['h']>=48 and n['b']<=bounds['h']+1 for n in bounds['nav']),bounds
    assert '[object Object]' not in page.locator('body').inner_text()
    return bounds


def native_first_book(browser,base,report):
    context=context_for(browser,base);page=context.new_page();observe(page,base,report)
    requests=[];page.on('request',lambda req:requests.append(req.url))
    page.goto(base+'game/');page.wait_for_selector('#game-title-screen:not([hidden])')
    assert page.locator('[data-title-heading]').inner_text()=='小貓的山海旅程'
    assert page.locator('[data-title-subtitle]').inner_text()=='佛法繪本探索遊戲'
    assert page.locator('[data-title-start]').inner_text()=='開始旅程'
    assert not any('/book/' in url or any('/'+book+'/assets/' in url for book in ORDER) for url in requests),requests
    page.screenshot(path=str(OUT/'title-1280x900.png'))
    page.locator('[data-title-settings]').click();page.wait_for_selector('#game-settings[open]')
    assert page.locator('#game-settings a').count()==3
    page.locator('[data-game-settings-close]').click()
    assert page.locator('[data-title-settings]').evaluate('(n)=>n===document.activeElement')
    page.locator('[data-title-start]').click();wait_map(page);assert_shell(page)
    assert page.locator('.wm-landmark.is-next').count()==1
    assert page.locator('.wm-landmark.is-next').get_attribute('data-book')==ORDER[0]
    assert page.locator('.wm-landmark.is-next .wm-status-chip').inner_text()=='新關卡'
    page.screenshot(path=str(OUT/'map-new-player-1280x900.png'))
    page.locator('[data-wm-next]').click();page.wait_for_selector('body[data-collection-book="four-truths"]')
    assert page.locator('.sz-game-nav').count()==0
    assert page.locator('[href$="index.html#sources"],.reading-links').count()>0
    total=int(page.locator('body').get_attribute('data-collection-total'));assert total==29,total
    trace=[0]
    for index in range(1,6):click_next(page,index);trace.append(index)
    assert snapshot(page)['completed']==[]
    page.reload();page.wait_for_selector('body[data-collection-index="5"]')
    page.set_viewport_size({'width':768,'height':1024});settle(page)
    assert page.locator('body').get_attribute('data-collection-index')=='5'
    page.screenshot(path=str(OUT/'reader-768x1024.png'))
    page.set_viewport_size({'width':1024,'height':768});settle(page)
    assert page.locator('body').get_attribute('data-collection-index')=='5'
    page.locator('.collection-reader-return').click();wait_map(page)
    assert not page.locator('#game-title-screen').is_visible()
    assert page.locator('.wm-landmark.is-next .wm-status-chip').inner_text()=='閱讀中 · 6／29'
    page.locator('[data-wm-next]').click();page.wait_for_selector('body[data-collection-index="5"]')
    for index in range(6,total):click_next(page,index);trace.append(index)
    assert snapshot(page)['completed']==[]
    assert page.locator('#next').inner_text()=='完成這本'
    page.locator('#next').click();wait_map(page);page.wait_for_selector('#wm-dialog[open]')
    saved=snapshot(page);assert saved['completed']==[ORDER[0]],saved
    assert page.locator('[data-wm-next-station]').count()==1
    assert page.locator('#wm-dialog .city-tactics-board').count()==0
    page.screenshot(path=str(OUT/'completion-first-book-1024x768.png'))
    page.locator('[data-wm-next-station]').click();page.wait_for_function('!document.querySelector("#wm-dialog").open')
    assert '/game/' in page.url and '/book/' not in page.url
    assert page.locator('.wm-landmark.is-next').get_attribute('data-book')==ORDER[1]
    assert page.locator('.wm-landmark.is-next .wm-status-chip').inner_text()=='新關卡'
    camera=page.evaluate('window.SutraZenWorldmap.getState().camera')
    page.screenshot(path=str(OUT/'map-next-station-1024x768.png'))
    # Actual review: no reward replay, counter mutation or mainline detour.
    page.locator('[data-game-nav="shelf"]').click();page.wait_for_selector('[data-collection-read="four-truths"]')
    assert page.locator('[data-collection-read]').count()==1
    assert page.locator('.collection-book-placeholder').count()==13
    page.screenshot(path=str(OUT/'shelf-one-completed-1024x768.png'))
    page.locator('[data-collection-read="four-truths"]').click();page.wait_for_selector('body[data-collection-index="0"]')
    assert page.locator('body').get_attribute('data-collection-mode')=='review'
    for index in range(1,total):click_next(page,index)
    page.locator('#next').click();page.wait_for_selector('[data-collection-read="four-truths"]')
    assert 'shelf' in page.url and 'completed=' not in page.url
    assert snapshot(page)['completed']==[ORDER[0]]
    page.locator('[data-game-nav="map"]').click();wait_map(page)
    assert page.locator('.wm-landmark.is-next').get_attribute('data-book')==ORDER[1]
    assert not page.locator('#wm-dialog').is_visible()
    after=page.evaluate('window.SutraZenWorldmap.getState().camera')
    assert all(abs(after[k]-camera[k])<.02 for k in ['x','y','scale']),(camera,after)
    report['nativeReading']={'firstBookSteps':total,'actualSequentialNextTrace':trace,
        'reloadAndRotationAt':5,'completionOnlyAfterExplicitButton':True,
        'nextStationReturnsMapWithoutAutostart':True,'nextBook':ORDER[1],
        'actualReviewSteps':total,'reviewNoRewardReplayOrMainlineChange':True}
    context.close()


def locks_and_history(browser,base,report):
    result=[]
    # Imported fixtures are deliberately separate from the native completion.
    scenarios=[('future-bookmarks',fixture([ORDER[0]],{ORDER[10]:5,ORDER[2]:4},ORDER[10]),ORDER[1]),
               ('sparse-history',fixture([ORDER[10]],{ORDER[10]:5},ORDER[10]),ORDER[0]),
               ('final-bookmark-is-not-reveal',fixture([],{ORDER[-1]:6},ORDER[-1]),ORDER[0]),
               ('historic-final-completion',fixture([ORDER[-1]]),ORDER[0]),
               ('first-thirteen',fixture(ORDER[:-1]),ORDER[-1]),
               ('all-fourteen',fixture(ORDER),None)]
    for name,saved,expected in scenarios:
        context=context_for(browser,base,saved);page=context.new_page();observe(page,base,report)
        page.goto(base+'game/#map');wait_map(page)
        state=page.evaluate('window.SutraZenWorldmap.getState().status')
        assert state['nextBookId']==expected,(name,state)
        current=snapshot(page)
        assert current['completed']==saved['completed'],(name,current)
        assert current['positions']==saved['positions'] and current['activeBook']==saved['activeBook'],(name,current)
        if name=='final-bookmark-is-not-reveal':
            assert '四向四果與十結' not in page.locator('#wm-route-strip').text_content()
        if name=='first-thirteen':assert '四向四果與十結' in page.locator('#wm-route-strip').text_content()
        if name=='all-fourteen':assert state['count']==14
        page.locator('[data-game-nav="shelf"]').click();page.wait_for_selector('#collection-books')
        assert page.locator('[data-collection-read]').count()==len(saved['completed'])
        result.append({'fixture':name,'retained':current,'mainline':expected})
        context.close()
    context=context_for(browser,base);page=context.new_page();observe(page,base,report)
    page.goto(base+'game/#map');wait_map(page)
    page.locator('.wm-secondary-tools > summary').click()
    page.locator('#wm-route-strip summary').click()
    page.locator('[data-wm-book="four-jhanas"]').click();page.wait_for_selector('#wm-dialog[open]')
    assert page.locator('#wm-dialog [data-wm-read]').count()==0
    assert page.locator('[data-wm-current]').count()==1
    page.locator('[data-wm-close]').click()
    assert page.locator('[data-wm-book="four-jhanas"]').evaluate('(n)=>n===document.activeElement')
    before=snapshot(page)
    for book in [ORDER[2],ORDER[10]]:
        for suffix in ['?collection=1','?collection=1&collectionReturn=game&collectionPage=4']:
            page.goto(base+book+'/book/'+suffix)
            page.wait_for_url(re.compile(r'.*/game/\?notice=locked#map'))
            wait_map(page)
            assert snapshot(page)==before,(book,suffix,snapshot(page),before)
        # Ordinary website remains free and does not become game progress.
        page.goto(base+book+'/book/');page.wait_for_selector('#next')
        original=page.locator('#position-text').inner_text();page.locator('#next').click()
        page.wait_for_function('(old)=>document.querySelector("#position-text").textContent!==old',arg=original)
        assert page.locator('body.collection-reading').count()==0
        assert snapshot(page)==before
    report['historyFixtures']=result
    report['entryGuards']={'lockedRouteDialogNoReaderAction':True,'focusRestored':True,
                           'futureOldAndGameQueriesBlocked':4,'bareOriginalReadersNativeNextUnaffected':2}
    context.close()


def camera_and_viewports(browser,base,report):
    samples=[]
    for width,height in SIZES:
        context=context_for(browser,base,has_touch=True,viewport={'width':width,'height':height})
        page=context.new_page();observe(page,base,report);page.goto(base+'game/#map');wait_map(page)
        bounds=assert_shell(page)
        landmark=page.locator('.wm-landmark.is-next');box=landmark.bounding_box()
        assert box and 0<=box['x']+box['width']/2<=width and 56<=box['y']+box['height']/2<height-64,box
        start=page.evaluate('window.SutraZenWorldmap.getState().camera')
        center={'x':box['x']+box['width']/2,'y':box['y']+box['height']/2}
        page.mouse.move(**center);page.mouse.down();page.mouse.move(center['x']+65,center['y']+32,steps=10);page.mouse.up();settle(page)
        moved=page.evaluate('window.SutraZenWorldmap.getState().camera')
        assert abs(start['x']-moved['x'])+abs(start['y']-moved['y'])>10
        assert not page.locator('#wm-dialog').is_visible() and '/book/' not in page.url
        page.locator('[data-wm-locate]').click();settle(page)
        scale=page.evaluate('window.SutraZenWorldmap.getState().camera.scale')
        page.locator('[data-wm-zoom-in]').click();settle(page)
        assert page.evaluate('window.SutraZenWorldmap.getState().camera.scale')>scale
        # One transform on the full original artwork, SVG, fog and markers.
        geometry=page.evaluate('''()=>{const w=document.querySelector('.wm-world'),img=w.querySelector('img'),n=w.querySelector('.is-next'),r=w.getBoundingClientRect(),i=img.getBoundingClientRect();return {world:[r.width,r.height],art:[i.width,i.height],same:w.contains(n)&&w.contains(document.querySelector('.wm-fog-layer'))&&w.contains(document.querySelector('.wm-lines')),transform:getComputedStyle(w).transform}}''')
        assert geometry['same'] and abs(geometry['world'][0]-geometry['art'][0])<1 and abs(geometry['world'][1]-geometry['art'][1])<1,geometry
        current=page.evaluate('window.SutraZenWorldmap.getState().camera')
        page.wait_for_timeout(130)
        page.locator('[data-game-nav="city"]').click();page.wait_for_selector('.city-tactics-board')
        assert_shell(page)
        assert page.locator('button[data-city-review]').count()==0
        assert page.locator('[data-city-label="guardian"]').inner_text()=='念-守門人'
        page.locator('[data-city-label="guardian"]').click();page.wait_for_selector('#city-dialog[open]')
        assert page.locator('#city-dialog h2').inner_text()=='念-守門人'
        assert page.locator('#city-dialog [data-city-reread]').count()==0
        assert page.locator('#city-dialog [data-city-current]').count()==1
        page.locator('[data-city-close]').click()
        page.screenshot(path=str(OUT/f'city-{width}x{height}.png'))
        page.locator('[data-game-nav="shelf"]').click();page.wait_for_selector('#collection-books');assert_shell(page)
        assert page.locator('[data-collection-read]').count()==0
        page.screenshot(path=str(OUT/f'shelf-empty-{width}x{height}.png'))
        page.locator('[data-game-nav="map"]').click();wait_map(page)
        resume=page.evaluate('window.SutraZenWorldmap.getState().camera')
        assert all(abs(current[k]-resume[k])<.02 for k in ['x','y','scale']),(current,resume)
        page.reload();wait_map(page)
        reload=page.evaluate('window.SutraZenWorldmap.getState().camera')
        assert all(abs(resume[k]-reload[k])<.02 for k in ['x','y','scale']),(resume,reload)
        page.set_viewport_size({'width':height,'height':width});settle(page)
        rotated=page.evaluate('window.SutraZenWorldmap.getState().camera')
        assert abs(rotated['scale']-reload['scale'])<.001
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
        page.set_viewport_size({'width':width,'height':height});settle(page)
        page.locator('[data-wm-overview]').click();settle(page)
        fit=page.evaluate('window.SutraZenWorldmap.getState().camera')
        assert fit['overview'] and abs(fit['scale']-fit['fitScale'])<.00001,fit
        page.screenshot(path=str(OUT/f'map-overview-{width}x{height}.png'))
        page.locator('[data-wm-locate]').click();settle(page)
        page.screenshot(path=str(OUT/f'map-current-{width}x{height}.png'))
        samples.append({'viewport':[width,height],'shell':bounds,'dragSuppressedClick':True,'sameWorldTransform':geometry,'cameraTabAndReloadRestore':True,'fit':fit})
        context.close()
    # CDP two-finger input is browser simulation, never claimed as real Safari.
    context=context_for(browser,base,has_touch=True,viewport={'width':390,'height':844})
    page=context.new_page();observe(page,base,report);page.goto(base+'game/#map');wait_map(page)
    box=page.locator('.wm-viewport').bounding_box();x=box['x']+box['width']/2;y=box['y']+box['height']/2
    cdp=context.new_cdp_session(page);old=page.evaluate('window.SutraZenWorldmap.getState().camera.scale')
    def touch(kind,distance):cdp.send('Input.dispatchTouchEvent',{'type':kind,'touchPoints':[] if kind in ['touchEnd','touchCancel'] else [{'x':x-distance,'y':y,'id':1},{'x':x+distance,'y':y,'id':2}]})
    touch('touchStart',35);touch('touchMove',70);touch('touchEnd',0);settle(page)
    zoom=page.evaluate('window.SutraZenWorldmap.getState().camera.scale');assert zoom>old,(old,zoom)
    assert page.evaluate('visualViewport.scale')==1 and not page.locator('#wm-dialog').is_visible()
    touch('touchStart',35);touch('touchMove',50);touch('touchCancel',0);settle(page)
    assert page.locator('.wm-viewport').get_attribute('data-camera-gesture')=='none'
    assert not page.locator('#wm-dialog').is_visible()
    report['viewports']=samples;report['simulatedPinch']={'before':old,'after':zoom,'documentScale':1,'touchCancelWithoutEntry':True,'physicalDevice':False}
    context.close()


def settings_and_unavailable_storage(browser,base,report):
    context=context_for(browser,base,fixture([ORDER[0]],{ORDER[1]:4},ORDER[1]));page=context.new_page();observe(page,base,report)
    page.goto(base+'game/#map');wait_map(page)
    page.evaluate('localStorage.setItem("sutrazen.qa.unrelated","keep")')
    page.locator('[data-game-settings]').click();page.wait_for_selector('#game-settings[open]')
    before=snapshot(page)
    page.once('dialog',lambda dialog:dialog.dismiss());page.locator('[data-game-reset]').click();assert snapshot(page)==before
    with page.expect_download() as event:page.locator('[data-game-backup]').click()
    backup=json.loads(Path(event.value.path()).read_text())
    assert backup['completed']==[ORDER[0]],backup
    page.locator('[data-game-import]').set_input_files({'name':'invalid.json','mimeType':'application/json','buffer':b'{"bad":true}'})
    page.wait_for_function('document.querySelector("[data-game-settings-status]").textContent.includes("不是可用")')
    assert snapshot(page)==before
    page.once('dialog',lambda dialog:dialog.accept());page.locator('[data-game-reset]').click()
    assert snapshot(page) is None and page.evaluate('localStorage.getItem("sutrazen.qa.unrelated")')=='keep'
    page.locator('[data-game-import]').set_input_files({'name':'backup.json','mimeType':'application/json','buffer':json.dumps(backup).encode()})
    page.wait_for_function('document.querySelector("[data-game-settings-status]").textContent.includes("已還原")')
    assert snapshot(page)['completed']==[ORDER[0]] and snapshot(page)['positions'][ORDER[1]]==4
    page.locator('[data-game-settings-close]').click()
    assert page.locator('[data-game-settings]').evaluate('(n)=>n===document.activeElement')
    context.close()
    cases=[]
    for kind in ['corrupt','blocked']:
        context=context_for(browser,base)
        if kind=='blocked':context.add_init_script('Object.defineProperty(window,"localStorage",{get(){throw new DOMException("QA storage blocked","SecurityError")}})')
        else:context.add_init_script('if(!sessionStorage.getItem("qa.corrupt.seeded")){localStorage.setItem("'+KEY+'","{corrupt");sessionStorage.setItem("qa.corrupt.seeded","yes")}')
        page=context.new_page();observe(page,base,report);page.goto(base+'game/#map');wait_map(page)
        assert page.locator('#game-shell-storage-notice').is_visible()
        assert page.locator('[data-wm-next]').is_enabled()
        page.locator('[data-wm-next]').click();page.wait_for_selector('body[data-collection-book="four-truths"]')
        if page.locator('.collection-reader-storage[open]').count():page.locator('.collection-reader-storage button').click()
        click_next(page,1)
        assert page.locator('.sz-game-nav').count()==0
        cases.append({'storage':kind,'warningShown':True,'nativeNextStillReadable':True})
        context.close()
    report['settings']={'resetCancelPreserves':True,'nativeBackupAndRestore':True,'invalidRestorePreserves':True,'clearOnlyOwnKey':True,'focusRestored':True}
    report['storageFallbacks']=cases


def isolated_previews_and_continue_title(browser,base,report):
    saved=fixture([ORDER[0]],{ORDER[1]:4,ORDER[10]:6},ORDER[10])
    context=context_for(browser,base,saved);page=context.new_page();observe(page,base,report)
    page.goto(base+'game/');page.wait_for_selector('#game-title-screen:not([hidden])')
    assert page.locator('[data-title-start]').inner_text()=='繼續旅程'
    page.locator('[data-title-start]').click();wait_map(page)
    assert '/book/' not in page.url and page.locator('.wm-landmark.is-next').get_attribute('data-book')==ORDER[1]
    context.close()
    checks=[]
    for path,ready in [('play/visual-v2/','.network-island'),('play/city/inspection.html','.inspection-frame')]:
        context=context_for(browser,base,saved)
        context.add_init_script('''window.qaStorageTouches=0;for(const key of ['localStorage','sessionStorage'])Object.defineProperty(window,key,{get(){window.qaStorageTouches++;throw new DOMException('Readonly preview must not use storage','SecurityError')}})''')
        page=context.new_page();observe(page,base,report);page.goto(base+path);page.wait_for_selector(ready)
        assert page.evaluate('window.qaStorageTouches')==0,path
        assert page.locator('a[href*="collection=1"],button[data-collection-read],button[data-city-reread]').count()==0,path
        stored=context.storage_state()['origins'][0]['localStorage']
        original=next(x['value'] for x in stored if x['name']==KEY)
        assert json.loads(original)==saved
        checks.append({'path':path,'storageTouches':0,'gameReadingActions':0,'originalSaveRetained':True})
        context.close()
    report['continueTitle']={'existingSaveShowsContinue':True,'entersMapOnly':True,'futureActiveDoesNotOverrideMainline':True}
    report['isolatedPreviewChecks']=checks


def supplied_title_art(browser,base,report):
    asset=ROOT/'play/assets/CC1A7C32-0620-4DB2-BCD2-A9457A83C259.jpeg'
    digest=hashlib.sha256(asset.read_bytes()).hexdigest()
    assert digest=='fc7cb28c894890127a20fd1bb898d2448950d51be86c3b36200faa6c2ae523e9'
    assert Image.open(asset).size==(2752,1536)
    checks=[]
    for width,height in SIZES:
        context=context_for(browser,base,viewport={'width':width,'height':height})
        page=context.new_page();observe(page,base,report);requests=[];page.on('request',lambda request:requests.append(request.url))
        page.goto(base+'game/');page.wait_for_selector('#game-title-screen.is-art-loaded')
        page.wait_for_function('document.querySelector("[data-title-art]").naturalWidth===2752')
        assert page.locator('[data-title-heading]').inner_text()=='小貓的山海旅程'
        assert page.locator('[data-title-subtitle]').inner_text()=='佛法繪本探索遊戲'
        assert page.locator('[data-title-art-notice]').is_hidden()
        assert page.locator('[data-title-start]').is_visible()
        assert not any('/book/' in url or any('/'+book+'/assets/' in url for book in ORDER) for url in requests)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1 && document.documentElement.scrollHeight<=innerHeight+1')
        box=page.locator('[data-title-start]').bounding_box();assert box['width']>=48 and box['height']>=48
        page.screenshot(path=str(OUT/f'title-{width}x{height}.png'))
        checks.append({'viewport':[width,height],'naturalDimensions':[2752,1536],'bookDownloadsBeforeBegin':0})
        context.close()
    report['titleArt']={'requestedFile':asset.name,'specifiedArtVerified':True,'sha256':digest,'sourceDimensions':[2752,1536],'viewports':checks,'verification':'Author supplied original JPEG; no substitute artwork'}


def review_entry_positions(browser,base,report):
    checks=[]
    for entry in ['map','shelf','city']:
        for saved_at,expected in [(28,0),(5,5)]:
            context=context_for(browser,base,fixture([ORDER[0]],{ORDER[0]:saved_at,ORDER[1]:4},ORDER[1]))
            page=context.new_page();observe(page,base,report)
            if entry=='map':
                page.goto(base+'game/#map');wait_map(page)
                page.locator('.wm-secondary-tools > summary').click();page.locator('#wm-route-strip summary').click()
                page.locator('[data-wm-book="four-truths"]').click();page.wait_for_selector('#wm-dialog[open]')
                page.locator('[data-wm-read="four-truths"]').click()
            elif entry=='shelf':
                page.goto(base+'play/visual-v2/shelf.html');page.locator('[data-collection-read="four-truths"]').click()
            else:
                page.goto(base+'play/city/');page.locator('[data-city-label="dock"]').click();page.wait_for_selector('#city-dialog[open]')
                page.locator('[data-city-reread]').click()
            page.wait_for_selector(f'body[data-collection-index="{expected}"]')
            assert page.locator('body').get_attribute('data-collection-mode')=='review'
            page.reload();page.wait_for_selector(f'body[data-collection-index="{expected}"]')
            click_next(page,expected+1)
            assert snapshot(page)['completed']==[ORDER[0]]
            assert snapshot(page)['activeBook']==ORDER[1] and snapshot(page)['positions'][ORDER[1]]==4
            page.locator('.collection-reader-return').click();page.wait_for_selector('#collection-books')
            assert 'shelf' in page.url and 'completed=' not in page.url
            checks.append({'entry':entry,'savedReviewPosition':saved_at,'actualInitialPosition':expected,'reloadAndNext':True,'mainlineAndCountPreserved':True})
            context.close()
    report['reviewEntryPositions']=checks


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    report=protect_originals()
    report.update({'specification':'SutraZen_Game_Immersion_Codex_Prompt_2026-11-22.md, full224 lines read',
                   'phase':'Local review only; no publication claim',
                   'javascriptErrors':[],'httpErrors':[],
                   'titleArt':{'requestedFile':'CC1A7C32-0620-4DB2-BCD2-A9457A83C259.jpeg','specifiedArtVerified':False,'reason':'Attachment not yet available; title flow is independent of this missing-art acceptance'},
                   'physicalSafari':'Not tested; desktop Chromium input and viewport simulation only',
                   'historicalCoverage':'Prior1192-step original reader report retained; obsolete game free-reading expectations are not rewritten'})
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_port}/'
    try:
        with sync_playwright() as playwright:
            browser=playwright.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
            native_first_book(browser,base,report)
            print('Native first-book completion and review passed.',flush=True)
            locks_and_history(browser,base,report)
            print('Locks and history fixtures passed.',flush=True)
            camera_and_viewports(browser,base,report)
            print('Five viewport, pointer and camera restore checks passed.',flush=True)
            settings_and_unavailable_storage(browser,base,report)
            isolated_previews_and_continue_title(browser,base,report)
            supplied_title_art(browser,base,report)
            review_entry_positions(browser,base,report)
            assert not report['javascriptErrors'],report['javascriptErrors']
            assert not report['httpErrors'],report['httpErrors']
            report['result']='passed'
            browser.close()
    finally:server.shutdown()
    (OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'result':'passed','report':str((OUT/'validation.json').relative_to(ROOT))},ensure_ascii=False))


if __name__=='__main__':main()
