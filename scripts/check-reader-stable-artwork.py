#!/usr/bin/env python3
"""Rendered-pixel framing for fourteen originals plus ordered/review adapters.

Native first flips and isolated last-step completion are explicitly distinct
from automated geometry chapter samples. Original manuscripts remain protected.
"""
from pathlib import Path
import functools,hashlib,http.server,importlib.util,io,json,re,subprocess,tempfile,threading,sys,zipfile
from lxml import html
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/previews/reader-stable-artwork'
s=importlib.util.spec_from_file_location('reader_qa_helpers',ROOT/'scripts/check-game-framing.py');helpers=importlib.util.module_from_spec(s);s.loader.exec_module(helpers)
q=helpers.q;BASELINE='3a72b2e33a086714ce30cd80fbebb3ab641d0dc3';VERSION='stable-art-1';SIZES=q.SIZES+[(2048,1115)]
BOOKS=json.loads((OUT/'selection.json').read_text())['books'];MODES=['public','ordered','review']
SHOTS={('four-truths','public',3,1280,900):'four-truths-rain-two-1280x900.png',('four-truths','public',4,1280,900):'four-truths-rain-one-1280x900.png',('four-truths','public',3,844,390):'four-truths-rain-two-844x390.png',('four-truths','public',4,844,390):'four-truths-rain-one-844x390.png',('five-aggregates','public',1,1024,768):'five-aggregates-three-two-1024x768.png',('six-senses','review',19,1024,768):'six-senses-windows-review-1024x768.png',('anapana','public',92,360,800):'anapana-quad-caption-hint-360x800.png',('seven-factors','public',27,1024,768):'seven-factors-fire-mask-1024x768.png',('four-jhanas','public',0,1280,900):'four-jhanas-label-1280x900.png',('four-truths','review',0,1280,900):'four-truths-review-back-shelf-1280x900.png',('four-truths','ordered',0,844,390):'four-truths-ordered-844x390.png',('four-truths','public',23,768,1024):'four-truths-heart-768x1024.png',('eightfold-path','public',110,768,1024):'eightfold-afterword-768x1024.png'}


def normalized_html(text):
    text=re.sub(r'\s*<script\b[^>]*\bsrc=["\']\.\./\.\./reader-layout\.js[^"\']*["\'][^>]*>\s*</script>','',text,flags=re.I)
    return re.sub(r'\?v=[A-Za-z0-9-]+','?v=CACHE',text)


def guard_sources():
    old=lambda p:subprocess.check_output(['git','show',BASELINE+':'+p],cwd=ROOT)
    prefixes=q.ORDER+['docs/'+b for b in q.ORDER]+['index.html','shelf.css','sitemap.xml','robots.txt','googlee0c995331ec518ae.html','reader-controls.css','reader-restart.js','picture-panel-focus.js','picture-panel-focus.css','docs/seo','map-topic-resources.css','scripts/site_seo.py','scripts/build-seo.py','scripts/check-seo.py']
    allowed={b+'/book/index.html' for b in q.ORDER}|{'reader-controls.css','docs/seven-factors/offline-manifest.json'};changes=set(subprocess.check_output(['git','diff','--name-only',BASELINE,'--',*prefixes],cwd=ROOT,text=True).splitlines());assert changes<=allowed,sorted(changes-allowed)
    for name in q.ORDER:
        path=name+'/book/index.html';before=old(path).decode();after=(ROOT/path).read_text();assert normalized_html(after)==normalized_html(before),path
        a,b=html.fromstring(before),html.fromstring(after)
        assert [n.text for n in a.xpath('//script[not(@src)]')]==[n.text for n in b.xpath('//script[not(@src)]')],path
        assert [html.tostring(n) for n in a.xpath('//noscript')]==[html.tostring(n) for n in b.xpath('//noscript')],path
    strict=['play/collection/store.js','play/route','play/story/completion-receipt.js','play/story/store.js','play/city/modules/store.js','play/journey-save.js','play/reader-bridge.js','play/visual-v2/assets','play/worldmap-v4/assets','play/story/assets','play/assets']
    assert not subprocess.check_output(['git','diff','--name-only',BASELINE,'--',*strict],cwd=ROOT,text=True).splitlines()
    bridge=(ROOT/'play/collection/reader-bridge.js').read_text().replace('./catalog.js?v=stable-art-1','./catalog.js').replace('../../game/?v=stable-art-1','../../game/?v=simple-ui-1').replace('./reader.css?v=stable-art-1','./reader.css');assert bridge==old('play/collection/reader-bridge.js').decode()
    catalog=(ROOT/'play/collection/catalog.js').read_text().replace("returnShelf: '回到書架'","returnShelf: '回收集書架'");assert catalog==old('play/collection/catalog.js').decode()
    count=len([p for p in subprocess.check_output(['git','ls-tree','-rz','--name-only',BASELINE,'--',*prefixes],cwd=ROOT,text=True).split('\0') if p])
    return {'baseline':BASELINE,'auditedOriginalFiles':count,'originalManuscriptsQuotesImagesBookRenderersInlineAndNoscript':'byte-for-byte preserved','authorizedOriginalExceptions':'Fourteen HTML reader-layout loader/cache queries and shared reader-controls framing CSS','collectionBridgeException':'catalog/reader CSS/return cache queries only; all policy/completion/save bytes unchanged','catalogException':'returnShelf label only; IDs/arrays/data unchanged','readingEligibilityReceiptStorageAndSiteSeoGoogle':'unchanged','totalOriginalReadingSteps':sum(v['steps'] for v in BOOKS.values())}


