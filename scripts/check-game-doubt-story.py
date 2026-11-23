#!/usr/bin/env python3
"""Independent first-book doubt story and dark translucent UI validation.

Browser histories are isolated fixtures. The native first-book walk is kept
separate from fixture-based history/review checks; no completion is manufactured
for that walk. This script never edits production source or historical evidence.
"""
from pathlib import Path
import functools,http.server,importlib.util,json,re,subprocess,threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/previews/game-doubt-story'
spec=importlib.util.spec_from_file_location('prologue_qa',ROOT/'scripts/check-game-prologue.py')
prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
q=prior.d.q;d=prior.d;q.BASE='44dce2f6624e568ff83d6cf79e675fe61a53c325'
SIZES=q.SIZES;STORY_KEY='sutrazen.play.story.v1'
ARRIVAL='咦？我剛才明明還趴在窗邊等朋友回訊息……怎麼一抬頭，就到了法輪遺跡？進去看看！'
RECEIPT='sutrazen.play.story-first-completion.v1'
LINES={
 'arrival-at-wheel':ARRIVAL,
 'doubt-at-ruins':'愚痴……',
 'doubt-detour':'這隻滿身問號的生物是什麼啊？竟然擋在入口……我先繞過牠，進去看看好了。',
 'first-book-insight':'讀完四聖諦，苦與離苦的路好像清楚一點了。「正智」和「慧根／慧力」，我也想繼續慢慢練習！',
 'doubt-recedes':'咦，剛才那隻怪生物身上的問號變少了……牠退進霧裡，入口也露出來了。先把剛才學到的記在心裡，再走下一站吧！',
}


def guard_sources():
    originals=q.ORDER+['docs/'+book for book in q.ORDER]+['index.html','shelf.css','sitemap.xml','robots.txt','googlee0c995331ec518ae.html','reader-controls.css','reader-layout.js','reader-restart.js','picture-panel-focus.js','picture-panel-focus.css','docs/seo','map-topic-resources.css','scripts/site_seo.py','scripts/build-seo.py','scripts/check-seo.py']
    changed=subprocess.check_output(['git','diff','--name-only',q.BASE,'--',*originals],cwd=ROOT,text=True).splitlines()
    assert set(changed)<= {'four-truths/book/index.html'},changed
    old=lambda path:subprocess.check_output(['git','show',q.BASE+':'+path],cwd=ROOT,text=True)
    html='four-truths/book/index.html';assert (ROOT/html).read_text().replace('../../play/collection/reader-bridge.js?v=doubt-1','../../play/collection/reader-bridge.js?v=1')==old(html)
    files=[p for p in subprocess.check_output(['git','ls-tree','-rz','--name-only',q.BASE,'--',*originals],cwd=ROOT,text=True).split('\0') if p]
    report={'baseline':q.BASE,'protectedOriginalFiles':len(files),'singleOriginalHtmlException':'Four-truths bridge src cache query only; normalize then full text equal','originalNarrationScriptureArtReaderJsAndCss':'byte-for-byte unchanged','rootHomepageSeoGoogleAndSharedReaderControls':'byte-for-byte unchanged'}
    paths=['play/collection/store.js','play/reader-bridge.js',
           'play/route','play/prologue','play/worldmap-v4/data.js',
           'play/worldmap-v4/camera.js','play/visual-v2/network-data.js',
           'play/visual-v2/assets','play/worldmap-v4/assets',
           'play/assets/CC1A7C32-0620-4DB2-BCD2-A9457A83C259.jpeg',
           'play/story/assets/kitten-traveler-portrait-concept.png']
    changed=subprocess.check_output(['git','diff','--name-only',q.BASE,'--',*paths],cwd=ROOT,text=True).splitlines()
    assert not changed,changed
    report['additionalUnchangedCoreAndArt']=paths
    bridge=(ROOT/'play/collection/reader-bridge.js').read_text()
    bridge=bridge.replace("const [{ store }, { CATALOG, COLLECTION_TEXT: text }, policy, {issueFirstCompletionReceipt}]", "const [{ store }, { CATALOG, COLLECTION_TEXT: text }, policy]")
    bridge=bridge.replace("import('../route/eligibility.js'), import('../story/completion-receipt.js?v=doubt-1').catch(() => ({issueFirstCompletionReceipt: () => false})),", "import('../route/eligibility.js'),")
    bridge=bridge.replace("      if (bookId === 'four-truths') issueFirstCompletionReceipt();\n",'')
    assert bridge==old('play/collection/reader-bridge.js')
    reset=(ROOT/'play/title-review.js').read_text().replace("import {clearFirstCompletionReceipt} from './story/completion-receipt.js?v=doubt-1';\n",'').replace("./story/store.js?v=doubt-1","./story/store.js?v=prologue-1").replace("  if (!clearFirstCompletionReceipt()) failures.push('first-completion-receipt');\n",'')
    assert reset==old('play/title-review.js')
    report['authorizedBridgeAndResetExceptions']='Exact receipt import/issue and receipt clear only; removing those lines and story cache query equals baseline'
    return report


