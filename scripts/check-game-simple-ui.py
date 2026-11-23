#!/usr/bin/env python3
"""Focused simple game UI; historical fixtures and native completion separate."""
from pathlib import Path
import functools,http.server,importlib.util,json,re,subprocess,threading,shutil
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/previews/game-simple-ui'
s=importlib.util.spec_from_file_location('framing_qa',ROOT/'scripts/check-game-framing.py');qa=importlib.util.module_from_spec(s);s.loader.exec_module(qa)
auto=qa.auto;q=qa.q;d=qa.d;city=qa.city;outro=qa.outro;story=auto.story
BASELINE='d82f68533f595db032c8a787a1a2c5606a53fb2f';VERSION='simple-ui-1';SIZES=q.SIZES+[(2048,1115)]
PLAZA_QUOTE='『在中央四衢街道』，這是四大的同義語，即：地界的、水界的、火界的、風界的。'
FULL_CONTROLS='[data-wm-overview],[data-wm-return],[data-wm-zoom],#city-overview-toggle,#city-overview-return'


def normalized(text):
    return re.sub(r"(set\('collectionStory',')[^']+",r'\1CACHE',re.sub(r'\?v=[A-Za-z0-9-]+','?v=CACHE',text))


def guard_sources():
    originals=q.ORDER+['docs/'+book for book in q.ORDER]+['index.html','shelf.css','sitemap.xml','robots.txt','googlee0c995331ec518ae.html','reader-controls.css','reader-layout.js','reader-restart.js','picture-panel-focus.js','picture-panel-focus.css','docs/seo','map-topic-resources.css','scripts/site_seo.py','scripts/build-seo.py','scripts/check-seo.py']
    old=lambda p:subprocess.check_output(['git','show',BASELINE+':'+p],cwd=ROOT)
    html=[book+'/book/index.html' for book in q.ORDER];changed=subprocess.check_output(['git','diff','--name-only',BASELINE,'--',*originals],cwd=ROOT,text=True).splitlines();assert set(changed)<=set(html),changed
    for path in html:assert normalized((ROOT/path).read_text())==normalized(old(path).decode()),path
    strict=['play/collection/store.js','play/collection/reader.css','play/reader-bridge.js','play/route','play/story/completion-receipt.js','play/story/assets','play/visual-v2/assets','play/worldmap-v4/assets','play/assets','play/city/modules/assets','play/worldmap-v4/data.js','play/visual-v2/network-data.js','play/visual-v2/shelf-copy.js','play/collection/catalog.js']
    changed=subprocess.check_output(['git','diff','--name-only',BASELINE,'--',*strict],cwd=ROOT,text=True).splitlines();assert not changed,changed
    for path in ['play/collection/reader-bridge.js','play/visual-v2/shelf.js','play/city/modules/store.js','play/story/store.js','play/journey-save.js']:
        assert normalized((ROOT/path).read_text())==normalized(old(path).decode()),path
    prior_scene_texts=re.findall(r"text:'([^']+)'",old('play/story/data.js').decode())
    assert re.findall(r"text:'([^']+)'",(ROOT/'play/story/data.js').read_text())==prior_scene_texts
    count=len([p for p in subprocess.check_output(['git','ls-tree','-rz','--name-only',BASELINE,'--',*originals],cwd=ROOT,text=True).split('\0') if p])
    return {'baseline':BASELINE,'protectedOriginalFiles':count,'originalSiteBooksScriptureArtSeoGoogle':'unchanged except reader cache queries','readingReceiptEligibilityStorageSchemaBackupAndArtwork':'unchanged except UI import/return cache queries','authorizedPresentationChanges':'Camera controls/normal legacy view, title/prologue entry, single shelf background, concise source and final completion dialogue'}


def critical_raw(page):return page.evaluate('(keys)=>keys.map(k=>localStorage.getItem(k))',[q.KEY,outro.STORY_KEY,city.CITY_KEY])
def map_ready(page):d.map_ready(page);assert page.locator(FULL_CONTROLS).count()==0;city.no_overflow(page)
def city_ready(page):
    page.wait_for_selector('.mod-city');page.wait_for_function('window.SutraZenModularCity?.getState()?.modules?.length===14');q.settle(page);assert page.locator(FULL_CONTROLS).count()==0;city.no_overflow(page)


def single_library_layer(page):
    layers=page.evaluate('''()=>{const result=[];for(const n of document.querySelectorAll('body,body *')){for(const pseudo of [null,'::before','::after']){const image=getComputedStyle(n,pseudo).backgroundImage;if(image.includes('library-concept.png'))result.push({tag:n.tagName,class:n.className,pseudo,image})}if(n instanceof HTMLImageElement&&n.src.includes('library-concept.png'))result.push({tag:n.tagName,class:n.className,src:n.src})}return result}''')
    assert len(layers)==1 and layers[0]['class']=='collection-stage',layers;return layers


