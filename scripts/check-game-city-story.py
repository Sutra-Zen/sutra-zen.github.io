#!/usr/bin/env python3
"""Independent one-time story, actual city rewards and reading-policy checks."""
from pathlib import Path
import functools,hashlib,http.server,importlib.util,json,subprocess,threading
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/previews/game-city-story'
s=importlib.util.spec_from_file_location('frame_qa',ROOT/'scripts/check-game-original-frame.py');f=importlib.util.module_from_spec(s);s.loader.exec_module(f)
d=f.d;d.q.BASE='be78106f6414ebf447eaedadd5c94883359be58e';SIZES=d.SIZES
LINE='咦？我剛才明明還趴在窗邊等朋友回訊息……怎麼一抬頭，就到了法輪遺跡？進去看看！'
STORY_KEY='sutrazen.play.story.v1'


def assert_intro(page):
    page.wait_for_selector('.story-dialogue:not([hidden])')
    assert page.locator('.story-dialogue__line').text_content()==LINE
    assert 'story-line' in (page.locator('.story-dialogue__next').get_attribute('aria-describedby') or '').split()
    page.locator('.story-dialogue img').evaluate('(i)=>i.decode()')
    assert page.locator('.story-dialogue__line').evaluate('''n=>{let s=getSelection();s.selectAllChildren(n);let same=s.toString()===n.textContent;s.removeAllRanges();return same}''')
    box=page.locator('.story-dialogue').bounding_box();dock=page.locator('.game-dock').bounding_box()
    assert box['x']>=0 and box['y']>=0 and box['x']+box['width']<=page.viewport_size['width']+1 and box['y']+box['height']<dock['y'],(box,dock)
    for selector in ['.story-dialogue__skip','.story-dialogue__next']:
        b=page.locator(selector).bounding_box();assert b['height']>=48 and b['width']>=48,b
    seen=page.evaluate('(key)=>JSON.parse(localStorage.getItem(key))',STORY_KEY)
    assert seen['seenSceneIds']==['arrival-at-wheel'],seen
    assert page.locator('[data-wm-city-entry]').count()==0
    assert page.locator('[data-game-nav="city"]').is_visible()
    return box


def intro_checks(browser,base,report):
    cases=[]
    for width,height in SIZES:
        c=d.q.context_for(browser,base,has_touch=True,viewport={'width':width,'height':height});p=c.new_page();d.q.observe(p,base,report)
        p.goto(base+'game/');p.wait_for_selector('#game-title-screen.is-art-loaded');p.locator('[data-title-start]').click();d.map_ready(p)
        box=assert_intro(p);p.screenshot(path=str(OUT/f'map-intro-{width}x{height}.png'))
        assert d.q.snapshot(p) is None
        p.locator('.story-dialogue__skip').click();assert p.locator('[data-wm-next]').evaluate('(n)=>n===document.activeElement');p.reload();d.map_ready(p)
        assert not p.locator('.story-dialogue').is_visible()
        p.locator('[data-wm-tools-open]').focus();p.locator('[data-wm-tools-open]').click();p.wait_for_selector('#wm-tools-dialog[open]');p.locator('[data-wm-story-replay]').click();assert_intro(p)
        assert p.locator('.story-dialogue__next').evaluate('(n)=>n===document.activeElement')
        assert p.locator('.story-dialogue__next').inner_text()=='回到海圖'
        p.locator('.story-dialogue__next').click();d.q.settle(p)
        assert '/book/' not in p.url and not p.locator('.story-dialogue').is_visible() and d.q.snapshot(p) is None
        cases.append({'viewport':[width,height],'exactHtmlNarration':True,'onceMarkedOnShow':True,'topOverlay':box,'skipReloadNoRepeat':True,'replayNoBookOrProgressMutation':True})
        c.close()
    report['introChecks']=cases
    # The fresh authored action uses the existing first-book guard, then returns without replay.
    c=d.q.context_for(browser,base);p=c.new_page();d.q.observe(p,base,report);p.goto(base+'game/#map');d.map_ready(p);assert_intro(p)
    p.locator('.story-dialogue__next').click();p.wait_for_selector('body[data-collection-book="four-truths"]')
    for at in [1,2]:d.q.click_next(p,at)
    p.reload();p.wait_for_selector('body[data-collection-index="2"]');p.locator('.collection-reader-return').click();d.map_ready(p)
    assert not p.locator('.story-dialogue').is_visible()
    assert d.q.snapshot(p)['completed']==[] and '3／29' in p.locator('[data-wm-next]').inner_text()
    report['introReaderAction']={'actualCtaEnteredFirstBook':True,'actualNextClicks':2,'reloadResumeAtIndex':2,'readerReturnNoRepeat':True,'completionZero':True}
    c.close()
    # Returning players must not receive the arrival scene because an arbitrary future bookmark exists.
    saved=d.q.fixture([d.q.ORDER[0]],{d.q.ORDER[1]:3,d.q.ORDER[10]:5},d.q.ORDER[10])
    c=d.q.context_for(browser,base,saved);p=c.new_page();d.q.observe(p,base,report);p.goto(base+'game/#map');d.map_ready(p)
    assert not p.locator('.story-dialogue').is_visible() and d.q.snapshot(p)==saved
    report['returningProfileIntroSuppressed']=True;c.close()


