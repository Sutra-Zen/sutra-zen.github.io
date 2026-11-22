#!/usr/bin/env python3
"""Independent authored crawl and scoped author-reset browser validation."""
from pathlib import Path
import functools,http.server,importlib.util,json,re,subprocess,threading,time
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/previews/game-prologue'
s=importlib.util.spec_from_file_location('city_qa',ROOT/'scripts/check-game-city-story.py');c=importlib.util.module_from_spec(s);s.loader.exec_module(c);d=c.d;d.q.BASE='35d59e3bc41faed5fe7b0d22d1a0797398c6de59';SIZES=d.SIZES
COPY=[
 '兩千多年前，印度的鹿野苑。\n佛陀向五位比丘說起了苦，也說起了走出苦的路。',
 '相傳，佛陀般涅槃後，弟子們齊聚王舍城，\n一同誦出他的教法。後人稱這場聚會為「第一次結集」。',
 '一代人誦給下一代人聽。\n今天翻開《阿含經》，依然能讀到佛陀與弟子關於離苦的問答。',
]
COLLECTION=d.q.KEY;ROUTE='sutrazen.play.route-metadata.v1';STORY=c.STORY_KEY


def context(browser,base,local=None,session=None,**kw):
    if local is not None:kw['storage_state']={'cookies':[],'origins':[{'origin':base.rstrip('/'),'localStorage':[{'name':key,'value':value} for key,value in local.items()]}]}
    ctx=d.q.context_for(browser,base,**kw)
    if session:
        ctx.add_init_script('if(!sessionStorage.getItem("qa.prologue.seeded")){for(const [key,value] of Object.entries('+json.dumps(session)+'))sessionStorage.setItem(key,value);sessionStorage.setItem("qa.prologue.seeded","yes")}')
    return ctx


def storage(page):
    return page.evaluate('''()=>({local:Object.fromEntries(Object.entries(localStorage).sort()),session:Object.fromEntries(Object.entries(sessionStorage).sort())})''')


def assert_copy(page):
    page.wait_for_selector('[data-prologue]')
    actual=page.locator('[data-prologue-paragraph]').evaluate_all('(nodes)=>nodes.map(n=>[...n.querySelectorAll("[data-prologue-line]")].map(line=>line.textContent).join("\\n"))')
    assert actual==COPY,actual
    assert page.locator('[data-prologue-line]').count()==6
    assert page.locator('.game-title-paper').evaluate('(n)=>n.hidden&&n.hasAttribute("inert")&&n.getAttribute("aria-hidden")==="true"')
    assert not page.locator('[data-title-start]').is_visible()
    selectable=page.locator('[data-prologue-copy]').evaluate('''n=>{let s=getSelection();s.selectAllChildren(n);let value=s.toString();s.removeAllRanges();return {copy:value,userSelect:getComputedStyle(n).userSelect}}''')
    assert selectable['userSelect']=='text' and '第一次結集' in selectable['copy']
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1&&document.documentElement.scrollHeight<=innerHeight+1')


def menu_ready(page):
    page.wait_for_function('!document.querySelector("[data-prologue]")')
    page.wait_for_selector('.game-title-paper:not([hidden])');d.q.settle(page)
    paper=page.locator('.game-title-paper').bounding_box();width,height=page.viewport_size.values()
    assert abs(paper['x']+paper['width']/2-width/2)<2 and abs(paper['y']+paper['height']/2-height/2)<2,paper
    assert page.locator('[data-title-brand]').evaluate('(n)=>Boolean(n.closest(".game-title-paper"))')
    assert page.locator('[data-title-heading]').inner_text()=='佛陀的解憂之旅'
    assert page.locator('[data-title-start]').evaluate('(n)=>n===document.activeElement')
    assert page.locator('#game-content').is_hidden()
    return paper


def skip(page):
    page.locator('[data-prologue-skip]').click();menu_ready(page);page.wait_for_timeout(420)


