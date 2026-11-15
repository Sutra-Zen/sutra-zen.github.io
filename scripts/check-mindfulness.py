#!/usr/bin/env python3
"""Validate the v3 source contract, paragraph/quote order, image overlays and reader controls."""
import argparse
import functools
import hashlib
import http.server
import io
import json
import re
import subprocess
import threading
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit, unquote

from lxml import html
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs/mindfulness'
OUT = ROOT / 'docs/previews/mindfulness'
BASELINE = '24983232d11bc9e775641bf444bcbe59055fe1ad'
STORY = json.loads((DOCS / 'storyboard.json').read_text())
CATALOG = json.loads((DOCS / 'scripture-catalog.json').read_text())['quotes']
BOOK = json.loads((ROOT / 'mindfulness/book/book-data.js').read_text().split('const BOOK = ')[1].rstrip(';\n'))
SIZES = [(360, 800), (800, 360), (768, 1024), (1024, 768), (1440, 900)]
LEGACY = ['four-truths', 'five-aggregates', 'six-senses', 'twelve-links', 'eightfold-path', 'four-fruits-ten-fetters', 'four-purities-six-recollections']


def baseline(path):
    return subprocess.check_output(['git', 'show', BASELINE + ':' + path], cwd=ROOT)


def static_checks():
    subprocess.run(['python', 'scripts/build-mindfulness.py', '--check'], cwd=ROOT, check=True)
    assert len(BOOK['scenes']) == 25
    assert sum(len(s['paragraphs']) for s in BOOK['scenes']) == 92
    assert sum(len(g['mappings']) for s in BOOK['scenes'] for g in s['quotes']) == 27
    assert {g['quoteId'] for s in BOOK['scenes'] for g in s['quotes']} == {q['id'] for q in CATALOG}
    assert all(not s['quotes'] for s in BOOK['scenes'][:4]) and not BOOK['scenes'][24]['quotes']
    for original, actual in zip(STORY['scenes'], BOOK['scenes']):
        assert actual['id'] == original['id'] and actual['image'] == original['asset']
        assert actual['artOverlay'] == original['artOverlay']
        assert actual['bakedText'] == original['bakedText']
        expected = original['narrationParagraphs'] if original['id'] != 'S25' else []
        assert actual['paragraphs'] == expected
        for group in actual['quotes']:
            q = next(q for q in CATALOG if q['id'] == group['quoteId'])
            assert group['text'] == q['videoText'] and group['source'] == q['sourceLabelAsVideo']
            assert group['afterParagraph'] == max(n for m in group['mappings'] for n in m['paragraphs'])
    for row in json.loads((DOCS / 'asset-manifest.json').read_text()):
        image = Image.open(DOCS / row['path'])
        assert image.size == (row['width'], row['height'])
        image.verify()
    for q in CATALOG:
        for path in q['evidenceFrames']:
            Image.open(DOCS / path).verify()
    pdf = DOCS / 'references/A_Wandering_Mind_Is_an_Unhappy_Mind.pdf'
    assert pdf.read_bytes().startswith(b'%PDF-')
    all_paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASELINE], cwd=ROOT, text=True).splitlines()
    for path in all_paths:
        if any(path.startswith(n + '/') for n in LEGACY) or path.startswith('.github/') or path in ['shelf.css', 'guide-header.css', 'guide-ui.css', 'reader-controls.css', 'reader-restart.js', '.nojekyll', 'CNAME']:
            assert (ROOT / path).read_bytes() == baseline(path), path
    before = baseline('index.html').decode()
    after = (ROOT / 'index.html').read_text()
    old_map, new_map = [json.loads(re.search(r'const dhammaData = (.*?);\s*\n', text)[1]) for text in [before, after]]
    assert old_map.keys() == new_map.keys()
    for key in old_map:
        if key in ['四念處', '四顛倒']:
            assert old_map[key]['content'][:-6] in new_map[key]['content']
            assert './mindfulness/' in new_map[key]['content']
        else:
            assert old_map[key] == new_map[key]
    root = html.fromstring(after)
    assert len(root.xpath('//ol[@class="sz-books"]/li')) == 14
    assert len(root.xpath('//*[contains(concat(" ",@class," ")," sz-ready ")]')) == 8
    assert len(root.xpath('//*[@class="sz-book-lock"]')) == 6
    assert root.xpath('//iframe/@src') == html.fromstring(before).xpath('//iframe/@src')
    guide = html.parse(str(ROOT / 'mindfulness/index.html'))
    for q in CATALOG:
        card = guide.xpath('//*[@id=$id]', id=q['id'])[0]
        assert q['videoText'] == card.xpath('.//blockquote/p')[0].text_content()
        assert q['sourceLabelAsVideo'] == card.xpath('.//h3')[0].text_content()
    for path in ['mindfulness/index.html', 'mindfulness/book/index.html']:
        for url in html.parse(str(ROOT / path)).xpath('//@href|//@src'):
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc:
                continue
            target = ((ROOT / path).parent / unquote(parsed.path)).resolve()
            if target.is_dir():
                target /= 'index.html'
            assert target.is_file(), (path, url)
            if parsed.fragment:
                assert html.parse(str(target)).xpath('//*[@id=$id]', id=parsed.fragment)
    print('v3 source, complete narration, all quote mappings, source files and legacy preservation: OK', flush=True)


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def copyfile(self, source, outputfile):
        try:
            super().copyfile(source, outputfile)
        except (BrokenPipeError, ConnectionResetError):
            pass


