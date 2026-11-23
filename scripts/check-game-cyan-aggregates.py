#!/usr/bin/env python3
"""Focused cyan semantic accents and lawful Five Aggregates story validation.

Own evidence only. Synthetic history cases are separate from the native first29
walk. Existing whole-site and fourteen-reader evidence remains untouched.
"""
from pathlib import Path
import colorsys,functools,http.server,importlib.util,json,re,subprocess,threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/previews/game-cyan-aggregates'
s=importlib.util.spec_from_file_location('doubt_qa',ROOT/'scripts/check-game-doubt-story.py');old=importlib.util.module_from_spec(s);s.loader.exec_module(old)
q=old.q;d=old.d;BASELINE='0d44d7229195d60bf1781e55e88ab53b8d7fcc7f';q.BASE=BASELINE
SIZES=q.SIZES;STORY_KEY=old.STORY_KEY
FIVE_SCENE='toward-aggregates-lake'
FIVE_TEXT='原來，四個重要的真理是苦、集、滅、道。但我還不太懂苦的心理運作……那邊有座五陰湖，去看看好了！'


def guard_sources():
    original_paths=q.ORDER+['docs/'+book for book in q.ORDER]+['index.html','shelf.css','sitemap.xml','robots.txt','googlee0c995331ec518ae.html','reader-controls.css','reader-layout.js','reader-restart.js','picture-panel-focus.js','picture-panel-focus.css','docs/seo','map-topic-resources.css','scripts/site_seo.py','scripts/build-seo.py','scripts/check-seo.py']
    original_html=[book+'/book/index.html' for book in q.ORDER]
    original_changes=subprocess.check_output(['git','diff','--name-only',BASELINE,'--',*original_paths],cwd=ROOT,text=True).splitlines();assert set(original_changes)<=set(original_html),original_changes
    baseline=lambda path:subprocess.check_output(['git','show',BASELINE+':'+path],cwd=ROOT,text=True)
    for path in original_html:
        before=baseline(path);after=(ROOT/path).read_text();old_tag=re.search(r'\.\./\.\./play/collection/reader-bridge\.js\?v=[^"\s]+',before).group()
        assert after.count('../../play/collection/reader-bridge.js?v=cyan-aggregates-1')==1,path
        assert after.replace('../../play/collection/reader-bridge.js?v=cyan-aggregates-1',old_tag)==before,path
    count=len([p for p in subprocess.check_output(['git','ls-tree','-rz','--name-only',BASELINE,'--',*original_paths],cwd=ROOT,text=True).split('\0') if p])
    report={'baseline':BASELINE,'protectedOriginalFiles':count,'fourteenReaderHtmlException':'Only each collection bridge query; normalize to its own baseline then full text equal','originalBookTextScriptureArtJsCssHomepageSeoGoogle':'byte-for-byte unchanged'}
    protected=['play/collection/store.js','play/collection/reader.css','play/reader-bridge.js','play/route','play/prologue','play/story/completion-receipt.js','play/worldmap-v4/camera.js','play/worldmap-v4/data.js','play/visual-v2/network-data.js','play/visual-v2/assets','play/worldmap-v4/assets','play/story/assets','play/assets']
    changed=subprocess.check_output(['git','diff','--name-only',BASELINE,'--',*protected],cwd=ROOT,text=True).splitlines();assert not changed,changed
    report['additionalUnchangedCoreAndArt']=protected
    bridge=(ROOT/'play/collection/reader-bridge.js').read_text().replace("new URL('../../game/?v=cyan-1', import.meta.url)","new URL('../../game/?v=doubt-2', import.meta.url)");assert bridge==baseline('play/collection/reader-bridge.js')
    store=(ROOT/'play/story/store.js').read_text().replace("./data.js?v=cyan-aggregates-1","./data.js?v=doubt-1");assert store==baseline('play/story/store.js')
    reset=(ROOT/'play/title-review.js').read_text().replace("./story/store.js?v=cyan-aggregates-1","./story/store.js?v=doubt-1");assert reset==baseline('play/title-review.js')
    report['cacheOnlyCoreExceptions']='Reader bridge return query, story data/store imports and author reset import; normalize then all other bytes unchanged'
    return report


