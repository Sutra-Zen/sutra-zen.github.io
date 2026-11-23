#!/usr/bin/env python3
"""Independent modular-city integration and native reading/browser evidence.

Only this round's preview directory is written. Native first29, historical
profiles, model probes and fault injections are reported separately.
"""
from pathlib import Path
import functools,http.server,importlib.util,json,re,subprocess,threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/previews/game-modular-city'
s=importlib.util.spec_from_file_location('mara_qa',ROOT/'scripts/check-game-mara-story.py');mara=importlib.util.module_from_spec(s);s.loader.exec_module(mara)
q=mara.q;d=mara.d;story=mara.story;cyan=mara.cyan
BASELINE='6bb59a61d5d045b87102989532a55dc814eafa42';q.BASE=BASELINE
CITY_KEY='sutrazen.play.city.v1';SIZES=q.SIZES


def context(browser,base,saved=None,seen=None,city=None,**options):
    entries=[]
    if saved is not None:entries.append({'name':q.KEY,'value':json.dumps(saved)})
    if seen is not None:entries.append({'name':mara.STORY_KEY,'value':json.dumps({'version':1,'seenSceneIds':seen})})
    if city is not None:entries.append({'name':CITY_KEY,'value':json.dumps(city)})
    if entries:options['storage_state']={'cookies':[],'origins':[{'origin':base.rstrip('/'),'localStorage':entries}]}
    return q.context_for(browser,base,**options)


def guard_sources():
    original_paths=q.ORDER+['docs/'+book for book in q.ORDER]+['index.html','shelf.css','sitemap.xml','robots.txt','googlee0c995331ec518ae.html','reader-controls.css','reader-layout.js','reader-restart.js','picture-panel-focus.js','picture-panel-focus.css','docs/seo','map-topic-resources.css','scripts/site_seo.py','scripts/build-seo.py','scripts/check-seo.py']
    html=[book+'/book/index.html' for book in q.ORDER];changed=subprocess.check_output(['git','diff','--name-only',BASELINE,'--',*original_paths],cwd=ROOT,text=True).splitlines();assert set(changed)<=set(html),changed
    baseline=lambda path:subprocess.check_output(['git','show',BASELINE+':'+path],cwd=ROOT,text=True)
    for path in html:
        before=baseline(path);after=(ROOT/path).read_text();tag=re.search(r'\.\./\.\./play/collection/reader-bridge\.js\?v=[^"\s]+',before).group()
        assert after.count('../../play/collection/reader-bridge.js?v=modular-city-1')==1,path
        assert after.replace('../../play/collection/reader-bridge.js?v=modular-city-1',tag)==before,path
    count=len([p for p in subprocess.check_output(['git','ls-tree','-rz','--name-only',BASELINE,'--',*original_paths],cwd=ROOT,text=True).split('\0') if p])
    report={'baseline':BASELINE,'protectedOriginalFiles':count,'fourteenReaderHtmlException':'Only collection bridge query; normalize each to its baseline then full text identical','originalBooksScriptureArtReaderJsCssHomepageSeoGoogle':'byte-for-byte unchanged'}
    paths=['play/collection/store.js','play/collection/reader.css','play/reader-bridge.js','play/route','play/prologue','play/story/store.js','play/story/completion-receipt.js','play/worldmap-v4/camera.js','play/worldmap-v4/data.js','play/visual-v2/network-data.js']
    paths += [p for p in subprocess.check_output(['git','ls-tree','-rz','--name-only',BASELINE,'--','play/story/assets','play/assets','play/visual-v2/assets','play/worldmap-v4/assets'],cwd=ROOT,text=True).split('\0') if p]
    changed=subprocess.check_output(['git','diff','--name-only',BASELINE,'--',*paths],cwd=ROOT,text=True).splitlines();assert not changed,changed
    report['additionalProtectedCoreAndExistingArt']=paths
    bridge=(ROOT/'play/collection/reader-bridge.js').read_text().replace("new URL('../../game/?v=modular-city-1', import.meta.url)","new URL('../../game/?v=mara-1', import.meta.url)");assert bridge==baseline('play/collection/reader-bridge.js')
    report['readerBridgeException']='Return cache query only; all other bytes identical'
    return report


def raw_storage(page):
    return page.evaluate('''()=>({local:Object.fromEntries(Object.entries(localStorage).sort()),session:Object.fromEntries(Object.entries(sessionStorage).sort())})''')


