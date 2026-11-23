#!/usr/bin/env python3
"""Automatic city presentation: original reading, labelled histories and UI."""
from pathlib import Path
import functools,http.server,importlib.util,json,re,subprocess,threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/previews/game-auto-city'
s=importlib.util.spec_from_file_location('outro_qa',ROOT/'scripts/check-game-outro-order.py');outro=importlib.util.module_from_spec(s);s.loader.exec_module(outro)
city=outro.city;q=outro.q;d=outro.d;story=outro.story;mara=outro.mara;cyan=outro.cyan
BASELINE='1ba30cfb016ed6affaefe1a62ee6ae9d1678efd9';VERSION='auto-city-1';SIZES=q.SIZES
MODULE_IDS=['truth_dock','city_body','six_gates','conditions_wheel','noble_path','confidence_harbor','mindfulness_guard','effort_garden','calm_insight_messengers','endeavor_boat','jhana_garden','faculties_links','awakening_companions','fruition_guide']
REMOVED_SELECTORS='[data-city-inventory-toggle],[data-city-inventory],[data-city-place],[data-city-place-all],[data-city-auto-place],[data-city-select-module],[data-city-thought-change],#city-label-toggle,#city-meaning-index,#city-thought-open,#city-placement-count,.city-tools,.mod-city__drag-ghost'
REMOVED_COPY=['繼續佈置','換個人想什麼','（心想）','(心想)','安置模組','待安置','已安置','自動安置','點選模組','＋']


def guard_sources():
    originals=q.ORDER+['docs/'+book for book in q.ORDER]+['index.html','shelf.css','sitemap.xml','robots.txt','googlee0c995331ec518ae.html','reader-controls.css','reader-layout.js','reader-restart.js','picture-panel-focus.js','picture-panel-focus.css','docs/seo','map-topic-resources.css','scripts/site_seo.py','scripts/build-seo.py','scripts/check-seo.py']
    html=[book+'/book/index.html' for book in q.ORDER];changed=subprocess.check_output(['git','diff','--name-only',BASELINE,'--',*originals],cwd=ROOT,text=True).splitlines();assert set(changed)<=set(html),changed
    before=lambda path:subprocess.check_output(['git','show',BASELINE+':'+path],cwd=ROOT,text=True)
    for path in html:
        old=before(path);new=(ROOT/path).read_text();tag=lambda text:re.search(r'\.\./\.\./play/collection/reader-bridge\.js\?v=[^"\s]+',text).group();assert new.replace(tag(new),tag(old))==old,path
    protected=['play/collection/store.js','play/collection/reader.css','play/reader-bridge.js','play/route','play/prologue','play/story/completion-receipt.js','play/story/assets','play/worldmap-v4/camera.js','play/worldmap-v4/data.js','play/visual-v2/network-data.js','play/visual-v2/assets','play/worldmap-v4/assets','play/assets','play/city/modules/assets']
    changed=subprocess.check_output(['git','diff','--name-only',BASELINE,'--',*protected],cwd=ROOT,text=True).splitlines();assert not changed,changed
    bridge=(ROOT/'play/collection/reader-bridge.js').read_text();bridge=re.sub(r"new URL\('../../game/\?v=[^']+', import.meta.url\)","new URL('../../game/?v=outro-order-1', import.meta.url)",bridge);assert bridge==before('play/collection/reader-bridge.js')
    for path in ['play/story/data.js','play/story/store.js','play/story/dialogue.js']:
        normalize=lambda text:re.sub(r'\?v=auto-city-1','?v=outro-order-1',text)
        assert normalize((ROOT/path).read_text())==before(path),path
    count=len([p for p in subprocess.check_output(['git','ls-tree','-rz','--name-only',BASELINE,'--',*originals],cwd=ROOT,text=True).split('\0') if p])
    return {'baseline':BASELINE,'protectedOriginalFiles':count,'originalSiteNarrationScripturePicturesReaderJsCssSeoGoogle':'unchanged; reader HTML only bridge cache query normalized','readingReceiptEligibilityCameraAndExistingArt':'byte-for-byte unchanged','storyOutroLogic':'unchanged except cache import queries','bridgeException':'return cache query only'}


def context(browser,base,saved=None,seen=None,layout=None,**options):
    return city.context(browser,base,saved,seen,city=layout,**options)