def context(browser,base,saved=None,seen=None,**options):
    return old.context(browser,base,saved,seen,**options)


def colors(page,selector):
    result=page.locator(selector).evaluate('''n=>{const s=getComputedStyle(n);return {background:s.backgroundColor,image:s.backgroundImage,color:s.color,outline:s.outlineColor,rect:n.getBoundingClientRect().toJSON()}}''')
    values=[old.rgba(v) for v in re.findall(r'rgba?\([^)]*\)',result['image'])] or [old.rgba(result['background'])]
    assert values and all(v[3]>.5 for v in values),result
    # Semantic accents are pale cyan, not a broad ban on green in illustrations
    # or the retained dark transparent menu surfaces.
    for value in values:
        hue,lightness,saturation=colorsys.rgb_to_hls(*(n/255 for n in value[:3]));hue*=360
        assert 160<=hue<=215 and lightness>=.55 and saturation>=.15,(selector,result,hue,lightness,saturation)
    foreground=old.rgba(result['color']);contrasts=[]
    for value in values:
        for backdrop in [0,255]:
            background=[channel*value[3]+backdrop*(1-value[3]) for channel in value[:3]]
            a,b=sorted([old.luminance(foreground[:3]),old.luminance(background)],reverse=True);contrasts.append((a+.05)/(b+.05))
    assert min(contrasts)>=4.5,(selector,result,min(contrasts))
    result['minTextContrastBlackOrWhiteBehind']=min(contrasts)
    return result


def new_scene_snapshot(page):
    panel=page.locator('.story-dialogue:not([hidden])');panel.wait_for()
    result=old.scene_snapshot(page);assert result['actor']=='traveler',result
    old.dialogue_geometry(page);old.portrait_unclipped(page)
    assert old.visible_marks(page,'.story-dialogue [data-doubt-portrait-mark]')==0
    assert result['id']==FIVE_SCENE and result['text']==FIVE_TEXT,result
    assert page.locator('.story-dialogue__next').inner_text()=='前往五陰湖'
    q.settle(page);assert page.locator('.story-dialogue__next').evaluate('(n)=>document.activeElement===n')
    return result


def assert_no_new_scene(page):
    assert not page.locator(f'.story-dialogue[data-scene="{FIVE_SCENE}"]:not([hidden])').is_visible()


def actual_first_to_aggregates(browser,base,report):
    ctx=context(browser,base,reduced_motion='no-preference');page=ctx.new_page();q.observe(page,base,report);old.fresh_map(page,base)
    for scene_id in list(old.LINES)[:3]:old.assert_scene(page,scene_id);page.locator('.story-dialogue__next').click()
    page.wait_for_selector('body[data-collection-index="0"]');trace=[0]
    for index in range(1,29):q.click_next(page,index);trace.append(index)
    assert q.snapshot(page)['completed']==[];page.locator('#next').click();d.map_ready(page)
    old.assert_scene(page,'first-book-insight');page.wait_for_timeout(1000);page.locator('.story-dialogue__next').click();old.assert_scene(page,'doubt-recedes');page.wait_for_timeout(1500);page.locator('.story-dialogue__next').click();page.wait_for_selector('#wm-dialog[open]')
    assert '法輪碼頭' in page.locator('#wm-dialog').inner_text() and q.snapshot(page)['completed']==['four-truths']
    page.screenshot(path=str(OUT/'actual-first29-original-reward-1280x900.png'))
    page.locator('[data-wm-next-station]').click();page.wait_for_selector(f'.story-dialogue[data-scene="{FIVE_SCENE}"]:not([hidden])')
    scene=new_scene_snapshot(page);assert '/book/' not in page.url
    before=q.snapshot(page);assert before['completed']==['four-truths'] and 'five-aggregates' not in before['positions']
    assert page.locator('.wm-landmark.is-next').get_attribute('data-book')=='five-aggregates'
    page.screenshot(path=str(OUT/'actual-first29-toward-five-1280x900.png'));action=colors(page,'.story-dialogue__next')
    page.locator('.story-dialogue__next').click();page.wait_for_selector('body[data-collection-book="five-aggregates"][data-collection-index="0"]')
    total=int(page.locator('body').get_attribute('data-collection-total'));assert total==54,total
    for index in [1,2,3]:q.click_next(page,index)
    page.reload();page.wait_for_selector('body[data-collection-index="3"]');page.set_viewport_size({'width':360,'height':800});page.locator('.collection-reader-return').click();d.map_ready(page)
    assert_no_new_scene(page);state=q.snapshot(page);assert state['completed']==['four-truths'] and state['positions']['five-aggregates']==3,state
    assert '4／54' in page.locator('[data-wm-next]').inner_text()
    page.screenshot(path=str(OUT/'actual-five-resume-360x800.png'))
    report['actualFirstToFive']={'actualFirstBookNextTrace':trace,'countZeroUntilExplicitFirstFinish':True,'originalFirstRewardAndNextStationPreserved':True,'newSceneAfterLocateBeforeOpeningBook':scene,'sceneOnlyAddsPresentationSeenFlag':before,'newSceneCta':action,'fiveActualNextIndices':[0,1,2,3],'fiveTotalSteps':total,'reloadRotationReturnResumesAtIndex':3,'fiveSceneNotRepeatedOnReturn':True,'completedStillOnlyFirst':True};ctx.close()