def context(browser,base,saved=None,seen=None,**options):
    if saved is not None or seen is not None:
        entries=[]
        if saved is not None:entries.append({'name':q.KEY,'value':json.dumps(saved)})
        if seen is not None:entries.append({'name':STORY_KEY,'value':json.dumps({'version':1,'seenSceneIds':seen})})
        options['storage_state']={'cookies':[],'origins':[{'origin':base.rstrip('/'),'localStorage':entries}]}
    return q.context_for(browser,base,**options)


def storage(page):
    return page.evaluate('''()=>({local:Object.fromEntries(Object.entries(localStorage).sort()),session:Object.fromEntries(Object.entries(sessionStorage).sort())})''')


def no_page_overflow(page):
    result=page.evaluate('''()=>({screen:[innerWidth,innerHeight],outer:[document.documentElement.scrollWidth,document.documentElement.scrollHeight]})''')
    assert all(a<=b+1 for a,b in zip(result['outer'],result['screen'])),result
    assert '[object Object]' not in page.locator('body').inner_text()
    return result


def assert_art_undimmed(page):
    result=page.locator('.wm-background').evaluate('''n=>{const result=[];for(let e=n;e&&e!==document.body;e=e.parentElement){const s=getComputedStyle(e);result.push({tag:e.tagName,class:e.className,opacity:s.opacity,filter:s.filter})}return result}''')
    assert all(n['opacity']=='1' and n['filter']=='none' for n in result),result
    return result


def rgba(color):
    values=[float(x) for x in re.findall(r'[\d.]+',color)]
    assert color.startswith(('rgb(','rgba(')) and len(values) in [3,4],color
    return values[:3]+[values[3] if len(values)==4 else 1]


def luminance(rgb):
    linear=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in [n/255 for n in rgb]]
    return sum(a*b for a,b in zip(linear,[.2126,.7152,.0722]))


def dark_translucent(page,selector,text_selector=None):
    """Use white behind dark alpha as a conservative artwork contrast bound."""
    target=page.locator(selector)
    style=target.evaluate('''n=>{const s=getComputedStyle(n);return {background:s.backgroundColor,image:s.backgroundImage,color:s.color,filter:s.backdropFilter}}''')
    bg=rgba(style['background'])
    stops=[rgba(value) for value in re.findall(r'rgba?\([^)]*\)',style['image'])]
    backgrounds=stops if stops else [bg]
    assert all(0<c[3]<1 and luminance(c[:3])<.12 for c in backgrounds),style
    text=page.locator(text_selector) if text_selector else target
    fg=rgba(text.evaluate('(n)=>getComputedStyle(n).color'))
    composed=max(([c*color[3]+255*(1-color[3]) for c in color[:3]] for color in backgrounds),key=luminance)
    a,b=sorted([luminance(fg[:3]),luminance(composed)],reverse=True);contrast=(a+.05)/(b+.05)
    assert contrast>=4.5,{'selector':selector,'style':style,'contrast':contrast}
    return {'selector':selector,'computed':style,'whiteBackdropTextContrast':contrast}


