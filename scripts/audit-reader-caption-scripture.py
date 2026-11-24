#!/usr/bin/env python3
"""Inventory actual native page turns and compare narration/scripture to data.

This verifies rendering and attribution links, not Buddhist interpretation.
The companion editorial audit separately checks the cited source texts.
"""
from pathlib import Path
import argparse, functools, hashlib, http.server, json, re, subprocess, threading
from urllib.parse import urlparse, unquote
from lxml import html
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/audits/reader-caption-scripture'
ORDER = ['four-truths','five-aggregates','six-senses','twelve-links',
         'eightfold-path','four-fruits-ten-fetters','four-purities-six-recollections',
         'mindfulness','right-effort','anapana','iddhipada','four-jhanas',
         'five-roots-powers','seven-factors']

EXTRACT = r'''book=>{
 const $=s=>document.querySelector(s),raw=pages[current];
 const item=typeof currentItem==='function'?currentItem():raw;
 const scene=Number.isInteger(raw.sceneIndex)?scenes[raw.sceneIndex]:null;
 const norm=s=>(s||'').replace(/\s+/g,'');
 function clean(n){if(!n)return '';const c=n.cloneNode(true);c.querySelectorAll('[aria-hidden="true"],.caption-sizer,#caption-sizer,[hidden]').forEach(x=>x.remove());return c.textContent.trim()}
 const narration=$('#narration')||$('#caption');
 const expectedCaption=(item.lines||[]).join('\n');
 const cards=typeof renderScripture==='function';
 let expectedVerse='',expectedDialog='',source='';
 if(scene){expectedVerse=typeof scene.heart==='string'?scene.heart:(book==='four-truths'?scene.verse:raw.verse);source=book==='four-truths'?scene.source:raw.source;}
 else if(book==='twelve-links'){expectedVerse=(item.number?'《雜阿含經》第'+item.number+'經\n':'')+(item.verse||'');source=item.number?'../#sa'+item.number:item.heart?'https://cbetaonline.dila.edu.tw/zh/T0251':'';}
 else if(Array.isArray(item.quotes)){
   const quoteBody=q=>q.originalText?(q.sourceType==='pali_with_editorial_chinese_paraphrase'?(q.translationNote||'')+'巴利原文'+q.originalText:q.originalText+(q.translationNote||'')):(q.text||'');
   const relation=q=>book==='mindfulness'&&q.relation!=='原片下方引文對應'?q.relation+' · ':book==='right-effort'&&q.relation!=='原片下方引文'?q.relation+' · ':'';
   expectedVerse=(cards?item.context||'':'')+item.quotes.map(q=>relation(q)+q.source+quoteBody(q)).join('\n')+(cards&&item.sourceNote?'補充說明：'+item.sourceNote:'');
   expectedDialog=item.quotes.map(q=>{
     const prefix=(book==='anapana'&&q.relation!=='影片下緣引文'?q.relation+' · ':relation(q))+q.source;
     if(q.originalText)return prefix+(q.sourceType==='pali_with_editorial_chinese_paraphrase'?(q.translationNote||'')+'巴利原文：'+q.originalText:q.originalText+(q.translationNote||''));
     return prefix+(q.text||'');
   }).join('\n');
   source=item.quotes.length?'../'+(['mindfulness','right-effort'].includes(book)?'':'index.html')+'#'+item.quotes[0].quoteId:'';
 }else{expectedVerse=book==='four-purities-six-recollections'?[item.verseLabel,item.verse].filter(Boolean).join('\n'):item.verse?(item.verseLabel||'')+'\n'+item.verse:'';source=item.source||'';}
 if(!Array.isArray(item.quotes))expectedDialog=expectedVerse;
 const actualCaption=clean(narration),actualVerse=$('#verse').textContent;
 const link=$('#source-link'),open=$('#open-verse'),fraction=$('#position-text').textContent.match(/(\d+)\s*\/\s*(\d+)/);
 return {page:Number(fraction[1]),total:Number(fraction[2]),scene:item.scene??raw.sceneIndex??null,cue:item.id??item.paragraphId??null,title:$('#page-title').textContent,
   caption:actualCaption,captionDisplayed:!$('#caption').hidden,narrationMatches:norm(actualCaption)===norm(expectedCaption),expectedCaption,
   scripture:actualVerse,scriptureDisplayed:!$('.scripture').hidden,scriptureMatches:norm(actualVerse)===norm(expectedVerse),expectedVerse,
   sourceHref:link.getAttribute('href'),sourceHidden:link.hidden,expectedSource:source,sourceMatches:link.hidden||!source||new URL(source,location.href).href===link.href,
   openDialog:!open.hidden,expectedDialog,quotes:item.quotes||[],context:item.context||'',sourceNote:item.sourceNote||'',
   summary:clean($('#summary-text'))||clean($('#art-summary')),classes:$('.page').className,
   dataset:{...$('.page').dataset},nextDisabled:$('#next').disabled};
}'''

def normalize(text): return re.sub(r'\s+', '', text or '')

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args): pass