def portrait_metadata(report):
    path=ROOT/'play/story/assets/kitten-traveler-portrait-concept.png';im=Image.open(path)
    assert im.size==(1254,1254) and im.mode=='RGBA' and im.getchannel('A').getextrema()==(0,255)
    report['portrait']={'path':str(path.relative_to(ROOT)),'dimensions':list(im.size),'mode':im.mode,'actualAlphaExtrema':list(im.getchannel('A').getextrema()),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'status':'New generated concept portrait; original book artwork unchanged'}


def story_storage_fallback(browser,base,report):
    c=d.q.context_for(browser,base);c.add_init_script('Object.defineProperty(window,"localStorage",{get(){throw new DOMException("QA storage blocked","SecurityError")}})')
    p=c.new_page();d.q.observe(p,base,report);p.goto(base+'game/#map');d.map_ready(p);p.wait_for_selector('.story-dialogue:not([hidden])')
    assert p.locator('.story-dialogue__line').text_content()==LINE and p.locator('.story-dialogue__notice').is_visible()
    p.locator('.story-dialogue__next').click();p.wait_for_selector('body[data-collection-book="four-truths"]')
    if p.locator('.collection-reader-storage[open]').count():p.locator('.collection-reader-storage button').click()
    d.q.click_next(p,1);p.locator('.collection-reader-return').click();d.map_ready(p)
    assert not p.locator('.story-dialogue').is_visible()
    report['storyStorageFallback']={'blockedLocalStorageWarningShown':True,'actualFirstBookNextStillWorks':True,'sameTabReturnDoesNotRepeat':True,'noPermanentSaveClaim':True};c.close()


def story_store_model(report):
    script='''import assert from 'node:assert/strict';
import {createStoryStore,STORY_STORAGE_KEY} from './play/story/store.js';
class Memory{constructor(){this.values=new Map()}getItem(k){return this.values.get(k)??null}setItem(k,v){this.values.set(k,String(v))}removeItem(k){this.values.delete(k)}}
const local=new Memory(),session=new Memory();local.setItem('sutrazen.play.collection.v1','{"preserve":"reading record"}');
const store=createStoryStore(local,session);assert.equal(store.markSeen('arrival-at-wheel'),true);assert.equal(store.markSeen('arrival-at-wheel'),true);assert.deepEqual(store.get().seenSceneIds,['arrival-at-wheel']);assert.equal(store.markSeen('unknown-scene'),false);assert.equal(createStoryStore(local,session).hasSeen('arrival-at-wheel'),true);assert.equal(local.getItem('sutrazen.play.collection.v1'),'{"preserve":"reading record"}');
const corrupt=new Memory();corrupt.setItem(STORY_STORAGE_KEY,'{');assert.equal(createStoryStore(corrupt,new Memory()).issue,'corrupt');
const disabledSession=new Memory(),disabled=createStoryStore(null,disabledSession);disabled.markSeen('arrival-at-wheel');assert.equal(createStoryStore(null,disabledSession).hasSeen('arrival-at-wheel'),true);
const quota=new Memory(),quotaSession=new Memory();quota.setItem=()=>{throw Error('quota')};const quotaStore=createStoryStore(quota,quotaSession);quotaStore.markSeen('arrival-at-wheel');assert.equal(createStoryStore(quota,quotaSession).hasSeen('arrival-at-wheel'),true);quota.values.set(STORY_STORAGE_KEY,JSON.stringify({version:1,seenSceneIds:[]}));assert.equal(createStoryStore(quota,quotaSession).hasSeen('arrival-at-wheel'),false);
console.log(JSON.stringify({dedupSeen:true,unknownSceneRejected:true,unrelatedReadingKeyUnchanged:true,reloadEquivalent:true,corruptStoryIsolated:true,disabledLocalSessionFallback:true,getWorksSetThrowsRecovery:true,changedCanonicalRawInvalidatesRecovery:true}));'''
    run=subprocess.run(['node','--input-type=module','-'],input=script,cwd=ROOT,text=True,capture_output=True,check=True)
    report['storyStoreModel']=json.loads(run.stdout)