def palette_five_sizes(browser,base,report):
    rows=[]
    for width,height in SIZES:
        saved=q.fixture(['four-truths'],{},'five-aggregates');ctx=context(browser,base,saved,list(old.LINES),viewport={'width':width,'height':height});page=ctx.new_page();q.observe(page,base,report)
        page.goto(base+'game/?v=cyan-1');old.prior.assert_copy(page);old.prior.skip(page);title=colors(page,'[data-title-start]');old.prior.menu_ready(page)
        page.locator('[data-title-start]').hover();hover=colors(page,'[data-title-start]');page.mouse.down();pressed=colors(page,'[data-title-start]');page.mouse.move(2,2);page.mouse.up()
        page.screenshot(path=str(OUT/f'title-cyan-{width}x{height}.png'));page.locator('[data-title-start]').click();d.map_ready(page);assert_no_new_scene(page)
        samples={selector:colors(page,selector) for selector in ['[data-wm-next]','[data-game-nav="map"].is-active','.wm-landmark.is-next .wm-label','.wm-landmark.is-next .wm-status-chip']}
        page.screenshot(path=str(OUT/f'map-current-cyan-{width}x{height}.png'));page.locator('[data-wm-tools-open]').focus();page.locator('[data-wm-tools-open]').click();page.wait_for_selector('#wm-tools-dialog[open]')
        page.locator('#wm-tools-dialog .wm-route-details>summary').click();current=colors(page,'#wm-tools-dialog button[aria-current=true]');page.locator('[data-wm-tools-close]').click()
        before=q.snapshot(page);page.locator('[data-wm-next]').click();scene=new_scene_snapshot(page);assert q.snapshot(page)==before
        next_color=colors(page,'.story-dialogue__next');page.screenshot(path=str(OUT/f'five-lake-dialogue-cyan-{width}x{height}.png'));page.locator('.story-dialogue__skip').click();assert_no_new_scene(page)
        page.locator('[data-game-nav="city"]').click();old.prior.c.city_loaded(page);city={'activeNav':colors(page,'[data-game-nav="city"].is-active'),'primary':colors(page,'.city-primary .primary')};page.screenshot(path=str(OUT/f'city-primary-cyan-{width}x{height}.png'))
        page.locator('[data-game-nav="shelf"]').click();page.wait_for_selector('#collection-books');shelf=colors(page,'[data-game-nav="shelf"].is-active');old.no_page_overflow(page);assert q.snapshot(page)==before
        page.screenshot(path=str(OUT/f'shelf-active-cyan-{width}x{height}.png'))
        rows.append({'viewport':[width,height],'title':title,'titleHover':hover,'titlePressed':pressed,'mapSemanticSurfaces':samples,'routeCurrent':current,'newScene':scene,'dialogueCta':next_color,'city':city,'shelfActiveNav':shelf,'darkPanelsAndWorldArtworkRetained':True,'noReadingProgressWritten':True});ctx.close()
    report['fiveViewportCyanSemanticSurfaces']=rows