def static_five_sizes(browser,base,report):
    cases=[];start_centers={}
    for width,height in SIZES:
        ctx=context(browser,base,viewport={'width':width,'height':height});p=ctx.new_page();d.q.observe(p,base,report);p.goto(base+'game/');p.wait_for_selector('#game-title-screen.is-art-loaded');assert_copy(p)
        assert p.locator('[data-prologue]').get_attribute('data-prologue-mode')=='static'
        before=storage(p);p.locator('[data-prologue-viewport]').click(position={'x':20,'y':20});assert p.locator('[data-prologue]').is_visible()
        p.screenshot(path=str(OUT/f'prologue-static-top-{width}x{height}.png'))
        viewport=p.locator('[data-prologue-viewport]');viewport.hover();p.mouse.wheel(0,600);d.q.settle(p)
        p.screenshot(path=str(OUT/f'prologue-static-bottom-{width}x{height}.png'))
        assert storage(p)==before
        skip(p);paper=menu_ready(p);assert not p.locator('[data-title-author-reset]').is_visible()
        assert storage(p)==before
        b=p.locator('[data-title-start]').bounding_box();start_centers[(width,height)]={'x':b['x']+b['width']/2,'y':b['y']+b['height']/2}
        p.screenshot(path=str(OUT/f'title-after-prologue-{width}x{height}.png'))
        cases.append({'viewport':[width,height],'exactThreeAuthoredBlocks':True,'htmlSelectable':True,'menuHiddenAndInert':True,'reducedMotionManualOnly':True,'nativeScrollAndSkip':True,'storageUnchanged':True,'paperCentered':paper})
        ctx.close()
    report['staticViewportChecks']=cases
    return start_centers


def natural_and_skip(browser,base,report,centers):
    saved=d.q.fixture(d.q.ORDER[:2],{'six-senses':4},'six-senses');local={COLLECTION:json.dumps(saved),'qa.unrelated':'keep'}
    ctx=context(browser,base,local,{'qa.session':'keep'},reduced_motion='no-preference');p=ctx.new_page();d.q.observe(p,base,report);p.goto(base+'game/');assert_copy(p);start=time.monotonic();before=storage(p)
    duration=p.locator('[data-prologue-copy]').evaluate('(n)=>n.getAnimations()[0].effect.getComputedTiming().duration');assert 30000<=duration<=45000,duration
    p.evaluate('''()=>{window.qaFilmEnds=0;let last=true;new MutationObserver(()=>{let active=document.querySelector('#game-title-screen').classList.contains('is-prologue-active');if(last&&!active)window.qaFilmEnds++;last=active}).observe(document.querySelector('#game-title-screen'),{attributes:true,attributeFilter:['class']})}''')
    p.wait_for_timeout(10000);assert p.locator('[data-prologue]').is_visible();p.screenshot(path=str(OUT/'natural-crawl-1280x900.png'))
    p.wait_for_function('!document.querySelector("[data-prologue]")',timeout=47000);elapsed=time.monotonic()-start;menu_ready(p)
    assert elapsed>=duration/1000-1 and elapsed<=duration/1000+4,(elapsed,duration)
    assert p.evaluate('window.qaFilmEnds')==1 and storage(p)==before
    p.screenshot(path=str(OUT/'natural-ended-menu-1280x900.png'))
    # The natural end has no initiating pointer event to suppress: a fresh
    # Start click must work immediately, unlike an explicit skip's guard.
    p.locator('[data-title-start]').click();d.map_ready(p)
    report['naturalPlayback']={'viewport':[1280,900],'actualWallSeconds':elapsed,'animationDurationMs':duration,'automaticFinishCount':1,'noSeekingOrFastForward':True,'storageUnchangedBeforeStart':True,'naturalEndFreshStartWorksWithoutSkipDelay':True};ctx.close()
    cases=[]
    for method in ['touch','Enter','Space','Escape']:
        ctx=context(browser,base,has_touch=True,reduced_motion='no-preference',viewport={'width':360,'height':800});p=ctx.new_page();d.q.observe(p,base,report);p.goto(base+'game/');assert_copy(p)
        if method=='touch':p.touchscreen.tap(**centers[(360,800)])
        else:p.keyboard.press(method)
        menu_ready(p);assert p.locator('#game-content').is_hidden()
        if method=='touch':p.touchscreen.tap(**centers[(360,800)]);assert p.locator('#game-content').is_hidden()
        p.wait_for_timeout(420);assert p.locator('#game-content').is_hidden()
        cases.append({'method':method,'didNotClickThroughToStart':True});ctx.close()
    report['skipInputChecks']=cases


