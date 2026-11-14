#!/usr/bin/env python3
"""Verify book 06, source fidelity, layout safety and existing book entrances.

python scripts/check-four-fruits-ten-fetters.py --verify-sources --screenshots
Requires Python Playwright, Pillow, lxml and /usr/bin/chromium.
"""
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
from urllib.parse import unquote, urlsplit

from lxml import html
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs/four-fruits-ten-fetters'
OUT = ROOT / 'docs/previews/four-fruits-ten-fetters'
BASELINE = 'bc29ec604dacf8515245669c553af8c27318a95d'
SIZES = [(390, 844), (844, 390), (768, 1024), (1024, 768)]
BOOK = json.loads((ROOT / 'four-fruits-ten-fetters/book/book-data.js').read_text().split('const BOOK = ', 1)[1].rstrip(';\n'))
STORY = json.loads((DOCS / 'storyboard.json').read_text())
SOURCES = json.loads((DOCS / 'verified-sources.json').read_text())


def baseline(path):
    return subprocess.check_output(['git', 'show', BASELINE + ':' + path], cwd=ROOT)


def normalize(text):
    return re.sub(r'\s+', '', text)


def check_static(verify_sources):
    subprocess.run(['python', 'scripts/build-four-fruits-ten-fetters.py', '--check'], cwd=ROOT, check=True)
    for asset in json.loads((DOCS / 'assets-manifest.json').read_text()):
        assert Image.open(DOCS / asset['path']).size == (asset['width'], asset['height'])
    original = [s for scene in STORY['scenes'] for s in scene['topSubtitle']]
    assert [p['lines'][0] for p in BOOK['pages'][:74]] == [s['text'] for s in original]
    assert [p['at'] for p in BOOK['pages'][:74]] == [s['at'] for s in original]
    assert len(BOOK['pages']) == 75 and len(BOOK['scenes']) == 12
    assert all(s['artOverlay'] == [] for s in BOOK['scenes'])
    if verify_sources:
        source_texts = {}
        for source in SOURCES['files']:
            raw = urllib.request.urlopen(source['url'], timeout=30).read()
            assert hashlib.sha256(raw).hexdigest() == source['sha256']
            tree = html.fromstring(raw)
            for ref in tree.xpath('//a[contains(@class,"ref")]'):
                ref.drop_tree()
            source_texts[source['id']] = normalize(tree.text_content())
        for quote in [*SOURCES['cues'].values(), *SOURCES['guideExcerpts'].values()]:
            for block in quote['blocks']:
                assert normalize(block) in source_texts[quote['canon']]
    # All five published books, shared styles and Pages settings stay byte-identical.
    paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASELINE], cwd=ROOT, text=True).splitlines()
    prefixes = ('four-truths/', 'five-aggregates/', 'six-senses/', 'twelve-links/', 'eightfold-path/', '.github/')
    for path in paths:
        if path.startswith(prefixes) or path in ['CNAME', '.nojekyll', 'shelf.css', 'reader-controls.css', 'guide-header.css', 'guide-ui.css']:
            assert (ROOT / path).read_bytes() == baseline(path), path
    old_index = baseline('index.html').decode()
    new_index = (ROOT / 'index.html').read_text()
    map_pattern = r'const dhammaData = (.*?);\s*\n'
    before = json.loads(re.search(map_pattern, old_index)[1])
    after = json.loads(re.search(map_pattern, new_index)[1])
    assert before.keys() == after.keys()
    for key in before:
        if key == '四向四果':
            assert after[key]['title'] == before[key]['title']
            assert before[key]['content'][:-6] in after[key]['content']
            assert './four-fruits-ten-fetters/' in after[key]['content']
        else:
            assert before[key] == after[key], key
    old_tree, tree = html.fromstring(old_index), html.fromstring(new_index)
    assert len(tree.xpath('//ol[@class="sz-books"]/li')) == 14
    assert len(tree.xpath('//*[contains(concat(" ",@class," ")," sz-ready ")]')) == 6
    assert len(tree.xpath('//*[@class="sz-book-lock"]')) == 8
    assert [el.get('src') for el in old_tree.xpath('//iframe')] == [el.get('src') for el in tree.xpath('//iframe')]
    assert tree.get_element_by_id('video-06').xpath('.//iframe')[0].get('src').endswith('/n0bco_NPmRI')
    guide = html.parse(str(ROOT / 'four-fruits-ten-fetters/index.html'))
    assert not guide.xpath('//details')
    assert len(guide.xpath('//*[@class="source-entry"]')) == 9
    for quote in [*SOURCES['cues'].values(), *SOURCES['guideExcerpts'].values()]:
        card = guide.xpath('//*[@id=$id]', id=quote['canon'].replace('.', '-'))[0]
        for block in quote['blocks']:
            assert normalize(block) in normalize(card.text_content())
    assert '莊春江' in guide.xpath('//*[@id="sn46-55"]')[0].text_content()
    for path in ['four-fruits-ten-fetters/index.html', 'four-fruits-ten-fetters/book/index.html']:
        local_tree = html.parse(str(ROOT / path))
        for url in local_tree.xpath('//@href|//@src'):
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc:
                continue
            target = ((ROOT / path).parent / unquote(parsed.path)).resolve()
            if target.is_dir():
                target /= 'index.html'
            assert target.is_file(), (path, url)
            if parsed.fragment:
                assert html.parse(str(target)).xpath('//*[@id=$id]', id=parsed.fragment), url
    for page in BOOK['pages'][:74]:
        assert guide.xpath('//*[@id=$id]', id=page['source'].split('#')[1])
    print('Content / images / source cards / shelf / unchanged existing books: OK', flush=True)


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def rects_overlap(a, b):
    return min(a['right'], b['right']) - max(a['left'], b['left']) > 1 and min(a['bottom'], b['bottom']) - max(a['top'], b['top']) > 1