def collection_raw(page):return city.collection_raw(page)
def state(page):return page.evaluate('window.SutraZenModularCity.getState()')
def camera(page):return page.evaluate('window.SutraZenModularCity.getCamera().camera')
def visible_ids(page):
    value=state(page);return value.get('visibleIds',value.get('placedIds'))


def close_thought(page):
    close=page.locator('.city-thought:not([hidden]) [data-city-thought-close]')
    if close.is_visible():close.click();q.settle(page)


def ready_city(page):
    page.wait_for_selector('.mod-city');page.wait_for_function('window.SutraZenModularCity?.getState()?.modules?.length===14')
    page.evaluate('''async()=>{const urls=[...new Set([...document.querySelectorAll('.mod-city img,.mod-city image,.city-thought image')].map(n=>n instanceof HTMLImageElement?n.currentSrc||n.src:n.href.baseVal))];await Promise.all(urls.filter(Boolean).map(async url=>{const i=new Image();i.src=url;await i.decode()}))}''');q.settle(page);assert not page.locator('.city-thought').is_visible(),'City entry must not force an actor popup';assert_clean_city(page)


def goto_city(page,base):page.goto(base+'play/city/?v='+VERSION+'#city');ready_city(page)


def assert_clean_city(page):
    assert page.locator(REMOVED_SELECTORS).count()==0,'Removed controls still in player DOM'
    text=page.locator('body').inner_text()
    for phrase in REMOVED_COPY:assert phrase not in text,phrase
    city.no_overflow(page)
    dock=page.locator('.game-dock').bounding_box();viewport=page.locator('.mod-city__viewport').bounding_box();assert viewport['y']<5 and viewport['height']>=dock['y']-3,(viewport,dock)
    assert page.locator('[data-game-nav="city"].is-active').count()==1
    return {'viewport':viewport,'dock':dock}


def click_actor_and_close(page,actor='lord',capture=None):
    page.locator(f'[data-city-actor="{actor}"]').click();panel=page.locator(f'.city-thought[data-actor="{actor}"]:not([hidden])');panel.wait_for()
    assert '心想' not in panel.inner_text() and panel.locator('button').count()==1
    close=panel.locator('[data-city-thought-close]');target=close.bounding_box();assert target['width']>=48 and target['height']>=48
    assert close.inner_text() in ['×','✕','✖'];box=panel.bounding_box();dock=page.locator('.game-dock').bounding_box();assert box['y']+box['height']<dock['y']
    if capture:page.screenshot(path=str(OUT/capture))
    close.click();assert not panel.is_visible();assert_clean_city(page)


def plaza_source_and_close(page):
    plaza=page.locator('[data-city-inspect="plaza"]');plaza.wait_for();rect=plaza.bounding_box();plaza.click(position={'x':rect['width']*.2,'y':rect['height']*.3})
    page.wait_for_selector('#city-dialog[open]');text=page.locator('#city-dialog').inner_text();assert 'SN' in text or '相應部' in text;assert '四大' in text
    close=page.locator('[data-city-close]');assert close.is_visible();close.click();page.wait_for_selector('#city-dialog:not([open])',state='attached');assert_clean_city(page)


def overview_return(page,label='fixture-overview'):
    before=camera(page);page.locator('#city-overview-toggle').click();page.wait_for_function('window.SutraZenModularCity.getCamera().camera.overview');q.settle(page)
    # Contract confirmed by root when implementation is ready.
    back=page.locator('#city-overview-return');back.wait_for();page.screenshot(path=str(OUT/f'{label}-{page.viewport_size["width"]}x{page.viewport_size["height"]}.png'));back.click();q.settle(page);after=camera(page)
    for key in ['x','y','scale']:assert abs(before[key]-after[key])<.05,(before,after)
    assert not after['overview'];return {'before':before,'after':after,'exactCameraReturn':True}