def skip_history_locked_and_replay(browser,base,report):
    rows=[]
    saved=q.fixture(['four-truths'],{},'five-aggregates');ctx=context(browser,base,saved,list(old.LINES));page=ctx.new_page();q.observe(page,base,report);old.fresh_map(page,base);page.locator('[data-wm-next]').click();new_scene_snapshot(page)
    assert q.snapshot(page)==saved;page.locator('.story-dialogue__skip').click();assert_no_new_scene(page);page.reload();d.map_ready(page);assert_no_new_scene(page);page.locator('[data-wm-next]').click();page.wait_for_selector('body[data-collection-book="five-aggregates"][data-collection-index="0"]')
    assert q.snapshot(page)['completed']==['four-truths'];rows.append({'fixture':'first-complete-five-unstarted','skipReturnsMapThenLegalReaderWithoutRepeat':True,'noCompletionFabricated':True});ctx.close()
    saved=q.fixture(['four-truths'],{},'five-aggregates');ctx=context(browser,base,saved,list(old.LINES));page=ctx.new_page();q.observe(page,base,report);old.fresh_map(page,base)
    target=page.locator('.wm-landmark[data-book="five-aggregates"]').first;target.focus();target.click();page.wait_for_selector('#wm-dialog[open]');page.locator('[data-wm-read="five-aggregates"]').click();new_scene_snapshot(page)
    page.keyboard.press('Escape');assert_no_new_scene(page);assert '/book/' not in page.url and q.snapshot(page)==saved
    rows.append({'fixture':'native-topic-popup','newSceneCtaKeepsFocusAfterDialogClose':True,'escapeSkipsWithoutOpeningBookOrWritingProgress':True});ctx.close()
    for index in [0,4]:
        saved=q.fixture(['four-truths'],{'five-aggregates':index},'five-aggregates');ctx=context(browser,base,saved,list(old.LINES));page=ctx.new_page();q.observe(page,base,report);old.fresh_map(page,base);page.locator('[data-wm-next]').click();page.wait_for_selector(f'body[data-collection-book="five-aggregates"][data-collection-index="{index}"]')
        q.click_next(page,index+1);page.locator('.collection-reader-return').click();d.map_ready(page);assert_no_new_scene(page);assert q.snapshot(page)['completed']==['four-truths']
        rows.append({'fixture':'existing-five-bookmark','resumeIndex':index,'noInsertedScene':True,'oneActualNextAndReturnNoExtraCompletion':True});ctx.close()
    saved=q.fixture(['four-truths','five-aggregates'],{'five-aggregates':53},'six-senses');ctx=context(browser,base,saved,list(old.LINES));page=ctx.new_page();q.observe(page,base,report);old.fresh_map(page,base);page.locator('[data-game-nav="shelf"]').click();page.wait_for_selector('[data-collection-read="five-aggregates"]');page.locator('[data-collection-read="five-aggregates"]').click();page.wait_for_selector('body[data-collection-book="five-aggregates"][data-collection-index="0"]')
    assert q.snapshot(page)['completed']==saved['completed'];rows.append({'fixture':'historic-five-completed','reviewStartsOriginalReaderWithoutScene':True,'originalCompletedSetRetained':True});ctx.close()
    saved=q.fixture([] ,{'five-aggregates':9},'five-aggregates');ctx=context(browser,base,saved,[]);page=ctx.new_page();q.observe(page,base,report);old.fresh_map(page,base)
    target=page.locator('.wm-landmark[data-book="five-aggregates"]').first;target.focus();target.click();page.wait_for_selector('#wm-dialog[open]');assert page.locator('[data-wm-read="five-aggregates"]').count()==0;assert_no_new_scene(page)
    page.goto(base+'five-aggregates/book/?collection=1&collectionReturn=game&collectionStory=cyan-1');page.wait_for_url(re.compile(r'.*/game/\?.*notice=locked#map'));d.map_ready(page);assert_no_new_scene(page);assert q.snapshot(page)==saved
    rows.append({'fixture':'locked-five-with-future-bookmark','lockedLandmarkAndDirectReaderCannotUseSceneToBypassFirst':True,'futureBookmarkPreserved':True});ctx.close()
    # Both existing explicit replays remain presentation-only; neither opens five.
    saved=q.fixture(['four-truths'],{},'five-aggregates');ctx=context(browser,base,saved,list(old.LINES));page=ctx.new_page();q.observe(page,base,report);old.fresh_map(page,base)
    before=page.evaluate('(keys)=>keys.map(k=>localStorage.getItem(k))',[q.KEY,STORY_KEY])
    for selector,scenes in [('[data-wm-story-replay]',list(old.LINES)[:3]),('[data-wm-completion-replay]',list(old.LINES)[3:])]:
        page.locator('[data-wm-tools-open]').focus();page.locator('[data-wm-tools-open]').click();page.locator(selector).click()
        for scene in scenes:old.assert_scene(page,scene);page.locator('.story-dialogue__next').click()
        assert '/book/' not in page.url;assert_no_new_scene(page)
    assert before==page.evaluate('(keys)=>keys.map(k=>localStorage.getItem(k))',[q.KEY,STORY_KEY])
    rows.append({'fixture':'explicit-existing-replays','openingAndCompletionReplayNoFiveEntryOrSeenOrCompletionWrites':True});ctx.close()
    report['isolatedEligibilitySkipHistoryReplay']=rows