def city_raw(page):
    return page.evaluate('(key)=>JSON.parse(localStorage.getItem(key)||"null")',CITY_KEY)


def collection_raw(page):
    return page.evaluate('(key)=>localStorage.getItem(key)',q.KEY)


def no_overflow(page):
    result=page.evaluate('''()=>({screen:[innerWidth,innerHeight],outer:[document.documentElement.scrollWidth,document.documentElement.scrollHeight]})''')
    assert all(a<=b+1 for a,b in zip(result['outer'],result['screen'])),result
    assert '[object Object]' not in page.locator('body').inner_text()
    return result


def city_state(page):
    return page.evaluate('window.SutraZenModularCity.getState()')


def close_thought(page):
    button=page.locator('.city-thought:not([hidden]) [data-city-thought-close]')
    if button.is_visible():button.click();q.settle(page)


def city_ready(page,close_os=True):
    page.wait_for_selector('.mod-city');page.wait_for_function('window.SutraZenModularCity?.getState()?.modules?.length===14')
    page.evaluate('''async()=>{const urls=[...new Set([...document.querySelectorAll('.mod-city img,.mod-city image,.city-thought image')].map(n=>n instanceof HTMLImageElement?n.currentSrc||n.src:n.href.baseVal))];await Promise.all(urls.filter(Boolean).map(async url=>{const i=new Image();i.src=url;await i.decode()}))}''');q.settle(page)
    if close_os:close_thought(page)
    no_overflow(page)


def inventory_open(page):
    toggle=page.locator('[data-city-inventory-toggle]')
    if toggle.get_attribute('aria-expanded')!='true':toggle.click()
    page.wait_for_selector('.mod-city__drawer:not([hidden])')


def place_click(page,module):
    close_thought(page);inventory_open(page);card=page.locator(f'[data-city-inventory="{module}"]');card.scroll_into_view_if_needed();card.click();target=page.locator(f'[data-city-place="{module}"]');target.wait_for();target.click()
    page.wait_for_function('(id)=>window.SutraZenModularCity.getState().placedIds.includes(id)',arg=module)
    return city_state(page)


def goto_city(page,base,close_os=True):
    page.goto(base+'play/city/?v=modular-city-1#city');city_ready(page,close_os)


def inventory_close(page):
    if page.locator('[data-city-inventory-toggle]').get_attribute('aria-expanded')=='true':page.locator('[data-city-inventory-close]').click()


def fit_city(page):
    close_thought(page)
    if not page.evaluate('window.SutraZenModularCity.getCamera().camera.overview'):page.locator('#city-overview-toggle').click()
    page.wait_for_function('window.SutraZenModularCity.getCamera().camera.overview');q.settle(page)


def touch_path(page,ctx,start,end,steps=14):
    client=ctx.new_cdp_session(page)
    def points(x,y):return [{'x':x,'y':y,'radiusX':2,'radiusY':2,'force':1,'id':1}]
    client.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':points(*start)})
    for index in range(1,steps+1):
        x=start[0]+(end[0]-start[0])*index/steps;y=start[1]+(end[1]-start[1])*index/steps
        client.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':points(x,y)});page.wait_for_timeout(18)
    client.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});client.detach();q.settle(page)


