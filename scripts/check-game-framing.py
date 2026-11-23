#!/usr/bin/env python3
"""Narrow shelf framing/Mara presentation QA; no repeated full-book completion."""
from pathlib import Path
import functools,hashlib,http.server,importlib.util,json,re,subprocess,threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/previews/game-framing'
s=importlib.util.spec_from_file_location('auto_city_qa',ROOT/'scripts/check-game-auto-city.py');auto=importlib.util.module_from_spec(s);s.loader.exec_module(auto)
q=auto.q;d=auto.d;city=auto.city;story=auto.story;outro=auto.outro
BASELINE='a9ee6ae8fda9e1ec01822aa013ad85bcdf551f3a';VERSION='framing-1';SIZES=q.SIZES+[(2048,1115)]


def normalize_queries(text):
    text=re.sub(r'\?v=[A-Za-z0-9-]+','?v=CACHE',text)
    return re.sub(r"(set\('collectionStory',')[^']+",r'\1CACHE',text)


def guard_sources():
    originals=q.ORDER+['docs/'+book for book in q.ORDER]+['index.html','shelf.css','sitemap.xml','robots.txt','googlee0c995331ec518ae.html','reader-controls.css','reader-layout.js','reader-restart.js','picture-panel-focus.js','picture-panel-focus.css','docs/seo','map-topic-resources.css','scripts/site_seo.py','scripts/build-seo.py','scripts/check-seo.py']
    html=[book+'/book/index.html' for book in q.ORDER];changes=subprocess.check_output(['git','diff','--name-only',BASELINE,'--',*originals],cwd=ROOT,text=True).splitlines();assert set(changes)<=set(html),changes
    old=lambda path:subprocess.check_output(['git','show',BASELINE+':'+path],cwd=ROOT)
    for path in html:assert normalize_queries((ROOT/path).read_text())==normalize_queries(old(path).decode()),path
    strict=['play/collection/store.js','play/collection/reader.css','play/reader-bridge.js','play/route','play/prologue','play/story/assets','play/story/completion-receipt.js','play/worldmap-v4/camera.js','play/worldmap-v4/data.js','play/visual-v2/network-data.js','play/visual-v2/assets','play/worldmap-v4/assets','play/assets','play/city/modules/assets','play/visual-v2/shelf-copy.js','play/collection/catalog.js']
    changes=subprocess.check_output(['git','diff','--name-only',BASELINE,'--',*strict],cwd=ROOT,text=True).splitlines();assert not changes,changes
    cached=['play/collection/reader-bridge.js','play/story/data.js','play/story/store.js','play/story/dialogue.js','play/worldmap-v4/worldmap.js','play/worldmap-v4/completion-feedback.js','play/visual-v2/shelf.js','play/city/modules/store.js','play/journey-save.js','play/city/thoughts.js','play/city/text.js']
    for path in cached:assert normalize_queries((ROOT/path).read_text())==normalize_queries(old(path).decode()),path
    count=len([p for p in subprocess.check_output(['git','ls-tree','-rz','--name-only',BASELINE,'--',*originals],cwd=ROOT,text=True).split('\0') if p]);asset=ROOT/'play/visual-v2/assets/library-concept.png'
    return {'baseline':BASELINE,'protectedOriginalFiles':count,'originalNarrationScriptureImagesReaderControlsHomepageSeoGoogle':'unchanged; cache query normalization only if needed','readingStoryReceiptEligibilityStoreAndBackupSchemas':'unchanged; cache query normalization only','originalLibraryArtworkSha256':hashlib.sha256(asset.read_bytes()).hexdigest(),'noArtworkRegeneration':True,'narrowPresentationExceptions':'Shelf full-width CSS and Mara world position/no sweat in city scene only'}


def shelf_ready(page):
    page.wait_for_selector('[data-book-card]');page.wait_for_function('document.querySelectorAll("[data-book-card]").length===14')
    page.evaluate(r'''async()=>{const box=document.querySelector('.collection-case'),url=getComputedStyle(box).backgroundImage.match(/url\(["']?(.*?)["']?\)/)?.[1];if(url){const i=new Image();i.src=url;await i.decode()}await Promise.all([...document.querySelectorAll('.earned-cover')].map(i=>i.decode()))}''');q.settle(page);auto.city.no_overflow(page)


def goto_shelf(page,base):page.goto(base+'play/visual-v2/shelf.html?v='+VERSION+'#shelf');shelf_ready(page)


def shelf_geometry(page):
    value=page.evaluate('''()=>{const stage=document.querySelector('.collection-stage'),bookcase=document.querySelector('.collection-case'),main=document.querySelector('main'),r=n=>n.getBoundingClientRect().toJSON();return {viewport:[innerWidth,innerHeight],stage:r(stage),case:r(bookcase),main:r(main),stageClientWidth:stage.clientWidth,scrollbarWidth:stage.offsetWidth-stage.clientWidth,caseBackground:getComputedStyle(bookcase).backgroundImage,caseMargin:getComputedStyle(bookcase).marginInline,stagePadding:getComputedStyle(stage).paddingInline}}''')
    width=value['viewport'][0]
    for name in ['stage','main']:assert abs(value[name]['left'])<1 and abs(value[name]['right']-width)<1,(name,value)
    assert abs(value['case']['left'])<1 and abs(value['case']['width']-value['stageClientWidth'])<1,value
    assert 'library-concept.png' in value['caseBackground'] and value['caseMargin'] in ['0px','0px 0px'] and value['stagePadding'] in ['0px','0px 0px'],value
    return value


