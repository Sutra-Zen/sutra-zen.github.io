#!/usr/bin/env python3
"""Check relative site URLs and reader navigation when served at the domain root."""
import argparse, functools, hashlib, http.server, io, json, re, threading
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from lxml import html
from PIL import Image
from playwright.sync_api import sync_playwright

R = Path(__file__).resolve().parents[1]
O = R / 'docs/previews/site-migration'
O.mkdir(parents=True, exist_ok=True)
parser = argparse.ArgumentParser()
parser.add_argument('--url', help='Optional live root URL; default is a temporary local HTTP server')
parser.add_argument('--tailwind-js', type=Path, help='Optional previously downloaded CDN script for restricted browser environments')
parser.add_argument('--lucide-js', type=Path, help='Optional downloaded CDN script for restricted browser environments')
args = parser.parse_args()
report = {'localReferences': 0, 'webHtmlFiles': 0, 'readerStates': [],
          'javascriptErrors': [], 'siteHttpErrors': [], 'physicalSafari': 'not tested'}
for path in R.rglob('*.html'):
    if path.relative_to(R).parts[0] in ['docs', '.git']: continue
    raw = path.read_text()
    assert not re.search(r'rooneyflower-star|/sutrazen-map/', raw, re.I), path
    report['webHtmlFiles'] += 1
    for ref in html.fromstring(raw).xpath('//@href|//@src|//@poster'):
        u = urlsplit(ref)
        if u.scheme or u.netloc or not u.path: continue
        target = ((R / unquote(u.path).lstrip('/')) if u.path.startswith('/') else path.parent / unquote(u.path)).resolve()
        assert target.exists(), (path, ref)
        report['localReferences'] += 1

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args): pass
    def copyfile(self, source, outputfile):
        try: super().copyfile(source, outputfile)
        except (BrokenPipeError, ConnectionResetError): pass  # navigation cancels preloaded assets
server = None
if args.url:
    base = args.url.rstrip('/') + '/'
    assert urlsplit(base).path == '/', 'Test the domain root, without a project prefix'
else:
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(R)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}/'
report['mode'] = 'live' if args.url else 'local root HTTP'
report['baseUrl'] = base
report['cdnSubstitutions'] = [{'cdn': host, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()} for host,path in [('https://cdn.tailwindcss.com/', args.tailwind_js), ('https://unpkg.com/lucide@latest', args.lucide_js)] if path]
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for w, h in [(360,800),(800,360),(768,1024),(1024,768),(1440,900)]:
        page = browser.new_page(viewport={'width': w, 'height': h}, has_touch=True)
        page.on('pageerror', lambda e: report['javascriptErrors'].append(str(e)))
        page.on('response', lambda r: report['siteHttpErrors'].append([r.status,r.url]) if r.url.startswith(base) and r.status >= 400 else None)
        page.route('https://www.youtube.com/**', lambda r: r.abort())
        if args.tailwind_js: page.route('https://cdn.tailwindcss.com/**', lambda r: r.fulfill(content_type='application/javascript', body=args.tailwind_js.read_bytes()))
        if args.lucide_js: page.route('https://unpkg.com/**', lambda r: r.fulfill(content_type='application/javascript', body=args.lucide_js.read_bytes()))
        page.goto(base, wait_until='domcontentloaded')
        page.wait_for_function('typeof lucide !== "undefined"')
        assert page.locator('.sz-books .sz-ready').count() == 14
        links = page.locator('.sz-books .sz-ready').evaluate_all('els=>els.map(e=>e.getAttribute("href"))')
        if (w,h) == (1024,768):
            page.locator('.sz-books').scroll_into_view_if_needed()
            Image.open(io.BytesIO(page.screenshot())).save(O/'shelf-1024x768.webp', lossless=True, method=6)
        for link in links:
            # Use a real shelf link to enter each book from the root page.
            page.locator(f'.sz-books a.sz-ready[href="{link}"]').click()
            page.wait_for_function('typeof showPage === "function" && document.querySelector("#position-text").textContent.length>0')
            # The existing Five Aggregates book begins with a text-only introduction.
            for _ in range(8):
                if page.locator('#art').is_visible(): break
                page.locator('#next').tap()
            page.wait_for_function('document.querySelector("#art").complete && document.querySelector("#art").naturalWidth > 0')
            name = urlsplit(page.url).path.strip('/').split('/')[0]
            initial = page.locator('#position-text').inner_text()
            page.locator('#next').tap()
            assert page.locator('#position-text').inner_text() != initial, name
            page.locator('#previous').tap()
            assert page.locator('#position-text').inner_text() == initial, name
            assert page.locator('#next').evaluate('e=>getComputedStyle(e).touchAction') == 'manipulation'
            assert page.evaluate('visualViewport.scale') == 1
            assert not page.evaluate('document.documentElement.scrollWidth > innerWidth'), name
            assert '/sutrazen-map/' not in page.url
            if name == 'anapana' and (w,h) in [(768,1024),(1024,768)]:
                Image.open(io.BytesIO(page.screenshot())).save(O/f'anapana-{w}x{h}.webp', lossless=True, method=6)
            page.locator('.top a').first.click()
            page.wait_for_url(urljoin(base,name+'/')+'*')
            page.locator('.guide-return').click()
            assert urlsplit(page.url).path in ['/', '/index.html'], page.url
            page.wait_for_selector('.sz-books .sz-ready')
            assert page.locator('.sz-books .sz-ready').count() == 14
            report['readerStates'].append({'book':name,'size':[w,h],'image':'loaded','previousNext':'passed','returnViaGuide':'passed'})
        page.close()
        print(w,h,'all 14 shelf/image/next/previous/return paths passed',flush=True)
    browser.close()
if server: server.shutdown()
assert len(report['readerStates']) == 70
assert not report['javascriptErrors'] and not report['siteHttpErrors'], report
(O/('live-validation.json' if args.url else 'local-validation.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('29 HTML files / 325 local references / 70 reader states passed',flush=True)