def context(browser,base,book,mode,size):
    options={'viewport':{'width':size[0],'height':size[1]},'has_touch':True,'reduced_motion':'reduce'}
    if mode!='public':
        i=q.ORDER.index(book);saved=q.fixture(q.ORDER[:i] if mode=='ordered' else q.ORDER,{book:0},book)
        options['storage_state']={'cookies':[],'origins':[{'origin':base.rstrip('/'),'localStorage':[{'name':q.KEY,'value':json.dumps(saved)}]}]}
    return browser.new_context(**options)


def uri(base,book,mode,index=0):
    value=base+book+'/book/'
    if mode!='public':value+='?collection=1&collectionReturn=game&collectionPage='+str(index)+'&collectionStory='+VERSION+('&collectionReview=1' if mode=='review' else '')
    return value


def settle(page):
    page.wait_for_function('typeof showPage==="function"&&document.body.classList.contains("reader-unified-controls")')
    page.evaluate('''async()=>{await document.fonts.ready;const a=document.querySelector('#art');if(a&&!document.querySelector('#art-frame').hidden&&a.src)await a.decode();for(let i=0;i<4;i++)await new Promise(requestAnimationFrame)}''')


def step_index(page):return int(re.match(r'\s*(\d+)\s*/',page.locator('#position-text').inner_text()).group(1))-1


def show_row(page,row):
    page.evaluate('(r)=>r.cueArg===null?showPage(r.pageArg):showPage(r.pageArg,r.cueArg)',row);settle(page);assert step_index(page)==row['index'],(row,step_index(page))


GEOMETRY=r'''()=>{
 const $=s=>document.querySelector(s),vis=n=>n&&!n.hidden&&n.checkVisibility()&&n.getBoundingClientRect().width>0,r=n=>n?.getBoundingClientRect().toJSON()||null;
 const page=$('.page'),scene=$('.scene'),frame=$('#art-frame'),art=$('#art'),a=r(art),scale=art.naturalWidth?Math.min(a.width/art.naturalWidth,a.height/art.naturalHeight):0;
 const paint=vis(frame)&&vis(art)?{x:a.x+(a.width-art.naturalWidth*scale)/2,y:a.y+(a.height-art.naturalHeight*scale)/2,width:art.naturalWidth*scale,height:art.naturalHeight*scale}:null;
 function textRects(selector){const root=$(selector);if(!vis(root))return [];const result=[],walk=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);let n;while(n=walk.nextNode()){
  const e=n.parentElement;if(!n.textContent.trim()||e.closest('[aria-hidden="true"],.caption-sizer,#caption-sizer,[hidden]')||getComputedStyle(e).visibility!=='visible')continue;
  const range=document.createRange();range.selectNodeContents(n);for(const raw of range.getClientRects()){let b={x:raw.x,y:raw.y,right:raw.right,bottom:raw.bottom};for(let p=e;p;p=p.parentElement){const st=getComputedStyle(p),pr=p.getBoundingClientRect();if(/hidden|clip|auto|scroll/.test(st.overflowX)){b.x=Math.max(b.x,pr.x);b.right=Math.min(b.right,pr.right)}if(/hidden|clip|auto|scroll/.test(st.overflowY)){b.y=Math.max(b.y,pr.y);b.bottom=Math.min(b.bottom,pr.bottom)}}b.x=Math.max(0,b.x);b.y=Math.max(0,b.y);b.right=Math.min(innerWidth,b.right);b.bottom=Math.min(innerHeight,b.bottom);if(b.right-b.x>.5&&b.bottom-b.y>.5)result.push({...b,width:b.right-b.x,height:b.bottom-b.y})}}
 return result}
 const visibleCaption=vis($('#caption'))?'#caption':'#reader-summary-caption',cap=textRects(visibleCaption),verse=textRects('#verse'),controls={};for(const selector of ['.top > a','.position','#open-verse','.reading-links a:first-child','.reading-links a:last-child']){const n=$(selector);if(vis(n)){const b=r(n);if(b.bottom>0&&b.y<innerHeight)controls[selector]=b}}
 const css=getComputedStyle(scene),masks=[...document.querySelectorAll('.picture-panel-focus,#panel-mask')].filter(vis).map(n=>({box:r(n),active:n.querySelectorAll('.active').length}));
 return {paint,frame:vis(frame)?r(frame):null,artLayer:vis($('#art-layer'))?r($('#art-layer')):null,natural:[art.naturalWidth,art.naturalHeight],fit:getComputedStyle(art).objectFit,classes:page.className,kind:page.dataset.readerArtKind,scene:r(scene),caption:vis($(visibleCaption))?r($(visibleCaption)):null,scripture:vis($('.scripture'))?r($('.scripture')):null,captionRects:cap,verseRects:verse,captionLines:new Set(cap.map(b=>b.y.toFixed(1))).size,verseLines:new Set(verse.map(b=>b.y.toFixed(1))).size,controls,masks,overlays:[...document.querySelectorAll('.art-overlay,.window-label,#overlay-labels > *')].filter(vis).map(n=>({box:r(n),text:n.textContent.slice(0,60)})),target:parseFloat(css.getPropertyValue('--reader-target-art-height'))||null,artHeight:parseFloat(css.getPropertyValue('--reader-art-height'))||null,outside:$('#outside-labels')?{insideCaption:Boolean($('#outside-labels').closest('#caption')),text:$('#outside-labels').textContent.slice(0,120)}:null,overflowX:document.documentElement.scrollWidth>innerWidth+1,scrollY,screen:[innerWidth,innerHeight]}
}'''