def native_first_auto_city_five(browser,base,report):
    ctx=context(browser,base);page=ctx.new_page();q.observe(page,base,report);page.goto(base+'game/?v='+VERSION+'#map');d.map_ready(page)
    for id in outro.ARRIVAL:outro.scene(page,id);page.locator('.story-dialogue__next').click()
    page.wait_for_selector('body[data-collection-book="four-truths"][data-collection-index="0"]');assert 'collectionStory='+VERSION in page.url;trace=[0]
    for index in range(1,29):q.click_next(page,index);trace.append(index)
    assert q.snapshot(page)['completed']==[];page.locator('#next').click();d.map_ready(page);outro.scene(page,outro.INSIGHT,True)
    for id in [outro.CUTOFF,outro.MARA,outro.TAIL]:outro.next_scene(page,id)
    assert not page.locator('#wm-dialog').is_visible();page.locator('.story-dialogue__next').click();outro.wait_reward(page)
    assert page.locator('[data-city-auto-notice][data-city-placement="automatic"]').count()==1
    notice=page.locator('#wm-dialog').inner_text();assert '法輪碼頭' in notice and '前往城池看看' in notice and not any(word in notice for word in ['安置','佈置'])
    before=q.snapshot(page);page.screenshot(path=str(OUT/'actual-first29-auto-city-notice-1280x900.png'));page.locator('.wm-completion-actions a').click();ready_city(page)
    assert state(page)['displayMode']=='automatic' and state(page)['baseVisible'] and visible_ids(page)==['truth_dock'] and page.locator('[data-city-module="truth_dock"]').count()>=1 and q.snapshot(page)==before
    assert page.locator('[data-city-actor="guardian"]').count()==0
    page.screenshot(path=str(OUT/'actual-first29-city-automatic-dock-1280x900.png'));click_actor_and_close(page,capture='actual-first29-lord-dialogue-1280x900.png');plaza_source_and_close(page);roundtrip=overview_return(page,'actual-first29-overview')
    page.locator('[data-game-nav="map"]').click();d.map_ready(page);assert not page.locator('.story-dialogue').is_visible();page.locator('[data-wm-next]').click();page.wait_for_selector('body[data-collection-book="five-aggregates"][data-collection-index="0"]')
    for index in [1,2,3]:q.click_next(page,index)
    page.reload();page.wait_for_selector('body[data-collection-index="3"]');page.set_viewport_size({'width':360,'height':800});page.locator('.collection-reader-return').click();d.map_ready(page);assert not page.locator('.story-dialogue').is_visible() and q.snapshot(page)['completed']==['four-truths'] and q.snapshot(page)['positions']['five-aggregates']==3
    page.locator('[data-game-nav="city"]').click();ready_city(page);assert visible_ids(page)==['truth_dock'];page.screenshot(path=str(OUT/'actual-five-resume-city-360x800.png'))
    report['nativeFirstAutoCityFive']={'actualFirstNextTrace':trace,'noCompletionUntilExplicitFinish':True,'outroOrder':[outro.INSIGHT,outro.CUTOFF,outro.MARA,outro.TAIL,'new-module-notification','city-automatic-truth-dock'],'noticeText':notice,'noManualPlacementOrExtraReadingWrite':True,'actorCloseAndPlazaSourceClose':True,'overviewReturn':roundtrip,'fiveActualNextTrace':[0,1,2,3],'reloadRotationResumeIndex':3,'cityStillAutomaticallyMatchesFirstOnly':True};ctx.close()