def seeded_profile():
    saved=d.q.fixture(d.q.ORDER[:13],{'four-fruits-ten-fetters':5,'four-truths':28},'four-fruits-ten-fetters')
    raw=json.dumps(saved);seen=json.dumps({'version':1,'seenSceneIds':['arrival-at-wheel']})
    local={COLLECTION:raw,ROUTE:json.dumps({'version':1,'knownBookIds':d.q.ORDER[:13],'openedBookIds':['four-truths'],'playedAnimationIds':['truth_dock']}),STORY:seen,'sutrazen.play.v1':'keep-prototype','sutrazen.reader.position':'keep-public-reader','auth.roles':'keep-role','site.preference':'keep-preference'}
    session={'sutrazen.play.collection.session.v1':json.dumps({'version':1,'baseRaw':raw,'state':saved}),'sutrazen.play.story.session.v1':json.dumps({'version':1,'baseRaw':seen,'state':{'version':1,'seenSceneIds':['arrival-at-wheel']}}),'sutrazen.play.camera.v1':json.dumps({'version':1,'x':1200,'y':500,'scale':1.3}),'sutrazen.play.map-tip.v1':'1','auth.roles':'keep-session-role','qa.other-session':'keep'}
    return local,session


def author_reset_checks(browser,base,report):
    local,session=seeded_profile();ctx=context(browser,base,local,session);p=ctx.new_page();d.q.observe(p,base,report);p.goto(base+'game/?author=1');assert_copy(p);skip(p)
    assert p.locator('[data-title-author-reset]').is_visible();button=p.locator('[data-title-author-reset]').bounding_box();assert button['height']>=48,button;before=storage(p)
    p.once('dialog',lambda dialog:dialog.dismiss());p.locator('[data-title-author-reset]').click();d.q.settle(p);assert storage(p)==before
    p.once('dialog',lambda dialog:dialog.accept());p.locator('[data-title-author-reset]').click();assert_copy(p)
    after=storage(p)
    for key in [COLLECTION,ROUTE,STORY]:assert key not in after['local'],(key,after)
    for key in ['sutrazen.play.collection.session.v1','sutrazen.play.story.session.v1','sutrazen.play.camera.v1','sutrazen.play.map-tip.v1']:assert key not in after['session'],key
    for key in ['sutrazen.play.v1','sutrazen.reader.position','auth.roles','site.preference']:assert after['local'][key]==before['local'][key]
    for key in ['auth.roles','qa.other-session','qa.prologue.seeded']:assert after['session'][key]==before['session'][key]
    skip(p);assert '已重置' in p.locator('[data-title-reset-status]').inner_text();assert p.locator('[data-title-start]').inner_text()=='開始旅程'
    p.screenshot(path=str(OUT/'author-reset-fresh-menu-1280x900.png'))
    p.locator('[data-title-start]').click();d.map_ready(p);c.assert_intro(p);assert d.q.snapshot(p) is None
    p.screenshot(path=str(OUT/'author-reset-first-arrival-1280x900.png'))
    p.locator('.story-dialogue__next').click();p.wait_for_selector('body[data-collection-book="four-truths"]');d.q.click_next(p,1);d.q.click_next(p,2);p.reload();p.wait_for_selector('body[data-collection-index="2"]');p.locator('.collection-reader-return').click();d.map_ready(p)
    assert not p.locator('[data-prologue]').is_visible() and not p.locator('.story-dialogue').is_visible();assert d.q.snapshot(p)['completed']==[] and '3／29' in p.locator('[data-wm-next]').inner_text()
    p.locator('[data-game-nav="city"]').click();c.city_loaded(p);assert p.locator('[data-companion]').count()==0 and p.locator('.city-extended-rewards [data-city-reward]').count()==0
    report['authorReset']={'authorQueryOnly':True,'nativeCancelAllStorageByteIdentical':True,'confirmedClearedCurrentCollectionRouteStoryAndCamera':True,'clearedRecoveryEntries':True,'prototypePublicReaderRolesAndUnrelatedKeysPreserved':True,'countAndAwardsFresh':True,'arrivalSceneShownAgain':True,'actualNextClicks':2,'reloadAndReturnResumeAtPage3':True,'mapReturnNoPrologueOrArrivalReplay':True};ctx.close()
    for url in ['game/','game/?author=0','play/worldmap-v4/?author=1']:
        ctx=context(browser,base);p=ctx.new_page();d.q.observe(p,base,report);p.goto(base+url)
        if '/play/' not in p.url:assert_copy(p);skip(p)
        else:d.map_ready(p)
        assert p.locator('[data-title-author-reset]').count()==0,url
        ctx.close()


