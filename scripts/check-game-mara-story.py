#!/usr/bin/env python3
"""Focused Mara presentation, actual first29, recovery and scope regressions.

Evidence is written only to this round's new preview directory. Synthetic
history/pending cases are labelled separately from the native reading walk.
"""
from pathlib import Path
import functools,hashlib,http.server,importlib.util,json,re,subprocess,threading
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/previews/game-mara-story'
s=importlib.util.spec_from_file_location('cyan_qa',ROOT/'scripts/check-game-cyan-aggregates.py');cyan=importlib.util.module_from_spec(s);s.loader.exec_module(cyan)
story=cyan.old;q=cyan.q;d=cyan.d;BASELINE='71de5285bef079f515abcc44577eb50a4aa8cea3';q.BASE=BASELINE
SIZES=q.SIZES;STORY_KEY=story.STORY_KEY;MARA_SCENE='mara-watches'
MARA_TEXT='站在遠方觀看的波旬心想：「可惡，小貓好像慢慢開始破除五蓋了……」'


def context(browser,base,saved=None,seen=None,**options):
    return story.context(browser,base,saved,seen,**options)


def guard_sources():
    originals=q.ORDER+['docs/'+book for book in q.ORDER]+['index.html','shelf.css','sitemap.xml','robots.txt','googlee0c995331ec518ae.html','reader-controls.css','reader-layout.js','reader-restart.js','picture-panel-focus.js','picture-panel-focus.css','docs/seo','map-topic-resources.css','scripts/site_seo.py','scripts/build-seo.py','scripts/check-seo.py']
    html=[book+'/book/index.html' for book in q.ORDER];changed=subprocess.check_output(['git','diff','--name-only',BASELINE,'--',*originals],cwd=ROOT,text=True).splitlines();assert set(changed)<=set(html),changed
    baseline=lambda path:subprocess.check_output(['git','show',BASELINE+':'+path],cwd=ROOT,text=True)
    for path in html:
        before=baseline(path);after=(ROOT/path).read_text();tag=re.search(r'\.\./\.\./play/collection/reader-bridge\.js\?v=[^"\s]+',before).group()
        assert after.count('../../play/collection/reader-bridge.js?v=mara-1')==1,path
        assert after.replace('../../play/collection/reader-bridge.js?v=mara-1',tag)==before,path
    count=len([p for p in subprocess.check_output(['git','ls-tree','-rz','--name-only',BASELINE,'--',*originals],cwd=ROOT,text=True).split('\0') if p])
    report={'baseline':BASELINE,'protectedOriginalFiles':count,'fourteenReaderHtmlException':'Only bridge cache query; normalize each to its own baseline then full text identical','originalTextScripturePicturesReaderJsCssHomepageSeoGoogle':'byte-for-byte unchanged'}
    paths=['play/collection/store.js','play/collection/reader.css','play/reader-bridge.js','play/route','play/prologue','play/story/completion-receipt.js','play/game-theme.css','play/worldmap-v4/camera.js','play/worldmap-v4/data.js','play/visual-v2/network-data.js','play/visual-v2/assets','play/worldmap-v4/assets','play/assets']
    paths += [p for p in subprocess.check_output(['git','ls-tree','-rz','--name-only',BASELINE,'--','play/story/assets'],cwd=ROOT,text=True).split('\0') if p]
    changed=subprocess.check_output(['git','diff','--name-only',BASELINE,'--',*paths],cwd=ROOT,text=True).splitlines();assert not changed,changed
    report['additionalUnchangedCoreAndExistingArt']=paths
    bridge=(ROOT/'play/collection/reader-bridge.js').read_text().replace("new URL('../../game/?v=mara-1', import.meta.url)","new URL('../../game/?v=cyan-1', import.meta.url)");assert bridge==baseline('play/collection/reader-bridge.js')
    store=(ROOT/'play/story/store.js').read_text().replace("./data.js?v=mara-1","./data.js?v=cyan-aggregates-1");assert store==baseline('play/story/store.js')
    reset=(ROOT/'play/title-review.js').read_text().replace("./story/store.js?v=mara-1","./story/store.js?v=cyan-aggregates-1");assert reset==baseline('play/title-review.js')
    report['authorizedCoreQueryExceptions']='Exact bridge return, story store import and reset import versions; all other bytes identical'
    return report