def cross_page_once(browser,base,report):
    c=d.q.context_for(browser,base);p=c.new_page();d.q.observe(p,base,report);p.goto(base+'game/');p.wait_for_selector('#game-title-screen.is-art-loaded');p.locator('[data-title-start]').click();d.map_ready(p);assert_intro(p)
    # Leave while the dialogue is still open: displayed, not dismissed, is once.
    p.locator('[data-game-nav="city"]').click();p.wait_for_selector('.city-tactics-board');p.locator('[data-game-nav="map"]').click();d.map_ready(p);assert not p.locator('.story-dialogue').is_visible()
    p.locator('[data-game-nav="shelf"]').click();p.wait_for_selector('#collection-books');p.locator('[data-game-nav="map"]').click();d.map_ready(p);assert not p.locator('.story-dialogue').is_visible()
    assert d.q.snapshot(p) is None
    state=c.storage_state();c.close()
    c=d.q.context_for(browser,base,storage_state=state);p=c.new_page();d.q.observe(p,base,report);p.goto(base+'game/');p.wait_for_selector('#game-title-screen.is-art-loaded');p.locator('[data-title-start]').click();d.map_ready(p);assert not p.locator('.story-dialogue').is_visible();assert d.q.snapshot(p) is None
    report['crossPageOnce']={'cityReturnWhileIntroWasOpenNoRepeat':True,'shelfReturnNoRepeat':True,'newBrowserContextWithSeenSaveNoRepeat':True,'noReadingProgressFabricated':True};c.close()


def fresh_intro_completion(browser,base,report):
    c=d.q.context_for(browser,base);p=c.new_page();d.q.observe(p,base,report);p.goto(base+'game/');p.wait_for_selector('#game-title-screen.is-art-loaded');p.locator('[data-title-start]').click();d.map_ready(p);assert_intro(p);p.locator('.story-dialogue__next').click();p.wait_for_selector('body[data-collection-book="four-truths"]')
    total=int(p.locator('body').get_attribute('data-collection-total'));assert total==29
    trace=[0]
    for at in range(1,total):d.q.click_next(p,at);trace.append(at)
    assert d.q.snapshot(p)['completed']==[] and p.locator('#next').inner_text()=='完成這本'
    p.locator('#next').click();d.map_ready(p);p.wait_for_selector('#wm-dialog[open]')
    assert d.q.snapshot(p)['completed']==['four-truths'] and not p.locator('.story-dialogue').is_visible()
    assert '法輪碼頭' in p.locator('#wm-dialog').inner_text()
    p.screenshot(path=str(OUT/'intro-first-book-completion-1280x900.png'))
    p.locator('[data-wm-next-station]').click();d.q.settle(p)
    assert '/book/' not in p.url and p.locator('.wm-landmark.is-next').get_attribute('data-book')=='five-aggregates'
    p.locator('[data-game-nav="shelf"]').click();p.wait_for_selector('[data-collection-read="four-truths"]');assert p.locator('[data-collection-read]').count()==1;p.locator('[data-collection-read="four-truths"]').click();p.wait_for_selector('body[data-collection-index="0"]')
    for at in range(1,total):d.q.click_next(p,at)
    p.locator('#next').click();p.wait_for_selector('#collection-books')
    assert 'shelf' in p.url and 'completed=' not in p.url and d.q.snapshot(p)['completed']==['four-truths']
    p.locator('[data-game-nav="map"]').click();d.map_ready(p)
    assert not p.locator('#wm-dialog').is_visible() and not p.locator('.story-dialogue').is_visible()
    assert p.locator('.wm-landmark.is-next').get_attribute('data-book')=='five-aggregates'
    report['freshIntroFullBook']={'actualSequentialReadingTrace':trace,'completionOnlyAfterExplicitButton':True,'firstRewardDockVisible':True,'nextStationFocusFiveAggregatesWithoutAutostart':True,'actualFullReviewSteps':29,'reviewNoRewardRepeatOrExtraCompletion':True,'introNeverRepeated':True};c.close()