def author_reset_new_seen(browser,base,report):
    local,session=old.prior.seeded_profile();local[STORY_KEY]=json.dumps({'version':1,'seenSceneIds':list(old.LINES)+[FIVE_SCENE]})
    ctx=old.prior.context(browser,base,local,session);page=ctx.new_page();q.observe(page,base,report);page.goto(base+'game/?author=1&v=cyan-1');old.prior.assert_copy(page);old.prior.skip(page)
    before=old.storage(page);page.once('dialog',lambda dialog:dialog.dismiss());page.locator('[data-title-author-reset]').click();assert old.storage(page)==before
    page.once('dialog',lambda dialog:dialog.accept());page.locator('[data-title-author-reset]').click();old.prior.assert_copy(page);old.prior.skip(page)
    after=old.storage(page);assert STORY_KEY not in after['local'] and q.KEY not in after['local']
    for key in ['sutrazen.play.v1','sutrazen.reader.position','auth.roles','site.preference']:assert after['local'][key]==before['local'][key],key
    page.locator('[data-title-start]').click();d.map_ready(page);old.assert_scene(page,'arrival-at-wheel');assert q.snapshot(page) is None;assert_no_new_scene(page)
    report['authorResetNewSeen']={'isolatedHistoricalProfile':True,'nativeCancelStorageByteIdentical':True,'confirmClearsNewFiveSceneWithSameV1Namespace':True,'publicReaderPrototypeAndOtherKeysRetained':True,'freshFirstArrivalShownFiveStillNotUnlocked':True};ctx.close()


def save(report):
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')


def main():
    OUT.mkdir(parents=True,exist_ok=True);report=guard_sources();report.update({'phase':'Local focused validation','javascriptErrors':[],'httpErrors':[],'physicalSafari':'Not tested; desktop Chromium viewport and input simulation','fixtureNotice':'Isolated synthetic history cases are separate from the actual first29 and four real Five Aggregates steps.'})
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(q.Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);actual_first_to_aggregates(browser,base,report);print('actualfirst29 thenfive passed',flush=True);palette_five_sizes(browser,base,report);print('palettefive sizes passed',flush=True);skip_history_locked_and_replay(browser,base,report);author_reset_new_seen(browser,base,report);browser.close()
        assert not report['javascriptErrors'],report['javascriptErrors'];assert not report['httpErrors'],report['httpErrors'];report['result']='passed'
    except Exception as error:report['result']='failed';report['error']=repr(error);raise
    finally:server.shutdown();save(report)
    print(json.dumps({'result':report['result'],'report':str(OUT/'validation.json')},ensure_ascii=False))


if __name__=='__main__':main()