def swipe_stage(page,ctx,direction,distance=110):
    bounds=page.locator('.collection-stage').bounding_box();x=bounds['x']+bounds['width']*.85;y=bounds['y']+bounds['height']*.5;distance=min(distance,bounds['height']*.35)
    auto.city.touch_path(page,ctx,(x,y+direction*distance/2),(x,y-direction*distance/2),steps=18);page.wait_for_timeout(120)


def shelf_single_background(browser,base,report):
    rows=[]
    for width,height in SIZES:
        for count in [0,14]:
            saved=q.fixture(q.ORDER[:count],{},q.ORDER[min(count,13)]);ctx=auto.context(browser,base,saved,viewport={'width':width,'height':height},has_touch=True);page=ctx.new_page();q.observe(page,base,report);page.goto(base+'play/visual-v2/shelf.html?v='+VERSION+'#shelf');qa.shelf_ready(page);before=critical_raw(page);layers=single_library_layer(page);geometry=page.evaluate('''()=>{const stage=document.querySelector('.collection-stage'),c=document.querySelector('.collection-case');return {stage:stage.getBoundingClientRect().toJSON(),case:c.getBoundingClientRect().toJSON(),width:innerWidth}}''');assert abs(geometry['stage']['left'])<1 and abs(geometry['stage']['right']-geometry['width'])<1 and abs(geometry['case']['left'])<1
            assert page.locator('[data-book-card]').count()==14 and page.locator('[data-collection-read]').count()==count
            page.screenshot(path=str(OUT/f'shelf-{count}-top-{width}x{height}.png'));swipe_stage(page,ctx,1)
            position=page.locator('.collection-stage').evaluate('(n)=>({top:n.scrollTop,max:n.scrollHeight-n.clientHeight})');assert 0<position['top']<position['max'],position
            single_library_layer(page);page.screenshot(path=str(OUT/f'shelf-{count}-middle-{width}x{height}.png'))
            for _ in range(22):
                value=page.locator('.collection-stage').evaluate('(n)=>({top:n.scrollTop,max:n.scrollHeight-n.clientHeight})')
                if value['top']>=value['max']-2:break
                swipe_stage(page,ctx,1,250)
            value=page.locator('.collection-stage').evaluate('(n)=>({top:n.scrollTop,max:n.scrollHeight-n.clientHeight})');assert value['top']>=value['max']-2,value
            # An additional upward swipe at the lower bound must not expose a
            # second copy of the painted shelf in the surrounding layers.
            swipe_stage(page,ctx,1,180);single_library_layer(page);page.screenshot(path=str(OUT/f'shelf-{count}-bottom-{width}x{height}.png'))
            for _ in range(22):
                if page.locator('.collection-stage').evaluate('(n)=>n.scrollTop')<=2:break
                swipe_stage(page,ctx,-1,250)
            assert page.locator('.collection-stage').evaluate('(n)=>n.scrollTop')<=2;swipe_stage(page,ctx,-1,180);single_library_layer(page)
            assert critical_raw(page)==before;city.no_overflow(page)
            rows.append({'viewport':[width,height],'fixture':f'{count} historical completed','geometry':geometry,'libraryLayers':layers,'nativeCdpUpDownTopMiddleBottomAndBothBoundaries':True,'noSecondPaintedHeaderOrReadingMutation':True});ctx.close()
    report['singleBackgroundShelfMatrix']=rows


def camera_controls_and_legacy(browser,base,report):
    rows=[];seen=outro.ARRIVAL+[outro.INSIGHT,outro.CUTOFF,outro.MARA,outro.TAIL]
    for width,height in SIZES:
        for area,key in [('map','sutrazen.play.camera.v1'),('city','sutrazen.play.city.camera.v1')]:
            saved=q.fixture(['four-truths'],{'four-truths':28,'five-aggregates':8},'five-aggregates');ctx=auto.context(browser,base,saved,seen,viewport={'width':width,'height':height},has_touch=True)
            ctx.add_init_script("if(!sessionStorage.getItem('qa.simple.camera-seeded')){sessionStorage.setItem("+json.dumps(key)+",JSON.stringify({version:1,x:800,y:450,scale:.23,overviewExplicit:true,returnView:{x:800,y:450,scale:1.35}}));sessionStorage.setItem('qa.simple.camera-seeded','1')}")
            page=ctx.new_page();q.observe(page,base,report);page.goto(base+('game/?v='+VERSION+'#map' if area=='map' else 'play/city/?v='+VERSION+'#city'));map_ready(page) if area=='map' else city_ready(page)
            getter='window.SutraZenWorldmap.getState().camera' if area=='map' else 'window.SutraZenModularCity.getCamera().camera';before=page.evaluate(getter);assert not before['overview'] and not before['overviewExplicit'] and before['scale']>=before['coverScale']-.001,before;raw=critical_raw(page)
            viewport=page.locator('.wm-viewport' if area=='map' else '.mod-city__viewport').bounding_box();x=viewport['x']+viewport['width']*.48;y=min(viewport['y']+viewport['height']*.6,page.locator('.game-dock').bounding_box()['y']-50)
            auto.city.touch_path(page,ctx,(x,y),(x+65,y));dragged=page.evaluate(getter);assert abs(before['x']-dragged['x'])+abs(before['y']-dragged['y'])>.1
            auto.pinch(page,ctx,x,y);zoomed=page.evaluate(getter);assert zoomed['scale']>dragged['scale']
            if area=='map':
                plus=page.locator('[data-wm-zoom-in]');plus.focus();plus.click();greater=page.evaluate(getter)['scale'];assert greater>=zoomed['scale'];minus=page.locator('[data-wm-zoom-out]');minus.focus();minus.click();assert page.evaluate(getter)['scale']<greater
                locate=page.locator('[data-wm-locate]');locate.focus();locate.click();q.settle(page)
            assert page.locator(FULL_CONTROLS).count()==0 and critical_raw(page)==raw and not page.locator('#wm-dialog[open],#city-dialog[open]').count();page.screenshot(path=str(OUT/f'{area}-simple-controls-{width}x{height}.png'))
            page.reload();map_ready(page) if area=='map' else city_ready(page);assert not page.evaluate(getter)['overview'] and critical_raw(page)==raw
            rows.append({'viewport':[width,height],'area':area,'fixture':'legacy explicit overview with return snapshot; first done/Five8','legacyAutomaticallyNormal':before,'noOverviewFullBackButtons':True,'nativeDragPinch':True,'mapPlusMinusLocateRetained':area=='map','reloadKeepsExplorationAndReading':True});ctx.close()
    report['cameraRemovalAndLegacyMatrix']=rows