def scroll_to_last(page,ctx,touch=False):
    stage=page.locator('.collection-stage');r=stage.bounding_box();last=page.locator('[data-book-card="four-fruits-ten-fetters"]')
    for _ in range(18):
        box=last.bounding_box()
        if box['y']>=r['y'] and box['y']+box['height']<=r['y']+r['height']-2:return
        if touch:
            auto.city.touch_path(page,ctx,(r['x']+r['width']*.85,r['y']+r['height']*.8),(r['x']+r['width']*.85,r['y']+r['height']*.2));page.wait_for_timeout(70)
        else:page.mouse.move(r['x']+r['width']*.85,r['y']+r['height']*.6);page.mouse.wheel(0,500);page.wait_for_timeout(70)
    box=last.bounding_box();assert box['y']>=r['y']-1 and box['y']+box['height']<=r['y']+r['height']+1,(box,r)


def shelf_matrix(browser,base,report):
    rows=[]
    for width,height in SIZES:
        for count in [0,1,14]:
            saved=q.fixture(q.ORDER[:count],{},q.ORDER[min(count,13)]);ctx=auto.context(browser,base,saved,viewport={'width':width,'height':height},has_touch=True);page=ctx.new_page();q.observe(page,base,report);goto_shelf(page,base);before=auto.collection_raw(page);geometry=shelf_geometry(page)
            assert page.locator('[data-book-card]').count()==14 and page.locator('[data-collection-read]').count()==count and page.locator('.earned-cover').count()==count
            assert page.locator('.collection-book-placeholder').count()==14-count and page.locator('#collection-empty').is_visible()==(count==0)
            page.screenshot(path=str(OUT/f'shelf-{count}-historical-{width}x{height}.png'));touch=width<=844 and min(width,height)<500;scroll_to_last(page,ctx,touch)
            page.screenshot(path=str(OUT/f'shelf-{count}-last-row-{width}x{height}.png'))
            if count==14:
                page.locator('[data-collection-read="four-fruits-ten-fetters"]').click();page.wait_for_selector('body[data-collection-book="four-fruits-ten-fetters"]');assert 'collectionReview=1' in page.url
                assert q.snapshot(page)['completed']==q.ORDER;page.locator('.collection-reader-return').click();shelf_ready(page);assert q.snapshot(page)['completed']==q.ORDER
            else:
                url=page.url;placeholder=page.locator('[data-book-card="four-fruits-ten-fetters"] .collection-book-placeholder');placeholder.tap() if touch else placeholder.click();q.settle(page);assert page.url==url and auto.collection_raw(page)==before
            rows.append({'viewport':[width,height],'fixture':f'{count} historical completed books','geometry':geometry,'fourteenCardsAndLockedReviewEligibilityRetained':True,'nativeScrollInput':'CDP single-finger swipe' if touch else 'browser mouse wheel','lastCardNativeTapOrClick':True,'lastBookOnlyReviewableWhenCompleted':True});ctx.close()
    report['shelfSixSizeThreeHistoryMatrix']=rows


def native_review_resume(browser,base,report):
    saved=q.fixture(['four-truths'],{'four-truths':28,'five-aggregates':8},'five-aggregates');ctx=auto.context(browser,base,saved,viewport={'width':360,'height':800});page=ctx.new_page();q.observe(page,base,report);goto_shelf(page,base)
    page.locator('[data-collection-read="four-truths"]').click();page.wait_for_selector('body[data-collection-book="four-truths"][data-collection-index="0"]')
    for index in [1,2,3]:q.click_next(page,index)
    page.reload();page.wait_for_selector('body[data-collection-index="3"]');page.locator('.collection-reader-return').click();shelf_ready(page);after=q.snapshot(page)
    assert after['completed']==['four-truths'] and after['activeBook']=='five-aggregates' and after['positions']['five-aggregates']==8 and after['positions']['four-truths']==3
    page.screenshot(path=str(OUT/'native-review-first-index3-return-360x800.png'));page.locator('[data-game-nav="map"]').click();d.map_ready(page);assert not page.locator('.story-dialogue').is_visible();page.locator('[data-wm-next]').click();page.wait_for_selector('body[data-collection-book="five-aggregates"][data-collection-index="8"]')
    report['nativeReviewResume']={'fixture':'first historically complete, mainline Five bookmark8','actualReviewNextTrace':[0,1,2,3],'reloadAndReturnKeepsReviewBookmark':True,'mainlineActiveFiveAndBookmark8Unchanged':True,'nativeMapContinueOpensOriginalFiveAt8':True,'completionCountStill1':True};ctx.close()