def portrait_failure_recovery(browser,base,report):
    c=d.q.context_for(browser,base);p=c.new_page();d.q.observe(p,base,report);aborted=[]
    def fail(route):aborted.append(route.request.url);route.abort()
    p.route('**/play/story/assets/kitten-traveler-portrait-concept.png',fail);p.goto(base+'game/#map');d.map_ready(p);p.wait_for_selector('.story-dialogue--no-art:not([hidden])')
    assert p.locator('.story-dialogue__line').text_content()==LINE and p.locator('.story-dialogue__next').is_visible()
    p.locator('.story-dialogue__skip').click();p.unroute('**/play/story/assets/kitten-traveler-portrait-concept.png',fail)
    p.locator('[data-wm-tools-open]').focus();p.locator('[data-wm-tools-open]').click();p.locator('[data-wm-story-replay]').click();p.locator('.story-dialogue img').evaluate('(i)=>i.decode()');d.q.settle(p)
    assert not p.locator('.story-dialogue').evaluate('(n)=>n.classList.contains("story-dialogue--no-art")')
    assert len(aborted)==1
    report['portraitFailureRecovery']={'expectedInjectedAbort':1,'fullTextAndActionsAvailable':True,'replayRecoveredPortraitLayout':True};c.close()


def city_loaded(page):
    page.wait_for_selector('.city-tactics-board')
    page.evaluate('''async()=>{const urls=[...new Set([...document.querySelectorAll('.city-tactics-board img,.city-tactics-board image')].map(n=>n instanceof HTMLImageElement?n.currentSrc||n.src:n.href.baseVal))];await Promise.all(urls.filter(Boolean).map(async url=>{const i=new Image();i.src=url;await i.decode()}))}''')
    d.q.settle(page)
    result=page.evaluate('''()=>({painted:[...document.querySelectorAll('.tactics-painted-layer,.tactics-art,.city-tactics-board')].map(n=>({class:n.className,filter:getComputedStyle(n).filter,opacity:getComputedStyle(n).opacity})),screen:[innerWidth,innerHeight],overflow:[document.documentElement.scrollWidth,document.documentElement.scrollHeight]})''')
    assert all(x['filter']=='none' and x['opacity']=='1' for x in result['painted']),result
    assert all(a<=b+1 for a,b in zip(result['overflow'],result['screen'])),result
    assert page.locator('.tactics-feature-cloud img').count()==0
    assert '[object Object]' not in page.locator('body').inner_text() and 'undefined' not in page.locator('body').inner_text()
    return result


def open_reward(page,reward):
    if not page.locator('#city-dialog').is_visible():page.locator('#city-meaning-index').click()
    page.wait_for_selector('#city-dialog[open]')
    page.locator(f'[data-city-reward-detail="{reward}"]').click()
    d.q.settle(page)
    assert page.locator('#city-dialog').evaluate('(n)=>n.scrollTop')==0
    close=page.locator('[data-city-close]').bounding_box();assert close and close['y']>=0
    return page.locator('#city-dialog')