def portrait_unclipped(page):
    result=page.locator('.story-dialogue__portrait').evaluate('''async n=>{const i=n.querySelector('img');await i.decode();const p=n.getBoundingClientRect(),r=i.getBoundingClientRect(),s=getComputedStyle(n),t=getComputedStyle(i);return {portrait:p.toJSON(),image:r.toJSON(),portraitOverflow:s.overflow,portraitRadius:s.borderRadius,imageClip:t.clipPath,imageRadius:t.borderRadius,fit:t.objectFit,natural:[i.naturalWidth,i.naturalHeight]}}''')
    assert result['portraitOverflow']=='visible' and result['portraitRadius']=='0px' and result['imageClip']=='none' and result['imageRadius']=='0px' and result['fit']=='contain',result
    p=result['portrait'];i=result['image']
    assert i['left']>=p['left'] and i['right']<=p['right']+.5 and i['top']>=p['top'] and i['bottom']<=p['bottom']+.5,result
    return result


def dialogue_geometry(page):
    panel=page.locator('.story-dialogue:not([hidden])');panel.wait_for()
    bounds=panel.bounding_box();dock=page.locator('.game-dock').bounding_box()
    assert bounds['x']>=0 and bounds['y']>=0 and bounds['x']+bounds['width']<=page.viewport_size['width']+1 and bounds['y']+bounds['height']<dock['y'],(bounds,dock)
    for selector in ['.story-dialogue__next','.story-dialogue__skip']:
        action=page.locator(selector)
        if not action.is_visible():continue
        action.scroll_into_view_if_needed();r=action.bounding_box();assert r['width']>=48 and r['height']>=48,r
    no_page_overflow(page);assert_art_undimmed(page)
    return bounds


def scene_snapshot(page):
    panel=page.locator('.story-dialogue:not([hidden])');panel.wait_for()
    return {'id':panel.get_attribute('data-scene'),'actor':panel.get_attribute('data-actor'),
            'speaker':panel.locator('h2').inner_text(),'text':panel.locator('.story-dialogue__line').text_content()}


def visible_marks(page,selector):
    return page.locator(selector).evaluate_all('''nodes=>nodes.filter(n=>{const s=getComputedStyle(n);return n.getClientRects().length&&s.visibility!=='hidden'&&Number(s.opacity)>.9}).length''')


def assert_scene(page,scene_id):
    page.wait_for_selector(f'.story-dialogue[data-scene="{scene_id}"]:not([hidden])')
    result=scene_snapshot(page);assert result['text']==LINES[scene_id],result
    assert result['actor']==('doubt' if scene_id=='doubt-at-ruins' else 'traveler'),result
    dialogue_geometry(page);portrait_unclipped(page)
    expected=6 if result['actor']=='doubt' else 0
    assert visible_marks(page,'.story-dialogue [data-doubt-portrait-mark]')==expected,result
    if scene_id in ['doubt-at-ruins','doubt-detour','first-book-insight']:stage_visible_below_dialogue(page)
    return result


def stage_visible_below_dialogue(page):
    q.settle(page)
    result=page.evaluate('''()=>{const frame=document.querySelector('[data-doubt-stage]'),panel=document.querySelector('.story-dialogue'),dock=document.querySelector('.game-dock');return {frame:frame.getBoundingClientRect().toJSON(),panel:panel.getBoundingClientRect().toJSON(),dock:dock.getBoundingClientRect().toJSON(),camera:window.SutraZenWorldmap.getState().camera,marks:[...frame.querySelectorAll('[data-doubt-mark]')].filter(n=>Number(getComputedStyle(n).opacity)>.9&&getComputedStyle(n).visibility!=='hidden').map(n=>n.getBoundingClientRect().toJSON())}}''')
    f,p,dock=result['frame'],result['panel'],result['dock']
    assert f['top']>=p['bottom'] and f['bottom']<=dock['top'] and f['left']>=0 and f['right']<=page.viewport_size['width'],result
    for mark in result['marks']:assert mark['top']>=p['bottom'] and mark['bottom']<=dock['top'] and mark['left']>=0 and mark['right']<=page.viewport_size['width'],result
    assert result['camera']['safeInsets']['top']>0,result
    return result


def backdrop_clear(page,selector):
    result=page.locator(selector).evaluate('(n)=>({background:getComputedStyle(n,"::backdrop").backgroundColor,filter:getComputedStyle(n,"::backdrop").backdropFilter})')
    assert rgba(result['background'])[3]==0 and result['filter']=='none',result
    return result