def histories(browser,base,report):
    rows=[]
    for count in [1,3,7,14]:
        saved=q.fixture(q.ORDER[:count],{},q.ORDER[min(count,13)]);ctx=context(browser,base,saved,layout={'version':1,'placedIds':[],'thoughtSeenIds':[]});page=ctx.new_page();q.observe(page,base,report);goto_city(page,base);before=collection_raw(page)
        assert visible_ids(page)==MODULE_IDS[:count] and all(not m['canPlace'] for m in state(page)['modules']),(count,visible_ids(page));assert page.locator('[data-city-actor="guardian"]').count()==(1 if count>=7 else 0)
        if count>=3:assert page.locator('.mod-city__art-layer [data-city-module="six_gates"]').count()==6
        assert city.city_raw(page)=={'version':1,'placedIds':[],'thoughtSeenIds':[]},'Deriving city should not migrate or write legacy placement data'
        if count==14:
            assert page.locator('[data-city-slot="awakening-mindfulness"] svg').count()==0
            assert all(page.locator('[data-city-slot="awakening-'+id+'"]').count()==1 for id in ['owl','rabbit','bird','turtle','lotus','deer'])
        page.screenshot(path=str(OUT/f'historical-{count}-read-automatic-1280x900.png'));page.reload();ready_city(page);assert visible_ids(page)==MODULE_IDS[:count] and collection_raw(page)==before
        rows.append({'fixture':f'{count} historical completed books, empty legacy placements','visibleIds':visible_ids(page),'noCollectionWriteOnCityVisitOrReload':True});ctx.close()
    for label,saved,layout,expected in [
        ('unearned old placedIds cannot grant buildings',q.fixture(['four-truths'],{},'five-aggregates'),{'version':1,'placedIds':MODULE_IDS,'thoughtSeenIds':[]},['truth_dock']),
        ('only historical seven-factors, no first base',q.fixture(['seven-factors'],{},'four-truths'),{'version':1,'placedIds':['awakening_companions'],'thoughtSeenIds':[]},[]),
        ('first and seven-factors, missing aggregates prerequisite',q.fixture(['four-truths','seven-factors'],{},'five-aggregates'),None,['truth_dock'])]:
        ctx=context(browser,base,saved,layout=layout);page=ctx.new_page();q.observe(page,base,report);goto_city(page,base);assert visible_ids(page)==expected and q.snapshot(page)==saved
        assert page.locator('[data-city-actor="guardian"]').count()==0;rows.append({'fixture':label,'expectedVisible':expected,'noInventedBookPrerequisitesOrCompletion':True});ctx.close()
    report['automaticHistoricalFixtures']=rows


def five_viewports(browser,base,report):
    rows=[]
    for width,height in SIZES:
        saved=q.fixture(q.ORDER[:7],{},q.ORDER[7]);ctx=context(browser,base,saved,viewport={'width':width,'height':height},has_touch=True,is_mobile=False);page=ctx.new_page();q.observe(page,base,report);goto_city(page,base);before=collection_raw(page);geometry=assert_clean_city(page);overview_return(page)
        click_actor_and_close(page,capture=f'lord-dialogue-fixture-{width}x{height}.png')
        # Actual single-finger drag, followed by pinch, on the integrated camera.
        viewport=page.locator('.mod-city__viewport').bounding_box();x=viewport['x']+viewport['width']*.5;y=viewport['y']+viewport['height']*.55;old=camera(page)
        city.touch_path(page,ctx,(x,y),(x+70,y));moved=camera(page);assert abs(old['x']-moved['x'])+abs(old['y']-moved['y'])>.1
        assert not page.locator('.city-thought').is_visible() and not page.locator('#city-dialog').is_visible();pinch(page,ctx,x,y);assert camera(page)['scale']>moved['scale']
        page.set_viewport_size({'width':height,'height':width});q.settle(page);assert visible_ids(page)==MODULE_IDS[:7] and collection_raw(page)==before;page.set_viewport_size({'width':width,'height':height});q.settle(page);assert_clean_city(page)
        page.screenshot(path=str(OUT/f'automatic-city-seven-{width}x{height}.png'))
        rows.append({'viewport':[width,height],'fullSceneAndDock':geometry,'noOldPlacementDomOrCopy':True,'nativeSingleFingerPanAndPinch':True,'dragDoesNotOpenActorOrSource':True,'rotationKeepsDerivedCityAndReading':True});ctx.close()
    # Legacy explicit overview has no return snapshot; back must still provide
    # a usable normal camera rather than a visible no-op.
    saved=q.fixture(q.ORDER[:3],{},q.ORDER[3]);ctx=context(browser,base,saved,viewport={'width':360,'height':800});ctx.add_init_script("sessionStorage.setItem('sutrazen.play.city.camera.v1',JSON.stringify({version:1,x:800,y:450,scale:.5,overviewExplicit:true,returnView:null}))")
    page=ctx.new_page();q.observe(page,base,report);goto_city(page,base);page.locator('#city-overview-return').click();q.settle(page);assert not camera(page)['overview'] and q.snapshot(page)==saved
    rows.append({'fixture':'legacy explicit overview without return snapshot','viewport':[360,800],'backFallsToNormalCityWithoutProgressMutation':True});ctx.close()
    report['fiveViewportAutomaticCity']=rows