def overlap(a,b):return min(a['x']+a['width'],b['x']+b['width'])-max(a['x'],b['x'])>.8 and min(a['y']+a['height'],b['y']+b['height'])-max(a['y'],b['y'])>.8


def measure(page,book,row,mode,size):
    g=page.evaluate(GEOMETRY);assert not g['overflowX'],(book,mode,row['index'],g)
    if g['paint'] and 'reader-stable-artwork' in g['classes']:
        p,f=g['paint'],g['frame'];assert g['fit']=='contain',g
        if g['kind']=='wide-document':
            assert abs(f['height']-g['artHeight'])<1 and p['x']>=f['x']-.8 and p['y']>=f['y']-.8 and p['x']+p['width']<=f['right']+.8 and p['y']+p['height']<=f['bottom']+.8,g
            assert not g['masks'] and not g['overlays'],('wide-document must have no image-relative teaching overlays',g)
        else:
            for key in ['x','y','width','height']:assert abs(p[key]-f[key])<1,(book,row['index'],'frame not actual painted box',g)
            assert abs(p['height']-g['artHeight'])<1,g
        assert abs(p['width']/p['height']-g['natural'][0]/g['natural'][1])<.002,g
        if g['artLayer']:
            for key in ['x','y','width','height']:assert abs(g['artLayer'][key]-p[key])<1,(book,'art-layer drift',g)
        for mask in g['masks']:
            for key in ['x','y','width','height']:assert abs(mask['box'][key]-p[key])<1,(book,'mask drift',g)
            assert mask['active']==1,(book,'mask active count',mask)
        if size[0]>size[1]:
            if g['caption']:assert p['y']>=g['caption']['bottom']-.8,g
            if g['scripture']:assert p['y']+p['height']<=g['scripture']['y']+.8,g
        if g['outside'] and g['outside']['text'].strip():assert g['outside']['insideCaption'],(book,'outside hint not in caption',g)
        for textkind in (['captionRects','verseRects'] if size[0]>size[1] else ['captionRects']):
            for rect in g[textkind]:
                for key,control in g['controls'].items():assert not overlap(rect,control),(book,mode,row['index'],textkind,key,g)
    assert page.locator('.reading-links a').all_inner_texts()==['閱讀原經','回修道地圖']
    assert page.locator('.reading-links a').last.get_attribute('href')=='../../index.html'
    if mode=='review':assert page.locator('.collection-reader-return').inner_text()=='回到書架'
    return g


