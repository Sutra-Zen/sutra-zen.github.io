#!/usr/bin/env python3
"""Focused first-completion tail ordering; native reading and labelled fixtures."""
from pathlib import Path
import functools,http.server,importlib.util,json,re,subprocess,threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/previews/game-outro-order'
s=importlib.util.spec_from_file_location('mod_city_qa',ROOT/'scripts/check-game-modular-city.py');city=importlib.util.module_from_spec(s);s.loader.exec_module(city)
q=city.q;d=city.d;story=city.story;mara=city.mara;cyan=city.cyan
BASELINE='2720747323f4d3a05474bf0c2919ac5332810cb2';VERSION='outro-order-1';STORY_KEY=mara.STORY_KEY
TAIL=cyan.FIVE_SCENE;CUTOFF='doubt-recedes';SIZES=q.SIZES
ARRIVAL=list(story.LINES)[:3];INSIGHT='first-book-insight';MARA='mara-watches'


def guard_sources():
    originals=q.ORDER+['docs/'+book for book in q.ORDER]+['index.html','shelf.css','sitemap.xml','robots.txt','googlee0c995331ec518ae.html','reader-controls.css','reader-layout.js','reader-restart.js','picture-panel-focus.js','picture-panel-focus.css','docs/seo','map-topic-resources.css','scripts/site_seo.py','scripts/build-seo.py','scripts/check-seo.py']
    html=[book+'/book/index.html' for book in q.ORDER];changes=subprocess.check_output(['git','diff','--name-only',BASELINE,'--',*originals],cwd=ROOT,text=True).splitlines();assert set(changes)<=set(html),changes
    before=lambda path:subprocess.check_output(['git','show',BASELINE+':'+path],cwd=ROOT,text=True)
    for path in html:
        old=before(path);new=(ROOT/path).read_text();oldtag=re.search(r'\.\./\.\./play/collection/reader-bridge\.js\?v=[^"\s]+',old).group();newtag=re.search(r'\.\./\.\./play/collection/reader-bridge\.js\?v=[^"\s]+',new).group()
        assert new.replace(newtag,oldtag)==old,path
    paths=['play/collection/store.js','play/collection/reader.css','play/reader-bridge.js','play/route','play/prologue','play/story/completion-receipt.js','play/story/assets','play/game-theme.css','play/worldmap-v4/camera.js','play/worldmap-v4/data.js','play/visual-v2/network-data.js','play/visual-v2/assets','play/worldmap-v4/assets','play/assets']
    changes=subprocess.check_output(['git','diff','--name-only',BASELINE,'--',*paths],cwd=ROOT,text=True).splitlines();assert not changes,changes
    modules=subprocess.check_output(['git','ls-tree','-rz','--name-only',BASELINE,'--','play/city/modules'],cwd=ROOT,text=True).split('\0')
    for path in filter(None,modules):
        old=subprocess.check_output(['git','show',BASELINE+':'+path],cwd=ROOT)
        new=(ROOT/path).read_bytes().replace(b'?v=outro-order-1',b'?v=modular-city-1')
        assert new==old,path
    bridge=(ROOT/'play/collection/reader-bridge.js').read_text();bridge=re.sub(r"new URL\('../../game/\?v=[^']+', import.meta.url\)","new URL('../../game/?v=modular-city-1', import.meta.url)",bridge);assert bridge==before('play/collection/reader-bridge.js')
    store=(ROOT/'play/story/store.js').read_text();store=re.sub(r"\./data.js\?v=[^']+","./data.js?v=mara-1",store);assert store==before('play/story/store.js')
    files=[p for p in subprocess.check_output(['git','ls-tree','-rz','--name-only',BASELINE,'--',*originals],cwd=ROOT,text=True).split('\0') if p]
    return {'baseline':BASELINE,'protectedOriginalFiles':len(files),'originalNarrationScriptureArtReaderJsCssHomepageSeoGoogle':'unchanged; reader HTML allows cache query only','coreReceiptEligibilityCollectionAndCityPlacement':'byte-for-byte unchanged','storySchemaStoreException':'data import query only','readerBridgeException':'return cache query only'}


def seen(page):
    return page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)||"null")?.seenSceneIds||[]',STORY_KEY)


def raw(page):
    return page.evaluate('(keys)=>keys.map(k=>localStorage.getItem(k))',[q.KEY,STORY_KEY,city.CITY_KEY])