def failed_reset_honesty(browser,base,report):
    local,session=seeded_profile();ctx=context(browser,base,local,session)
    ctx.add_init_script('''{const remove=Storage.prototype.removeItem;Storage.prototype.removeItem=function(key){if(this===window.localStorage&&key==='sutrazen.play.collection.v1')throw new DOMException('QA removal blocked','SecurityError');return remove.call(this,key)}}''')
    p=ctx.new_page();d.q.observe(p,base,report);p.goto(base+'game/?author=1');assert_copy(p);skip(p);p.once('dialog',lambda dialog:dialog.accept());p.locator('[data-title-author-reset]').click();assert_copy(p);skip(p)
    text=p.locator('[data-title-reset-status]').inner_text();assert '無法永久保存' in text and '已重置，可以' not in text,text
    assert p.evaluate('(key)=>localStorage.getItem(key)',COLLECTION)==local[COLLECTION]
    assert p.evaluate('localStorage.getItem("auth.roles")')==local['auth.roles']
    p.screenshot(path=str(OUT/'author-reset-storage-warning.png'))
    report['failedReset']={'injectedCollectionRemovalDenied':True,'persistentRecordStillPresent':True,'temporaryOnlyWarningHonest':True,'unrelatedKeyPreserved':True};ctx.close()


def author_button_sizes(browser,base,report):
    cases=[]
    for width,height in SIZES:
        ctx=context(browser,base,viewport={'width':width,'height':height});p=ctx.new_page();d.q.observe(p,base,report);p.goto(base+'game/?author=1');assert_copy(p);skip(p)
        button=p.locator('[data-title-author-reset]');button.scroll_into_view_if_needed();bounds=button.bounding_box();assert bounds['height']>=48 and bounds['y']>=0 and bounds['y']+bounds['height']<=height,bounds
        before=storage(p);p.once('dialog',lambda dialog:dialog.dismiss());button.click();assert storage(p)==before
        assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1&&document.documentElement.scrollHeight<=innerHeight+1')
        if width in [360,844]:p.screenshot(path=str(OUT/f'author-trial-menu-{width}x{height}.png'))
        cases.append({'viewport':[width,height],'nativeAuthorResetReachable':True,'height':bounds['height'],'cancelPreservesStorage':True});ctx.close()
    report['authorButtonViewports']=cases