def city_reward_checks(browser,base,report):
    cases=[]
    for width,height in SIZES:
        for completed in [0,13]:
            saved=d.q.fixture(d.q.ORDER[:completed]);c=d.q.context_for(browser,base,saved,viewport={'width':width,'height':height});p=c.new_page();d.q.observe(p,base,report);p.goto(base+'play/city/');visual=city_loaded(p)
            assert d.q.snapshot(p)==saved
            if completed==0:
                assert p.locator('.tactics-feature-cloud').count()>0
                assert p.locator('[data-companion]').count()==0 and p.locator('.city-faculties-network').count()==0
                p.screenshot(path=str(OUT/f'city-0-{width}x{height}.png'))
                dialog=open_reward(p,'conditions_wheel');assert dialog.locator('[data-city-source-kind]').get_attribute('data-city-source-kind')=='extended';assert dialog.locator('[data-city-reread]').count()==0 and dialog.locator('.city-source-link').count()==0
                p.locator('[data-city-close]').click();p.locator('[data-city-label="guardian"]').click();assert p.locator('#city-dialog [data-city-source-kind]').get_attribute('data-city-source-kind')=='canonical';assert p.locator('#city-dialog [data-city-reread]').count()==0;p.locator('[data-city-close]').click()
            else:
                assert p.locator('.tactics-feature-cloud').count()==0
                assert p.locator('[data-companion]').count()==7
                assert all(n.is_visible() for n in p.locator('[data-companion] svg').all()) and p.locator('[data-companion="mindfulness"]').is_visible()
                assert p.locator('[data-companion="mindfulness"] svg').count()==0 and p.locator('[data-companion="mindfulness"]').get_attribute('data-uses-existing-guardian')=='true'
                art=p.locator('[data-companion] svg image').evaluate_all('(nodes)=>nodes.map(n=>n.href.baseVal)');assert len(art)==6 and all('/seven-factors/assets/12.webp' in url for url in art),art
                assert p.locator('[data-faculty-zone]').count()==5 and p.locator('[data-faculty-link]').count()==5
                rewards=p.locator('[data-city-reward]').evaluate_all('(nodes)=>nodes.map(n=>n.dataset.cityReward)')
                assert set(['conditions_wheel','noble_path','confidence_harbor','effort_garden','calm_insight_messengers','endeavor_boat','jhana_garden','faculties_links','awakening_companions']).issubset(rewards),rewards
                assert 'fruition_guide' not in rewards
                p.screenshot(path=str(OUT/f'city-13-history-fixture-{width}x{height}.png'))
                dialog=open_reward(p,'awakening_companions');assert dialog.locator('[data-city-source-kind]').get_attribute('data-city-source-kind')=='extended';assert '繪本場景延伸' in dialog.inner_text() and '已安置' in dialog.locator('.status-label').inner_text();assert '/seven-factors/#sources' in dialog.locator('.city-source-link').get_attribute('href');assert dialog.locator('[data-city-reread="seven-factors"]').count()==1
                p.screenshot(path=str(OUT/f'companions-source-history-fixture-{width}x{height}.png'))
                p.locator('[data-city-close]').click();p.locator('#city-meaning-index').click();assert p.locator('[data-city-meaning="dock"]').count()==0;assert p.locator('[data-city-reward-detail="fruition_guide"]').count()==1;p.locator('[data-city-close]').click()
                dialog=open_reward(p,'noble_path');assert dialog.locator('[data-city-source-kind]').get_attribute('data-city-source-kind')=='mixed';assert '繪本延伸' in dialog.locator('[data-city-source-kind]').inner_text();p.locator('[data-city-close]').click()
            assert d.q.snapshot(p)==saved
            cases.append({'viewport':[width,height],'historicalCompletedCount':completed,'fullColorAndNoOuterOverflow':visual,'localFogOnly':True,'completedIdsUnchanged':True,'sevenCompanions':completed==13,'canonicalVersusCreativeSourceLabels':True});c.close()
    report['cityVisualAndRewards']=cases