def context(browser,base,saved=None,seen_ids=None,**kwargs):
    return city.context(browser,base,saved,seen_ids,**kwargs)


def goto_map(page,base):
    page.goto(base+'game/?v='+VERSION+'#map');d.map_ready(page)


def scene(page,id,completion=False,replaying=False):
    panel=page.locator(f'.story-dialogue[data-scene="{id}"]:not([hidden])');panel.wait_for();result=story.scene_snapshot(page)
    expected=cyan.FIVE_TEXT if id==TAIL else mara.MARA_TEXT if id==MARA else story.LINES[id]
    assert result['text']==expected,result
    story.dialogue_geometry(page);story.portrait_unclipped(page);q.settle(page)
    assert page.locator('.story-dialogue__next').evaluate('(n)=>document.activeElement===n'),result
    if id==TAIL:
        expected_cta='回到海圖' if replaying else '看看旅程的變化' if completion else '前往五陰湖';assert page.locator('.story-dialogue__next').inner_text()==expected_cta
        if completion:
            assert panel.get_attribute('data-context')=='first-completion'
            assert page.locator('.story-dialogue__skip').inner_text()=='看閱讀回饋'
    return result


def next_scene(page,target,completion=True,replaying=False):
    page.locator('.story-dialogue__next').click();return scene(page,target,completion,replaying)


def assert_navigation_blocked(page,id):
    before=raw(page);url=page.url
    for selector in ['[data-game-nav="city"]','[data-game-nav="shelf"]','[data-game-nav="map"]','[data-wm-next]','[data-wm-tools-open]']:
        button=page.locator(selector);button.scroll_into_view_if_needed();button.click();q.settle(page)
        assert page.url==url and page.locator(f'.story-dialogue[data-scene="{id}"]:not([hidden])').is_visible() and not page.locator('#wm-dialog').is_visible(),selector
        assert raw(page)==before,selector
    # Native landmark entry is guarded even after keyboard focus locates it.
    landmark=page.locator('.wm-landmark[data-book="five-aggregates"]').first;landmark.focus();landmark.click();q.settle(page)
    assert page.url==url and raw(page)==before and not page.locator('#wm-dialog').is_visible()
    # Keyboard-generated click must be blocked too.
    nav=page.locator('[data-game-nav="city"]');nav.focus();page.keyboard.press('Enter');q.settle(page)
    assert page.url==url and raw(page)==before
    # Refocus the actual story action before subsequent keyboard assertions.
    page.locator('.story-dialogue__next').focus()
    return {'nativeCityShelfMapPrimaryToolsLandmarkAndKeyboardEntryBlocked':True,'collectionStoryCityBytesUnchanged':True}


def wait_reward(page):
    page.wait_for_selector('#wm-dialog.wm-completion-dialog[open]');assert not page.locator('.story-dialogue').is_visible();assert '法輪碼頭' in page.locator('#wm-dialog').inner_text();assert CUTOFF in seen(page)


