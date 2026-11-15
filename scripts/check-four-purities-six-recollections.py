#!/usr/bin/env python3
"""Check book 07 source fidelity, actual-image overlays, touch navigation and legacy entrances."""
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
BASELINE = '31ebc8679723ab9908f771436bc0563cc4b04270'
DOCS = ROOT / 'docs/four-purities-six-recollections'
OUT = ROOT / 'docs/previews/four-purities-six-recollections'
BOOK = json.loads((ROOT / 'four-purities-six-recollections/book/book-data.js').read_text().split('const BOOK = ')[1].rstrip(';\n'))
STORY = json.loads((DOCS / 'storyboard.json').read_text())
SOURCES = json.loads((DOCS / 'verified-sources.json').read_text())
SIZES = [(390, 844), (844, 390), (768, 1024), (1024, 768)]


def old(path):
    return subprocess.check_output(['git', 'show', BASELINE + ':' + path], cwd=ROOT)


def normalized(text):
    return re.sub(r'\s+', '', text)


def static_checks(verify_sources):
    subprocess.run(['python', 'scripts/build-four-purities-six-recollections.py', '--check'], cwd=ROOT, check=True)
    for asset in json.loads((DOCS / 'assets-manifest.json').read_text()):
        assert Image.open(DOCS / asset['path']).size == (asset['width'], asset['height'])
    original = [dict(c, scene=s['id']) for s in STORY['scenes'] for c in s['topSubtitle']['cues']]
    corrections = DOCS / 'editorial-corrections.json'
    approved = json.loads(corrections.read_text()) if corrections.exists() else []
    assert len(original) == 93 and len(BOOK['pages']) == 95
    for expected, actual in zip(original, BOOK['pages'][:93]):
        text = expected['text']
        for c in approved:
            if c['scene'] == expected['scene'] and c['startSec'] == expected['startSec']:
                assert text == c['original']
                text = c['replacement']
        assert actual['lines'] == [text]
        assert actual['atSec'] == expected['startSec'] and actual['scene'] == expected['scene']
    assert BOOK['pages'][93]['end'] and BOOK['pages'][94]['afterword']
    assert BOOK['pages'][93]['image'] == BOOK['pages'][92]['image']
    for s, actual in zip(STORY['scenes'], BOOK['scenes']):
        assert actual['artOverlay'] == s['artOverlay']
    if verify_sources:
        texts = {}
        for source in SOURCES['files']:
            data = urllib.request.urlopen(source['url'], timeout=30).read()
            assert hashlib.sha256(data).hexdigest() == source['sha256']
            tree = html.fromstring(data)
            for ref in tree.xpath('//a[contains(@class,"ref")]'):
                ref.drop_tree()
            texts[source['id']] = normalized(tree.text_content())
        for q in SOURCES['quotes'].values():
            for block in q['blocks']:
                assert normalized(block) in texts[q['canon']]
    # Existing books, shared interfaces, and Pages configuration are untouched.
    existing = ['four-truths/', 'five-aggregates/', 'six-senses/', 'twelve-links/', 'eightfold-path/', 'four-fruits-ten-fetters/', '.github/']
    paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASELINE], cwd=ROOT, text=True).splitlines()
    for path in paths:
        if any(path.startswith(prefix) for prefix in existing) or path in ['CNAME', '.nojekyll', 'shelf.css', 'guide-header.css', 'guide-ui.css', 'reader-controls.css', 'reader-restart.js']:
            assert (ROOT / path).read_bytes() == old(path), path
    root_html = (ROOT / 'index.html').read_text()
    before, after = [json.loads(re.search(r'const dhammaData = (.*?);\s*\n', t)[1]) for t in [old('index.html').decode(), root_html]]
    for key in before:
        if key in ['四不壞淨', '六念']:
            assert before[key]['content'][:-6] in after[key]['content']
            assert './four-purities-six-recollections/' in after[key]['content']
        else:
            assert before[key] == after[key]
    tree = html.fromstring(root_html)
    assert len(tree.xpath('//ol[@class="sz-books"]/li')) == 14
    assert len(tree.xpath('//*[contains(concat(" ",@class," ")," sz-ready ")]')) == 7
    assert len(tree.xpath('//*[@class="sz-book-lock"]')) == 7
    assert tree.get_element_by_id('video-07').xpath('.//iframe')[0].get('src').endswith('/jCXyluhcEb0')
    assert tree.xpath('//iframe/@src') == html.fromstring(old('index.html')).xpath('//iframe/@src')
    guide = html.parse(str(ROOT / 'four-purities-six-recollections/index.html'))
    assert len(guide.xpath('//article[@class="source-entry"]')) == 4 and not guide.xpath('//details')
    assert '莊春江' in guide.xpath('//*[@id="sn55-1"]')[0].text_content()
    assert '溫柔起點' not in guide.getroot().text_content()
    for q in SOURCES['quotes'].values():
        card = guide.xpath('//*[@id=$id]', id=q['canon'].replace('.', '-'))[0]
        for block in q['blocks']:
            assert normalized(block) in normalized(card.text_content())
    for path in ['four-purities-six-recollections/index.html', 'four-purities-six-recollections/book/index.html']:
        local = html.parse(str(ROOT / path))
        for url in local.xpath('//@href|//@src'):
            u = urlsplit(url)
            if u.scheme or u.netloc:
                continue
            target = ((ROOT / path).parent / unquote(u.path)).resolve()
            if target.is_dir():
                target /= 'index.html'
            assert target.is_file(), (path, url)
            if u.fragment:
                assert html.parse(str(target)).xpath('//*[@id=$id]', id=u.fragment)
    print('Original 93 captions, 8 illustrations, reference hashes, sources, shelf and preservation: OK', flush=True)


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def copyfile(self, source, outputfile):
        try:
            super().copyfile(source, outputfile)
        except (BrokenPipeError, ConnectionResetError):
            pass  # A navigation may cancel the browser's preload request.