def viewport_theme_checks(browser,base,report):
    rows=[]
    for width,height in SIZES:
        ctx=context(browser,base,viewport={'width':width,'height':height});p=ctx.new_page();q.observe(p,base,report)
        p.goto(base+'game/');prior.assert_copy(p);prior.skip(p)
        title=dark_translucent(p,'.game-title-paper','[data-title-heading]');prior.menu_ready(p)
        p.screenshot(path=str(OUT/f'title-dark-{width}x{height}.png'))
        p.locator('[data-title-settings]').click();p.wait_for_selector('#game-settings[open]')
        settings=dark_translucent(p,'#game-settings','#game-settings-title');backdrop_clear(p,'#game-settings')
        assert p.locator('#game-settings').get_by_text(re.compile('深色模式|亮色模式|切換主題')).count()==0
        p.screenshot(path=str(OUT/f'settings-dark-{width}x{height}.png'));p.locator('[data-game-settings-close]').click()
        p.locator('[data-title-start]').click();d.map_ready(p);assert_scene(p,'arrival-at-wheel')
        dialogue=dark_translucent(p,'.story-dialogue','.story-dialogue__line');ears=portrait_unclipped(p)
        p.screenshot(path=str(OUT/f'arrival-full-ears-{width}x{height}.png'))
        p.locator('.story-dialogue__next').click();assert_scene(p,'doubt-at-ruins')
        assert p.locator('[data-doubt-stage]').get_attribute('data-doubt-state')=='waiting'
        assert visible_marks(p,'[data-doubt-stage] [data-doubt-mark]')==7
        p.screenshot(path=str(OUT/f'doubt-before-reading-{width}x{height}.png'))
        p.locator('.story-dialogue__next').click();assert_scene(p,'doubt-detour');assert q.snapshot(p) is None
        p.locator('.story-dialogue__skip').click();assert d.camera(p)['safeInsets']['top']==0
        p.locator('[data-wm-tools-open]').focus();p.locator('[data-wm-tools-open]').click();p.wait_for_selector('#wm-tools-dialog[open]')
        tools=dark_translucent(p,'#wm-tools-dialog','#wm-tools-title');backdrop_clear(p,'#wm-tools-dialog');p.locator('[data-wm-tools-close]').click()
        p.locator('[data-game-nav="city"]').click();prior.c.city_loaded(p)
        p.locator('[data-city-label="town"]').click();p.wait_for_selector('#city-dialog[open]')
        city=dark_translucent(p,'#city-dialog','#city-dialog-title');backdrop_clear(p,'#city-dialog')
        p.screenshot(path=str(OUT/f'city-dark-dialog-{width}x{height}.png'));p.locator('[data-city-close]').click()
        p.locator('[data-game-nav="shelf"]').click();p.wait_for_selector('#collection-books')
        shelf=dark_translucent(p,'.collection-empty','.collection-empty h2');no_page_overflow(p)
        p.screenshot(path=str(OUT/f'shelf-dark-{width}x{height}.png'))
        rows.append({'viewport':[width,height],'title':title,'settings':settings,'dialogue':dialogue,'tools':tools,'city':city,'shelf':shelf,'portraitFullContainNoCircularClip':ears,'waitingWorldQuestionMarks':7,'doubtOnlySpokenLine':'愚痴……','noReadingCompletionOrBookmark':q.snapshot(p) is None,'worldArtUndimmed':True})
        ctx.close()
    report['fiveViewportThemeAndDialogue']=rows