def native_full_flow(browser,base,report):
    ctx=context(browser,base,viewport={'width':1280,'height':900});page=ctx.new_page();q.observe(page,base,report);goto_map(page,base)
    for id in ARRIVAL:scene(page,id);page.locator('.story-dialogue__next').click()
    page.wait_for_selector('body[data-collection-book="four-truths"][data-collection-index="0"]');trace=[0]
    for index in range(1,29):q.click_next(page,index);trace.append(index)
    assert q.snapshot(page)['completed']==[];page.locator('#next').click();d.map_ready(page);scene(page,INSIGHT,True)
    progress=q.snapshot(page);assert progress['completed']==['four-truths'];blocked=assert_navigation_blocked(page,INSIGHT)
    next_scene(page,CUTOFF);next_scene(page,MARA);assert CUTOFF not in seen(page)
    page.reload();d.map_ready(page);scene(page,MARA,True);assert q.snapshot(page)==progress
    next_scene(page,TAIL);assert TAIL in seen(page) and CUTOFF not in seen(page) and q.snapshot(page)==progress
    page.screenshot(path=str(OUT/'actual-first29-tail-before-reward-1280x900.png'));assert_navigation_blocked(page,TAIL)
    page.reload();d.map_ready(page);tail=scene(page,TAIL,True);assert q.snapshot(page)==progress and CUTOFF not in seen(page)
    page.screenshot(path=str(OUT/'actual-first29-tail-restored-1280x900.png'));page.locator('.story-dialogue__next').click();wait_reward(page);assert q.snapshot(page)==progress
    page.screenshot(path=str(OUT/'actual-first29-reward-after-tail-1280x900.png'))
    page.locator('.wm-completion-actions a').click();city.city_ready(page);assert city.city_state(page)['baseVisible'] and city.city_state(page)['placedIds']==[]
    city.place_click(page,'truth_dock');city.close_thought(page);city.inventory_close(page);assert q.snapshot(page)==progress
    page.screenshot(path=str(OUT/'actual-first29-city-handplaced-dock-1280x900.png'))
    page.locator('[data-game-nav="map"]').click();d.map_ready(page);assert not page.locator('.story-dialogue').is_visible();assert city.city_raw(page)['placedIds']==['truth_dock']
    page.locator('[data-wm-next]').click();page.wait_for_selector('body[data-collection-book="five-aggregates"][data-collection-index="0"]')
    for index in [1,2,3]:q.click_next(page,index)
    page.reload();page.wait_for_selector('body[data-collection-index="3"]');page.set_viewport_size({'width':360,'height':800});page.locator('.collection-reader-return').click();d.map_ready(page)
    assert not page.locator('.story-dialogue').is_visible() and q.snapshot(page)['positions']['five-aggregates']==3 and q.snapshot(page)['completed']==['four-truths'] and city.city_raw(page)['placedIds']==['truth_dock']
    page.screenshot(path=str(OUT/'actual-five-index3-return-360x800.png'))
    report['nativeFirstTailCityFive']={'actualFirstNextTrace':trace,'noCompletionBeforeExplicitFinish':True,'outroOrder':[INSIGHT,CUTOFF,MARA,TAIL,'original-reward','city-handplace-truth_dock','five-original-reader'],'navigationBlock':blocked,'maraReloadRestoresPending':True,'tailSeenOnShowButCutoffPendingUntilAcknowledged':True,'tailReloadRetainsCompletionContext':tail,'originalRewardOnlyAfterTail':True,'cityOptionalBeforeFiveAndNoDuplicateTail':True,'fiveActualNextTrace':[0,1,2,3],'reloadRotationReturnAtIndex':3,'completedStillFirstOnly':True};ctx.close()


def pending_fixture():
    return q.fixture(['four-truths'],{'four-truths':28},'five-aggregates')


def five_sizes_tail(browser,base,report):
    rows=[]
    for width,height in SIZES:
        state=pending_fixture();ctx=context(browser,base,state,ARRIVAL+[INSIGHT,MARA,TAIL],viewport={'width':width,'height':height});page=ctx.new_page();q.observe(page,base,report);goto_map(page,base);snapshot=scene(page,TAIL,True);before=q.snapshot(page)
        color=cyan.colors(page,'.story-dialogue__next');page.screenshot(path=str(OUT/f'tail-pending-fixture-{width}x{height}.png'))
        page.locator('.story-dialogue__skip').click();wait_reward(page);assert q.snapshot(page)==before;page.locator('[data-wm-next-station]').click();assert not page.locator('.story-dialogue').is_visible() and '/book/' not in page.url
        assert page.locator('.wm-landmark.is-next').first.get_attribute('data-book')=='five-aggregates';page.reload();d.map_ready(page);assert not page.locator('.story-dialogue').is_visible() and q.snapshot(page)==state
        rows.append({'viewport':[width,height],'fixture':'first-complete pending tail already shown, no cutoff','scene':snapshot,'cyanCta':color,'fullPortraitButtonsAboveDock':True,'tailSkipThenOriginalRewardAndNextStationWithoutRepeatedTransition':True,'collectionUnchanged':True});ctx.close()
    report['fiveViewportTailFixtures']=rows