def failed_recovery_cleanup(browser,base,report):
    cases=[];recovery_key='sutrazen.play.collection.session.v1'
    old=d.q.fixture(d.q.ORDER[:13],{'four-fruits-ten-fetters':5},'four-fruits-ten-fetters')
    for also_block_write,cached_old_store in [(False,False),(True,False),(False,True)]:
        ctx=context(browser,base,{'auth.roles':'keep-role'})
        if cached_old_store:
            baseline_store=subprocess.check_output(['git','show',d.q.BASE+':play/collection/store.js'],cwd=ROOT,text=True)
            ctx.route('**/play/collection/store.js',lambda route:route.fulfill(status=200,content_type='application/javascript',body=baseline_store))
        # A valid null-boundary recovery is the exact edge that could revive
        # old achievements after reset. Only this one session key is blocked.
        seed=json.dumps({recovery_key:json.dumps({'version':1,'baseRaw':None,'state':old}),'qa.unrelated-session':'keep'})
        ctx.add_init_script('''{if(!sessionStorage.getItem('qa.recovery.seeded')){for(const [k,v] of Object.entries('''+seed+'''))sessionStorage.setItem(k,v);sessionStorage.setItem('qa.recovery.seeded','yes')}const remove=Storage.prototype.removeItem,set=Storage.prototype.setItem;Storage.prototype.removeItem=function(key){if(this===window.sessionStorage&&key==='''+json.dumps(recovery_key)+''')throw new DOMException('QA session removal blocked','SecurityError');return remove.call(this,key)};Storage.prototype.setItem=function(key,value){if('''+str(also_block_write).lower()+'''&&this===window.sessionStorage&&key==='''+json.dumps(recovery_key)+''')throw new DOMException('QA session replacement blocked','SecurityError');return set.call(this,key,value)}}''')
        p=ctx.new_page();d.q.observe(p,base,report);p.goto(base+'game/?author=1');assert_copy(p);skip(p)
        before=p.evaluate('''async()=>{const {store}=await import('/play/collection/store.js');return store.get()}''');assert len(before['completed'])==13
        p.once('dialog',lambda dialog:dialog.accept());p.locator('[data-title-author-reset]').click();assert_copy(p);skip(p)
        assert '無法永久保存' in p.locator('[data-title-reset-status]').inner_text()
        after=p.evaluate('''async()=>{const {store}=await import('/play/collection/store.js');return store.get()}''')
        assert after=={'version':1,'positions':{},'completed':[],'activeBook':'four-truths'},after
        assert p.evaluate('localStorage.getItem("auth.roles")')=='keep-role' and p.evaluate('sessionStorage.getItem("qa.unrelated-session")')=='keep'
        p.reload();assert_copy(p);skip(p)
        reloaded=p.evaluate('''async()=>{const {store}=await import('/play/collection/store.js');return store.get()}''')
        if not also_block_write:assert reloaded==after,reloaded
        else:assert reloaded==old,reloaded
        cases.append({'sessionRecoveryRemovalDenied':True,'replacementAlsoDenied':also_block_write,'cachedBaselineStoreResponse':cached_old_store,'resetMemoryFresh':True,'temporaryOnlyWarningHonest':True,'reloadFreshWhenRecoveryReplacementWorks':not also_block_write,'ifAllRecoveryWritesDeniedOldStateMayReturnAsWarned':also_block_write,'unrelatedKeysPreserved':True})
        ctx.close()
    report['staleRecoveryResetRegression']=cases


def guard_core(report):
    protected=['play/collection/reader-bridge.js','play/reader-bridge.js','play/route','play/worldmap-v4/data.js','play/worldmap-v4/camera.js','play/visual-v2/network-data.js','play/visual-v2/assets','play/worldmap-v4/assets','play/story/assets']
    changes=subprocess.check_output(['git','diff','--name-only',d.q.BASE,'--',*protected],cwd=ROOT,text=True).splitlines();assert not changes,changes
    old=subprocess.check_output(['git','show',d.q.BASE+':play/collection/store.js'],cwd=ROOT,text=True);new=(ROOT/'play/collection/store.js').read_text()
    reset=re.compile(r'  reset\(\) \{\n.*?\n  \},\n  exportBackup:',re.S)
    assert reset.sub('AUTHORIZED_RESET_ONLY',old)==reset.sub('AUTHORIZED_RESET_ONLY',new)
    report['protectedGameCoreAndArt']=protected;report['collectionStoreException']='Only reset() cleanup block changed; all other bytes identical'


def main():
    OUT.mkdir(parents=True,exist_ok=True);report=d.q.protect_originals();report.update({'phase':'Local review only','javascriptErrors':[],'httpErrors':[],'physicalSafari':'Not tested; desktop Chromium viewport/input simulation','exactAuthorCopy':COPY})
    guard_core(report)
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(d.q.Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
    try:
        with sync_playwright() as p:
            b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);centers=static_five_sizes(b,base,report);natural_and_skip(b,base,report,centers);author_reset_checks(b,base,report);author_button_sizes(b,base,report);failed_reset_honesty(b,base,report);failed_recovery_cleanup(b,base,report);b.close()
    finally:server.shutdown()
    assert not report['javascriptErrors'],report['javascriptErrors'];assert not report['httpErrors'],report['httpErrors'];report['result']='passed';(OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'result':report['result'],'report':str((OUT/'validation.json').relative_to(ROOT))},ensure_ascii=False))


if __name__=='__main__':main()