def selected_rows(book,special=False):
    info=BOOKS[book];ids=set(range(min(5,info['steps'])))
    for key in ['sameImageCaptionPair','sameImageVersePair','oneTwoCaptionParagraphSameImage']:
        for row in info.get(key,[]) or []:ids.add(row['index'])
    normals=[r for r in info['allRows'] if r['image'] and not any(k in r['special'] for k in ['document','heart','afterword','textSummary']) and r['dimensions'][0]/r['dimensions'][1]<1.9]
    ids.add(max(normals,key=lambda r:r['verseChars'])['index']);ids.add(normals[-1]['index'])
    for key in ['overlay','focusPanel','mask']:
        if info['specialIndices'].get(key):ids.add(info['specialIndices'][key][0])
    if book=='five-aggregates':ids.update([3,4,5])
    if book=='six-senses':ids.update([19,20])
    if book=='anapana':ids.update([92,94])
    if book=='seven-factors':ids.add(27)
    if special:
        for indices in info['specialIndices'].values():
            if indices:ids.add(indices[0]);ids.add(indices[-1])
    else:ids={i for i in ids if not any(k in info['allRows'][i]['special'] for k in ['document','heart','afterword','textSummary','no-image'])}
    return [info['allRows'][i] for i in sorted(ids)]


def screenshot(page,book,mode,row,size,native=False):
    name=SHOTS.get((book,mode,row['index'],*size))
    if not name:return
    if row['index']<5 and not native and (OUT/name).exists():return
    page.screenshot(path=str(OUT/name))


def scroll_long_text(page,book,row,size):
    if size[0]<=size[1]:
        before=step_index(page);page.mouse.move(2,size[1]*.5);page.mouse.wheel(0,100000);page.wait_for_timeout(60)
        local=[]
        for selector in ['#caption','#reader-summary-caption','.verse-body']:
            element=page.locator(selector)
            if not element.is_visible():continue
            info=element.evaluate('(n)=>({height:n.clientHeight,scroll:n.scrollHeight,overflow:getComputedStyle(n).overflowY})')
            if info['scroll']>info['height']+2 and info['overflow'] in ['auto','scroll']:
                box=element.bounding_box();top=max(0,box['y']);bottom=min(size[1],box['y']+box['height']);assert bottom>top,(book,row['index'],'portrait local text not in scrollable viewport',box)
                page.mouse.move(box['x']+box['width']/2,(top+bottom)/2);page.mouse.wheel(0,100000);page.wait_for_timeout(80);assert element.evaluate('(n)=>n.scrollTop')>0,(book,row['index'],'portrait local text did not scroll',selector)
                local.append({'region':selector,**info,'nativeWheelToEnd':True})
        data=page.evaluate("""()=>{const n=document.querySelector('#verse'),walk=document.createTreeWalker(n,NodeFilter.SHOW_TEXT);let last,node;while(node=walk.nextNode())if(node.textContent.trim())last=node;const range=document.createRange();if(last){range.setStart(last,Math.max(0,last.length-1));range.setEnd(last,last.length)}const position=document.querySelector('.position').getBoundingClientRect();return {scrollY,documentHeight:document.documentElement.scrollHeight,lastCharacter:last?range.getBoundingClientRect().toJSON():null,links:document.querySelector('.reading-links').getBoundingClientRect().toJSON(),safeBottom:position.top}}""")
        if data['lastCharacter']:assert data['lastCharacter']['bottom']<=data['safeBottom']+1,(book,row['index'],'portrait last text inaccessible',data)
        assert data['links']['bottom']<=data['safeBottom']+1 and data['links']['top']>=0,(book,row['index'],'portrait reading links inaccessible',data)
        assert step_index(page)==before
        page.locator('.verse-body').evaluate('(n)=>n.scrollTop=0');page.evaluate('window.scrollTo(0,0)');return {'portraitNaturalFlow':True,'nativeWheelToEndPreservesStep':True,'localScrollRegions':local,**data}
    values=[]
    for selector in ['#caption','#reader-summary-caption','.verse-body']:
        element=page.locator(selector)
        if not element.is_visible():continue
        data=element.evaluate('(n)=>({height:n.clientHeight,scroll:n.scrollHeight,overflow:getComputedStyle(n).overflowY})')
        if data['scroll']>data['height']+2:
            assert data['overflow'] in ['auto','scroll'],(book,row['index'],selector,data)
            element.evaluate('(n)=>n.scrollTop=n.scrollHeight');assert element.evaluate('(n)=>n.scrollTop')>0
            element.evaluate('(n)=>n.scrollTop=0');box=element.bounding_box()
            if box['height']>8:
                before=step_index(page);page.mouse.move(box['x']+box['width']*.5,box['y']+box['height']*.5);page.mouse.wheel(0,200);page.wait_for_timeout(60);assert element.evaluate('(n)=>n.scrollTop')>0 and step_index(page)==before
            element.evaluate('(n)=>n.scrollTop=0');values.append({'region':selector,**data,'nativeWheelStaysOnReadingStep':True})
    return values