def dependency_and_drag(browser,base,report):
    cases=[]
    # Three historically completed books own the modules, but no city is built.
    saved=q.fixture(q.ORDER[:3],{},q.ORDER[3]);ctx=context(browser,base,saved);page=ctx.new_page();q.observe(page,base,report);goto_city(page,base)
    initial=city_state(page);assert initial['placedIds']==[] and sum(m['unlocked'] for m in initial['modules'])==3
    six=next(m for m in initial['modules'] if m['id']=='six_gates');assert six['unlocked'] and not six['canPlace'] and six['missingModuleIds']==['city_body']
    reading=collection_raw(page);place_click(page,'city_body');inventory_open(page);card=page.locator('[data-city-inventory="six_gates"]');card.scroll_into_view_if_needed();card.click();q.settle(page)
    source=card.bounding_box();target=page.locator('[data-city-place="six_gates"]').bounding_box();assert source and target
    page.mouse.move(source['x']+source['width']/2,source['y']+source['height']/2);page.mouse.down();page.mouse.move(target['x']+target['width']/2,target['y']+target['height']/2,steps=18);page.mouse.up()
    page.wait_for_function('window.SutraZenModularCity.getState().placedIds.includes("six_gates")');close_thought(page)
    assert page.locator('.mod-city__art-layer [data-city-module="six_gates"]').count()==6 and page.locator('[data-city-actor="guardian"]').count()==0 and collection_raw(page)==reading
    inventory_close(page);fit_city(page);page.screenshot(path=str(OUT/'historical-three-native-drag-six-gates-1280x900.png'));page.reload();city_ready(page);page.set_viewport_size({'width':360,'height':800});q.settle(page)
    assert city_state(page)['placedIds']==['city_body','six_gates'] and page.locator('.mod-city__art-layer [data-city-module="six_gates"]').count()==6
    cases.append({'fixture':'historical first3, no city layout','ownedNotPlaced':True,'sixGatesWaitForBodyPlacement':True,'nativeClickBodyThenMouseDragSixToPlus':True,'sixSeparateGateArtSlots':6,'guardianStillAbsent':True,'reloadAndRotateKeepsPlacedIds':['city_body','six_gates'],'collectionBytesUnchanged':True});ctx.close()
    saved=q.fixture(q.ORDER[:7],{},q.ORDER[7]);city={'version':1,'placedIds':['city_body','six_gates'],'thoughtSeenIds':['city-lord-introduction']};ctx=context(browser,base,saved,city=city);page=ctx.new_page();q.observe(page,base,report);goto_city(page,base)
    assert page.locator('[data-city-actor="guardian"]').count()==0;reading=collection_raw(page);place_click(page,'mindfulness_guard')
    assert page.locator('[data-city-actor="guardian"]').count()==1 and collection_raw(page)==reading
    close_thought(page);inventory_close(page);fit_city(page);page.screenshot(path=str(OUT/'historical-mindfulness-hand-placed-one-guardian-1280x900.png'))
    cases.append({'fixture':'historical first7, body+gates already placed','guardianOnlyAfterActualMindfulnessPlacement':True,'guardianActorCount':1,'collectionBytesUnchanged':True});ctx.close()
    # A known-but-unearned layout from a restore cannot reveal an unread module.
    saved=q.fixture([q.ORDER[12]],{},q.ORDER[0]);city={'version':1,'placedIds':['awakening_companions'],'thoughtSeenIds':[]};ctx=context(browser,base,saved,city=city);page=ctx.new_page();q.observe(page,base,report);goto_city(page,base)
    result=city_state(page);assert not result['baseVisible'] and result['placedIds']==[] and result['savedPlacedIds']==['awakening_companions']
    awake=next(m for m in result['modules'] if m['id']=='awakening_companions');assert awake['unlocked'] and not awake['canPlace'];inventory_open(page);assert page.locator('[data-city-place-all]').is_disabled()
    assert q.snapshot(page)==saved and page.locator('[data-city-actor="guardian"]').count()==0
    cases.append({'fixture':'only historical book13 with deferred saved placement','ownedRetainedWithoutInventingPrerequisiteReadingOrBuildings':True,'effectivePlacedEmpty':True,'autoPlaceDisabledWithoutBase':True});ctx.close()
    # Real touch scroll and vertical DND, through the integrated app callbacks.
    saved=q.fixture(['four-truths'],{},'five-aggregates');ctx=context(browser,base,saved,viewport={'width':360,'height':800},has_touch=True,is_mobile=True);page=ctx.new_page();q.observe(page,base,report);goto_city(page,base);inventory_open(page)
    tray=page.locator('.mod-city__inventory-list');bounds=tray.bounding_box();assert bounds
    for _ in range(12):
        state=tray.evaluate('(n)=>({left:n.scrollLeft,max:n.scrollWidth-n.clientWidth})')
        if state['left']>=state['max']-2:break
        touch_path(page,ctx,(bounds['x']+bounds['width']-15,bounds['y']+bounds['height']/2),(bounds['x']+15,bounds['y']+bounds['height']/2));page.wait_for_timeout(100)
    last=page.locator('[data-city-inventory="fruition_guide"]').bounding_box();assert last and bounds['x']<=last['x']+last['width']/2<=bounds['x']+bounds['width'] and city_state(page)['placedIds']==[]
    card=page.locator('[data-city-inventory="truth_dock"]');card.scroll_into_view_if_needed();card.tap();q.settle(page);source=card.bounding_box();target=page.locator('[data-city-place="truth_dock"]').bounding_box();reading=collection_raw(page)
    touch_path(page,ctx,(source['x']+source['width']/2,source['y']+source['height']/2),(target['x']+target['width']/2,target['y']+target['height']/2))
    page.wait_for_function('window.SutraZenModularCity.getState().placedIds.includes("truth_dock")');assert collection_raw(page)==reading and page.locator('.mod-city__drag-ghost').count()==0
    cases.append({'fixture':'first done, phone touch','nativeHorizontalTraySwipeReachesLastCardWithoutPlacement':True,'nativeVerticalTouchDragTruthToPlusPersistsExactlyOnce':True,'ghostRemoved':True,'collectionBytesUnchanged':True});ctx.close()
    report['historicalDependencyAndNativeDrag']=cases