def settle(page):
    page.wait_for_function('document.querySelector("#art").complete && document.querySelector("#art").naturalWidth > 0')
    page.evaluate('() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))')


def screenshot(page, name):
    Image.open(io.BytesIO(page.screenshot(type='png'))).save(OUT / name, lossless=True, method=6)


def browser_checks(capture):
    OUT.mkdir(parents=True, exist_ok=True)
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}/'
    report = {'baseline': BASELINE, 'pageStates': 0, 'paragraphs': 92, 'quoteMappings': 27, 'quoteIds': 18, 'viewports': [], 'javascriptErrors': [], 'httpErrors': [], 'realIPadSafari': 'not tested'}
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        for width, height in SIZES:
            page = browser.new_page(viewport={'width': width, 'height': height}, has_touch=True)
            page.on('pageerror', lambda e: report['javascriptErrors'].append(str(e)))
            page.on('response', lambda r: report['httpErrors'].append(r.url) if r.url.startswith(base) and r.status >= 400 else None)
            page.goto(base + 'mindfulness/book/')
            page.wait_for_function('typeof showPage === "function"')
            for i, scene in enumerate(BOOK['scenes']):
                page.select_option('#page-select', scene['id'])
                settle(page)
                r = page.evaluate('''() => {
                  const $=s=>document.querySelector(s), rect=s=>$(s).getBoundingClientRect().toJSON();
                  return {narration:[...document.querySelectorAll('.narration-paragraph')].map(p=>p.textContent),
                    quotes:[...document.querySelectorAll('#reading-content .scripture-card')].map(el=>({id:el.dataset.quoteId,after:Number(el.dataset.afterParagraph),text:el.querySelector('blockquote').textContent,source:el.querySelector('h3').textContent,relation:el.querySelector('.quote-relation').textContent,mappings:[...el.querySelectorAll('.quote-mapping')].map(m=>m.textContent),previous:el.previousElementSibling.id,visible:getComputedStyle(el).display!=='none'})),
                    image:$('#art').getAttribute('src'),natural:[$('#art').naturalWidth,$('#art').naturalHeight],art:rect('#art-frame'),
                    labels:[...document.querySelectorAll('#art-frame .art-label')].map(el=>({text:el.textContent,rect:el.getBoundingClientRect().toJSON(),font:parseFloat(getComputedStyle(el).fontSize),color:getComputedStyle(el).color})),
                    number:$('#position-text').textContent,overflow:document.documentElement.scrollWidth>innerWidth,touch:getComputedStyle($('#next')).touchAction,
                    summaryOnImage:Boolean($('#art-frame .summary-overlay')&&!$('#art-frame .summary-overlay').hidden),
                    summaryCards:[...document.querySelectorAll('#summary-cards .summary-card')].map(el=>el.textContent),cardsHidden:$('#summary-cards').hidden,
                    summaryImage:[...document.querySelectorAll('#art-frame .summary-row')].map(el=>el.textContent)};
                }''')
                assert r['narration'] == [p['text'] for p in scene['paragraphs']]
                assert r['image'] == '../../docs/mindfulness/' + scene['image']
                assert r['natural'] == scene['dimensions']
                assert r['number'] == f'{i + 1} / 25 頁'
                assert not r['overflow'] and r['touch'] == 'manipulation'
                assert len(r['quotes']) == len(scene['quotes'])
                for actual in r['quotes']:
                    group = next(q for q in scene['quotes'] if q['quoteId'] == actual['id'])
                    assert actual['text'] == group['text'] and actual['source'] == group['source'] and actual['visible']
                    assert actual['after'] == group['afterParagraph']
                    assert actual['previous'] == scene['paragraphs'][group['afterParagraph'] - 1]['id']
                    assert len(actual['mappings']) == len(group['mappings'])
                    if group['relation'] != '原片下方引文對應':
                        assert actual['relation'] == group['relation']
                art = r['art']
                assert abs(art['width'] / art['height'] - scene['dimensions'][0] / scene['dimensions'][1]) < .005
                assert len(r['labels']) == len(scene['artOverlay'])
                for actual, planned in zip(r['labels'], scene['artOverlay']):
                    rect = actual['rect']
                    assert actual['text'] == planned['text']
                    assert abs(rect['x'] - art['x'] - art['width'] * planned['x'] / 100) < 1
                    assert abs(rect['y'] - art['y'] - art['height'] * planned['y'] / 100) < 1
                    assert abs(rect['width'] - art['width'] * planned['width'] / 100) < 1
                    assert abs(actual['font'] - art['width'] * planned['fontSizeCqw'] / 100) < .1
                    assert actual['color'] == ('rgb(255, 255, 255)' if planned['color'] == 'white' else 'rgb(17, 17, 17)')
                    assert rect['right'] <= art['right'] + 1 and rect['bottom'] <= art['bottom'] + 1
                if scene['summaryRows']:
                    assert not r['narration'] and not r['quotes']
                    assert r['summaryCards'] == scene['summaryRows'] and r['summaryImage'] == scene['summaryRows']
                    assert r['summaryOnImage'] == (art['width'] >= 900)
                    assert r['cardsHidden'] == r['summaryOnImage']
                    if width <= 1024:
                        assert not r['cardsHidden']
                if capture and (((width, height) in [(768, 1024), (1024, 768)] and scene['id'] in ['S03', 'S10', 'S18', 'S19', 'S21', 'S25']) or (width == 1440 and scene['id'] == 'S25')):
                    screenshot(page, f'{scene["id"]}-{width}x{height}.webp')
                report['pageStates'] += 1
            # Shared end-page restart, then rapid page turns and keyboard.
            page.locator('#next').tap()
            assert page.locator('#position-text').inner_text() == '1 / 25 頁'
            assert page.locator('#previous').is_disabled()
            for _ in range(8):
                page.locator('#next').tap()
            assert page.locator('#position-text').inner_text() == '9 / 25 頁'
            assert page.evaluate('visualViewport.scale') == 1
            page.locator('#previous').tap(); page.keyboard.press('ArrowRight')
            assert page.locator('#position-text').inner_text() == '9 / 25 頁'
            # Image zoom keeps every overlay on the same image-relative positions.
            page.select_option('#page-select', 'S19'); page.locator('#open-image').click()
            assert page.locator('#image-dialog').evaluate('el=>el.open')
            for _ in range(3):
                page.locator('#zoom-in').click()
            assert page.locator('#zoom-level').inner_text() == '250%'
            zoomed = page.locator('#zoom-frame').evaluate('el=>({w:el.getBoundingClientRect().width,labels:[...el.querySelectorAll(".art-label")].map(l=>({left:l.getBoundingClientRect().x-el.getBoundingClientRect().x,font:parseFloat(getComputedStyle(l).fontSize)}))})')
            for actual, expected in zip(zoomed['labels'], BOOK['scenes'][18]['artOverlay']):
                assert abs(actual['left'] - zoomed['w'] * expected['x'] / 100) < 1
                assert abs(actual['font'] - zoomed['w'] * expected['fontSizeCqw'] / 100) < .1
            page.locator('#zoom-scroll').evaluate('el=>{el.scrollLeft=200;el.scrollTop=100}')
            page.locator('#image-dialog form button').click()
            page.locator('#fullscreen').click()
            page.wait_for_function('document.fullscreenElement || document.body.classList.contains("fullscreen-fallback")')
            assert page.locator('#fullscreen').inner_text() == '退出全螢幕'
            page.locator('#fullscreen').click()
            page.wait_for_function('!document.fullscreenElement && !document.body.classList.contains("fullscreen-fallback")')
            assert page.locator('#position-text').inner_text() == '19 / 25 頁'
            if width == 360:
                page.evaluate('document.documentElement.requestFullscreen = undefined')
                page.locator('#fullscreen').click()
                assert page.locator('body').evaluate('el=>el.classList.contains("fullscreen-fallback")')
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth')
                page.locator('#fullscreen').click()
                assert not page.locator('body').evaluate('el=>el.classList.contains("fullscreen-fallback")')
            # Reading scroll / direction keys never advance a scene.
            page.locator('.reading-text').focus(); page.keyboard.press('ArrowRight')
            assert page.locator('#position-text').inner_text() == '19 / 25 頁'
            page.locator('.reading-text').evaluate('el=>el.scrollTop=el.scrollHeight')
            page.select_option('#page-select', 'S10')
            # Sources land on the matching visible quote card; going back retains scene.
            page.locator('.scripture-card[data-quote-id="Q06"] a').click()
            assert page.url.endswith('/mindfulness/#Q06')
            assert page.locator('#Q06 blockquote').is_visible()
            page.go_back(); page.wait_for_function('typeof showPage === "function"')
            assert page.locator('#position-text').inner_text() == '10 / 25 頁'
            page.locator('.top a').click(); page.locator('.book-cover').click()
            page.wait_for_function('typeof showPage === "function"')
            assert page.locator('#position-text').inner_text() == '10 / 25 頁'
            page.reload(); page.wait_for_function('typeof showPage === "function"')
            assert page.locator('#position-text').inner_text() == '10 / 25 頁'
            page.set_viewport_size({'width': height, 'height': width}); settle(page)
            assert page.locator('#position-text').inner_text() == '10 / 25 頁'
            page.close()
            report['viewports'].append({'width': width, 'height': height, 'scenes': 25, 'controls': 'passed'})
            print(f'{width}x{height}: 25 scenes, full narration/quotes, overlays, zoom, fullscreen, sources and restart OK', flush=True)
        page = browser.new_page(viewport={'width': 1024, 'height': 768})
        page.on('pageerror', lambda e: report['javascriptErrors'].append(str(e)))
        cache = {}
        for url in ['https://cdn.tailwindcss.com/', 'https://unpkg.com/lucide@latest']:
            r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30)
            cache[url] = (r.read(), r.headers.get('Content-Type', 'application/javascript'))
        def cdn(route):
            body, content_type = cache[route.request.url]
            route.fulfill(status=200, body=body, content_type=content_type)
        page.route('https://cdn.tailwindcss.com/**', cdn)
        page.route('https://unpkg.com/lucide@latest', cdn)
        page.goto(base)
        page.locator('.sz-book[href="./mindfulness/book/"]').click()
        page.wait_for_function('typeof showPage === "function"')
        assert page.locator('#position-text').inner_text().endswith('/ 25 頁')
        for key in ['四念處', '四顛倒']:
            page.goto(base); page.evaluate('key=>openModal(key)', key)
            page.locator('#modalBody a[href="./mindfulness/"]').click()
            assert page.locator('h1').inner_text() == '四念處與四顛倒'
        for entry, number in [('S05', 5), ('S12', 12), ('S17', 17), ('S19', 19)]:
            page.goto(base + 'mindfulness/')
            page.locator('.chapter-grid a[href="book/?scene=' + entry + '"]').click()
            page.wait_for_function('typeof showPage === "function"')
            assert page.locator('#position-text').inner_text() == f'{number} / 25 頁'
            page.select_option('#page-select', 'S10')
            page.locator('.scripture-card[data-quote-id="Q06"] a').click()
            page.go_back(); page.wait_for_function('typeof showPage === "function"')
            assert page.locator('#position-text').inner_text() == '10 / 25 頁'
        for name in LEGACY:
            page.goto(base + name + '/book/')
            page.locator('#next').wait_for(state='visible')
            before = page.locator('#position-text').inner_text()
            page.locator('#next').click()
            assert page.locator('#position-text').inner_text() != before
            page.locator('.top a').click()
            assert urlsplit(page.url).path == '/' + name + '/'
        browser.close()
    server.shutdown()
    assert not report['javascriptErrors'], report['javascriptErrors']
    assert not report['httpErrors'], report['httpErrors']
    report['legacyReaders'] = 'all seven open/next/return passed'
    (OUT / 'validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print('125 scene states and all seven existing book entrances passed.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--screenshots', action='store_true')
    args = parser.parse_args()
    static_checks()
    browser_checks(args.screenshots)