def matrix(browser,base,report,special=False):
    # Reuse one reader per book/mode, then resize its actual DOM. Avoid reloading
    # the originals' large embedded art for every dimension.
    records=report.setdefault('ordinaryMatrix',[]);existing={(tuple(r['viewport']),r['mode'],r['book']) for r in records}
    for mode in MODES:
        for book in q.ORDER:
            ctx=context(browser,base,book,mode,SIZES[0]);page=ctx.new_page();q.observe(page,base,report);page.goto(uri(base,book,mode));settle(page)
            if mode!='public':page.wait_for_selector('body[data-collection-book="'+book+'"]')
            native_done=any(r['book']==book and r['mode']==mode and r.get('nativeFirstNextTrace')==[0,1,2,3,4] for r in records)
            for size in SIZES:
                if (tuple(size),mode,book) in existing:continue
                page.set_viewport_size({'width':size[0],'height':size[1]});settle(page)
                trace=[]
                if not native_done:
                    show_row(page,BOOKS[book]['allRows'][0]);trace=[0];screenshot(page,book,mode,BOOKS[book]['allRows'][0],size,native=True)
                    for index in [1,2,3,4]:
                        page.locator('#next').click();page.wait_for_function('n=>Number(document.querySelector("#position-text").textContent.match(/\\d+/)[0])===n+1',arg=index);settle(page);trace.append(index);screenshot(page,book,mode,BOOKS[book]['allRows'][index],size,native=True)
                    native_done=True
                assert page.locator('#next').evaluate('(n)=>getComputedStyle(n).touchAction')=='manipulation'
                heights={};samples=selected_rows(book,special);metrics=[]
                for row in samples:
                    show_row(page,row);g=measure(page,book,row,mode,size);screenshot(page,book,mode,row,size)
                    if g['paint'] and 'reader-stable-artwork' in g['classes']:
                        identity=row['image'];heights.setdefault(identity,[]).append((row['index'],g['paint']['height'],g['paint']['y']))
                    metrics.append({'index':row['index'],'paintedHeight':g['paint']['height'] if g['paint'] else None,'target':g['target'],'captionVisibleLines':g['captionLines'],'verseVisibleLines':g['verseLines'],'overlayCount':len(g['overlays']),'maskCount':len(g['masks'])})
                for image,values in heights.items():assert max(v[1] for v in values)-min(v[1] for v in values)<1,(book,mode,size,image,values)
                if book=='four-truths':
                    rain=next(v for v in heights.values() if {3,4}<={x[0] for x in v});rain=[x for x in rain if x[0] in [3,4]]
                    if size[0]>size[1] or max(m['captionVisibleLines'] for m in metrics if m['index'] in [3,4])<=2:assert max(v[2] for v in rain)-min(v[2] for v in rain)<1,('rain1/2caption artY',mode,size,rain)
                longrow=max(samples,key=lambda r:r['verseChars']);show_row(page,longrow);scroll=scroll_long_text(page,book,longrow,size)
                if page.locator('#open-verse').is_visible():
                    page.locator('#open-verse').click();page.wait_for_selector('#verse-dialog[open]');assert page.locator('#dialog-verse').inner_text().strip();page.locator('#verse-dialog form button').click()
                if mode=='public':assert q.snapshot(page) is None
                else:assert len(q.snapshot(page)['completed'])==(q.ORDER.index(book) if mode=='ordered' else 14)
                report['geometryStates']=report.get('geometryStates',0)+len(samples)
                records.append({'viewport':list(size),'book':book,'mode':mode,'nativeFirstNextTrace':trace,'nativeFirstTraceRecordedAt1280':not bool(trace),'geometryProbeIndices':[r['index'] for r in samples],'samples':metrics,'sameImageHeights':heights,'longTextScroll':scroll,'noCompletionFromProbes':True})
            ctx.close();print('ordinary',mode,book,'all6 viewports passed',flush=True);save(report)