def os_geometry(page):
    panel=page.locator('.city-thought:not([hidden])');panel.wait_for();box=panel.bounding_box();dock=page.locator('.game-dock').bounding_box()
    assert box['x']>=0 and box['y']>=0 and box['x']+box['width']<=page.viewport_size['width']+1 and box['y']+box['height']<dock['y'],(box,dock)
    for selector in ['[data-city-thought-close]','[data-city-thought-change]']:
        button=panel.locator(selector);button.scroll_into_view_if_needed();r=button.bounding_box();assert r['height']>=48 and r['width']>=48,r
    assert panel.locator('.city-thought__line').evaluate('(n)=>parseFloat(getComputedStyle(n).fontSize)')>=16
    no_overflow(page);return box


def five_size_os_and_camera(browser,base,report):
    cases=[]
    for width,height in SIZES:
        saved=q.fixture(['four-truths'],{},'five-aggregates');ctx=context(browser,base,saved,viewport={'width':width,'height':height});page=ctx.new_page();q.observe(page,base,report);goto_city(page,base,close_os=False)
        page.wait_for_selector('.city-thought[data-actor="lord"]:not([hidden])');lord=os_geometry(page);page.screenshot(path=str(OUT/f'lord-screen-thought-{width}x{height}.png'));close_thought(page);fit_city(page)
        page.locator('[data-city-actor="mara"]').click();page.wait_for_selector('.city-thought[data-actor="mara"]:not([hidden])');mara_box=os_geometry(page);reading=collection_raw(page)
        page.locator('#city-overview-toggle').click();page.wait_for_function('!window.SutraZenModularCity.getCamera().camera.overview');q.settle(page);after=os_geometry(page)
        assert abs(mara_box['x']-after['x'])<1 and abs(mara_box['y']-after['y'])<1 and collection_raw(page)==reading
        page.screenshot(path=str(OUT/f'mara-screen-thought-camera-independent-{width}x{height}.png'));close_thought(page)
        page.locator('[data-city-actor="lord"]').click();page.wait_for_selector('.city-thought[data-actor="lord"]:not([hidden])');os_geometry(page);close_thought(page)
        static=page.locator('.mod-city__npc .mod-city__actor-art,.mod-city__sweat').evaluate_all('(nodes)=>nodes.map(n=>getComputedStyle(n).animationName)');assert static and all(name=='none' for name in static),static
        cases.append({'viewport':[width,height],'actualLordThenMaraActorClick':True,'lordPanel':lord,'maraPanelBeforeCamera':mara_box,'maraPanelAfterCamera':after,'screenSpaceReadableAndAboveDock':True,'overviewReturnsToExploration':True,'reducedMotionStopsNpcAndSweat':True,'collectionUnchangedByOsAndCamera':True});ctx.close()
    report['fiveViewportOsAndCamera']=cases


def settings_open(page):
    button=page.locator('[data-game-settings]');button.focus();button.click();page.wait_for_selector('#game-settings[open]')


def upload_backup(page,value):
    page.locator('[data-game-import]').set_input_files({'name':'qa-journey.json','mimeType':'application/json','buffer':json.dumps(value,ensure_ascii=False).encode()})
    page.wait_for_function('document.querySelector("[data-game-import]").value===""')
    return page.locator('[data-game-settings-status]').inner_text()