def anchor_result(raw, reader):
    if not raw: return None
    parsed = urlparse(raw)
    if parsed.netloc: return {'url':raw,'kind':'external-source'}
    target = (ROOT/reader/'book'/unquote(parsed.path)).resolve()
    if target.is_dir(): target /= 'index.html'
    if not target.is_relative_to(ROOT): return {'url':raw,'error':'outside repository'}
    if not target.exists(): return {'url':raw,'error':'target missing','path':str(target)}
    data = html.fromstring(target.read_bytes())
    anchors = data.xpath('//*[@id=$value]',value=unquote(parsed.fragment)) if parsed.fragment else [data]
    return {'url':raw,'kind':'local-guide','path':str(target.relative_to(ROOT)),
            'fragment':parsed.fragment,'matches':len(anchors),
            'targetText':anchors[0].text_content().strip() if anchors else '',
            'links':anchors[0].xpath('.//a/@href') if anchors else []}

def save(rows, report):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'pages.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    (OUT/'runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--resume',action='store_true')
    parser.add_argument('--book',choices=ORDER)
    args=parser.parse_args()
    report={'baseline':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'scope':'All native Next steps in public readers, isolated browser contexts. No completion granted.',
            'interpretation':'Content/source interpretation is reviewed separately; this checks data to DOM/dialog and source targets.',
            'books':[],'mismatches':[],'sourceTargetIssues':[],'javascriptErrors':[],'httpErrors':[],
            'physicalDevices':'Not tested; this is a text-content audit, not a device-layout certification.'}
    rows=[]
    selected=[args.book] if args.book else ORDER
    if args.resume:
      report=json.loads((OUT/'runtime.json').read_text());rows=json.loads((OUT/'pages.json').read_text())
      report['books']=[r for r in report['books'] if r['book'] not in selected]
      report['mismatches']=[r for r in report['mismatches'] if r['book'] not in selected]
      report['sourceTargetIssues']=[r for r in report['sourceTargetIssues'] if r['book'] not in selected]
      rows=[r for r in rows if r['book'] not in selected]
      report['recheck']='Four Jhanas context-only expected model corrected; other completed native turns retained unchanged.'
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_port}/'
    try:
      with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        for book in selected:
          context=browser.new_context(viewport={'width':1280,'height':900},reduced_motion='reduce')
          page=context.new_page();page.on('pageerror',lambda e:report['javascriptErrors'].append(str(e)))
          page.on('response',lambda r:report['httpErrors'].append({'url':r.url,'status':r.status}) if r.status>=400 and r.url.startswith(base) else None)
          page.goto(base+book+'/book/');page.wait_for_function('typeof showPage==="function"&&document.body.classList.contains("reader-unified-controls")')
          total=page.evaluate("Number(document.querySelector('#position-text').textContent.match(/\\d+\\s*\\/\\s*(\\d+)/)[1])")
          seen_dialogs=set();source_targets={};count=0
          for index in range(total):
            page.evaluate('()=>new Promise(requestAnimationFrame)')
            row=page.evaluate(EXTRACT,book);row['book']=book
            assert row['page']==index+1,(book,index,row['page'])
            for key in ['narrationMatches','scriptureMatches','sourceMatches']:
              if not row[key]:report['mismatches'].append({'book':book,'page':index+1,'kind':key})
            href=row['sourceHref'] if not row['sourceHidden'] else None
            if href and href not in source_targets:
              target=anchor_result(href,book);source_targets[href]=target
              if target and (target.get('error') or target.get('matches',1)!=1):report['sourceTargetIssues'].append({'book':book,**target})
            dialog_key=(row['scripture'],row['expectedDialog'])
            if row['openDialog'] and dialog_key not in seen_dialogs:
              page.locator('#open-verse').click();page.wait_for_selector('#verse-dialog[open]')
              text=page.locator('#dialog-verse').text_content()
              row['dialogMatches']=normalize(text)==normalize(row['expectedDialog'])
              row['dialogText']=text
              if not row['dialogMatches']:report['mismatches'].append({'book':book,'page':index+1,'kind':'dialogMatches'})
              page.keyboard.press('Escape');seen_dialogs.add(dialog_key)
            rows.append(row);count+=1
            if index<total-1:page.locator('#next').click()
          report['books'].append({'book':book,'steps':count,'uniqueScriptureStates':len({r['scripture'] for r in rows if r['book']==book}),
                                  'dialogsOpened':len(seen_dialogs),'sourceTargets':list(source_targets.values()),
                                  'nativeNextClicks':count-1,'lastAction':page.locator('#next').inner_text(),
                                  'readerContentSha256':hashlib.sha256(json.dumps([r for r in rows if r['book']==book],ensure_ascii=False,sort_keys=True).encode()).hexdigest()})
          context.close();save(rows,report);print(book,count,'native steps checked',flush=True)
        browser.close()
      rows.sort(key=lambda r:(ORDER.index(r['book']),r['page']));report['books'].sort(key=lambda r:ORDER.index(r['book']))
      report['steps']=len(rows);report['result']='passed' if not any(report[k] for k in ['mismatches','sourceTargetIssues','javascriptErrors','httpErrors']) else 'findings'
    finally:server.shutdown();save(rows,report)
    print(json.dumps({k:len(v) if isinstance(v,list) else v for k,v in report.items() if k!='books'},ensure_ascii=False),flush=True)

if __name__=='__main__': main()