def final_sources_and_companions(browser,base,report):
    source_rows=[]
    for count in [3,7,14]:
        saved=q.fixture(q.ORDER[:count],{},q.ORDER[min(count,13)]);ctx=context(browser,base,saved);page=ctx.new_page();q.observe(page,base,report);goto_city(page,base);before=collection_raw(page)
        plaza_source_and_close(page);assert collection_raw(page)==before
        page.screenshot(path=str(OUT/f'historical-{count}-read-automatic-1280x900.png'))
        source_rows.append({'fixture':f'{count} historical completions','nativePlazaClickAfterCityOutlineAutomaticallyVisible':True,'sourceXClosesAndKeepsCollectionBytes':True});ctx.close()
    saved=q.fixture(q.ORDER,{},q.ORDER[0]);ctx=context(browser,base,saved);page=ctx.new_page();q.observe(page,base,report);goto_city(page,base);before=collection_raw(page);companions=[]
    for role,expected in [('owl','擇法夥伴・貓頭鷹'),('rabbit','精進夥伴・兔子'),('bird','喜夥伴・藍鳥'),('turtle','輕安夥伴・烏龜'),('lotus','定夥伴・蓮花'),('deer','捨夥伴・小鹿')]:
        actor='awakening-'+role;page.locator(f'[data-city-actor="{actor}"]').click();panel=page.locator(f'.city-thought[data-actor="{actor}"]:not([hidden])');panel.wait_for();assert panel.locator('h2').inner_text()==expected and panel.locator('button').count()==1
        text=panel.locator('.city-thought__line').inner_text();assert text and not any(word in panel.inner_text() for word in REMOVED_COPY)
        page.screenshot(path=str(OUT/f'companion-{role}-dialogue-1280x900.png'));panel.locator('[data-city-thought-close]').click();assert not panel.is_visible() and collection_raw(page)==before
        companions.append({'actor':actor,'name':expected,'fictionalDialogue':text,'actualClickAndX':True})
    assert page.locator('[data-city-actor="guardian"]').count()==1 and page.locator('[data-city-slot="awakening-mindfulness"] svg').count()==0
    metadata=city.city_raw(page);assert len(metadata['thoughtSeenIds'])==6;page.reload();ready_city(page);assert len(city.city_raw(page)['thoughtSeenIds'])==6 and collection_raw(page)==before
    # A repeated conversation is allowed but does not duplicate its seen flag.
    click_actor_and_close(page,'awakening-owl');assert len(city.city_raw(page)['thoughtSeenIds'])==6 and collection_raw(page)==before
    report['finalTargetedSourcesAndCompanions']={'historicalPlazaHits':source_rows,'actualSixCompanionConversations':companions,'sameV1MetadataShape':sorted(metadata.keys()),'sixSeenFlagsPersistAndDeduplicate':True,'oneGuardianNoSecondMindfulnessCat':True,'collectionBytesUnchanged':True};ctx.close()


def pinch(page,ctx,x,y):
    client=ctx.new_cdp_session(page)
    def points(d):return [{'x':x-d,'y':y,'id':1,'radiusX':2,'radiusY':2,'force':1},{'x':x+d,'y':y,'id':2,'radiusX':2,'radiusY':2,'force':1}]
    client.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':points(25)})
    for i in range(1,11):client.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':points(25+3*i)});page.wait_for_timeout(20)
    client.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});client.detach();q.settle(page)