def minimal_dialog(page,expected_quote=None,canonical=True):
    panel=page.locator('#city-dialog[open]');panel.wait_for();content=page.locator('#city-dialog-content');assert panel.locator('button').count()==1 and panel.locator('[data-city-close]').count()==1
    assert content.locator('a,button,img,svg,figure,picture').count()==0,content.inner_html();text=content.inner_text()
    assert not any(word in text for word in ['前往關卡','重新閱讀','閱讀原經','查看原經','複習','查看相關繪本出處']),text
    if expected_quote:
        assert content.locator('[data-city-explanation=canonical]').text_content()==expected_quote,text
    if not canonical:assert 'SN35.245' not in text and 'SN 35.245' not in text,text
    close=panel.locator('[data-city-close]');box=close.bounding_box();assert box['width']>=48 and box['height']>=48
    return text


def concise_city_sources(browser,base,report):
    rows=[]
    for width,height in SIZES:
        saved=q.fixture(q.ORDER,{},q.ORDER[0]);ctx=auto.context(browser,base,saved,viewport={'width':width,'height':height});page=ctx.new_page();q.observe(page,base,report);page.goto(base+'play/city/?v='+VERSION+'#city');city_ready(page);before=auto.collection_raw(page)
        # Source points are located through their existing world-space button.
        plaza=page.locator('[data-city-inspect="plaza"]');plaza.focus();box=plaza.bounding_box();plaza.click(position={'x':box['width']*.2,'y':box['height']*.3});quote=minimal_dialog(page,PLAZA_QUOTE);page.screenshot(path=str(OUT/f'plaza-short-quote-{width}x{height}.png'));page.locator('[data-city-close]').click()
        assert auto.collection_raw(page)==before;rows.append({'viewport':[width,height],'canonicalPlazaExactAuthorQuote':quote,'onlyNameQuoteAndX':True,'noReadingMutation':True});ctx.close()
    report['minimalCanonicalSourceMatrix']=rows


def extended_and_seven_correspondences(browser,base,report):
    saved=q.fixture(q.ORDER,{},q.ORDER[0]);ctx=auto.context(browser,base,saved);page=ctx.new_page();q.observe(page,base,report);page.goto(base+'play/city/?v='+VERSION+'#city');city_ready(page);before=auto.collection_raw(page)
    entries=page.evaluate("async()=>{const m=await import('/play/city/explanations.js?v=simple-ui-1');return Object.entries(m.MODULE_EXPLANATIONS).filter(([id,v])=>v.kind==='extended').map(([id,v])=>({id,...v}))}")
    assert entries and all('SN35.245' not in e['title']+e['text'] and 'SN 35.245' not in e['title']+e['text'] for e in entries)
    for id,fx,fy in [('truth_dock',.8,.2),('effort_garden',.8,.5)]:
        target=page.locator('[data-city-inspect="'+id+'"]');target.focus();r=target.bounding_box();target.click(position={'x':r['width']*fx,'y':r['height']*fy});text=minimal_dialog(page,canonical=False);assert len(text)<250,text;page.locator('[data-city-close]').click()
    roles=[('guardian','念'),('awakening-owl','擇法'),('awakening-rabbit','精進'),('awakening-bird','喜'),('awakening-turtle','輕安'),('awakening-lotus','定'),('awakening-deer','捨')];lines=[]
    for actor,term in roles:
        target=page.locator('[data-city-actor="'+actor+'"]');target.focus();target.click();panel=page.locator('.city-thought[data-actor="'+actor+'"]:not([hidden])');panel.wait_for();line=panel.locator('.city-thought__line').inner_text()
        if actor=='guardian':assert line=='先看看來的是誰，再提醒大家。六道門仍要正常通行，我會留意眼前發生的事。'
        else:assert term in line and '覺支' in line and '\n' not in line and 'SN35' not in panel.inner_text(),line
        assert panel.locator('.city-thought__line').count()==1 and panel.locator('button').count()==1;page.screenshot(path=str(OUT/f'seven-correspondence-{actor}-1280x900.png'));panel.locator('[data-city-thought-close]').click();lines.append({'actor':actor,'singleLineCorrespondence':line})
    assert auto.collection_raw(page)==before;report['extensionsAndSevenAnimals']={'fixture':'all14 historical completed','extendedTitlesAndTopicTextWithoutSN35':entries,'nativeTwoExtendedScenerySourcesAndX':True,'sixFictionalCompanionsAndOriginalCanonicalGuardian':lines,'noReadingMutation':True};ctx.close()


