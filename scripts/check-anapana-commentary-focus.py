#!/usr/bin/env python3
"""Scoped regression for the author's quiet-place/scripture/comic corrections."""
import functools, hashlib, http.server, io, json, subprocess, threading
from pathlib import Path
from lxml import html
from PIL import Image
from playwright.sync_api import sync_playwright

R = Path(__file__).resolve().parents[1]
BASE = '623bc69a98f220f1ab5fd06f0c2b6f21a555de33'
O = R / 'docs/previews/anapana-commentary-focus'
O.mkdir(parents=True, exist_ok=True)
def load(raw, key):
    return json.loads(raw.split('const ' + key + ' = ')[1].rstrip(';\n'))
def before(path):
    return subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=R)

subprocess.run(['python3', 'scripts/build-anapana.py', '--check'], cwd=R, check=True)
book = load((R / 'anapana/book/book-data.js').read_text(), 'BOOK')
old = load(before('anapana/book/book-data.js').decode(), 'BOOK')
focus = load((R / 'anapana/book/panel-focus-data.js').read_text(), 'PANEL_FOCUS')['scenes']
assert book['scenes'] == old['scenes'] and len(book['pages']) == 119
label_ids = {'Q10', 'Q15', 'Q20', 'Q25', 'Q26'}
for item, original in zip(book['pages'], old['pages']):
    expected = json.loads(json.dumps(original))
    if item.get('paragraphId') == 'S02-P06':
        expected['quotes'] = [{'quoteId': 'sa803', 'source': '《雜阿含經》第803經',
          'text': '或入林中、閑房、樹下，或空露地，端身正坐，繫念面前。',
          'relation': '原文對讀', 'verification': 'canonical/sa803.html；節錄末標點作句號'}]
        expected['sourceNote'] = None
    for quote in expected['quotes']:
        if quote['quoteId'] in label_ids:
            quote['source'] = quote['source'].replace('（影片譯文）', '')
    assert item == expected, item.get('paragraphId')
assert '（影片譯文）' not in json.dumps(book, ensure_ascii=False)
original_focus = load(before('anapana/book/panel-focus-data.js').decode(), 'PANEL_FOCUS')['scenes']
assert all(focus[s] == value for s, value in original_focus.items())
quiet = next(p for p in book['pages'] if p.get('paragraphId') == 'S02-P06')
canonical = R / 'docs/anapana/canonical/sa803.html'
record = next(x for x in json.loads((R / 'docs/anapana/verified-sources.json').read_text())['files'] if x['id'] == 'sa803')
assert hashlib.sha256(canonical.read_bytes()).hexdigest() == record['sha256']
tree = html.parse(str(canonical))
for a in tree.xpath('//a[contains(@class,"ref")]'): a.drop_tree()
assert quiet['quotes'][0]['text'][:-1] in tree.getroot().text_content()
# Author-reviewed mapping, separate from the implementation's focus data.
expected_focus = {'S10': [None]*2 + ['p1']*2 + ['p2']*3 + ['p3']*4 + ['p4']*3,
                  'S11': ['p1']*4 + ['p2']*3 + ['p3']*2 + [None]*3}
for s, expected in expected_focus.items():
    assert focus[s]['pages'] == expected
    assert focus[s]['paragraphIds'] == [p['paragraphId'] for p in book['pages'] if p['scene'] == s]
# Preserve every source/illustration and all other books/shared files.
for path in subprocess.check_output(['git','ls-tree','-r','--name-only','-z',BASE],cwd=R,text=True).rstrip('\0').split('\0'):
    if path.startswith(('docs/', 'scripts/', 'anapana/book/')): continue
    assert (R/path).read_bytes() == before(path), path

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args): pass
server = http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)))
threading.Thread(target=server.serve_forever,daemon=True).start()
url = f'http://127.0.0.1:{server.server_port}/'
report = {'baseline': BASE, 'pageStates':0, 'mainControlComicStates':0, 'zoomStates':0,
          'errors':[], 'httpErrors':[], 'viewports':[], 'physicalSafari':'not tested'}
def settle(page):
    page.wait_for_function('document.querySelector("#art-frame").hidden || (document.querySelector("#art").complete && document.querySelector("#art").naturalWidth>0)')
    page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