def all_read_autoplace_and_backups(browser,base,report):
    saved=q.fixture(q.ORDER,{},q.ORDER[0]);ctx=context(browser,base,saved);page=ctx.new_page();q.observe(page,base,report);goto_city(page,base)
    initial=city_state(page);assert len(initial['modules'])==14 and len({m['id'] for m in initial['modules']})==14 and sum(m['unlocked'] for m in initial['modules'])==14 and initial['placedIds']==[]
    assert page.locator('[data-city-actor="guardian"]').count()==0;reading=collection_raw(page);inventory_open(page);page.locator('[data-city-place-all]').click();page.wait_for_function('window.SutraZenModularCity.getState().placedIds.length===14');close_thought(page)
    result=city_state(page);assert len(set(result['placedIds']))==14 and collection_raw(page)==reading
    assert page.locator('[data-city-actor="guardian"]').count()==1 and page.locator('.mod-city__art-layer [data-city-module="six_gates"]').count()==6
    companions=['awakening-owl','awakening-rabbit','awakening-bird','awakening-turtle','awakening-lotus','awakening-deer']
    assert all(page.locator(f'[data-city-slot="{slot}"]').count()==1 for slot in companions)
    assert page.locator('[data-city-slot="awakening-mindfulness"] svg').count()==0
    assert page.locator('[data-city-place-all]').is_disabled();inventory_close(page);fit_city(page);page.screenshot(path=str(OUT/'historical-all14-explicit-autoplace-1280x900.png'))
    page.locator('[data-city-actor="lord"]').click();page.wait_for_selector('.city-thought[data-actor="lord"]:not([hidden])');os_geometry(page);close_thought(page)
    page.evaluate('''()=>{localStorage.setItem('qa.modular.keep-local','retained');sessionStorage.setItem('qa.modular.keep-session','retained')}''');settings_open(page)
    with page.expect_download() as download:page.locator('[data-game-backup]').click()
    file=download.value;path='/tmp/modular-city-journey-v2-qa.json';file.save_as(path);backup=json.loads(Path(path).read_text())
    assert backup['format']=='sutrazen.journey' and backup['version']==2 and backup['collection']['completed']==q.ORDER and backup['city']['placedIds']==result['placedIds']
    before=raw_storage(page);invalid=json.loads(json.dumps(backup));invalid['city']['placedIds']=['unknown-module'];status=upload_backup(page,invalid)
    assert raw_storage(page)==before and ('不是' in status or '無法' in status),status
    page.once('dialog',lambda dialog:dialog.dismiss());page.locator('[data-game-reset]').click();assert raw_storage(page)==before
    page.once('dialog',lambda dialog:dialog.accept());page.locator('[data-game-reset]').click();page.wait_for_function('window.SutraZenModularCity.getState().placedIds.length===0&&!window.SutraZenModularCity.getState().baseVisible')
    assert q.snapshot(page) is None;assert page.evaluate('localStorage.getItem("qa.modular.keep-local")')=='retained' and page.evaluate('sessionStorage.getItem("qa.modular.keep-session")')=='retained'
    status=upload_backup(page,backup);page.wait_for_function('window.SutraZenModularCity.getState().placedIds.length===14');assert q.snapshot(page)==backup['collection'] and city_raw(page)['placedIds']==backup['city']['placedIds']
    assert page.locator('.mod-city').count()==1 and page.locator('[data-city-actor="guardian"]').count()==1
    legacy=q.fixture(['four-truths'],{'five-aggregates':4},'five-aggregates');upload_backup(page,legacy);page.wait_for_function('window.SutraZenModularCity.getState().placedIds.length===0');assert q.snapshot(page)==legacy
    assert city_state(page)['baseVisible'] and page.locator('[data-city-actor="guardian"]').count()==0
    page.locator('[data-game-settings-close]').click();page.locator('#city-continue').click();page.wait_for_selector('body[data-collection-book="five-aggregates"][data-collection-index="4"]')
    assert q.snapshot(page)['completed']==['four-truths']
    report['historicalAllReadAndBackupUi']={'fixture':'all14 historical completions, no city key','initialOwned':14,'initialPlaced':0,'nativePlaceAllOnlyOwnedAndDependencies':result['placedIds'],'noCollectionWriteFromPlacement':True,'sixGates':6,'guardianActorExactlyOne':True,'sixNonMindfulnessCompanions':companions,'awakeningMindfulnessOnlyGlowNoSecondGuardianSprite':True,'duplicatePlaceAllDisabled':True,'actualLordActorClick':True,'nativeDownloadedBackupFormat':'sutrazen.journey v2','invalidCityBackupNoPartialMutation':True,'settingsResetCancelAllStorageByteIdentical':True,'settingsResetClearsCityAndReadingOnly':True,'newV2RestoreReturnsAllPlacementsAndReading':True,'legacyV1RestoreClearsCityAndKeepsExactReading':True,'legacyFiveBookmarkStillReadableWithNoConstruction':True,'unrelatedLocalAndSessionKeysPreserved':True};ctx.close()