def assert_story(page,id):
    panel=page.locator(f'.story-dialogue[data-scene="{id}"]:not([hidden])');panel.wait_for();auto.story.dialogue_geometry(page)
    expected=auto.cyan.FIVE_TEXT if id==outro.TAIL else auto.mara.MARA_TEXT if id==outro.MARA else story.LINES[id]
    assert panel.locator('.story-dialogue__line').inner_text()==expected
    assert not any(label in panel.inner_text() for label in ['看閱讀回饋','看看旅程的變化'])
    if id in [outro.INSIGHT,outro.CUTOFF,outro.MARA,outro.TAIL]:assert not panel.locator('.story-dialogue__skip').is_visible()
    return panel


def native_completion_script(browser,base,report):
    # Updated with final reward-dialogue selectors when root signals READY.
    ctx=auto.context(browser,base);page=ctx.new_page();q.observe(page,base,report);page.goto(base+'game/?v='+VERSION+'#map');map_ready(page)
    for id in outro.ARRIVAL:assert_story(page,id);page.locator('.story-dialogue__next').click()
    page.wait_for_selector('body[data-collection-book="four-truths"][data-collection-index="0"]');trace=[0]
    for index in range(1,29):q.click_next(page,index);trace.append(index)
    assert q.snapshot(page)['completed']==[];page.locator('#next').click();map_ready(page);assert_story(page,outro.INSIGHT)
    page.keyboard.press('Escape');assert_story(page,outro.INSIGHT)
    for id in [outro.CUTOFF,outro.MARA,outro.TAIL]:page.locator('.story-dialogue__next').click();assert_story(page,id)
    page.locator('.story-dialogue__next').click();page.wait_for_selector('.story-dialogue:not([hidden]) [data-city-auto-notice]');panel=page.locator('.story-dialogue:not([hidden])');assert not page.locator('#wm-dialog[open]').count();assert panel.locator('button:visible').count()==2
    labels=panel.locator('button:visible').all_inner_texts();assert set(labels)=={'前往城池看看','前往下一站'},labels;before=q.snapshot(page);assert before['completed']==['four-truths'];page.screenshot(path=str(OUT/'native-first29-final-notice-dialogue-1280x900.png'))
    page.reload();map_ready(page);page.wait_for_selector('.story-dialogue:not([hidden]) [data-city-auto-notice]');assert q.snapshot(page)==before
    panel=page.locator('.story-dialogue:not([hidden])');panel.get_by_role('button',name='前往城池看看',exact=True).click();city_ready(page);assert auto.visible_ids(page)==['truth_dock'] and q.snapshot(page)==before
    page.locator('[data-game-nav="map"]').click();map_ready(page);assert not page.locator('.story-dialogue').is_visible();page.locator('[data-wm-next]').click();page.wait_for_selector('body[data-collection-book="five-aggregates"][data-collection-index="0"]')
    for index in [1,2,3]:q.click_next(page,index)
    page.reload();page.wait_for_selector('body[data-collection-index="3"]');page.locator('.collection-reader-return').click();map_ready(page);assert q.snapshot(page)['completed']==['four-truths'] and q.snapshot(page)['positions']['five-aggregates']==3
    report['nativeFirstCompletionScript']={'actualFirstNextTrace':trace,'oldIntermediateLabelsAbsent':True,'order':[outro.INSIGHT,outro.CUTOFF,outro.MARA,outro.TAIL,'notification-in-dialogue'],'finalActions':labels,'noticeReloadResumesWithoutExtraCompletion':True,'nativeCityThenFive0To3ReloadReturn':True};ctx.close()