def actual_first_completion(browser,base,report):
    ctx=context(browser,base,reduced_motion='no-preference');p=ctx.new_page();q.observe(p,base,report);fresh_map(p,base)
    before=[]
    for scene_id in ['arrival-at-wheel','doubt-at-ruins','doubt-detour']:
        before.append(assert_scene(p,scene_id));p.locator('.story-dialogue__next').click()
    p.wait_for_selector('body[data-collection-book="four-truths"]');assert p.locator('body').get_attribute('data-collection-total')=='29'
    trace=[0]
    for index in range(1,6):q.click_next(p,index);trace.append(index)
    assert q.snapshot(p)['completed']==[];p.reload();p.wait_for_selector('body[data-collection-index="5"]')
    p.set_viewport_size({'width':844,'height':390});p.locator('.collection-reader-return').click();d.map_ready(p)
    assert not p.locator('.story-dialogue').is_visible() and '6／29' in p.locator('[data-wm-next]').inner_text()
    p.locator('[data-wm-next]').click();p.wait_for_selector('body[data-collection-index="5"]')
    for index in range(6,29):q.click_next(p,index);trace.append(index)
    assert q.snapshot(p)['completed']==[] and p.locator('#next').inner_text()=='完成這本'
    assert p.evaluate('(key)=>sessionStorage.getItem(key)||localStorage.getItem(key)',RECEIPT) is None
    p.locator('#next').click();d.map_ready(p);first=assert_scene(p,'first-book-insight')
    assert q.snapshot(p)['completed']==['four-truths']
    assert p.evaluate('(key)=>sessionStorage.getItem(key)||localStorage.getItem(key)',RECEIPT) is None
    p.wait_for_timeout(1000);assert visible_marks(p,'[data-doubt-stage] [data-doubt-mark]')==2
    p.screenshot(path=str(OUT/'actual-first-read-questionmarks-thinning-844x390.png'))
    p.locator('.story-dialogue__next').click();second=assert_scene(p,'doubt-recedes');p.wait_for_timeout(1600)
    assert p.locator('[data-doubt-stage]').get_attribute('data-doubt-state')=='receding'
    assert p.locator('.doubt-stage__creature').evaluate('(n)=>Number(getComputedStyle(n).opacity)')<.01
    p.screenshot(path=str(OUT/'actual-first-read-creature-receded-844x390.png'))
    p.locator('.story-dialogue__next').click();p.wait_for_selector('#wm-dialog[open]')
    assert '法輪碼頭' in p.locator('#wm-dialog').inner_text() and q.snapshot(p)['completed']==['four-truths']
    p.screenshot(path=str(OUT/'actual-first-book-reward-844x390.png'))
    p.locator('[data-wm-next-station]').click();assert '/book/' not in p.url
    assert p.locator('.wm-landmark.is-next').get_attribute('data-book')=='five-aggregates'
    p.reload();d.map_ready(p);assert not p.locator('.story-dialogue').is_visible() and not p.locator('#wm-dialog').is_visible()
    saved=q.snapshot(p);seen=p.evaluate('(key)=>JSON.parse(localStorage.getItem(key))',STORY_KEY);assert seen['version']==1 and seen['seenSceneIds']==list(LINES)
    # A real public reader review goes via its chapter menu, not a fake store write.
    p.locator('[data-game-nav="shelf"]').click();p.wait_for_selector('[data-collection-read="four-truths"]');p.locator('[data-collection-read="four-truths"]').click();p.wait_for_selector('body[data-collection-index="0"]')
    options=p.locator('#page-select option').evaluate_all('(nodes)=>nodes.map(n=>n.value)');p.locator('#page-select').select_option(options[-1]);p.wait_for_selector('body[data-collection-index="28"]');p.locator('#next').click();p.wait_for_selector('#collection-books')
    assert q.snapshot(p)['completed']==['four-truths'] and 'completed=' not in p.url
    assert p.evaluate('(key)=>sessionStorage.getItem(key)||localStorage.getItem(key)',RECEIPT) is None
    p.locator('[data-game-nav="map"]').click();d.map_ready(p);assert not p.locator('.story-dialogue').is_visible()
    # Explicit replay is presentation-only and leaves both records byte identical.
    raw=p.evaluate('(key)=>localStorage.getItem(key)',q.KEY);seen_raw=p.evaluate('(key)=>localStorage.getItem(key)',STORY_KEY)
    p.locator('[data-wm-tools-open]').focus();p.locator('[data-wm-tools-open]').click();p.locator('[data-wm-completion-replay]').click()
    assert_scene(p,'first-book-insight');p.locator('.story-dialogue__next').click();assert_scene(p,'doubt-recedes');p.locator('.story-dialogue__next').click()
    assert '/book/' not in p.url and not p.locator('#wm-dialog').is_visible()
    assert p.evaluate('(key)=>localStorage.getItem(key)',q.KEY)==raw and p.evaluate('(key)=>localStorage.getItem(key)',STORY_KEY)==seen_raw
    report['actualFirstBook']={'beforeBookScenes':before,'actualSequentialNextIndices':trace,'reloadRotateAndReturnAtIndex':5,'completionEmptyUntilExplicitFinish':True,'receiptOnlyIssuedByActualFinishThenConsumed':True,'afterBookScenes':[first,second],'questionMarksBefore':7,'questionMarksAfter':2,'retreatThenOriginalReward':True,'nextStationFiveAggregatesNoAutostart':True,'reloadNoRepeatedStoryOrReward':True,'actualReviewChapterSelectionLastStepNoNewReceiptOrReward':True,'explicitStoryReplayNoProgressOrSeenWrites':True,'savedAfterFirstCompletion':saved};ctx.close()