def special_matrix(browser,base,report):
    """Native image→heart/ending transitions plus all special text samples.

    Later showPage calls are geometry probes only, never completion evidence.
    Reuses each original book/mode DOM through all six rotations/resizes.
    """
    records=report.setdefault('specialMatrix',[])
    for mode in MODES:
        for book in q.ORDER:
            ctx=context(browser,base,book,mode,SIZES[0]);page=ctx.new_page();q.observe(page,base,report);page.goto(uri(base,book,mode));settle(page)
            for size in SIZES:
                page.set_viewport_size({'width':size[0],'height':size[1]});settle(page)
                info=BOOKS[book];ids={info['steps']-1}
                for key in ['no-image','heart','document-scene','afterword','textSummary','summary']:
                    values=info['specialIndices'].get(key,[])
                    if values:ids.update([values[0],values[-1]])
                heart_metrics=None;heart_indices=info['specialIndices'].get('heart',[])
                if heart_indices:
                    index=heart_indices[0];previous=info['allRows'][index-1];show_row(page,previous);before=measure(page,book,previous,mode,size)
                    page.locator('#next').click();settle(page);assert step_index(page)==index
                    after=page.evaluate(GEOMETRY);assert 'reader-framed-heart' in after['classes']
                    assert abs(after['scripture']['height']-before['frame']['height'])<1,(book,mode,size,'heart-frame height jump',before,after)
                    assert abs(after['scripture']['width']-before['frame']['width'])<1,(book,mode,size,'heart-frame width jump',before,after)
                    if before['caption'] and after['caption']:assert abs(after['caption']['y']-before['caption']['y'])<1,(book,mode,size,'heart caption y jump',before,after)
                    heart_metrics={'nativeTransition':[index-1,index],'imageFrame':before['frame'],'heartFrame':after['scripture'],'captionTopBeforeAfter':[before['caption']['y'] if before['caption'] else None,after['caption']['y'] if after['caption'] else None]}
                samples=[]
                for index in sorted(ids):
                    row=info['allRows'][index];show_row(page,row);g=measure(page,book,row,mode,size);screenshot(page,book,mode,row,size)
                    for selector in ['#art-summary','#summary-text']:
                        text=page.locator(selector)
                        if text.count() and text.evaluate('(n)=>!n.hidden&&Boolean(n.textContent.trim())'):assert text.is_visible(),(book,index,size,'original summary copy in hidden parent',selector)
                    if 'reader-framed-heart' in g['classes']:
                        assert abs(g['scripture']['height']-g['artHeight'])<1,g
                        content=page.locator('#verse').inner_text();assert len(content)>300 and page.locator('#verse strong').count()>=1,(book,index,'heart missing original quote/highlight')
                        detail=page.locator('.verse-body').evaluate('(n)=>({client:n.clientWidth,scroll:n.scrollWidth,height:n.clientHeight,textMode:getComputedStyle(document.querySelector("#verse")).writingMode,overflow:getComputedStyle(n).overflowX})')
                        assert detail['textMode']=='vertical-rl' and detail['overflow']=='auto',(book,index,detail)
                        if detail['scroll']>detail['client']+2:
                            before_index=step_index(page);box=page.locator('.verse-body').bounding_box();page.mouse.move(box['x']+box['width']/2,box['y']+box['height']/2);page.mouse.wheel(-300,0);page.wait_for_timeout(80)
                            assert abs(page.locator('.verse-body').evaluate('(n)=>n.scrollLeft'))>0 and step_index(page)==before_index,(book,index,'native heart horizontal scroll failed')
                            page.locator('.verse-body').evaluate('(n)=>n.scrollLeft=0')
                        # Both visible native grid variants retain the original speech text.
                        for rect in g['captionRects']:
                            for key,control in g['controls'].items():assert not overlap(rect,control),(book,index,'heart caption/control overlap',key,g)
                    elif 'reader-framed-ending' in g['classes']:
                        detail=ending_scroll(page,book,index,size)
                    else:
                        assert g['paint'],(book,index,'special unexpectedly empty',g);detail={'illustratedSummaryOrWideDocument':True,'frame':g['frame'],'paint':g['paint']}
                    samples.append({'index':index,'classes':g['classes'],'detail':detail,'captionTop':g['caption']['y'] if g['caption'] else None})
                if mode!='public':assert len(q.snapshot(page)['completed'])==(q.ORDER.index(book) if mode=='ordered' else 14)
                else:assert q.snapshot(page) is None
                records.append({'viewport':list(size),'book':book,'mode':mode,'nativeHeartTransition':heart_metrics,'specialSamples':samples,'noCompletionFromGeometry':True})
            ctx.close();print('special',mode,book,len(SIZES),'sizes passed',flush=True)