def final_notice_branches_and_reset(browser,base,report):
    rows=[];seen=outro.ARRIVAL+[outro.INSIGHT,outro.CUTOFF,outro.MARA,outro.TAIL]
    for width,height in SIZES:
        saved=q.fixture(['four-truths'],{'four-truths':28},'five-aggregates');ctx=auto.context(browser,base,saved,seen,viewport={'width':width,'height':height});page=ctx.new_page();q.observe(page,base,report)
        page.goto(base+'game/?v='+VERSION+'&completed=four-truths#map');map_ready(page);page.wait_for_selector('.story-dialogue[data-context="completion-reward"]:not([hidden])');auto.story.dialogue_geometry(page);auto.story.portrait_unclipped(page)
        panel=page.locator('.story-dialogue:not([hidden])');assert panel.locator('button:visible').all_inner_texts()==['前往城池看看','前往下一站'];assert not any(word in panel.inner_text() for word in ['看閱讀回饋','看看旅程的變化']);page.screenshot(path=str(OUT/f'final-notice-fixture-{width}x{height}.png'))
        page.keyboard.press('Escape');q.settle(page);assert not panel.is_visible() and 'completed=' not in page.url and q.snapshot(page)==saved
        page.reload();map_ready(page);assert not page.locator('.story-dialogue').is_visible() and q.snapshot(page)==saved
        page.goto(base+'game/?v='+VERSION+'&completed=four-truths#map');map_ready(page);page.locator('.story-dialogue:not([hidden])').get_by_role('button',name='前往下一站',exact=True).click();q.settle(page)
        assert '/book/' not in page.url and 'completed=' not in page.url and not page.locator('.story-dialogue').is_visible() and q.snapshot(page)==saved
        rows.append({'viewport':[width,height],'fixture':'isolated historical first29-last, accepted outro; not new completion proof','finalTwoChoiceDialogueReadableAndAboveDock':True,'escapeClearsPresentationUrlWithoutProgressMutation':True,'nextChoiceOnlyLocatesFive':True});ctx.close()
    saved=q.fixture(['four-truths'],{'four-truths':28},'five-aggregates');ctx=auto.context(browser,base,saved,seen,viewport={'width':360,'height':800});page=ctx.new_page();q.observe(page,base,report);page.goto(base+'game/?v='+VERSION+'&completed=four-truths#map');map_ready(page)
    page.locator('[data-game-settings]').click();page.wait_for_selector('#game-settings[open]');page.once('dialog',lambda dialog:dialog.accept());page.locator('[data-game-reset]').click();assert 'completed=' not in page.url and q.snapshot(page) is None
    page.locator('[data-game-settings-close]').click();page.wait_for_selector('.story-dialogue[data-scene="arrival-at-wheel"]:not([hidden])');page.reload();map_ready(page);assert not page.locator('.story-dialogue:not([hidden]) [data-city-auto-notice]').count() and q.snapshot(page) is None
    rows.append({'fixture':'reset during final notice, phone','resetClearsCompletedUrlThenReloadCannotShowOldNoticeOrCompletion':True});ctx.close()
    for completed in ['four-truths','five-aggregates']:
        saved=q.fixture([],{'five-aggregates':3},'four-truths');ctx=auto.context(browser,base,saved,outro.ARRIVAL);page=ctx.new_page();q.observe(page,base,report);page.goto(base+'game/?v='+VERSION+'&completed='+completed+'#map');map_ready(page)
        assert not page.locator('.story-dialogue:not([hidden]) [data-city-auto-notice]').count() and q.snapshot(page)==saved and q.snapshot(page)['completed']==[]
        rows.append({'fixture':'unread book URL '+completed+' plus locked future bookmark','cannotForgeCompletionOrNewSceneryNotice':True});ctx.close()
    report['finalNoticeFixtureBranches']=rows


# Title/prologue helpers prepared independently; included for one-key reproducibility.
import json
import time
from pathlib import Path
from urllib.parse import urlparse, parse_qs

TP_VERSION='simple-ui-1'
TP_STORY='sutrazen.play.story.v1'
TP_CITY='sutrazen.play.city.v1'
TP_COPY=[
 '兩千多年前，印度的鹿野苑。\n佛陀向五位比丘說起了苦，也說起了走出苦的路。',
 '相傳，佛陀般涅槃後，弟子們齊聚王舍城，\n一同誦出他的教法。後人稱這場聚會為「第一次結集」。',
 '一代人誦給下一代人聽。\n今天翻開《阿含經》，依然能讀到佛陀與弟子關於離苦的問答。',
]
TP_SEEN=['arrival-at-wheel','doubt-at-ruins','doubt-detour','first-book-insight','doubt-recedes','mara-watches','toward-aggregates-lake']


def tp_context(browser,base,helpers,local=None,**options):
    if local is not None:
        options['storage_state']={'cookies':[],'origins':[{'origin':base.rstrip('/'),'localStorage':[{'name':k,'value':v} for k,v in local.items()]}]}
    return helpers.q.context_for(browser,base,**options)


def tp_raw(page,helpers):
    return page.evaluate('(keys)=>Object.fromEntries(keys.map(k=>[k,localStorage.getItem(k)]))',[helpers.q.KEY,TP_CITY,TP_STORY,'qa.simple-ui.unrelated'])