def settle(page):
    page.evaluate('() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))')
    page.wait_for_function('document.querySelector("#art-frame").hidden || (document.querySelector("#art").complete && document.querySelector("#art").naturalWidth > 0)')


def capture(page, name):
    Image.open(io.BytesIO(page.screenshot(type='png'))).save(OUT / name, lossless=True, method=6)


def overlap(a, b):
    return min(a['right'], b['right']) - max(a['left'], b['left']) > 1 and min(a['bottom'], b['bottom']) - max(a['top'], b['top']) > 1


def browser_checks(screenshots):
    OUT.mkdir(parents=True, exist_ok=True)
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}/'
    report = {'baseline': BASELINE, 'pageChecks': 0, 'viewports': [], 'javascriptErrors': [], 'localHttpErrors': [], 'realIPadSafari': 'not tested'}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        for width, height in SIZES:
            page = browser.new_page(viewport={'width': width, 'height': height}, has_touch=True)
            page.on('pageerror', lambda e: report['javascriptErrors'].append(str(e)))
            page.on('response', lambda r: report['localHttpErrors'].append(r.url) if r.url.startswith(base) and r.status >= 400 else None)
            page.goto(base + 'four-purities-six-recollections/book/')
            page.wait_for_function('typeof showPage === "function"')
            frames = {}
            for i, expected in enumerate(BOOK['pages']):
                page.evaluate('showPage', i)
                settle(page)
                r = page.evaluate('''() => {
                    const $=s=>document.querySelector(s), rect=s=>$(s).getBoundingClientRect().toJSON();
                    return {caption:$('#narration').textContent,verse:$('#verse').textContent,number:$('#position-text').textContent,
                    color:getComputedStyle($('#caption')).color,align:getComputedStyle($('#caption')).textAlign,
                    art:rect('#art-frame'),captionRect:rect('#caption'),scripture:rect('.scripture'),previous:rect('#previous'),next:rect('#next'),back:rect('.top a'),menu:rect('.position'),
                    natural:[$('#art').naturalWidth,$('#art').naturalHeight],artHidden:$('#art-frame').hidden,
                    overlays:[...document.querySelectorAll('.art-overlay')].map(el=>({text:el.textContent,rect:el.getBoundingClientRect().toJSON(),font:parseFloat(getComputedStyle(el).fontSize)})),
                    shade:!$('#closing-shade').hidden,shadeColor:getComputedStyle($('#closing-shade')).backgroundColor,
                    overflow:document.documentElement.scrollWidth>innerWidth,touch:getComputedStyle($('#next')).touchAction,
                    nextLabel:$('#next').getAttribute('aria-label')};
                }''')
                assert r['caption'] == ''.join(expected['lines'])
                assert r['verse'] == '\n'.join(filter(None, [expected['verseLabel'], expected['verse']]))
                assert r['number'] == f'{i + 1} / 95 頁'
                assert not r['overflow'] and r['touch'] == 'manipulation'
                plan = next(s for s in BOOK['scenes'] if s['id'] == expected['scene'])
                overlays = plan['artOverlay']
                assert len(r['overlays']) == len(overlays)
                if expected['image']:
                    assert r['natural'] == expected['dimensions']
                    art = r['art']
                    assert abs(art['width'] / art['height'] - expected['dimensions'][0] / expected['dimensions'][1]) < .005
                    if not expected.get('end'):
                        assert r['color'] == 'rgb(17, 17, 17)' and r['align'] == 'left'
                        assert art['top'] >= r['captionRect']['bottom'] - 1
                        assert art['bottom'] <= r['scripture']['top'] + 1
                    else:
                        assert r['shade'] and r['shadeColor'] == 'rgba(0, 0, 0, 0.65)'
                        assert r['overlays'][0]['text'].count('\n') == 1
                    if width > height:
                        for control in ['previous', 'next', 'back', 'menu']:
                            assert not overlap(art, r[control]), (width, i, control)
                        assert 0 <= art['top'] < art['bottom'] <= height
                    for actual, o in zip(r['overlays'], overlays):
                        box = actual['rect']
                        assert actual['text'] == o['text']
                        assert abs(box['x'] + box['width'] / 2 - art['x'] - art['width'] * o['xPct'] / 100) < 1
                        assert abs(box['y'] + box['height'] / 2 - art['y'] - art['height'] * o['yPct'] / 100) < 1
                        assert abs(actual['font'] - art['width'] * o['fontSizePctOfImageWidth'] / 100) < .1
                        assert box['left'] >= art['left'] - 1 and box['right'] <= art['right'] + 1
                        assert box['top'] >= art['top'] - 1 and box['bottom'] <= art['bottom'] + 1
                    signature = tuple(round(art[k], 1) for k in ['x', 'y', 'width', 'height'])
                    if expected['scene'] in frames:
                        assert signature == frames[expected['scene']], (width, i, 'image jumps')
                    frames[expected['scene']] = signature
                else:
                    assert r['artHidden'] and r['nextLabel'] == '回到第一頁'
                report['pageChecks'] += 1
            # End-page restart and normal following pages use shared controls.
            page.locator('#next').tap()
            assert page.locator('#position-text').inner_text() == '1 / 95 頁'
            assert page.locator('#previous').is_disabled()
            for _ in range(8):
                page.locator('#next').tap()
            assert page.locator('#position-text').inner_text() == '9 / 95 頁'
            assert page.evaluate('visualViewport.scale') == 1
            page.locator('#previous').tap()
            page.keyboard.press('ArrowRight')
            assert page.locator('#position-text').inner_text() == '9 / 95 頁'
            for scene in BOOK['scenes']:
                page.select_option('#page-select', scene['id'])
                assert page.locator('#position-text').inner_text() == f'{scene["start"] + 1} / 95 頁'
            # Full scripture opens in both orientations, scrolls, and links to its source card.
            page.select_option('#page-select', 'S06')
            position = page.locator('#position-text').inner_text()
            page.locator('#open-verse').click()
            assert page.locator('#verse-dialog').evaluate('el=>el.open')
            assert page.locator('#dialog-verse').inner_text() == page.locator('#verse').inner_text()
            if width == 390 or height == 390:
                page.evaluate('document.documentElement.style.fontSize="28px"')
                settle(page)
            scroll = page.locator('.verse-scroll').evaluate('el=>{el.scrollTop=el.scrollHeight;return {top:el.scrollTop,range:el.scrollHeight-el.clientHeight}}')
            if height == 390:
                assert scroll['range'] > 0 and scroll['top'] > 0
            page.keyboard.press('ArrowRight')
            assert page.locator('#position-text').inner_text() == position
            page.locator('.verse-scroll').evaluate('''el=>{
                el.dispatchEvent(new TouchEvent('touchstart',{bubbles:true,touches:[new Touch({identifier:1,target:el,clientX:240,clientY:120})]}));
                el.dispatchEvent(new TouchEvent('touchend',{bubbles:true,changedTouches:[new Touch({identifier:1,target:el,clientX:90,clientY:122})]}));
            }''')
            assert page.locator('#position-text').inner_text() == position
            page.evaluate('document.documentElement.style.fontSize=""')
            page.locator('#dialog-source').click()
            assert page.url.endswith('/four-purities-six-recollections/#sn55-1')
            assert page.locator('#sn55-1 .source-text').is_visible()
            page.go_back()
            page.wait_for_function('typeof showPage === "function"')
            assert page.locator('#position-text').inner_text() == position
            page.locator('.top a').click()
            page.locator('.book-cover').click()
            page.wait_for_function('typeof showPage === "function"')
            assert page.locator('#position-text').inner_text() == position
            page.reload()
            page.wait_for_function('typeof showPage === "function"')
            assert page.locator('#position-text').inner_text() == position
            page.set_viewport_size({'width': height, 'height': width})
            settle(page)
            assert page.locator('#position-text').inner_text() == position
            page.set_viewport_size({'width': width, 'height': height})
            settle(page)
            if screenshots and width >= 768 and height >= 768:
                for scene in BOOK['scenes']:
                    page.select_option('#page-select', scene['id'])
                    settle(page)
                    capture(page, f'{scene["id"]}-{width}x{height}.webp')
            page.goto(base + 'four-purities-six-recollections/')
            assert page.locator('.guide-return').inner_text() == '回三十七道品修道地圖'
            assert page.locator('.source-entry').count() == 4 and page.locator('details').count() == 0
            assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
            if screenshots and width == 768:
                capture(page, 'guide-768x1024.webp')
            page.close()
            report['viewports'].append({'width': width, 'height': height, 'pages': 95, 'interactions': 'passed'})
            print(f'{width}x{height}: all 95 states, overlay geometry, restart, modal, sources and rotation OK', flush=True)
        page = browser.new_page(viewport={'width': 1024, 'height': 768})
        page.on('pageerror', lambda e: report['javascriptErrors'].append(str(e)))
        # Use system-CA-verified public CDN responses: Chromium does not trust the proxy CA.
        cached = {}
        for url in ['https://cdn.tailwindcss.com/', 'https://unpkg.com/lucide@latest']:
            response = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30)
            cached[url] = (response.read(), response.headers.get('Content-Type', 'application/javascript'))
        def cdn(route):
            data, content_type = cached[route.request.url]
            route.fulfill(status=200, body=data, content_type=content_type)
        page.route('https://cdn.tailwindcss.com/**', cdn)
        page.route('https://unpkg.com/lucide@latest', cdn)
        page.goto(base)
        page.locator('.sz-book[href="./four-purities-six-recollections/book/"]').click()
        page.wait_for_function('typeof showPage === "function"')
        assert page.locator('#position-text').inner_text().endswith('/ 95 頁')
        for key in ['四不壞淨', '六念']:
            page.goto(base)
            page.evaluate('key=>openModal(key)', key)
            page.locator('#modalBody a[href="./four-purities-six-recollections/"]').click()
            assert page.locator('h1').inner_text() == BOOK['title']
        for name in ['four-truths', 'five-aggregates', 'six-senses', 'twelve-links', 'eightfold-path', 'four-fruits-ten-fetters']:
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
    assert not report['localHttpErrors'], report['localHttpErrors']
    report['existingReaders'] = 'all six opened, next-page and return passed'
    (OUT / 'validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print('380 page states / four sizes / all six legacy entrances passed.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-sources', action='store_true')
    parser.add_argument('--screenshots', action='store_true')
    args = parser.parse_args()
    static_checks(args.verify_sources)
    browser_checks(args.screenshots)
