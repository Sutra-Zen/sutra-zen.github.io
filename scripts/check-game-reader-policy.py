#!/usr/bin/env python3
"""Test game access/save/reader behavior independently of the immersion camera UI.

The /game/ return destination is intercepted as an empty same-origin landing page
so these tests isolate real reader bridges and persistence, not title/camera work.
All saves are disposable browser fixtures, never author progress.
"""
from pathlib import Path
import argparse
import functools
import http.server
import json
import threading
from urllib.parse import urlsplit, parse_qs
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
KEY = 'sutrazen.play.collection.v1'
OLD_KEY = 'sutrazen.play.v1'
OLD = {'version': 1, 'positions': {}, 'freePositions': {}, 'completed': [],
       'activeBook': 'four-truths', 'orderedBook': 'four-truths', 'mode': 'ordered',
       'settings': {'locale': 'zh-Hant', 'reducedMotion': False}}

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_): pass
    def copyfile(self, source, target):
        try: super().copyfile(source, target)
        except (BrokenPipeError, ConnectionResetError): pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'docs/previews/game-reader-policy')
    args = parser.parse_args(); args.output.mkdir(parents=True, exist_ok=True)
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}/'
    report = {'scope': 'Real reader/store policy; blank same-origin /game/ return transport only. No camera, title-screen or physical Safari claim.',
              'fixtures': 'Isolated disposable browser saves, never author progress', 'checks': [], 'javascriptErrors': [], 'httpErrors': []}
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        def new_page(state):
            context = browser.new_context(viewport={'width': 1024, 'height': 768}, reduced_motion='reduce')
            page = context.new_page()
            blank = lambda route: route.fulfill(content_type='text/html', body='<html lang="zh-Hant"><title>Policy return transport</title></html>')
            page.route('**/game/**', blank); page.route('**/__policy_fixture.html', blank)
            page.on('pageerror', lambda e: report['javascriptErrors'].append(str(e)))
            page.on('response', lambda r: report['httpErrors'].append(r.url) if r.url.startswith(base) and r.status >= 400 else None)
            page.goto(base+'__policy_fixture.html')
            page.evaluate('([key,raw,oldKey,old])=>{localStorage.setItem(key,raw);localStorage.setItem(oldKey,old);localStorage.setItem("unrelated-policy-setting","keep");}', [KEY,json.dumps(state,ensure_ascii=False,indent=1),OLD_KEY,json.dumps(OLD)])
            return context, page
        def state(completed=(), positions=None, active='four-truths'):
            return {'version':1,'completed':list(completed),'positions':positions or {},'activeBook':active}
        def saved(page): return page.evaluate('(key)=>JSON.parse(localStorage.getItem(key))', KEY)
        def raw(page): return page.evaluate('(key)=>localStorage.getItem(key)', KEY)
        def wait_reader(page, book, index=None):
            page.wait_for_function('(id)=>document.body?.dataset.collectionBook===id&&!!window.SutraZenCollectionBridge', arg=book)
            if index is not None: page.wait_for_function('(i)=>document.body.dataset.collectionIndex===String(i)',arg=index)
        # All historical collection return hints, bookmarks, review flags and mixed
        # journey parameters use exactly the same game access policy.
        fixture = state(positions={'four-jhanas':73,'six-senses':8},active='four-jhanas')
        context,page = new_page(fixture); before=raw(page); old_before=page.evaluate('(key)=>localStorage.getItem(key)',OLD_KEY)
        attempts = [
            'four-jhanas/book/?collection=1',
            'four-jhanas/book/?collection=1&collectionReturn=game&collectionPage=130',
            'four-jhanas/book/?collection=1&collectionReturn=worldmap-v4',
            'four-jhanas/book/?collection=1&collectionReturn=https%3A%2F%2Fevil.invalid%2F',
            'four-jhanas/book/?collection=1&collectionReview=1',
            'four-jhanas/book/?collection=1&journey=game',
            'six-senses/book/?collection=1&journey=free',
        ]
        for target in attempts:
            page.goto(base+target,wait_until='domcontentloaded');page.wait_for_url('**/game/?notice=locked#map')
            assert raw(page)==before, target
            assert page.evaluate('(key)=>localStorage.getItem(key)',OLD_KEY)==old_before, target
        report['checks'].append({'lockedEntryVariants':attempts,'result':'denied before bookmark/completion/v1 mutation'})
        # A public reader remains free and inert with respect to game state.
        page.goto(base+'four-jhanas/book/');page.wait_for_selector('#next');assert not page.locator('.collection-reader-return').count()
        old_position=page.locator('#position-text').inner_text();page.locator('#next').click();assert page.locator('#position-text').inner_text()!=old_position
        assert raw(page)==before;report['checks'].append('Bare public Four Jhanas is readable and makes no collection write');context.close()
        # Real first-book Next flow, including halfway rejection, reload and explicit
        # formal ending. Future bookmark remains preserved but never controls access.
        context,page=new_page(fixture)
        page.goto(base+'four-truths/book/?collection=1&collectionReturn=worldmap-v4');wait_reader(page,'four-truths',0)
        assert page.locator('.collection-reader-return').get_attribute('href')==base+'game/#map'
        for index in range(1,6):page.locator('#next').click();wait_reader(page,'four-truths',index)
        assert page.evaluate('async()=>{const{store}=await import("/play/collection/store.js");return store.complete("four-truths")}') is False
        page.reload(wait_until='domcontentloaded');wait_reader(page,'four-truths',5)
        page.locator('.collection-reader-return').click();page.wait_for_url('**/game/#map');assert saved(page)['completed']==[]
        page.goto(base+'four-truths/book/?collection=1');wait_reader(page,'four-truths',5)
        for index in range(6,29):page.locator('#next').click();wait_reader(page,'four-truths',index)
        assert saved(page)['completed']==[];assert page.locator('#next').inner_text()=='完成這本'
        page.locator('#next').click();page.wait_for_url('**/game/?completed=four-truths#map')
        assert saved(page)['completed']==['four-truths'];assert saved(page)['activeBook']=='five-aggregates';assert saved(page)['positions']['four-jhanas']==73
        report['checks'].append('Actual Four Truths Next0→5 halfway complete rejected/reload/return/resume5→28; arrival does not complete, explicit finish counts once and advances current to Five Aggregates');context.close()
        # Historical out-of-order completed books stay reviewable. Review writes
        # only its own bookmark, not activeBook, completion, or new-reward query.
        history=state(['four-truths','four-jhanas'],{'four-truths':28,'five-aggregates':4,'six-senses':73,'four-jhanas':43},'five-aggregates')
        context,page=new_page(history)
        page.goto(base+'four-truths/book/?collection=1&collectionReturn=game&collectionReview=1');wait_reader(page,'four-truths',0)
        assert page.locator('body').get_attribute('data-collection-mode')=='review'
        assert page.locator('.collection-reader-return').get_attribute('href')==base+'game/#shelf'
        for index in range(1,6):page.locator('#next').click();wait_reader(page,'four-truths',index)
        page.locator('.collection-reader-return').click();page.wait_for_url('**/game/#shelf');assert saved(page)['activeBook']=='five-aggregates'
        page.goto(base+'four-truths/book/?collection=1');wait_reader(page,'four-truths',5)
        for index in range(6,29):page.locator('#next').click();wait_reader(page,'four-truths',index)
        page.locator('#next').click();page.wait_for_url('**/game/#shelf')
        result=saved(page);assert result['completed']==history['completed'];assert result['activeBook']==history['activeBook'];assert result['positions']['five-aggregates']==4;assert result['positions']['six-senses']==73;assert 'completed' not in parse_qs(urlsplit(page.url).query)
        page.goto(base+'four-jhanas/book/?collection=1');wait_reader(page,'four-jhanas',43);page.locator('#next').click();wait_reader(page,'four-jhanas',44);page.locator('.collection-reader-return').click();page.wait_for_url('**/game/#shelf');assert saved(page)['activeBook']=='five-aggregates'
        report['checks'].append('Historical Four Jhanas review stays available; completed Four Truths review0→5 return/resume5→28 finish returns shelf with no completed marker, reward or mainline-active change');context.close()
        # Another restore can revoke access while a reader is open; both bridge
        # and real store recheck rather than trusting original URL/entry state.
        context,page=new_page(state(['four-truths'],{'five-aggregates':0},'five-aggregates'))
        page.goto(base+'five-aggregates/book/?collection=1');wait_reader(page,'five-aggregates',0)
        replacement=state([] ,{'five-aggregates':53},'five-aggregates')
        page.evaluate('async value=>{const{store}=await import("/play/collection/store.js");store.restoreBackup(JSON.stringify(value))}',replacement)
        page.wait_for_url('**/game/?notice=locked#map');assert saved(page)==replacement
        report['checks'].append('Restore while reading revokes future eligibility and redirects without overwriting its preserved bookmark');context.close()
        # Existing old three-book journey still works when no collection flag is
        # present; the mixed-URL test above proved the converse precedence.
        context,page=new_page(state()) ; before=raw(page)
        page.goto(base+'four-truths/book/?journey=ordered');page.wait_for_function('!!window.SutraZenJourneyBridge');page.locator('#next').click();page.wait_for_function('SutraZenJourneyBridge.index===1')
        assert raw(page)==before;assert page.evaluate('(key)=>JSON.parse(localStorage.getItem(key)).positions["four-truths"]',OLD_KEY)==1
        assert page.evaluate('localStorage.getItem("unrelated-policy-setting")')=='keep';report['checks'].append('Bare old journey mode still reads/saves its own namespace; collection and unrelated keys unchanged');context.close()
        # Quota failure leaves a readable but stale canonical local value. The
        # same-tab fallback must carry a completion and bookmark across documents.
        context,page=new_page(state(positions={'four-truths':28,'four-jhanas':73}))
        canonical_before=raw(page)
        context.add_init_script("""(() => {
          const original=Storage.prototype.setItem;
          Storage.prototype.setItem=function(key,value){
            if(this===localStorage&&key==='sutrazen.play.collection.v1'&&!window.__policyAllowWrites)throw new DOMException('quota','QuotaExceededError');
            return original.call(this,key,value);
          };
        })();""")
        page.goto(base+'four-truths/book/?collection=1');wait_reader(page,'four-truths',28)
        if page.locator('.collection-reader-storage[open]').count():page.locator('.collection-reader-storage button').click()
        page.locator('#next').click();page.wait_for_url('**/game/?completed=four-truths#map')
        recovered=page.evaluate('async()=>{const{store}=await import("/play/collection/store.js");return {state:store.get(),issue:store.issue}}')
        assert recovered['state']['completed']==['four-truths'];assert recovered['issue']=='unavailable';assert raw(page)==canonical_before
        page.goto(base+'five-aggregates/book/?collection=1');wait_reader(page,'five-aggregates',0)
        if page.locator('.collection-reader-storage[open]').count():page.locator('.collection-reader-storage button').click()
        for index in range(1,4):page.locator('#next').click();wait_reader(page,'five-aggregates',index)
        page.reload(wait_until='domcontentloaded');wait_reader(page,'five-aggregates',3)
        if page.locator('.collection-reader-storage[open]').count():page.locator('.collection-reader-storage button').click()
        assert raw(page)==canonical_before
        page.evaluate('window.__policyAllowWrites=true');page.locator('#next').click();wait_reader(page,'five-aggregates',4)
        assert saved(page)['completed']==['four-truths'];assert saved(page)['positions']['five-aggregates']==4;assert saved(page)['positions']['four-jhanas']==73
        assert page.evaluate('sessionStorage.getItem("sutrazen.play.collection.session.v1")') is None
        assert page.evaluate('async()=>(await import("/play/collection/store.js")).store.issue') is None
        report['checks'].append('Actual quota-blocked local writes keep stale canonical bytes while same-tab recovery carries explicit completion and Five Aggregates step3 across navigation/reload; successful local retry clears fallback without losing future bookmark')
        context.close()
        browser.close()
    server.shutdown();assert not report['javascriptErrors'] and not report['httpErrors'],report
    (args.output/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'result':'passed','checks':len(report['checks']),'report':str(args.output/'validation.json')},ensure_ascii=False))

if __name__=='__main__':main()