def history_and_guard_checks(browser,base,report):
    cases=[]
    saved=q.fixture(['four-truths'],{'four-truths':28,'five-aggregates':4,'four-jhanas':9},'four-jhanas')
    for label,seen in [('old-v1-arrival-only',['arrival-at-wheel']),('historical-encounter-no-receipt',list(LINES)[:3])]:
        ctx=context(browser,base,saved,seen);p=ctx.new_page();q.observe(p,base,report);p.goto(base+'game/?completed=four-truths#map');d.map_ready(p)
        assert not p.locator('.story-dialogue').is_visible() and q.snapshot(p)==saved
        assert p.locator('[data-doubt-stage]').get_attribute('data-doubt-state')=='hidden'
        assert p.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).seenSceneIds',STORY_KEY)==seen
        p.reload();d.map_ready(p);assert not p.locator('.story-dialogue').is_visible()
        p.goto(base+'four-jhanas/book/?collection=1&collectionReturn=game');p.wait_for_url('**/game/?notice=locked#map');d.map_ready(p)
        assert q.snapshot(p)==saved and not p.locator('.story-dialogue').is_visible()
        assert p.locator('.wm-landmark.is-next').get_attribute('data-book')=='five-aggregates'
        cases.append({'fixture':label,'forgedCompletionQueryAndReloadNoNewStory':True,'version1SeenPreserved':True,'historicalCompletedAndFutureBookmarkUnchanged':True,'futureReaderStillLocked':True});ctx.close()
    # Existing first-book bookmark continues directly without adding a new cutscene.
    partial=q.fixture([],{q.ORDER[0]:4},q.ORDER[0]);ctx=context(browser,base,partial,[]);p=ctx.new_page();q.observe(p,base,report);fresh_map(p,base)
    assert not p.locator('.story-dialogue').is_visible();p.locator('[data-wm-next]').click();p.wait_for_selector('body[data-collection-index="4"]');q.click_next(p,5);p.locator('.collection-reader-return').click();d.map_ready(p)
    assert not p.locator('.story-dialogue').is_visible() and q.snapshot(p)['completed']==[]
    cases.append({'fixture':'existing-first-bookmark','resumeIndex':4,'noInsertedEncounterOrCompletion':True});ctx.close()
    # A presentation receipt alone cannot mark a book completed or evade its policy.
    incomplete=q.fixture([],{q.ORDER[0]:28},q.ORDER[0]);ctx=context(browser,base,incomplete,list(LINES)[:3])
    ctx.add_init_script('''sessionStorage.setItem('''+json.dumps(RECEIPT)+''',JSON.stringify({version:1,event:'four-truths-reader-finished'}))''')
    p=ctx.new_page();q.observe(p,base,report);p.goto(base+'game/?completed=four-truths#map');d.map_ready(p)
    assert not p.locator('.story-dialogue').is_visible() and not p.locator('#wm-dialog').is_visible() and q.snapshot(p)==incomplete
    assert p.evaluate('(k)=>sessionStorage.getItem(k)||localStorage.getItem(k)',RECEIPT) is None
    cases.append({'fixture':'receipt-without-actual-completion','noStoryRewardOrCompletionFabricated':True,'receiptConsumed':True});ctx.close()
    report['isolatedHistoryAndPolicyChecks']=cases