def author_reset_and_ui_failures(browser,base,report):
    saved=q.fixture(q.ORDER,{},q.ORDER[0]);city={'version':1,'placedIds':['truth_dock','city_body','six_gates'],'thoughtSeenIds':['city-lord-introduction','mara-at-city']};local={q.KEY:json.dumps(saved),CITY_KEY:json.dumps(city),'qa.modular.keep-local':'retained','sutrazen.reader.position':'retained'}
    ctx=story.prior.context(browser,base,local,{'qa.modular.keep-session':'retained'});page=ctx.new_page();q.observe(page,base,report);page.goto(base+'game/?author=1&v=modular-city-1');story.prior.assert_copy(page);story.prior.skip(page);before=raw_storage(page)
    page.once('dialog',lambda dialog:dialog.dismiss());page.locator('[data-title-author-reset]').click();assert raw_storage(page)==before
    page.once('dialog',lambda dialog:dialog.accept());page.locator('[data-title-author-reset]').click();story.prior.assert_copy(page);story.prior.skip(page)
    assert city_raw(page) is None and q.snapshot(page) is None and page.evaluate('localStorage.getItem("qa.modular.keep-local")')=='retained' and page.evaluate('localStorage.getItem("sutrazen.reader.position")')=='retained'
    page.locator('[data-title-start]').click();d.map_ready(page);story.assert_scene(page,'arrival-at-wheel');page.locator('[data-game-nav="city"]').click();city_ready(page);assert not city_state(page)['baseVisible'] and city_state(page)['placedIds']==[]
    reset={'nativeAuthorCancelByteIdentical':True,'confirmClearsLoadedCityStoreAndReading':True,'freshFirstArrivalAndGrassOnlyCity':True,'publicReaderAndUnrelatedKeysPreserved':True};ctx.close()
    saved=q.fixture(['four-truths'],{},'five-aggregates');ctx=context(browser,base,saved)
    ctx.add_init_script('''{const set=Storage.prototype.setItem;Storage.prototype.setItem=function(key,value){if(this===window.localStorage&&key==='sutrazen.play.city.v1')throw new DOMException('QA city quota','QuotaExceededError');return set.call(this,key,value)}}''')
    page=ctx.new_page();q.observe(page,base,report);goto_city(page,base);reading=collection_raw(page);place_click(page,'truth_dock');inventory_open(page);assert page.locator('.mod-city__storage-note').is_visible()
    assert city_raw(page) is None;page.reload();city_ready(page);assert city_state(page)['placedIds']==['truth_dock'] and city_state(page)['persistence']=='session' and collection_raw(page)==reading
    quota={'cityLocalWriteDeniedOnly':True,'actualPlacementContinuesWithWarning':True,'sameTabSessionFallbackRestoresPlacementOnReload':True,'readingUnchanged':True};ctx.close()
    report['authorResetAndStorageFailure']={'authorReset':reset,'quotaUi':quota}


def art_retry_persistent_failure(browser,base,report):
    saved=q.fixture(['four-truths'],{},'five-aggregates');ctx=context(browser,base,saved);page=ctx.new_page();failures=[]
    def unavailable(route):failures.append(route.request.url);route.fulfill(status=404,content_type='text/plain',body='QA intentionally missing atlas')
    # This atlas affects a placed/thumbnail asset while the ground keeps working.
    page.route('**/play/city/modules/assets/buildings-atlas-concept.png',unavailable);page.on('pageerror',lambda error:report['javascriptErrors'].append(str(error)))
    page.goto(base+'play/city/?v=modular-city-1#city');page.wait_for_selector('.mod-city__art-notice:not([hidden])');close_thought(page);reading=collection_raw(page)
    count=len(failures);page.locator('[data-city-art-retry]').click();page.wait_for_function('!document.querySelector(".mod-city__art-notice").hidden');page.wait_for_timeout(150)
    assert len(failures)>count and collection_raw(page)==reading
    report['artRetryFailure']={'expectedInjected404Url':'buildings-atlas-concept.png','requests':len(failures),'retryStillShowsHonestNotice':True,'groundNotBlocked':True,'collectionUnchanged':True};ctx.close()