def mara_snapshot(page):
    panel=page.locator(f'.story-dialogue[data-scene="{MARA_SCENE}"]:not([hidden])');panel.wait_for()
    result=story.scene_snapshot(page);assert result['text']==MARA_TEXT and result['speaker']=='波旬' and result['actor']=='mara',result
    story.dialogue_geometry(page);result['portrait']=story.portrait_unclipped(page)
    assert story.visible_marks(page,'.story-dialogue [data-doubt-portrait-mark]')==0
    q.settle(page);assert page.locator('.story-dialogue__next').evaluate('(n)=>document.activeElement===n')
    return result


def seen(page):
    return page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).seenSceneIds',STORY_KEY)


def actual_first_mara_five(browser,base,report):
    ctx=context(browser,base,viewport={'width':844,'height':390},reduced_motion='no-preference');page=ctx.new_page();q.observe(page,base,report);page.goto(base+'game/?v=mara-1#map');d.map_ready(page)
    for scene_id in list(story.LINES)[:3]:story.assert_scene(page,scene_id);page.locator('.story-dialogue__next').click()
    page.wait_for_selector('body[data-collection-index="0"]');trace=[0]
    for index in range(1,29):q.click_next(page,index);trace.append(index)
    assert q.snapshot(page)['completed']==[];page.locator('#next').click();d.map_ready(page)
    story.assert_scene(page,'first-book-insight');page.wait_for_timeout(1000);page.locator('.story-dialogue__next').click();story.assert_scene(page,'doubt-recedes');page.wait_for_timeout(1500);page.locator('.story-dialogue__next').click()
    mara=mara_snapshot(page);assert q.snapshot(page)['completed']==['four-truths'] and 'doubt-recedes' not in seen(page) and MARA_SCENE in seen(page)
    page.screenshot(path=str(OUT/'actual-first29-mara-before-reload-844x390.png'));state=q.snapshot(page);page.reload();d.map_ready(page);mara_snapshot(page);assert q.snapshot(page)==state
    page.screenshot(path=str(OUT/'actual-first29-mara-restored-844x390.png'));page.locator('.story-dialogue__next').click();page.wait_for_selector('#wm-dialog[open]');assert '法輪碼頭' in page.locator('#wm-dialog').inner_text() and 'doubt-recedes' in seen(page)
    page.screenshot(path=str(OUT/'actual-first29-original-reward-844x390.png'));page.locator('[data-wm-next-station]').click();five=cyan.new_scene_snapshot(page)
    assert q.snapshot(page)['completed']==['four-truths'] and 'five-aggregates' not in q.snapshot(page)['positions']
    page.locator('.story-dialogue__next').click();page.wait_for_selector('body[data-collection-book="five-aggregates"][data-collection-index="0"]')
    for index in [1,2,3]:q.click_next(page,index)
    page.reload();page.wait_for_selector('body[data-collection-index="3"]');page.set_viewport_size({'width':360,'height':800});page.locator('.collection-reader-return').click();d.map_ready(page)
    assert not page.locator('.story-dialogue').is_visible() and q.snapshot(page)['completed']==['four-truths'] and '4／54' in page.locator('[data-wm-next]').inner_text()
    page.screenshot(path=str(OUT/'actual-five-resume-360x800.png'))
    report['actualFirstMaraFive']={'nativeFirstNextTrace':trace,'noCompletionBeforeExplicitFinish':True,'postOrder':['first-book-insight','doubt-recedes',MARA_SCENE,'original-reward',cyan.FIVE_SCENE],'mara':mara,'actualMaraReloadRestoresSameSceneWithoutProgressWrite':True,'maraSeenButRetreatCutoffPendingUntilAction':True,'originalRewardPreserved':True,'fiveScene':five,'nativeFiveNextTrace':[0,1,2,3],'reloadRotationReturnResumesIndex':3,'completionStillFirstOnly':True};ctx.close()