def tp_profile(helpers):
    saved=helpers.q.fixture(['four-truths'],{'four-truths':28,'five-aggregates':8},'five-aggregates')
    local={helpers.q.KEY:json.dumps(saved),TP_CITY:json.dumps({'version':1,'placedIds':['truth_dock'],'thoughtSeenIds':['city-lord-introduction']}),TP_STORY:json.dumps({'version':1,'seenSceneIds':TP_SEEN}),'qa.simple-ui.unrelated':'keep'}
    return saved,local


def tp_assert_prologue(page):
    page.wait_for_selector('[data-prologue]')
    paragraphs=page.locator('[data-prologue-paragraph]').evaluate_all('(ns)=>ns.map(n=>[...n.querySelectorAll("[data-prologue-line]")].map(s=>s.textContent).join("\\n"))')
    assert paragraphs==TP_COPY,paragraphs
    assert page.locator('[data-prologue-line]').count()==6
    assert page.locator('[data-prologue] button').count()==1
    button=page.locator('[data-prologue-skip]')
    assert button.inner_text()=='點一下進入選單'
    assert page.locator('.prologue-action').count()==0,'Old top skip button is still present'
    box=button.bounding_box();screen=page.viewport_size
    assert box['width']>=48 and box['height']>=48 and box['y']>screen['height']*.6,(box,screen)
    assert page.locator('.game-title-paper').evaluate('(n)=>n.hidden&&n.hasAttribute("inert")&&n.getAttribute("aria-hidden")==="true"')
    assert not page.locator('[data-title-start]').is_visible()
    selected=page.locator('[data-prologue-copy]').evaluate('(n)=>{const s=getSelection();s.selectAllChildren(n);const text=s.toString();s.removeAllRanges();return {text,select:getComputedStyle(n).userSelect}}')
    assert selected['select']=='text' and '第一次結集' in selected['text']
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1&&document.documentElement.scrollHeight<=innerHeight+1')
    return box


def tp_menu_ready(page,helpers):
    page.wait_for_function('!document.querySelector("[data-prologue]")')
    page.wait_for_selector('.game-title-paper:not([hidden])');helpers.q.settle(page)
    paper=page.locator('.game-title-paper').bounding_box();screen=page.viewport_size
    assert abs(paper['x']+paper['width']/2-screen['width']/2)<3,paper
    assert abs(paper['y']+paper['height']/2-screen['height']/2)<3,paper
    assert page.locator('[data-title-brand]').evaluate('(n)=>Boolean(n.closest(".game-title-paper"))')
    assert page.locator('[data-title-heading]').inner_text()=='佛陀的解憂之旅'
    assert page.locator('#game-content').is_hidden()
    assert page.locator('[data-title-start]').evaluate('(n)=>n===document.activeElement')
    return paper


def tp_skip(page,helpers,method='click',guard_probe=True):
    action=page.locator('[data-prologue-skip]')
    if method=='click':action.click()
    elif method=='tap':action.tap()
    else:action.focus();page.keyboard.press(method)
    if guard_probe:
        start=page.locator('[data-title-start]').bounding_box()
        page.mouse.click(start['x']+start['width']/2,start['y']+start['height']/2)
        assert page.locator('#game-content').is_hidden(),'Skip input clicked through to the map'
    tp_menu_ready(page,helpers)
    page.wait_for_timeout(420)
    assert page.locator('#game-content').is_hidden()


def tp_six_size_prologue(browser,base,report,OUT,helpers):
    rows=[]
    for index,(width,height) in enumerate(helpers.SIZES):
        method=['click','Enter','Space'][index%3]
        ctx=tp_context(browser,base,helpers,viewport={'width':width,'height':height},has_touch=True)
        page=ctx.new_page();helpers.q.observe(page,base,report)
        page.goto(base+'game/?v='+TP_VERSION);page.wait_for_selector('#game-title-screen.is-art-loaded')
        button=tp_assert_prologue(page);before=tp_raw(page,helpers)
        assert page.locator('[data-prologue]').get_attribute('data-prologue-mode')=='static'
        page.locator('[data-prologue-viewport]').click(position={'x':10,'y':10})
        assert page.locator('[data-prologue]').is_visible(),'Static copy tap must not skip'
        page.locator('[data-prologue-viewport]').hover();page.mouse.wheel(0,700);helpers.q.settle(page)
        page.screenshot(path=str(Path(OUT)/f'prologue-bottom-cta-{width}x{height}.png'))
        tp_skip(page,helpers,method);assert tp_raw(page,helpers)==before
        page.screenshot(path=str(Path(OUT)/f'title-menu-after-bottom-cta-{width}x{height}.png'))
        rows.append({'viewport':[width,height],'exactThreeParagraphSixLineCopy':True,'onlyBottomCta':button,'reducedMotionStaticManual':True,'nativeSkipMethod':method,'followthroughBlockedAndFocusedStart':True,'readingCityStoryStorageUnchanged':True})
        ctx.close()
    report['titlePrologueSixSizes']=rows