def ending_scroll(page,book,index,size):
    scene=page.locator('.scene');before=step_index(page)
    data=scene.evaluate("""n=>{const t=document.createTreeWalker(n,NodeFilter.SHOW_TEXT);let total=0,last,node;while(node=t.nextNode()){if(node.textContent.trim()&&!node.parentElement.closest('[hidden],[aria-hidden="true"],#page-title,#caption-sizer,.caption-sizer')&&node.parentElement.checkVisibility()){total+=node.textContent.trim().length;last=node}}const styles=getComputedStyle(n);return {textCharacters:total,client:n.clientHeight,scroll:n.scrollHeight,overflow:styles.overflowY,top:n.getBoundingClientRect().top,paddingTop:styles.paddingTop}}""")
    assert data['textCharacters']>20,(book,index,'ending text missing',data)
    if size[0]>size[1]:
        assert data['overflow']=='auto' and float(data['paddingTop'][:-2])==8,(book,index,data)
        scene.evaluate('(n)=>n.scrollTop=n.scrollHeight')
    else:
        page.mouse.move(size[0]*.85,size[1]*.6);page.mouse.wheel(0,100000);page.wait_for_timeout(60)
    end=scene.evaluate("""n=>{const t=document.createTreeWalker(n,NodeFilter.SHOW_TEXT);let last,node;while(node=t.nextNode())if(node.textContent.trim()&&!node.parentElement.closest('[hidden],[aria-hidden="true"],#page-title,#caption-sizer,.caption-sizer')&&node.parentElement.checkVisibility())last=node;const r=document.createRange();r.setStart(last,last.length-1);r.setEnd(last,last.length);return {last:r.getBoundingClientRect().toJSON(),windowHeight:innerHeight,sceneScroll:n.scrollTop,controls:[...document.querySelectorAll('.controls button,.position,.reading-links,#open-verse')].filter(e=>e.checkVisibility()).map(e=>e.getBoundingClientRect().toJSON())}}""")
    assert 0<=end['last']['top']<size[1] and end['last']['bottom']<=size[1]+1,(book,index,'last ending text cannot scroll into screen',data,end)
    for control in end['controls']:assert not overlap(end['last'],control),(book,index,'ending final text obstructed',data,end)
    assert step_index(page)==before
    scene.evaluate('(n)=>n.scrollTop=0');page.evaluate('window.scrollTo(0,0)');return {**data,'endOfOriginalTextReachable':True,'readingStepUnchanged':True}


def ratio_calibration(browser,base,report):
    results=[]
    for size in SIZES:
        ctx=browser.new_context(viewport={'width':size[0],'height':size[1]});page=ctx.new_page();q.observe(page,base,report);page.goto(uri(base,'four-truths','public'));settle(page);row=BOOKS['four-truths']['allRows'][0];normal=measure(page,'four-truths',row,'public',size)
        page.route('**/reader-calibration-four-three.svg',lambda route:route.fulfill(content_type='image/svg+xml',body='<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300"><rect width="400" height="300" fill="#b7d8df"/></svg>'))
        page.evaluate('document.querySelector("#art").src="reader-calibration-four-three.svg"');settle(page);cal=measure(page,'four-truths',row,'public',size);assert abs(normal['paint']['height']-cal['paint']['height'])<1,(size,normal,cal)
        results.append({'viewport':list(size),'fixture':'Isolated 4:3 SVG ruler only; no deployed illustration changed','real16to9Height':normal['paint']['height'],'test4to3Height':cal['paint']['height'],'naturalRatio':[400,300]});ctx.close()
    report['fourThreeCalibrationOnly']=results


def game_resume_and_last_step(browser,base,report):
    saved=q.fixture([],{'four-truths':2},'four-truths');ctx=q.context_for(browser,base,saved=saved,viewport={'width':844,'height':390});page=ctx.new_page();q.observe(page,base,report);page.goto(uri(base,'four-truths','ordered',2));settle(page);page.locator('#next').click();page.wait_for_selector('body[data-collection-index="3"]');page.reload();settle(page);assert step_index(page)==3
    page.locator('.collection-reader-return').click();d=helpers.d;d.map_ready(page);page.locator('[data-wm-next]').click();page.wait_for_selector('body[data-collection-index="3"]');assert q.snapshot(page)['completed']==[];ctx.close()
    saved=q.fixture(['four-truths'],{'four-truths':28,'five-aggregates':8},'five-aggregates');ctx=q.context_for(browser,base,saved=saved,viewport={'width':360,'height':800});page=ctx.new_page();q.observe(page,base,report);page.goto(uri(base,'four-truths','review',0));settle(page);assert page.locator('.collection-reader-return').inner_text()=='回到書架'
    for index in [1,2,3]:page.locator('#next').click();page.wait_for_selector('body[data-collection-index="'+str(index)+'"]')
    page.reload();settle(page);assert step_index(page)==3;page.locator('.collection-reader-return').click();page.wait_for_selector('#collection-books');assert q.snapshot(page)['completed']==['four-truths'] and q.snapshot(page)['positions']['five-aggregates']==8;ctx.close()
    saved=q.fixture([],{'four-truths':28},'four-truths');ctx=q.context_for(browser,base,saved=saved);page=ctx.new_page();q.observe(page,base,report);page.goto(uri(base,'four-truths','ordered',28));settle(page);assert q.snapshot(page)['completed']==[] and page.locator('#next').inner_text()=='完成這本';page.locator('#next').click();helpers.d.map_ready(page);assert q.snapshot(page)['completed']==['four-truths'];ctx.close()
    report['gameIntegration']={'nativeOrderedNextReloadReturnResumeIndex':3,'nativeReview0to3ReloadBackToShelfNewLabel':True,'reviewKeepsMainlineFive8AndCompleted1':True,'isolatedLastStepFixtureExplicitFinishRecordsOnce':True,'lastStepFixtureNotClaimedAsNewFull29Read':True}