def skip_history_replay(browser,base,report):
    rows=[];state=pending_fixture()
    # Isolated receipt fixture exercises skip on the first reflection itself;
    # the genuine receipt/reader handoff is independently covered by native29.
    ctx=context(browser,base,state,ARRIVAL);ctx.add_init_script("if(!sessionStorage.getItem('qa.outro.receipt-seeded')){sessionStorage.setItem('sutrazen.play.story-first-completion.v1',JSON.stringify({version:1,event:'four-truths-reader-finished'}));sessionStorage.setItem('qa.outro.receipt-seeded','1')}")
    page=ctx.new_page();q.observe(page,base,report);goto_map(page,base);scene(page,INSIGHT,True);before=q.snapshot(page);page.locator('.story-dialogue__skip').click();scene(page,TAIL,True)
    assert CUTOFF not in seen(page) and MARA in seen(page) and q.snapshot(page)==before
    page.reload();d.map_ready(page);scene(page,TAIL,True);assert CUTOFF not in seen(page) and q.snapshot(page)==before;page.locator('.story-dialogue__next').click();wait_reward(page)
    rows.append({'fixture':'explicit isolated receipt at first insight, not native reader completion','skipInsightThenTailReloadStaysTailBeforeCutoff':True,'tailConfirmShowsRewardOnlyAfterAcknowledgement':True,'collectionUnchanged':True});ctx.close()
    # Pending early outro skip still routes through the tail, never straight reward.
    for target,ids in [(CUTOFF,ARRIVAL+[INSIGHT]),(MARA,ARRIVAL+[INSIGHT,MARA])]:
        ctx=context(browser,base,state,ids);page=ctx.new_page();q.observe(page,base,report);goto_map(page,base);scene(page,target,True);before=q.snapshot(page)
        page.locator('.story-dialogue__skip').click();scene(page,TAIL,True);assert not page.locator('#wm-dialog').is_visible() and CUTOFF not in seen(page) and q.snapshot(page)==before
        page.reload();d.map_ready(page);scene(page,TAIL,True);assert CUTOFF not in seen(page) and q.snapshot(page)==before
        page.locator('.story-dialogue__skip').click();wait_reward(page);assert q.snapshot(page)==before;rows.append({'fixture':'pending '+target,'skipMustVisitTailBeforeReward':True,'reloadAfterSkipStaysTailUntilAcknowledged':True,'noReadingWrites':True});ctx.close()
    # An old reachable interleaving showed the lake line before the unfinished
    # insight chain had reached Mara. Do not skip the missing retreat/Mara.
    ids=ARRIVAL+[INSIGHT,TAIL];ctx=context(browser,base,state,ids);page=ctx.new_page();q.observe(page,base,report);goto_map(page,base);scene(page,CUTOFF,True);before=q.snapshot(page)
    next_scene(page,MARA);page.locator('.story-dialogue__next').click();wait_reward(page);assert q.snapshot(page)==before
    rows.append({'fixture':'old interrupted insight plus lake seen, Mara not seen','resumeRetreatThenMaraBeforeRewardWithoutRepeatingPreviouslySeenLake':True,'collectionUnchanged':True});ctx.close()
    # Legacy Mara confirmed the old cutoff, but the lake line was never seen.
    ctx=context(browser,base,state,ARRIVAL+[INSIGHT,CUTOFF,MARA]);page=ctx.new_page();q.observe(page,base,report);goto_map(page,base);scene(page,TAIL,True);before=q.snapshot(page);page.locator('.story-dialogue__next').click();wait_reward(page);assert q.snapshot(page)==before
    rows.append({'fixture':'legacy cutoff+Mara, no tail/five bookmark','oneTimeTailCatchupThenReward':True});ctx.close()
    # Mere historic completion/URL flags do not forge a receipt; existing lake
    # bookmarks, including zero, never force the new tail into normal reading.
    cases=[('pre-story historical completion',state,[]),('tail already accepted',state,ARRIVAL+[INSIGHT,CUTOFF,MARA,TAIL]),('five bookmark zero',q.fixture(['four-truths'],{'four-truths':28,'five-aggregates':0},'five-aggregates'),ARRIVAL+[INSIGHT,CUTOFF,MARA]),('five bookmark four',q.fixture(['four-truths'],{'four-truths':28,'five-aggregates':4},'five-aggregates'),ARRIVAL+[INSIGHT,CUTOFF,MARA]),('first review in progress',q.fixture(['four-truths'],{'four-truths':4},'five-aggregates'),ARRIVAL+[INSIGHT,CUTOFF,MARA])]
    for label,saved,ids in cases:
        ctx=context(browser,base,saved,ids);page=ctx.new_page();q.observe(page,base,report);goto_map(page,base);assert not page.locator('.story-dialogue').is_visible() and q.snapshot(page)==saved,label
        rows.append({'fixture':label,'noForcedCompletionTail':True,'readingStateUnchanged':True});ctx.close()
    # A locked book never obtains the transition or qualifies itself.
    ctx=context(browser,base,q.fixture([],{'five-aggregates':3},'four-truths'),ARRIVAL);page=ctx.new_page();q.observe(page,base,report);goto_map(page,base)
    target=page.locator('.wm-landmark[data-book="five-aggregates"]').first;target.focus();target.click();page.wait_for_selector('#wm-dialog[open]');assert page.locator('[data-wm-read="five-aggregates"]').count()==0 and not page.locator('.story-dialogue').is_visible() and q.snapshot(page)['completed']==[]
    rows.append({'fixture':'future bookmark but first incomplete','fiveStaysLockedNoTailAndNoCompletion':True});ctx.close()
    # Explicit replay is presentation-only, including the newly appended tail.
    ids=ARRIVAL+[INSIGHT,CUTOFF,MARA,TAIL];ctx=context(browser,base,state,ids);page=ctx.new_page();q.observe(page,base,report);goto_map(page,base);before=raw(page)
    page.locator('[data-wm-tools-open]').focus();page.locator('[data-wm-tools-open]').click();page.locator('[data-wm-completion-replay]').click();scene(page,INSIGHT)
    for id in [CUTOFF,MARA,TAIL]:next_scene(page,id,False,True)
    page.locator('.story-dialogue__next').click();assert raw(page)==before and not page.locator('.story-dialogue').is_visible() and not page.locator('#wm-dialog').is_visible() and '/book/' not in page.url
    rows.append({'fixture':'explicit completed-book replay','includesTailReadonlyNoSeenOrCollectionOrCityWrites':True,'noRewardAndNoReaderEntry':True});ctx.close();report['skipHistoricalAndReplayFixtures']=rows