def reset_new_scenes(browser,base,report):
    local,session=prior.seeded_profile();local[STORY_KEY]=json.dumps({'version':1,'seenSceneIds':list(LINES)})
    receipt=json.dumps({'version':1,'event':'four-truths-reader-finished'});local[RECEIPT]=receipt;session[RECEIPT]=receipt
    ctx=prior.context(browser,base,local,session);p=ctx.new_page();q.observe(p,base,report);p.goto(base+'game/?author=1');prior.assert_copy(p);prior.skip(p)
    before=storage(p);p.once('dialog',lambda dialog:dialog.dismiss());p.locator('[data-title-author-reset]').click();assert storage(p)==before
    p.once('dialog',lambda dialog:dialog.accept());p.locator('[data-title-author-reset]').click();prior.assert_copy(p);prior.skip(p)
    after=storage(p)
    for key in [q.KEY,STORY_KEY,RECEIPT,'sutrazen.play.route-metadata.v1']:assert key not in after['local'],key
    for key in [RECEIPT,'sutrazen.play.story.session.v1','sutrazen.play.collection.session.v1']:assert key not in after['session'],key
    for key in ['sutrazen.play.v1','sutrazen.reader.position','auth.roles','site.preference']:assert after['local'][key]==before['local'][key],key
    p.locator('[data-title-start]').click();d.map_ready(p)
    for scene_id in list(LINES)[:3]:assert_scene(p,scene_id);p.locator('.story-dialogue__next').click()
    p.wait_for_selector('body[data-collection-index="0"]');assert q.snapshot(p)['completed']==[]
    report['authorResetNewScenes']={'nativeCancelByteIdentical':True,'confirmedAllNewSceneIdsAndBothReceiptCopiesCleared':True,'sameNamespaceVersion1':True,'originalPublicReaderAndOtherKeysPreserved':True,'arrivalAndDoubtEncounterCanPlayFreshAgain':True};ctx.close()


def actor_asset_failure(browser,base,report):
    cases=[]
    for actor,filename in [('traveler','kitten-traveler-portrait-concept.png'),('doubt','doubt-creature-concept.png')]:
        ctx=context(browser,base);p=ctx.new_page();q.observe(p,base,report);aborted=[]
        def abort(route):aborted.append(route.request.url);route.abort()
        pattern='**/play/story/assets/'+filename;p.route(pattern,abort);fresh_map(p,base)
        for scene_id in list(LINES)[:3]:
            p.wait_for_selector(f'.story-dialogue[data-scene="{scene_id}"]:not([hidden])')
            current=scene_snapshot(p);assert current['text']==LINES[scene_id]
            if current['actor']==actor:p.wait_for_selector('.story-dialogue--no-art:not([hidden])')
            dialogue_geometry(p);p.locator('.story-dialogue__next').click()
        p.wait_for_selector('body[data-collection-index="0"]');q.click_next(p,1)
        assert q.snapshot(p)['completed']==[] and aborted
        cases.append({'actor':actor,'expectedInjectedAbortCount':len(aborted),'fullTextAndAllNextActionsStillReachRealReader':True,'actualReaderNextWorks':True,'noCompletionFabricated':True});ctx.close()
    report['actorAssetFailure']=cases


def pending_and_optional_receipt_failure(browser,base,report):
    cases=[];saved=q.fixture(['four-truths'],{'four-truths':28},'five-aggregates')
    for label,seen,receipt in [('pending-last-line',list(LINES)[:4],False),('explicit-dismiss',list(LINES)[:3],True)]:
        ctx=context(browser,base,saved,seen)
        if receipt:ctx.add_init_script("if(!sessionStorage.getItem('qa.doubt.seeded')){sessionStorage.setItem('"+RECEIPT+"',JSON.stringify({version:1,event:'four-truths-reader-finished'}));sessionStorage.setItem('qa.doubt.seeded','yes')}")
        p=ctx.new_page();q.observe(p,base,report);fresh_map(p,base)
        assert_scene(p,'first-book-insight' if receipt else 'doubt-recedes')
        p.locator('.story-dialogue__skip' if receipt else '.story-dialogue__next').click();p.wait_for_selector('#wm-dialog[open]')
        assert 'doubt-recedes' in p.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).seenSceneIds',STORY_KEY)
        assert q.snapshot(p)==saved;p.reload();d.map_ready(p);assert not p.locator('.story-dialogue').is_visible() and not p.locator('#wm-dialog').is_visible()
        cases.append({'isolatedFixture':label,'pendingResumesOnlyRemainingLine':not receipt,'explicitDismissAcknowledgesRemainingQueue':receipt,'reloadNoRepeatedQueueOrReward':True,'collectionUnchanged':True});ctx.close()
    # Only this optional module is denied inside the reader. The map is allowed
    # to load it normally on return, so its mandatory bootstrap is not sabotaged.
    saved=q.fixture([],{q.ORDER[0]:27},q.ORDER[0]);ctx=context(browser,base,saved,list(LINES)[:3]);p=ctx.new_page();q.observe(p,base,report);aborted=[]
    def fail_reader_helper(route):
        if '/four-truths/book/' in route.request.frame.url:aborted.append(route.request.url);route.abort()
        else:route.continue_()
    p.route('**/play/story/completion-receipt.js?v=doubt-1',fail_reader_helper)
    p.goto(base+'four-truths/book/?collection=1&collectionReturn=game&collectionPage=27');p.wait_for_selector('body[data-collection-index="27"]');q.click_next(p,28)
    assert q.snapshot(p)['completed']==[];p.locator('#next').click();d.map_ready(p);p.wait_for_selector('#wm-dialog[open]')
    assert aborted and q.snapshot(p)['completed']==['four-truths'] and not p.locator('.story-dialogue').is_visible()
    report['pendingAndOptionalReceiptFailure']={'pendingFixtures':cases,'injectedReaderOnlyReceiptModuleAbort':len(aborted),'fixtureStartedAtIndex':27,'actualNativeNextTo28AndExplicitFinishStillWorks':True,'normalExistingCompletionRewardWithoutNewStory':True};ctx.close()