def historical_reward_edges(browser,base,report):
    fixtures=[('before-seven',d.q.ORDER[:12],0,False),('only-seven',['seven-factors'],0,True),('body-and-seven',['five-aggregates','seven-factors'],7,False),('roots-and-body',['five-aggregates','five-roots-powers'],0,False),('roots-faith-source',['five-aggregates','five-roots-powers','four-purities-six-recollections'],0,False),('all-fourteen',d.q.ORDER,7,False)]
    cases=[]
    for label,done,companions,pending in fixtures:
        saved=d.q.fixture(done);c=d.q.context_for(browser,base,saved);p=c.new_page();d.q.observe(p,base,report);p.goto(base+'play/city/');city_loaded(p)
        assert p.locator('[data-companion]').count()==companions,(label,companions)
        if pending:
            assert p.locator('#city-pending-rewards').is_visible();p.locator('#city-pending-rewards').click();p.locator('[data-city-reward-detail="awakening_companions"]').click();assert p.locator('#city-dialog [data-city-source-kind]').get_attribute('data-city-source-kind')=='extended';assert '預覽' in p.locator('#city-dialog .status-label').inner_text();assert p.locator('#city-dialog [data-city-reread="seven-factors"]').count()==1
        if label=='body-and-seven':
            guardian=p.locator('[data-companion="mindfulness"]');assert guardian.get_attribute('data-companion-placed')=='false' and not guardian.is_visible();assert p.locator('[data-concealed-feature="guardian"]').count()==1;assert len([n for n in p.locator('[data-companion] svg').all() if n.is_visible()])==6
            dialog=open_reward(p,'awakening_companions');assert '念-守門人待城門與四念處齊備' in dialog.locator('.status-label').inner_text()
        if label=='roots-and-body':assert p.locator('[data-faculty-zone]').count()==0
        if label=='roots-faith-source':assert p.locator('[data-faculty-zone]').count()==1 and p.locator('[data-faculty-zone="faith"]').count()==1
        if label=='before-seven':
            dialog=open_reward(p,'awakening_companions');assert dialog.locator('[data-city-reread]').count()==0 and dialog.locator('.city-source-link').count()==0
        if label=='all-fourteen':assert p.locator('[data-city-reward="fruition_guide"]').count()==1
        assert d.q.snapshot(p)==saved
        visible_source=len([n for n in p.locator('[data-companion] svg').all() if n.is_visible()])
        guardian=p.locator('[data-companion="mindfulness"]')
        cases.append({'fixture':label,'completedIdsRetained':done,'companionDomCount':companions,
            'visibleSourceCompanionCount':visible_source,'existingGuardianVisible':bool(guardian.count() and guardian.is_visible()),
            'existingGuardianPending':bool(guardian.count() and guardian.get_attribute('data-companion-placed')=='false'),
            'explicitPendingStatusVerified':label=='body-and-seven','pendingOnly':pending,'readingSaveUnchanged':True});c.close()
    saved=d.q.fixture([],{d.q.ORDER[12]:5,d.q.ORDER[11]:4},d.q.ORDER[12]);c=d.q.context_for(browser,base,saved);p=c.new_page();d.q.observe(p,base,report);p.goto(base+'play/city/');city_loaded(p)
    assert p.locator('[data-companion]').count()==0 and p.locator('[data-faculty-zone]').count()==0
    p.goto(base+'seven-factors/book/?collection=1&collectionReturn=game&collectionPage=5');p.wait_for_url('**/game/?notice=locked#map');d.map_ready(p);assert not p.locator('.story-dialogue').is_visible();assert d.q.snapshot(p)==saved and p.locator('.wm-landmark.is-next').get_attribute('data-book')=='four-truths';assert p.locator('[data-wm-city-entry]').count()==0;c.close()
    report['historicalRewardFixtures']=cases;report['futureBookmarksNoRewardsOrAccess']=True


def main():
    OUT.mkdir(parents=True,exist_ok=True);report=d.q.protect_originals();report.update({'phase':'Local review only','javascriptErrors':[],'httpErrors':[],'physicalSafari':'Not tested; Chromium viewport/input simulation only','fixtures':'Completed-book fixtures are isolated historical saves, not claimed native fourteen-book completions.'});portrait_metadata(report);story_store_model(report)
    paths=['play/collection/store.js','play/collection/reader-bridge.js','play/reader-bridge.js','play/route','play/worldmap-v4/data.js','play/visual-v2/network-data.js','play/worldmap-v4/camera.js','play/title-screen.js','play/title-screen.css','play/game-ui-text.js','play/assets/CC1A7C32-0620-4DB2-BCD2-A9457A83C259.jpeg']
    changed=subprocess.check_output(['git','diff','--name-only',d.q.BASE,'--',*paths],cwd=ROOT,text=True).splitlines();assert not changed,changed;report['protectedGameCore']=paths
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(d.q.Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
    try:
        with sync_playwright() as p:
            b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);intro_checks(b,base,report);story_storage_fallback(b,base,report);cross_page_once(b,base,report);fresh_intro_completion(b,base,report);portrait_failure_recovery(b,base,report);city_reward_checks(b,base,report);historical_reward_edges(b,base,report);b.close()
    finally:server.shutdown()
    assert not report['javascriptErrors'],report['javascriptErrors'];assert not report['httpErrors'],report['httpErrors'];report['result']='passed';(OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'result':report['result'],'report':str((OUT/'validation.json').relative_to(ROOT))},ensure_ascii=False))


if __name__=='__main__':main()