def reset_in_completion_context(browser,base,report):
    state=pending_fixture();ctx=context(browser,base,state,ARRIVAL+[INSIGHT,MARA,TAIL]);page=ctx.new_page();q.observe(page,base,report);goto_map(page,base);scene(page,TAIL,True)
    page.evaluate('localStorage.setItem("qa.outro.keep","untouched")');before=city.raw_storage(page);city.settings_open(page)
    page.once('dialog',lambda dialog:dialog.dismiss());page.locator('[data-game-reset]').click();assert city.raw_storage(page)==before
    page.once('dialog',lambda dialog:dialog.accept());page.locator('[data-game-reset]').click();assert q.snapshot(page) is None and seen(page)==['arrival-at-wheel'] and page.evaluate('localStorage.getItem("qa.outro.keep")')=='untouched'
    page.locator('[data-game-settings-close]').click();scene(page,'arrival-at-wheel');assert CUTOFF not in seen(page) and TAIL not in seen(page)
    report['settingsResetDuringPendingOutro']={'fixture':'pending tail','settingsUsableWhileOtherNavigationBlocked':True,'cancelAllStorageByteIdentical':True,'confirmClearsSameStoryV1AndReadingAndCity':True,'unrelatedKeyPreserved':True,'freshArrivalFromSameStorySingleton':True};ctx.close()


def save(report):
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')


def main():
    OUT.mkdir(parents=True,exist_ok=True);report=guard_sources();report.update({'phase':'Local outro ordering validation','javascriptErrors':[],'httpErrors':[],'fixtureNotice':'Only nativeFirstTailCityFive is an actual complete first29 read; pending/history/reset/five-size scenes use isolated synthetic saves.','physicalSafari':'Not tested; Chromium desktop viewports and native browser clicks, not physical iPhone/iPad Safari.'})
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(q.Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);native_full_flow(browser,base,report);print('native first29 -> tail -> reward -> city -> five passed',flush=True);five_sizes_tail(browser,base,report);skip_history_replay(browser,base,report);reset_in_completion_context(browser,base,report);browser.close()
        assert not report['javascriptErrors'],report['javascriptErrors'];assert not report['httpErrors'],report['httpErrors'];report['result']='passed'
    except Exception as error:report['result']='failed';report['error']=repr(error);raise
    finally:server.shutdown();save(report)
    print(json.dumps({'result':report['result'],'report':str(OUT/'validation.json')},ensure_ascii=False))


if __name__=='__main__':main()