def tp_natural_prologue(browser,base,report,OUT,helpers):
    saved,local=tp_profile(helpers)
    ctx=tp_context(browser,base,helpers,local,viewport={'width':1280,'height':900},reduced_motion='no-preference')
    page=ctx.new_page();helpers.q.observe(page,base,report);page.goto(base+'game/?v='+TP_VERSION)
    tp_assert_prologue(page);before=tp_raw(page,helpers);started=time.monotonic()
    page.wait_for_function('document.querySelector("[data-prologue-copy]")?.getAnimations()?.length>0')
    duration=page.locator('[data-prologue-copy]').evaluate('(n)=>n.getAnimations()[0].effect.getComputedTiming().duration')
    assert 30000<=duration<=45000,duration
    page.evaluate('''()=>{window.qaNaturalEnds=0;let active=true;new MutationObserver(()=>{const now=document.querySelector('#game-title-screen').classList.contains('is-prologue-active');if(active&&!now)window.qaNaturalEnds++;active=now}).observe(document.querySelector('#game-title-screen'),{attributes:true,attributeFilter:['class']})}''')
    page.wait_for_timeout(10000);assert page.locator('[data-prologue]').is_visible();page.screenshot(path=str(Path(OUT)/'natural-prologue-crawl-1280x900.png'))
    page.wait_for_function('!document.querySelector("[data-prologue]")',timeout=48000)
    elapsed=time.monotonic()-started;tp_menu_ready(page,helpers)
    assert elapsed>=duration/1000-1 and elapsed<duration/1000+5,(elapsed,duration)
    assert page.evaluate('window.qaNaturalEnds')==1 and tp_raw(page,helpers)==before
    page.screenshot(path=str(Path(OUT)/'natural-prologue-ended-menu-1280x900.png'))
    page.locator('[data-title-start]').click();helpers.d.map_ready(page)
    assert helpers.q.snapshot(page)==saved
    report['naturalProloguePlayback']={'actualWallSeconds':elapsed,'durationMs':duration,'noSeekingOrFastForward':True,'automaticEndCount':1,'naturalEndPrimaryWorksWithoutSkipDelay':True,'readingCityStoryBytesUnchanged':True}
    ctx.close()


def tp_settings_return_title(browser,base,report,OUT,helpers):
    saved,local=tp_profile(helpers);rows=[]
    routes=[('map','game/?v='+TP_VERSION+'#map'),('city','play/city/?v='+TP_VERSION+'#city'),('shelf','play/visual-v2/shelf.html?v='+TP_VERSION+'#shelf')]
    for origin,url in routes:
        ctx=tp_context(browser,base,helpers,local,viewport={'width':360,'height':800});page=ctx.new_page();helpers.q.observe(page,base,report)
        page.goto(base+url)
        if origin=='map':helpers.d.map_ready(page)
        elif origin=='city':page.wait_for_selector('.mod-city');helpers.q.settle(page)
        else:page.wait_for_selector('[data-book-card]');helpers.q.settle(page)
        before=tp_raw(page,helpers);page.locator('[data-game-settings]').click();page.wait_for_selector('#game-settings[open]')
        title=page.locator('[data-game-title]');assert title.inner_text()=='回到遊戲開始畫面'
        title.click();page.wait_for_url('**/game/**screen=title*');tp_menu_ready(page,helpers)
        params=parse_qs(urlparse(page.url).query);assert params.get('screen')==['title'] and params.get('v')==[TP_VERSION],page.url
        assert not page.locator('[data-prologue]').count() and tp_raw(page,helpers)==before
        page.screenshot(path=str(Path(OUT)/f'settings-{origin}-direct-title-menu-360x800.png'))
        assert page.locator('[data-title-start]').inner_text()=='繼續旅程'
        page.locator('[data-title-start]').click();helpers.d.map_ready(page)
        assert 'screen=' not in page.url and helpers.q.snapshot(page)==saved
        assert not page.locator('.story-dialogue').is_visible()
        if origin=='shelf':
            page.locator('[data-wm-next]').click();page.wait_for_selector('body[data-collection-book="five-aggregates"][data-collection-index="8"]')
            page.reload();page.wait_for_selector('body[data-collection-index="8"]')
            page.locator('.collection-reader-return').click();helpers.d.map_ready(page)
            assert helpers.q.snapshot(page)['positions']['five-aggregates']==8 and helpers.q.snapshot(page)['completed']==['four-truths']
        rows.append({'origin':origin,'settingsNativeTitleLink':True,'directMenuWithoutPrologue':True,'collectionCityStoryRawBytesUnchanged':True,'continueKeepsMainlineFiveBookmark8':True,'nativeReaderReloadAt8':origin=='shelf'})
        ctx.close()
    report['settingsReturnTitlePreservesProgress']=rows