def five_size_actor_director(browser,base,report):
    cases=[]
    for width,height in SIZES:
        viewport={'width':width,'height':height};ctx=context(browser,base,viewport=viewport);p=ctx.new_page();q.observe(p,base,report);fresh_map(p,base);assert_scene(p,'arrival-at-wheel');p.locator('.story-dialogue__next').click();assert_scene(p,'doubt-at-ruins')
        waiting=stage_visible_below_dialogue(p);p.screenshot(path=str(OUT/f'doubt-before-reading-{width}x{height}.png'));p.locator('.story-dialogue__skip').click();assert d.camera(p)['safeInsets']['top']==0;ctx.close()
        saved=q.fixture(['four-truths'],{'four-truths':28},'five-aggregates');ctx=context(browser,base,saved,list(LINES)[:3],viewport=viewport)
        ctx.add_init_script("sessionStorage.setItem('"+RECEIPT+"',JSON.stringify({version:1,event:'four-truths-reader-finished'}))")
        p=ctx.new_page();q.observe(p,base,report);fresh_map(p,base);assert_scene(p,'first-book-insight');p.wait_for_timeout(1000);assert visible_marks(p,'[data-doubt-stage] [data-doubt-mark]')==2
        thinning=stage_visible_below_dialogue(p);p.screenshot(path=str(OUT/f'post-director-isolated-fixture-{width}x{height}.png'));p.locator('.story-dialogue__skip').click();assert d.camera(p)['safeInsets']['top']==0
        cases.append({'viewport':[width,height],'freshBeforeReading':waiting,'isolatedPostCompletionFixture':thinning,'fullCreatureAndAllVisibleMarksBetweenDialogueAndDock':True,'temporaryTopInsetClearedOnClose':True});ctx.close()
    report['fiveSizeWorldActorVisibility']=cases


def fresh_map(page,base):
    page.goto(base+'game/#map');d.map_ready(page)


def save_report(report):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')


def main():
    OUT.mkdir(parents=True,exist_ok=True);report=guard_sources();report.update({'phase':'Local independent validation','javascriptErrors':[],'httpErrors':[],'physicalSafari':'Not tested; Chromium desktop viewport/touch emulation','fixtureNotice':'Historical profiles are isolated fixtures, separate from the actual sequential first-book walk.'})
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(q.Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);viewport_theme_checks(browser,base,report);actual_first_completion(browser,base,report);history_and_guard_checks(browser,base,report);reset_new_scenes(browser,base,report);actor_asset_failure(browser,base,report);pending_and_optional_receipt_failure(browser,base,report);five_size_actor_director(browser,base,report);browser.close()
        assert not report['javascriptErrors'],report['javascriptErrors'];assert not report['httpErrors'],report['httpErrors'];report['result']='passed'
    except Exception as error:report['result']='failed';report['error']=repr(error);raise
    finally:server.shutdown();save_report(report)
    print(json.dumps({'result':report['result'],'report':str(OUT/'validation.json')},ensure_ascii=False))


if __name__=='__main__':main()