def five_size_mara_and_skip(browser,base,report):
    cases=[]
    for width,height in SIZES:
        state=q.fixture(['four-truths'],{'four-truths':28},'five-aggregates');ctx=context(browser,base,state,list(story.LINES)[:4]+[MARA_SCENE],viewport={'width':width,'height':height});page=ctx.new_page();q.observe(page,base,report);page.goto(base+'game/?v=mara-1#map');d.map_ready(page)
        scene=mara_snapshot(page);color=cyan.colors(page,'.story-dialogue__next');page.screenshot(path=str(OUT/f'mara-pending-isolated-{width}x{height}.png'));assert q.snapshot(page)==state
        page.locator('.story-dialogue__skip').click();page.wait_for_selector('#wm-dialog[open]');assert 'doubt-recedes' in seen(page);page.reload();d.map_ready(page)
        assert not page.locator('.story-dialogue').is_visible() and not page.locator('#wm-dialog').is_visible() and q.snapshot(page)==state
        cases.append({'viewport':[width,height],'fixture':'pending Mara, separate from native first29','scene':scene,'cyanCta':color,'fullPortraitAndButtonsAboveDock':True,'skipAcknowledgesCutoffAndReloadDoesNotRepeat':True,'collectionUnchanged':True});ctx.close()
    report['fiveSizePendingMaraAndSkip']=cases


def history_replay_reset_and_failure(browser,base,report):
    state=q.fixture(['four-truths'],{'four-truths':28},'five-aggregates');old_seen=list(story.LINES)+[cyan.FIVE_SCENE]
    ctx=context(browser,base,state,old_seen);page=ctx.new_page();q.observe(page,base,report);page.goto(base+'game/?v=mara-1&completed=four-truths#map');d.map_ready(page)
    assert not page.locator('.story-dialogue').is_visible() and seen(page)==old_seen and q.snapshot(page)==state
    if page.locator('#wm-dialog').is_visible():page.locator('[data-wm-close]').click()
    before=page.evaluate('(keys)=>keys.map(k=>localStorage.getItem(k))',[q.KEY,STORY_KEY]);page.locator('[data-wm-tools-open]').focus();page.locator('[data-wm-tools-open]').click();page.locator('[data-wm-completion-replay]').click()
    for scene_id in ['first-book-insight','doubt-recedes']:story.assert_scene(page,scene_id);page.locator('.story-dialogue__next').click()
    mara_snapshot(page);page.locator('.story-dialogue__next').click();assert before==page.evaluate('(keys)=>keys.map(k=>localStorage.getItem(k))',[q.KEY,STORY_KEY]) and not page.locator('#wm-dialog').is_visible() and '/book/' not in page.url
    report['historyAndReplay']={'isolatedPreMaraHistoricalSceneRecord':old_seen,'oldRetreatCutoffPreventsForcedNewSceneEvenCompletedQuery':True,'explicitReplayIncludesMaraReadonly':True,'collectionAndSeenBytesUnchanged':True,'noRewardOrBookEntry':True};ctx.close()
    local,session=story.prior.seeded_profile();local[STORY_KEY]=json.dumps({'version':1,'seenSceneIds':list(story.LINES)[:4]+[MARA_SCENE,cyan.FIVE_SCENE]})
    ctx=story.prior.context(browser,base,local,session);page=ctx.new_page();q.observe(page,base,report);page.goto(base+'game/?author=1&v=mara-1');story.prior.assert_copy(page);story.prior.skip(page);before=story.storage(page)
    page.once('dialog',lambda dialog:dialog.dismiss());page.locator('[data-title-author-reset]').click();assert story.storage(page)==before
    page.once('dialog',lambda dialog:dialog.accept());page.locator('[data-title-author-reset]').click();story.prior.assert_copy(page);story.prior.skip(page);after=story.storage(page)
    assert STORY_KEY not in after['local'] and q.KEY not in after['local']
    for key in ['sutrazen.play.v1','sutrazen.reader.position','auth.roles','site.preference']:assert after['local'][key]==before['local'][key]
    page.locator('[data-title-start]').click();d.map_ready(page);story.assert_scene(page,'arrival-at-wheel');assert q.snapshot(page) is None
    report['authorReset']={'isolatedPendingMaraProfile':True,'nativeCancelByteIdentical':True,'confirmedClearsMaraSeenAndPendingCutoffSameV1Key':True,'otherSiteKeysPreserved':True,'freshFirstArrivalRestored':True};ctx.close()
    ctx=context(browser,base,state,list(story.LINES)[:4]+[MARA_SCENE]);page=ctx.new_page();q.observe(page,base,report);aborted=[]
    def abort(route):aborted.append(route.request.url);route.abort()
    page.route('**/play/story/assets/mara-portrait-concept.png',abort);page.goto(base+'game/?v=mara-1#map');d.map_ready(page);page.wait_for_selector('.story-dialogue--no-art[data-scene="mara-watches"]:not([hidden])')
    assert story.scene_snapshot(page)['text']==MARA_TEXT;story.dialogue_geometry(page);page.locator('.story-dialogue__next').click();page.wait_for_selector('#wm-dialog[open]');page.locator('[data-wm-next-station]').click();cyan.new_scene_snapshot(page);page.locator('.story-dialogue__next').click();page.wait_for_selector('body[data-collection-book="five-aggregates"][data-collection-index="0"]');q.click_next(page,1)
    assert q.snapshot(page)['completed']==['four-truths'] and aborted
    report['missingMaraArt']={'expectedInjectedAborts':len(aborted),'fullTextAndButtonsRemainUsable':True,'normalRewardThenFiveOriginalReaderAndNativeNext':True,'noExtraCompletion':True};ctx.close()