def check_mask(page, root, sid, local):
    definition = focus.get(sid)
    active = definition['pages'][local-1] if definition else None
    mask = page.locator(root+' .picture-panel-focus')
    assert mask.is_visible() == bool(active)
    if not active: return
    assert mask.get_attribute('data-active-panel') == active
    assert mask.locator('span.active').count() == 1
    assert mask.locator('span:not(.active)').count() == len(definition['panels'])-1
    dims = mask.evaluate('e=>({r:e.getBoundingClientRect().toJSON(),cells:[...e.children].map(c=>({r:c.getBoundingClientRect().toJSON(),color:getComputedStyle(c).backgroundColor,active:c.classList.contains("active")}))})')
    art = page.locator('#zoom-art' if root == '#zoom-frame' else '#art').bounding_box()
    assert abs(dims['r']['width']/dims['r']['height']-1672/941)<.002
    assert abs(dims['r']['width']-art['width'])<1 and abs(dims['r']['height']-art['height'])<1
    for cell, spec in zip(dims['cells'],definition['panels']):
        for axis, extent in [('x','width'),('y','height')]:
            assert abs(cell['r'][axis]-dims['r'][axis]-dims['r'][extent]*spec[axis]/100)<1
        assert cell['color'] == ('rgba(0, 0, 0, 0)' if cell['active'] else 'rgba(5, 12, 20, 0.76)')

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for w,h in [(360,800),(800,360),(768,1024),(1024,768),(1440,900)]:
        page = browser.new_page(viewport={'width':w,'height':h},has_touch=True)
        page.on('pageerror',lambda e:report['errors'].append(str(e)))
        page.on('response',lambda r: report['httpErrors'].append(r.url) if r.url.startswith(url) and r.status>=400 else None)
        page.route('https://www.youtube.com/**',lambda r:r.abort())
        page.goto(url+'anapana/book/'); page.wait_for_function('typeof showPage==="function"')
        for i,item in enumerate(book['pages']):
            page.evaluate('i=>showPage(i)',i); settle(page)
            assert page.locator('#narration p').all_text_contents() == item['lines']
            assert page.locator('#verse blockquote').all_text_contents() == [q['text'] for q in item['quotes']]
            assert page.locator('#verse h3').all_text_contents() == [q['source'] for q in item['quotes']]
            assert page.locator('#position-text').inner_text() == f'{i+1} / 119 頁'
            assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
            if item['image']:
                check_mask(page,'#art-frame',item['scene'],item['paragraphNumber'])
                assert page.locator('#caption').bounding_box()['y']+page.locator('#caption').bounding_box()['height'] <= page.locator('#art').bounding_box()['y']+1
            report['pageStates']+=1
        # Actual previous/next buttons must follow the same paragraphs/masks.
        page.select_option('#page-select','S10')
        for sid in ['S10','S11']:
            for local in range(1,len(expected_focus[sid])+1):
                settle(page); assert page.locator('.page').get_attribute('data-paragraph') == f'{sid}-P{local:02}'
                check_mask(page,'#art-frame',sid,local)
                page.locator('#next').click(); report['mainControlComicStates']+=1
        page.select_option('#page-select','S10'); page.locator('#previous').click()
        assert page.locator('.page').get_attribute('data-scene')=='S09'
        assert page.locator('#art-frame .picture-panel-focus').is_hidden()
        for sid in ['S10','S11']:
            for panel in focus[sid]['panels']:
                local = expected_focus[sid].index(panel['id'])+1
                i = next(i for i,x in enumerate(book['pages']) if x.get('paragraphId')==f'{sid}-P{local:02}')
                page.evaluate('i=>showPage(i)',i);settle(page)
                if sid=='S10':
                    narrow=page.locator('#art-frame').bounding_box()['width']<600
                    assert page.locator('#outside-labels').is_visible()==(narrow and panel['id']=='p3')
                if (w,h) in [(768,1024),(1024,768)]:
                    Image.open(io.BytesIO(page.screenshot())).save(O/f'{sid}-{panel["id"]}-{w}x{h}.webp',lossless=True,method=6)
                page.locator('#art').click();page.wait_for_function('document.querySelector("#zoom-art").complete && document.querySelector("#zoom-art").naturalWidth>0');settle(page)
                check_mask(page,'#zoom-frame',sid,local);report['zoomStates']+=1
                page.locator('#image-dialog form button').click()
                page.set_viewport_size({'width':h,'height':w});settle(page)
                assert page.locator('.page').get_attribute('data-paragraph')==f'{sid}-P{local:02}'
                check_mask(page,'#art-frame',sid,local)
                page.set_viewport_size({'width':w,'height':h})
        page.select_option('#page-select','S02')
        for _ in range(5):page.locator('#next').tap()
        assert page.locator('.page').get_attribute('data-paragraph')=='S02-P06'
        assert page.evaluate('visualViewport.scale')==1
        assert page.locator('#next').evaluate('e=>getComputedStyle(e).touchAction')=='manipulation'
        assert page.locator('#source-link').get_attribute('href')=='../index.html#sa803'
        assert not page.locator('#verse .source-note').count()
        if (w,h) in [(768,1024),(1024,768)]:
            Image.open(io.BytesIO(page.screenshot())).save(O/f'quiet-place-{w}x{h}.webp',lossless=True,method=6)
        page.locator('#open-verse').click()
        assert quiet['quotes'][0]['text'] in page.locator('#dialog-verse').inner_text()
        page.locator('#dialog-source').click(); assert page.url.endswith('#sa803')
        assert page.locator('#sa803').is_visible()
        page.go_back();page.wait_for_function('typeof showPage==="function"')
        assert page.locator('.page').get_attribute('data-paragraph')=='S02-P06'
        page.reload();page.wait_for_function('typeof showPage==="function"')
        assert page.locator('.page').get_attribute('data-paragraph')=='S02-P06'
        page.locator('.top a').click();assert page.url==url+'anapana/index.html'
        page.goto(url+'anapana/book/');page.wait_for_function('typeof showPage==="function"')
        page.locator('.reading-links a').last.click();assert page.url==url+'index.html'
        report['viewports'].append([w,h]);page.close();print(w,h,'passed',flush=True)
    browser.close()
server.shutdown()
assert report['pageStates']==595 and report['mainControlComicStates']==130 and report['zoomStates']==35
assert not report['errors'] and not report['httpErrors']
(O/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('595 page states / 130 main-button comic states / 35 zoom+rotation states passed',flush=True)