def tp_author_reset_prologue(browser,base,report,OUT,helpers):
    saved,local=tp_profile(helpers);ctx=tp_context(browser,base,helpers,local,viewport={'width':360,'height':800});page=ctx.new_page();helpers.q.observe(page,base,report)
    page.goto(base+'game/?author=1&v='+TP_VERSION+'&screen=title');tp_menu_ready(page,helpers)
    assert page.locator('[data-title-author-reset]').is_visible();before=tp_raw(page,helpers)
    page.once('dialog',lambda dialog:dialog.dismiss());page.locator('[data-title-author-reset]').click();assert tp_raw(page,helpers)==before
    page.once('dialog',lambda dialog:dialog.accept());page.locator('[data-title-author-reset]').click();tp_assert_prologue(page)
    after=tp_raw(page,helpers)
    for key in [helpers.q.KEY,TP_CITY,TP_STORY]:assert after[key] is None,(key,after)
    assert after['qa.simple-ui.unrelated']=='keep'
    page.screenshot(path=str(Path(OUT)/'author-reset-replays-bottom-cta-prologue-360x800.png'))
    tp_skip(page,helpers,'Enter');assert page.locator('[data-title-start]').inner_text()=='開始旅程'
    page.locator('[data-title-start]').click();helpers.d.map_ready(page)
    page.wait_for_selector('.story-dialogue[data-scene="arrival-at-wheel"]:not([hidden])')
    assert helpers.q.snapshot(page) is None
    page.screenshot(path=str(Path(OUT)/'author-reset-fresh-arrival-360x800.png'))
    report['authorResetStillFreshWithNewPrologue']={'fixture':'first complete plus Five bookmark8 and legacy city/thought metadata','nativeCancelLeavesRawBytesIdentical':True,'confirmedClearsOnlyGameCollectionCityStory':True,'unrelatedKeyPreserved':True,'sameExactCopyAndSingleBottomCta':True,'freshArrivalAfterMenuStart':True}
    ctx.close()


def tp_run(browser,base,report,OUT,helpers):
    Path(OUT).mkdir(parents=True,exist_ok=True)
    tp_six_size_prologue(browser,base,report,OUT,helpers)
    tp_natural_prologue(browser,base,report,OUT,helpers)
    tp_settings_return_title(browser,base,report,OUT,helpers)
    tp_author_reset_prologue(browser,base,report,OUT,helpers)


def curate_evidence(report):
    keep={
      'native-first29-final-notice-dialogue-1280x900.png','final-notice-fixture-360x800.png',
      'shelf-14-top-1280x900.png','shelf-14-middle-1280x900.png','shelf-14-bottom-1280x900.png',
      'shelf-0-top-360x800.png','shelf-0-middle-360x800.png','shelf-0-bottom-360x800.png',
      'plaza-short-quote-360x800.png','seven-correspondence-awakening-owl-1280x900.png',
      'city-simple-controls-360x800.png','settings-shelf-direct-title-menu-360x800.png',
      'prologue-bottom-cta-360x800.png','natural-prologue-crawl-1280x900.png','author-reset-fresh-arrival-360x800.png'}
    for name in keep:assert (OUT/name).is_file(),name
    archive=Path('/tmp/game-simple-ui-full-matrix');archive.mkdir(parents=True,exist_ok=True)
    for path in OUT.glob('*.png'):
        if path.name not in keep:shutil.move(str(path),str(archive/path.name))
    report['evidenceFiles']={'representativePngCount':len(keep),'auxiliaryScreenshotsWorkspaceOnly':str(archive),'completeMatrixNumbersRemainInTrackedValidation':True}


def save(report):OUT.mkdir(parents=True,exist_ok=True);(OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')


def main():
    OUT.mkdir(parents=True,exist_ok=True);report=guard_sources();report.update({'phase':'Local simple game UI integration','javascriptErrors':[],'httpErrors':[],'fixtureNotice':'Only nativeFirstCompletionScript walks and explicitly finishes first29. Camera/shelf/source/title histories are synthetic isolated profiles.','physicalSafari':'Not tested; Chromium viewport/mouse/CDP simulation.'})
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(q.Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);native_completion_script(browser,base,report);print('native first29 scripted reward passed',flush=True);final_notice_branches_and_reset(browser,base,report);camera_controls_and_legacy(browser,base,report);shelf_single_background(browser,base,report);concise_city_sources(browser,base,report);extended_and_seven_correspondences(browser,base,report);tp_run(browser,base,report,OUT,helpers=qa);browser.close()
        for command in [['python3','-B','scripts/build-game-entry.py','--check'],['python3','-B','scripts/build-seo.py','--check']]:subprocess.run(command,cwd=ROOT,check=True,capture_output=True,text=True)
        report['generatorAndSeo']='passed';assert not report['javascriptErrors'],report['javascriptErrors'];assert not report['httpErrors'],report['httpErrors'];report['result']='passed';curate_evidence(report)
    except Exception as error:report['result']='failed';report['error']=repr(error);raise
    finally:server.shutdown();save(report)
    print(json.dumps({'result':report['result'],'report':str(OUT/'validation.json')},ensure_ascii=False))


if __name__=='__main__':main()