def ordinary_motion_and_original_site(browser,base,report):
    saved=q.fixture(['four-truths'],{},'five-aggregates');ctx=context(browser,base,saved,reduced_motion='no-preference');page=ctx.new_page();q.observe(page,base,report);goto_city(page,base);reading=collection_raw(page)
    motion=page.evaluate('''async()=>{const ids=['desire','anger','sloth','restlessness','doubt'];const data=Object.fromEntries(ids.map(id=>[id,[]]));const sweat=[];for(let i=0;i<42;i++){for(const id of ids){const n=document.querySelector(`[data-city-actor="${id}"] .mod-city__actor-art`),s=getComputedStyle(n),m=new DOMMatrixReadOnly(s.transform);data[id].push(Math.atan2(m.b,m.a)*180/Math.PI)}sweat.push(...[...document.querySelectorAll('.mod-city__sweat')].map(n=>Number(getComputedStyle(n).opacity)));await new Promise(r=>setTimeout(r,100))}return {data,sweatMax:Math.max(...sweat),sweatMin:Math.min(...sweat)}}''')
    summary={}
    for actor,angles in motion['data'].items():
        assert max(map(abs,angles))<=3.1 and max(angles)-min(angles)>.25,(actor,angles)
        summary[actor]={'minDegrees':min(angles),'maxDegrees':max(angles)}
    assert motion['sweatMax']>.25 and motion['sweatMin']<.1 and collection_raw(page)==reading,motion
    report['normalMotion']={'sampleDurationSeconds':4.2,'actualComputedRotation':summary,'allFiveWithinPlusMinus3Degrees':True,'lordSweatOpacityRange':[motion['sweatMin'],motion['sweatMax']],'collectionUnchanged':True};ctx.close()
    # Original-page external CDN assets use the managed proxy; this exception
    # affects this isolated browser's inspection only, never website TLS config.
    ctx=context(browser,base,ignore_https_errors=True);page=ctx.new_page();q.observe(page,base,report);page.goto(base);page.wait_for_selector('#map-heading');assert page.locator('#books a.sz-book.sz-ready').count()==14
    count=page.evaluate('Object.keys(dhammaData).length');assert count==32,count
    page.locator('button[onclick="openModal(\'道路總說\')"]').click();page.wait_for_selector('#detailModal:not(.hidden)');assert page.locator('#detailModal a').count()>=3
    page.locator('#detailModal').get_by_role('button',name='關閉',exact=True).last.click();page.wait_for_selector('#detailModal.hidden',state='attached')
    checks=[]
    for book in q.ORDER[:3]:
        page.goto(base+book+'/book/');page.wait_for_selector('#next');page.wait_for_function('!document.querySelector("#next").disabled')
        before=page.locator('body').inner_text();page.locator('#next').click();page.wait_for_function('(text)=>document.body.innerText!==text',arg=before)
        links=page.locator('.reading-links a');assert links.count()==2 and links.nth(0).inner_text()=='閱讀原經' and links.nth(1).inner_text()=='回修道地圖'
        assert links.nth(1).get_attribute('href')=='../../index.html'
        assert page.evaluate('(keys)=>keys.every(k=>localStorage.getItem(k)===null)',[q.KEY,CITY_KEY])
        assert not page.locator('body').evaluate('(n)=>n.classList.contains("game-shell")')
        checks.append({'book':book,'nativeNextWorks':True,'originalSourceMapLinks':True,'noGameShellOrGameStorageWrites':True})
    report['originalWebsiteSmoke']={'homepageMapAnchorAndModal':True,'readableShelfBooks':14,'mindMapTopicKeys':32,'bareOriginalReaders':checks,'proxyHttpsExceptionForOriginalExternalCdnOnly':True};ctx.close()