def city_framing(browser,base,report):
    rows=[]
    for width,height in SIZES:
        for count in [1,14]:
            saved=q.fixture(q.ORDER[:count],{},q.ORDER[min(count,13)]);ctx=auto.context(browser,base,saved,viewport={'width':width,'height':height});page=ctx.new_page();q.observe(page,base,report);page.goto(base+'play/city/?v='+VERSION+'#city');auto.ready_city(page);before=auto.collection_raw(page)
            positions=page.evaluate('''()=>Object.fromEntries(['mara','lord'].map(id=>{const n=document.querySelector('[data-city-actor="'+id+'"]');return [id,{x:parseFloat(n.style.left),y:parseFloat(n.style.top)}]}))''');assert positions['mara']['x']<positions['lord']['x'] and positions['mara']['y']<positions['lord']['y']
            assert page.locator('.mod-city__sweat').count()==0;old=auto.camera(page);page.locator('#city-overview-toggle').click();page.wait_for_function('window.SutraZenModularCity.getCamera().camera.overview');q.settle(page)
            page.screenshot(path=str(OUT/f'city-{count}-overview-{width}x{height}.png'));page.locator('[data-city-actor="mara"]').click();panel=page.locator('.city-thought[data-actor="mara"]:not([hidden])');panel.wait_for();assert panel.locator('h2').inner_text()=='波旬';page.screenshot(path=str(OUT/f'city-{count}-mara-dialogue-{width}x{height}.png'));panel.locator('[data-city-thought-close]').click();auto.plaza_source_and_close(page)
            page.locator('#city-overview-return').click();q.settle(page);new=auto.camera(page)
            for key in ['x','y','scale']:assert abs(old[key]-new[key])<.05,(old,new)
            assert not new['overview'] and auto.collection_raw(page)==before and page.locator('.mod-city__sweat').count()==0
            rows.append({'viewport':[width,height],'fixture':f'{count} historical completed books','worldPositions':positions,'maraUpperLeftOfLordWithOriginalRightFacingArt':True,'sweatNodes':0,'nativeMaraXPlazaSourceXAndExactOverviewReturn':True,'readingJsonByteUnchanged':True});ctx.close()
    report['cityMaraAndNoSweatMatrix']=rows


def notification_smoke(browser,base,report):
    saved=q.fixture(['four-truths'],{'four-truths':28},'five-aggregates');seen=outro.ARRIVAL+[outro.INSIGHT,outro.CUTOFF,outro.MARA,outro.TAIL];ctx=auto.context(browser,base,saved,seen);page=ctx.new_page();q.observe(page,base,report)
    page.goto(base+'game/?v='+VERSION+'&completed=four-truths#map');d.map_ready(page);page.wait_for_selector('#wm-dialog.wm-completion-dialog[open]');assert page.locator('[data-city-auto-notice][data-city-placement="automatic"]').count()==1 and '法輪碼頭' in page.locator('#wm-dialog').inner_text();page.locator('[data-wm-city-update]').click();auto.ready_city(page)
    assert auto.visible_ids(page)==['truth_dock'] and q.snapshot(page)==saved;report['automaticNoticeSmoke']={'fixture':'historical confirmed outro plus explicit completed URL; not a new completion proof','automaticNotificationAndNativeCityLinkPreserved':True,'cityDerivedTruthDockAndReadingUnchanged':True,'nativeFirst29NotRepeatedForPresentationOnlyChange':True};ctx.close()


def save(report):OUT.mkdir(parents=True,exist_ok=True);(OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')


def main():
    OUT.mkdir(parents=True,exist_ok=True);report=guard_sources();report.update({'phase':'Local narrow city/shelf framing regression','javascriptErrors':[],'httpErrors':[],'fixtureNotice':'All completed counts are isolated historical fixtures. Native review 0-3 and existing mainline continuation are actual clicks; No new end-of-book completion is exercised or claimed in this narrow round.','physicalSafari':'Not tested; Chromium desktop viewport/mouse/CDP touch simulation.'})
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(q.Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);shelf_matrix(browser,base,report);print('shelf six sizes x three histories passed',flush=True);native_review_resume(browser,base,report);city_framing(browser,base,report);notification_smoke(browser,base,report);browser.close()
        for command in [['python3','-B','scripts/build-game-entry.py','--check'],['python3','-B','scripts/build-seo.py','--check']]:subprocess.run(command,cwd=ROOT,check=True,capture_output=True,text=True)
        report['seoAndGeneratedEntry']='passed';assert not report['javascriptErrors'],report['javascriptErrors'];assert not report['httpErrors'],report['httpErrors'];report['result']='passed'
    except Exception as error:report['result']='failed';report['error']=repr(error);raise
    finally:server.shutdown();save(report)
    print(json.dumps({'result':report['result'],'report':str(OUT/'validation.json')},ensure_ascii=False))


if __name__=='__main__':main()