def offline_archive(browser,report):
    relative='downloads/SutraZen-Seven-Factors-Offline.zip';old_bytes=subprocess.check_output(['git','show',BASELINE+':'+relative],cwd=ROOT)
    with zipfile.ZipFile(io.BytesIO(old_bytes)) as old,zipfile.ZipFile(ROOT/relative) as current:
        assert current.testzip() is None
        assert set(current.namelist())-set(old.namelist())=={'reader-layout.js'}
        for name in ['reader-layout.js','reader-controls.css']:assert current.read(name)==(ROOT/name).read_bytes()
        content=[n for n in old.namelist() if n.endswith(('.webp','.png','.jpeg','.jpg','book-data.js','book.js'))]
        assert all(old.read(n)==current.read(n) for n in content)
        assert html.tostring(html.fromstring(old.read('seven-factors/index.html')).find('body'))==html.tostring(html.fromstring(current.read('seven-factors/index.html')).find('body'))
        static={'archiveBytes':(ROOT/relative).stat().st_size,'members':len(current.namelist()),'CRC':'passed','added':['reader-layout.js'],'sharedLayoutAndCssEqualCurrentRepository':True,'allOriginalImagesNarrationQuotesAndBookJsEqualOldArchive':True,'offlineGuideBodyEqualOldArchiveSeoHeadSyncedFromExistingSite':True}
        with tempfile.TemporaryDirectory(prefix='reader-stable-offline-') as folder:
            current.extractall(folder)
            server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(q.Quiet,directory=folder));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
            try:
                ctx=browser.new_context(viewport={'width':844,'height':390});page=ctx.new_page();q.observe(page,base,report)
                page.route('**/*',lambda route:route.continue_() if route.request.url.startswith(base) else route.abort())
                page.goto(base+'seven-factors/book/');settle(page);trace=[step_index(page)]
                for index in [1,2,3]:page.locator('#next').click();settle(page);assert step_index(page)==index;trace.append(index)
                show_row(page,BOOKS['seven-factors']['allRows'][30]);ending_trace=[step_index(page)]
                for index in range(31,37):page.locator('#next').click();settle(page);assert step_index(page)==index;ending_trace.append(index)
                assert 'reader-framed-ending' in page.locator('.page').get_attribute('class');assert q.snapshot(page) is None
                static.update({'network':'All requests outside extracted localhost archive aborted','nativeBeginningTrace':trace,'nativeSummaryToEndingTrace':ending_trace,'notClaimedFull37OfflineRead':True});ctx.close()
            finally:server.shutdown()
    report['rebuiltSevenFactorsOffline']=static



def save(report):OUT.mkdir(parents=True,exist_ok=True);(OUT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')


def main():
    OUT.mkdir(parents=True,exist_ok=True);report=guard_sources();report.update({'phase':'Local rendered artwork stabilization','javascriptErrors':[],'httpErrors':[],'physicalSafari':'Not tested; Chromium viewport/input simulation','geometryProbeNotice':'Every reader first0-4 is native Next; later indices are geometry probes, not claims of completing1192 steps. Game histories are isolated fixtures.'})
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(q.Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);matrix(browser,base,report);special_matrix(browser,base,report);ratio_calibration(browser,base,report);game_resume_and_last_step(browser,base,report);offline_archive(browser,report);browser.close()
        assert not report['javascriptErrors'],report['javascriptErrors'];assert not report['httpErrors'],report['httpErrors'];report['result']='passed'
    except Exception as error:report['result']='failed';report['error']=repr(error);raise
    finally:server.shutdown();save(report)
    print(json.dumps({'result':report['result'],'report':str(OUT/'validation.json')},ensure_ascii=False))


if __name__=='__main__':main()