def native_first_and_dock(browser,base,report):
    ctx=context(browser,base,reduced_motion='no-preference');page=ctx.new_page();q.observe(page,base,report);page.goto(base+'game/?v=modular-city-1#map');d.map_ready(page)
    for scene_id in list(story.LINES)[:3]:story.assert_scene(page,scene_id);page.locator('.story-dialogue__next').click()
    page.wait_for_selector('body[data-collection-index="0"]');trace=[0]
    for index in range(1,29):q.click_next(page,index);trace.append(index)
    assert q.snapshot(page)['completed']==[];page.locator('#next').click();d.map_ready(page)
    for scene_id in ['first-book-insight','doubt-recedes']:story.assert_scene(page,scene_id);page.locator('.story-dialogue__next').click()
    mara.mara_snapshot(page);page.locator('.story-dialogue__next').click();page.wait_for_selector('#wm-dialog[open]');page.locator('.wm-completion-actions a').click();city_ready(page)
    initial=city_state(page);assert initial['baseVisible'] and initial['placedIds']==[]
    assert page.locator('[data-city-slot="four-elements-garden"]').count()==1 and page.locator('[data-city-actor="lord"]').count()==1
    assert page.locator('[data-city-module="six_gates"]').count()==0 and page.locator('[data-city-actor="guardian"]').count()==0
    page.screenshot(path=str(OUT/'native-first-city-base-unplaced-1280x900.png'));reading=collection_raw(page);placed=place_click(page,'truth_dock');assert placed['placedIds']==['truth_dock'] and collection_raw(page)==reading
    assert page.locator('[data-city-slot="truth-dock"]').count()==1;page.screenshot(path=str(OUT/'native-truth-dock-hand-placed-1280x900.png'));page.reload();city_ready(page);assert city_state(page)['placedIds']==['truth_dock']
    page.locator('[data-game-nav="map"]').click();d.map_ready(page);page.locator('[data-wm-next]').click();cyan.new_scene_snapshot(page);page.locator('.story-dialogue__next').click();page.wait_for_selector('body[data-collection-book="five-aggregates"][data-collection-index="0"]')
    for index in [1,2,3]:q.click_next(page,index)
    page.reload();page.wait_for_selector('body[data-collection-index="3"]');page.set_viewport_size({'width':360,'height':800});page.locator('.collection-reader-return').click();d.map_ready(page);assert q.snapshot(page)['completed']==['four-truths'] and '4／54' in page.locator('[data-wm-next]').inner_text()
    page.locator('[data-game-nav="city"]').click();city_ready(page);assert city_state(page)['placedIds']==['truth_dock'];page.screenshot(path=str(OUT/'native-city-persists-after-reading-360x800.png'))
    report['nativeFirstAndHandPlacement']={'firstBookActualNextTrace':trace,'maraStorylineAndOriginalRewardPreserved':True,'firstCompletionCreatesFreeGardenAndLordButNoPlacedReward':True,'sixGatesAndGuardianAbsent':True,'nativeClickTruthDockCardThenPlus':True,'placedIds':['truth_dock'],'collectionBytesUnchangedByPlacement':True,'placementReloadPersists':True,'fiveActualNextTrace':[0,1,2,3],'fiveReloadRotateReturnResumesIndex':3,'cityPlacementSurvivesReaderRoundTrip':True};ctx.close()


def save(report):
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')


def main():
    OUT.mkdir(parents=True,exist_ok=True);report=guard_sources();report.update({'phase':'Local integrated modular city validation','javascriptErrors':[],'httpErrors':[],'physicalSafari':'Not tested; Chromium desktop viewport, mouse and CDP touch simulation','fixtureNotice':'Only nativeFirstAndHandPlacement is a full native first29 walk. Historical/placement/reset/backup/failure cases are isolated synthetic profiles, not claims of reading all14.'})
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(q.Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);native_first_and_dock(browser,base,report);dependency_and_drag(browser,base,report);five_size_os_and_camera(browser,base,report);all_read_autoplace_and_backups(browser,base,report);author_reset_and_ui_failures(browser,base,report);art_retry_persistent_failure(browser,base,report);ordinary_motion_and_original_site(browser,base,report);browser.close()
        assert not report['javascriptErrors'],report['javascriptErrors'];assert not report['httpErrors'],report['httpErrors'];report['result']='passed'
    except Exception as error:report['result']='failed';report['error']=repr(error);raise
    finally:server.shutdown();save(report)
    print(json.dumps({'result':report['result'],'report':str(OUT/'validation.json')},ensure_ascii=False))


if __name__=='__main__':main()