def backups_reset(browser,base,report):
    saved=q.fixture(q.ORDER,{},q.ORDER[0]);ctx=context(browser,base,saved,layout={'version':1,'placedIds':[],'thoughtSeenIds':[]});page=ctx.new_page();q.observe(page,base,report);goto_city(page,base);city.settings_open(page)
    with page.expect_download() as download:page.locator('[data-game-backup]').click()
    file=download.value;path='/tmp/auto-city-journey-v2-qa.json';file.save_as(path);backup=json.loads(Path(path).read_text());assert backup['format']=='sutrazen.journey' and backup['version']==2 and backup['collection']==saved and backup['city']['placedIds']==[]
    page.evaluate('localStorage.setItem("qa.auto-city.keep","retained")');before=city.raw_storage(page);page.once('dialog',lambda dialog:dialog.dismiss());page.locator('[data-game-reset]').click();assert city.raw_storage(page)==before
    page.once('dialog',lambda dialog:dialog.accept());page.locator('[data-game-reset]').click();assert q.snapshot(page) is None and visible_ids(page)==[] and page.evaluate('localStorage.getItem("qa.auto-city.keep")')=='retained'
    city.upload_backup(page,backup);page.wait_for_function('window.SutraZenModularCity.getState().placedIds.length===14');assert visible_ids(page)==MODULE_IDS and q.snapshot(page)==saved
    before=city.raw_storage(page);bad=json.loads(json.dumps(backup));bad['city']['placedIds']=['unknown-module'];city.upload_backup(page,bad);assert city.raw_storage(page)==before
    legacy=q.fixture(q.ORDER[:3],{'five-aggregates':3},q.ORDER[3]);city.upload_backup(page,legacy);page.wait_for_function('window.SutraZenModularCity.getState().placedIds.length===3');assert visible_ids(page)==MODULE_IDS[:3] and q.snapshot(page)==legacy
    page.locator('[data-game-settings-close]').click();assert_clean_city(page)
    report['backupAndResetFixtures']={'fixture':'historical all14, empty legacy placements','downloadedV2PreservesReading':True,'nativeResetCancelByteIdentical':True,'confirmedResetClearsAutomaticCityWithoutUnrelatedKey':True,'v2RestoreAutomaticallyDerivesAll14':True,'invalidCityNoPartialMutation':True,'legacyV1RestoreAutomaticallyDerivesThreeAndKeepsBookmarks':True};ctx.close()


def original_smoke(browser,base,report):
    ctx=q.context_for(browser,base,ignore_https_errors=True);page=ctx.new_page();q.observe(page,base,report);page.goto(base);page.wait_for_selector('#map-heading');assert page.locator('#books a.sz-book.sz-ready').count()==14 and page.evaluate('Object.keys(dhammaData).length')==32
    readers=[]
    for book in q.ORDER[:3]:
        page.goto(base+book+'/book/');page.wait_for_selector('#next');before=page.locator('body').inner_text();page.locator('#next').click();q.settle(page);assert page.locator('body').inner_text()!=before
        links=page.locator('a').evaluate_all('nodes=>nodes.map(n=>({text:n.textContent,href:n.getAttribute("href")}))');assert any('閱讀原經' in a['text'] for a in links) and any('回修道地圖' in a['text'] and a['href']=='../../index.html' for a in links)
        assert not page.locator('.game-dock').count();readers.append(book)
    assert q.snapshot(page) is None;report['originalSiteSmoke']={'readableShelfBooks':14,'mapTopicKeys':32,'threeBareReadersNativeNextSourceAndMapLinks':readers,'noGameShellOrCollectionWrites':True};ctx.close()


def save(report):OUT.mkdir(parents=True,exist_ok=True);(OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')


def main():
    OUT.mkdir(parents=True,exist_ok=True);report=guard_sources();report.update({'phase':'Local automatic city integration','javascriptErrors':[],'httpErrors':[],'fixtureNotice':'Only nativeFirstAutoCityFive is a real complete first29 walk. Historical layouts/backups/viewport cases are explicitly isolated synthetic saves.','physicalSafari':'Not tested; Chromium desktop viewport/mouse/CDP touch simulation.'})
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(q.Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);native_first_auto_city_five(browser,base,report);print('actual first29 -> outro -> auto notice -> city -> five passed',flush=True);histories(browser,base,report);five_viewports(browser,base,report);final_sources_and_companions(browser,base,report);backups_reset(browser,base,report);original_smoke(browser,base,report);browser.close()
        for command in [['python3','-B','scripts/build-game-entry.py','--check'],['python3','-B','scripts/build-seo.py','--check']]:subprocess.run(command,cwd=ROOT,check=True,capture_output=True,text=True)
        report['generatedEntryAndSeoCheck']='passed';assert not report['javascriptErrors'],report['javascriptErrors'];assert not report['httpErrors'],report['httpErrors'];report['result']='passed'
    except Exception as error:report['result']='failed';report['error']=repr(error);raise
    finally:server.shutdown();save(report)
    print(json.dumps({'result':report['result'],'report':str(OUT/'validation.json')},ensure_ascii=False))


if __name__=='__main__':main()