def settled(page):
    page.evaluate('() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))')
    page.wait_for_function('document.querySelector("#art").complete && document.querySelector("#art").naturalWidth > 0')


def screenshot(page, filename):
    """Keep every screenshot pixel while avoiding large PNGs in the repository."""
    Image.open(io.BytesIO(page.screenshot(type='png'))).save(OUT / filename, lossless=True, method=6)


def check_browser(screenshots, entrances_only=False):
    OUT.mkdir(parents=True, exist_ok=True)
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}/'
    report = {'baseline': BASELINE, 'viewports': [], 'pageChecks': 0, 'javascriptErrors': [], 'localHttpErrors': [], 'realIPadSafari': 'not tested'}
    if entrances_only:
        report = json.loads((OUT / 'reader-validation.json').read_text())
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        for width, height in ([] if entrances_only else SIZES):
            context = browser.new_context(viewport={'width': width, 'height': height}, has_touch=True)
            page = context.new_page()
            page.on('pageerror', lambda e: report['javascriptErrors'].append(str(e)))
            page.on('response', lambda r: report['localHttpErrors'].append(r.url) if r.url.startswith(base) and r.status >= 400 else None)
            page.goto(base + 'four-fruits-ten-fetters/book/')
            page.wait_for_function('typeof showPage === "function"')
            scene_frames = {}
            for i, expected in enumerate(BOOK['pages'][:74]):
                page.evaluate('showPage', i)
                settled(page)
                actual = page.evaluate('''() => {
                    const $ = s => document.querySelector(s), rect = s => $(s).getBoundingClientRect().toJSON();
                    return {
                      caption: $('#narration').textContent, verse: $('#verse').textContent,
                      href: $('#source-link').getAttribute('href'), number: $('#position-text').textContent,
                      captionRect:rect('#caption'), narrationRect:rect('#narration'), art:rect('#art-frame'), scripture:rect('.scripture'),
                      previous:rect('#previous'), next:rect('#next'), menu:rect('.position'), back:rect('.top a'),
                      color:getComputedStyle($('#caption')).color, align:getComputedStyle($('#caption')).textAlign,
                      selectable:getComputedStyle($('#narration')).userSelect,
                      overlays:$('#art-overlays').childElementCount,
                      natural:[$('#art').naturalWidth,$('#art').naturalHeight],
                      overflow:document.documentElement.scrollWidth > innerWidth,
                      touchAction:getComputedStyle($('#next')).touchAction,
                      disabled:[$('#previous').disabled,$('#next').disabled],
                    };
                }''')
                assert actual['caption'] == expected['lines'][0], (width, i, 'caption')
                assert actual['verse'] == expected['verseLabel'] + '\n' + expected['verse']
                assert actual['href'] == expected['source']
                assert actual['number'] == f'{i + 1} / 75 頁'
                assert actual['disabled'] == [i == 0, False]
                assert actual['natural'] == expected['dimensions']
                assert actual['touchAction'] == 'manipulation'
                assert actual['align'] == 'left' and actual['selectable'] != 'none'
                assert actual['overlays'] == 0 and not actual['overflow']
                color = '#171611' if expected['scene'] in ['S01', 'S10'] else '#fffdf8'
                rgb = 'rgb(' + ', '.join(str(int(color[j:j + 2], 16)) for j in (1, 3, 5)) + ')'
                assert actual['color'] == rgb, (width, i, actual['color'])
                assert actual['narrationRect']['bottom'] <= actual['captionRect']['bottom'] + 1
                art = actual['art']
                assert abs(art['width'] / art['height'] - expected['dimensions'][0] / expected['dimensions'][1]) < .01
                assert art['top'] >= actual['captionRect']['bottom'] - 1
                assert art['bottom'] <= actual['scripture']['top'] + 1
                if width > height:
                    assert 0 <= art['top'] < art['bottom'] <= height
                    for control in ['previous', 'next', 'menu', 'back']:
                        assert not rects_overlap(art, actual[control]), (width, i, control)
                    # Captions must not disappear beneath return/menu controls either.
                    for control in ['menu', 'back']:
                        assert not rects_overlap(actual['narrationRect'], actual[control]), (width, i, control, 'caption')
                signature = tuple(round(art[k], 1) for k in ['x', 'y', 'width', 'height'])
                if expected['scene'] in scene_frames:
                    assert signature == scene_frames[expected['scene']], (width, i, 'image jumps between subtitles')
                scene_frames[expected['scene']] = signature
                report['pageChecks'] += 1
            # Menu must jump to the first subtitle of all eleven scenes.
            for scene in BOOK['scenes']:
                page.select_option('#page-select', scene['id'])
                assert page.locator('#position-text').inner_text() == f'{scene["start"] + 1} / 75 頁'
            # Navigation, rapid taps and keyboard after button focus.
            page.evaluate('showPage(0)')
            for _ in range(8):
                page.locator('#next').tap()
            assert page.locator('#position-text').inner_text() == '9 / 75 頁'
            for _ in range(4):
                page.locator('#previous').tap()
            assert page.locator('#position-text').inner_text() == '5 / 75 頁'
            page.keyboard.press('ArrowRight')
            assert page.locator('#position-text').inner_text() == '6 / 75 頁'
            assert page.evaluate('visualViewport.scale') == 1
            assert 'user-scalable=no' not in page.locator('meta[name="viewport"]').get_attribute('content')
            # Horizontal reading swipe; scripture scrolling and selected text do not turn pages.
            page.evaluate('''() => {
              const el=document.querySelector('#art');
              el.dispatchEvent(new TouchEvent('touchstart',{bubbles:true,touches:[new Touch({identifier:1,target:el,clientX:240,clientY:160})]}));
              el.dispatchEvent(new TouchEvent('touchend',{bubbles:true,changedTouches:[new Touch({identifier:1,target:el,clientX:100,clientY:162})]}));
            }''')
            assert page.locator('#position-text').inner_text() == '7 / 75 頁'
            page.select_option('#page-select', 'S06')
            saved_position = page.locator('#position-text').inner_text()
            if width > height:
                page.locator('#open-verse').click()
                assert page.locator('#verse-dialog').evaluate('(el)=>el.open')
                assert page.locator('#dialog-verse').inner_text() == page.locator('#verse').inner_text()
                assert page.locator('#dialog-source').get_attribute('href') == page.locator('#source-link').get_attribute('href')
                scroll = '.verse-scroll'
            else:
                scroll = '.verse-body'
            # Large text makes the original (unchanged) long verse require scrolling
            # on a phone, as it can with a user's accessibility text size.
            if width == 390 or height == 390:
                page.evaluate('document.documentElement.style.fontSize="24px"')
                settled(page)
            scrolling = page.locator(scroll).evaluate('el=>{el.scrollTop=el.scrollHeight;return {top:el.scrollTop,range:el.scrollHeight-el.clientHeight}}')
            if width == 390 or (width > height and height == 390):
                assert scrolling['range'] > 0 and scrolling['top'] > 0
            page.locator(scroll).focus()
            page.keyboard.press('ArrowRight')
            assert page.locator('#position-text').inner_text() == saved_position
            page.locator(scroll).evaluate('''el=>{
              el.dispatchEvent(new TouchEvent('touchstart',{bubbles:true,touches:[new Touch({identifier:2,target:el,clientX:240,clientY:160})]}));
              el.dispatchEvent(new TouchEvent('touchend',{bubbles:true,changedTouches:[new Touch({identifier:2,target:el,clientX:100,clientY:162})]}));
            }''')
            assert page.locator('#position-text').inner_text() == saved_position
            page.evaluate('document.documentElement.style.fontSize=""')
            if width > height:
                page.locator('#verse-dialog button').click()
                # Modal source lands on the appropriate open guide card.
                page.locator('#open-verse').click()
                page.locator('#dialog-source').click()
            else:
                page.locator('#source-link').click()
            assert page.url.endswith('/four-fruits-ten-fetters/#ea28-7')
            assert page.locator('#ea28-7 .source-text').is_visible()
            page.go_back()
            page.wait_for_function('typeof showPage === "function"')
            assert page.locator('#position-text').inner_text() == saved_position
            # Real return link and reload preserve position.
            page.locator('.top a').click()
            assert page.url.endswith('/four-fruits-ten-fetters/')
            page.locator('.book-cover').click()
            page.wait_for_function('typeof showPage === "function"')
            assert page.locator('#position-text').inner_text() == saved_position
            page.reload()
            page.wait_for_function('typeof showPage === "function"')
            assert page.locator('#position-text').inner_text() == saved_position
            page.set_viewport_size({'width': height, 'height': width})
            settled(page)
            assert page.locator('#position-text').inner_text() == saved_position
            page.set_viewport_size({'width': width, 'height': height})
            settled(page)
            if screenshots:
                for scene in BOOK['scenes']:
                    if width >= 768 and height >= 768 or scene['id'] in ['S02', 'S05', 'S09']:
                        page.evaluate('showPage', scene['start'])
                        settled(page)
                        screenshot(page, f'{scene["id"]}-{width}x{height}.webp')
            page.goto(base + 'four-fruits-ten-fetters/')
            assert page.locator('.guide-return').count() == 1
            assert page.locator('.guide-return').inner_text() == '回三十七道品修道地圖'
            assert page.locator('.source-entry').count() == 9
            assert page.locator('details').count() == 0
            assert page.locator('iframe').get_attribute('src').endswith('/n0bco_NPmRI')
            assert not page.evaluate('document.documentElement.scrollWidth > innerWidth')
            if screenshots and width == 768:
                screenshot(page, 'guide-768x1024.webp')
                page.locator('#sources').scroll_into_view_if_needed()
                screenshot(page, 'sources-768x1024.webp')
            context.close()
            report['viewports'].append({'width': width, 'height': height, 'pages': 74, 'interactions': 'passed'})
            print(f'{width}x{height}: all 74 pages / geometry / controls / scroll / rotation / persistence OK', flush=True)
        if not entrances_only:
            (OUT / 'reader-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
        # Verify homepage shelf/scene entrances and every prior reader still opens and turns.
        page = browser.new_page(viewport={'width': 1024, 'height': 768})
        page.on('pageerror', lambda e: report['javascriptErrors'].append(str(e)))
        # Chromium's native HTTPS path does not trust the managed proxy CA.
        # Fetch the exact public CDN resources with the system CA through urllib;
        # keep certificate verification enabled and do not replace them with mocks.
        cdn_responses = {}
        for url in ['https://cdn.tailwindcss.com/', 'https://unpkg.com/lucide@latest']:
            response = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30)
            cdn_responses[url] = (response.read(), response.headers.get('Content-Type', 'application/javascript'))
        def cdn_route(route):
            body, content_type = cdn_responses[route.request.url]
            route.fulfill(status=200, body=body, content_type=content_type)
        page.route('https://cdn.tailwindcss.com/**', cdn_route)
        page.route('https://unpkg.com/lucide@latest', cdn_route)
        page.goto(base)
        if screenshots:
            page.locator('#books').scroll_into_view_if_needed()
            screenshot(page, 'shelf-1024x768.webp')
        page.locator('.sz-book[href="./four-fruits-ten-fetters/book/"]').click()
        page.wait_for_function('typeof showPage === "function"')
        assert page.locator('#position-text').inner_text().endswith('/ 75 頁')
        page.goto(base)
        page.wait_for_function('typeof openModal === "function"')
        page.locator('[onclick*="openModal(\'四向四果\')"]').click()
        page.wait_for_function('getComputedStyle(document.querySelector("#detailModal")).opacity === "1"')
        if screenshots:
            screenshot(page, 'map-entry-1024x768.webp')
        page.locator('#modalBody a[href="./four-fruits-ten-fetters/"]').click()
        assert page.locator('h1').inner_text() == BOOK['title']
        assert page.locator('iframe').get_attribute('src').endswith('/n0bco_NPmRI')
        for name in ['four-truths', 'five-aggregates', 'six-senses', 'twelve-links', 'eightfold-path']:
            page.goto(base + name + '/book/')
            page.locator('#next').wait_for(state='visible')
            before = page.locator('#position-text').inner_text()
            page.locator('#next').click()
            assert page.locator('#position-text').inner_text() != before, name
            page.locator('.top a').click()
            assert urlsplit(page.url).path == '/' + name + '/', name
        browser.close()
    server.shutdown()
    assert not report['javascriptErrors'], report['javascriptErrors']
    assert not report['localHttpErrors'], report['localHttpErrors']
    report['existingReaders'] = 'all five opened, next-page and return-guide passed'
    (OUT / 'validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print('296 page states and existing book regression checks passed.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-sources', action='store_true')
    parser.add_argument('--screenshots', action='store_true')
    parser.add_argument('--entrances-only', action='store_true', help='Reuse saved reader checks when only the homepage/regression test changed.')
    args = parser.parse_args()
    check_static(args.verify_sources)
    check_browser(args.screenshots, args.entrances_only)