def asset_metadata(report):
    path=ROOT/'play/story/assets/mara-portrait-concept.png';image=Image.open(path);assert image.mode=='RGBA',image.mode
    alpha=image.getchannel('A');bounds=alpha.point(lambda v:255 if v>=32 else 0).getbbox();assert alpha.getextrema()==(0,255) and bounds and bounds[0]>0 and bounds[1]>0 and bounds[2]<image.width and bounds[3]<image.height,bounds
    report['maraAsset']={'path':str(path.relative_to(ROOT)),'nativeSize':list(image.size),'mode':image.mode,'alphaExtrema':list(alpha.getextrema()),'alpha32VisibleBounds':list(bounds),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'fullSilhouetteNotTouchingCanvasEdges':True,'orientation':'Right-facing appearance inspected separately in actual source and browser screenshots'}


def save(report):
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')


def main():
    OUT.mkdir(parents=True,exist_ok=True);report=guard_sources();report.update({'phase':'Local focused Mara validation','javascriptErrors':[],'httpErrors':[],'physicalSafari':'Not tested; Chromium desktop viewport/input emulation','fixtureNotice':'Five-size pending/history/reset/failure profiles are isolated fixtures; only actualFirstMaraFive contains the native full29 walk.'});asset_metadata(report)
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(q.Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);actual_first_mara_five(browser,base,report);print('actualfirst29 Mara reload andfive passed',flush=True);five_size_mara_and_skip(browser,base,report);history_replay_reset_and_failure(browser,base,report);browser.close()
        assert not report['javascriptErrors'],report['javascriptErrors'];assert not report['httpErrors'],report['httpErrors'];report['result']='passed'
    except Exception as error:report['result']='failed';report['error']=repr(error);raise
    finally:server.shutdown();save(report)
    print(json.dumps({'result':report['result'],'report':str(OUT/'validation.json')},ensure_ascii=False))


if __name__=='__main__':main()
