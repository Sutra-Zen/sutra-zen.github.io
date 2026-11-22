#!/usr/bin/env python3
"""Focused first-public-/game/ validation using the original complete readers.

The full1192-step source reading check is preserved in its historical report.
This release walks the first198 original steps through the new public mount.
"""
from pathlib import Path
import argparse
from datetime import datetime, timezone
import functools
import hashlib
import http.server
import json
import re
import subprocess
import threading

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/previews/play-game-release'
MAIN_BASE = 'b9a0dad2c2c34d7e15e6dc5e55d6125de630f57b'
DRAFT_BASE = 'a2b3225'
SIZES = [(1280, 900), (390, 844), (844, 390), (768, 1024), (1024, 768)]
COLLECTION_KEY = 'sutrazen.play.collection.v1'
ORDER = ['four-truths', 'five-aggregates', 'six-senses', 'twelve-links',
         'eightfold-path', 'four-purities-six-recollections', 'mindfulness',
         'right-effort', 'anapana', 'iddhipada', 'four-jhanas',
         'five-roots-powers', 'seven-factors', 'four-fruits-ten-fetters']
MODULE_RE = re.compile(rb'<script type="module" src="\.\./\.\./play/(?:collection/)?reader-bridge\.js\?v=1"></script>\n?')


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def copyfile(self, source, destination):
        try:
            super().copyfile(source, destination)
        except (BrokenPipeError, ConnectionResetError):
            pass


def original_source_guard():
    paths = ORDER + ['docs/' + book for book in ORDER]
    files = subprocess.check_output(
        ['git', 'ls-tree', '-rz', '--name-only', MAIN_BASE, '--', *paths],
        cwd=ROOT, text=True,
    ).split('\0')
    files = [path for path in files if path]
    normalized_readers = []
    for path in files:
        original = subprocess.check_output(['git', 'show', MAIN_BASE + ':' + path], cwd=ROOT)
        current = (ROOT / path).read_bytes()
        if path.endswith('/book/index.html'):
            expected = 2 if path.split('/')[0] in ORDER[:3] else 1
            assert len(MODULE_RE.findall(current)) == expected, path
            assert MODULE_RE.sub(b'', current) == original, path
            normalized_readers.append({'path': path, 'permittedModuleTags': expected,
                                       'normalizedSha256': hashlib.sha256(original).hexdigest()})
        else:
            assert current == original, path
    root_paths = ['index.html', 'shelf.css', 'reader-controls.css', 'reader-layout.js',
                  'reader-restart.js', 'picture-panel-focus.js', 'picture-panel-focus.css',
                  'sitemap.xml', 'robots.txt', 'googlee0c995331ec518ae.html', 'docs/seo']
    changed = subprocess.check_output(['git', 'diff', '--name-only', MAIN_BASE, '--', *root_paths], cwd=ROOT, text=True).splitlines()
    assert not changed, changed
    core_paths = ['play/collection/store.js', 'play/collection/catalog.js',
                  'play/collection/reader.css', 'play/progress.js', 'play/reader-bridge.js',
                  'play/route/data.js', 'play/route/selectors.js', 'play/route/metadata.js']
    core_changed = subprocess.check_output(['git', 'diff', '--name-only', DRAFT_BASE, '--', *core_paths], cwd=ROOT, text=True).splitlines()
    assert not core_changed, core_changed
    bridge = (ROOT / 'play/collection/reader-bridge.js').read_text()
    original_bridge = subprocess.check_output(['git', 'show', DRAFT_BASE + ':play/collection/reader-bridge.js'], cwd=ROOT, text=True)
    public_return = """  const requestedReturn = new URLSearchParams(location.search).get('collectionReturn');
  const worldmapReturn = requestedReturn === 'worldmap-v4';
  const gameReturn = requestedReturn === 'game';
  const shelfURL = new URL(gameReturn ? '../../game/' : worldmapReturn ? '../worldmap-v4/' : '../visual-v2/shelf.html', import.meta.url);
  const returnLabel = worldmapReturn || gameReturn ? (await import('../worldmap-v4/text.js')).T.returnJourney : text.returnShelf;"""
    draft_return = """  const worldmapReturn = new URLSearchParams(location.search).get('collectionReturn') === 'worldmap-v4';
  const shelfURL = new URL(worldmapReturn ? '../worldmap-v4/' : '../visual-v2/shelf.html', import.meta.url);
  const returnLabel = worldmapReturn ? (await import('../worldmap-v4/text.js')).T.returnJourney : text.returnShelf;"""
    assert bridge.count(public_return) == 1
    assert bridge.replace(public_return, draft_return) == original_bridge
    return {'mainBaseline': MAIN_BASE, 'draftBaseline': DRAFT_BASE,
            'originalBookAndSourceFiles': len(files),
            'fourteenReaders': normalized_readers,
            'allOtherOriginalContent': 'byte-for-byte unchanged',
            'rootHomepageSeoGoogleAndControls': 'byte-for-byte unchanged',
            'collectionAndOldJourneyStoresAndRouteLogic': 'byte-for-byte unchanged',
            'readerBridge': 'Only collectionReturn=game destination/label branch; normalizing this block gives byte-exact draft bridge',
            'priorAllFourteenReadingEvidence': 'docs/previews/play-collection/validation.json:1192 original steps; unchanged core not fully re-walked'}


def settle(page):
    page.evaluate('()=>new Promise(done=>requestAnimationFrame(()=>requestAnimationFrame(done)))')


def no_overflow(page):
    settle(page)
    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1')


def observe(page, base, report):
    page.on('pageerror', lambda error: report['javascriptErrors'].append(str(error)))
    page.on('response', lambda response: report['httpErrors'].append(response.url) if response.url.startswith(base) and response.status >= 400 else None)


def fixture(completed=(), positions=None, active=None):
    return {'version': 1, 'completed': list(completed), 'positions': positions or {},
            'activeBook': active or ORDER[0]}


def restore_fixture(page, state):
    assert page.evaluate("""async state=>{
      const {store}=await import('/play/collection/store.js');
      return store.restoreBackup(JSON.stringify(state));
    }""", state)
    settle(page)


def native_core_hashes():
    paths = ['game/index.html', 'play/worldmap-v4/worldmap.js',
             'play/collection/catalog.js', 'play/collection/store.js',
             'play/collection/reader-bridge.js', 'play/route/data.js',
             'play/route/selectors.js', 'play/route/metadata.js']
    paths += [book + '/book/index.html' for book in ORDER[:3]]
    return {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in paths}


def native_first_three(browser, base, report, capture_feedback=False):
    started_hashes = native_core_hashes()
    context = browser.new_context(viewport={'width': 1280, 'height': 900}, reduced_motion='reduce')
    context.add_init_script("localStorage.setItem('sutrazen.play.v1','release-preserve-v1');localStorage.setItem('unrelated','release-preserve-other')")
    page = context.new_page()
    observe(page, base, report)
    page.goto(base + 'game/', wait_until='domcontentloaded')
    page.wait_for_selector('.wm-world')
    assert '0／14' in page.locator('#wm-count').inner_text()
    assert '未發布' not in page.locator('body').inner_text()
    page.screenshot(path=str(OUT / 'new-player-game-1280x900.png'), full_page=True)
    page.locator('[data-wm-next]').click()
    finished = []
    for book_id, total in zip(ORDER[:3], [29, 54, 115]):
        page.wait_for_function('(id)=>document.body?.dataset.collectionBook===id', arg=book_id)
        assert page.locator('body').get_attribute('data-collection-index') == '0'
        assert page.locator('body').get_attribute('data-collection-total') == str(total)
        assert 'collectionReturn=game' in page.url
        assert page.locator('.collection-reader-return').evaluate('e=>e.href') == base + 'game/'
        for index in range(1, total):
            page.locator('#next').click()
            page.wait_for_function('(n)=>document.body?.dataset.collectionIndex===String(n)', arg=index)
            if book_id == 'four-truths' and index == 5:
                page.reload(wait_until='domcontentloaded')
                page.wait_for_function('document.body?.dataset.collectionIndex==="5"')
                page.locator('.collection-reader-return').click()
                page.wait_for_url('**/game/**')
                page.wait_for_selector('.wm-world')
                assert '0／14' in page.locator('#wm-count').inner_text()
                page.locator('[data-wm-next]').click()
                page.wait_for_function('document.body?.dataset.collectionIndex==="5"')
            if book_id == 'five-aggregates' and index == 3:
                page.set_viewport_size({'width': 390, 'height': 844})
                settle(page)
                assert page.locator('body').get_attribute('data-collection-index') == '3'
                no_overflow(page)
                page.screenshot(path=str(OUT / 'native-reader-five-aggregates-390x844.png'), full_page=True)
                page.set_viewport_size({'width': 1024, 'height': 768})
                settle(page)
                assert page.locator('body').get_attribute('data-collection-index') == '3'
        assert page.locator('#next').inner_text().strip() == '完成這本'
        assert page.evaluate('(key)=>JSON.parse(localStorage.getItem(key)).completed', COLLECTION_KEY) == finished
        page.locator('#next').click()
        page.wait_for_url('**/game/**')
        page.wait_for_selector('#wm-dialog.wm-completion-dialog[open]')
        finished.append(book_id)
        assert page.evaluate('(key)=>JSON.parse(localStorage.getItem(key)).completed', COLLECTION_KEY) == finished
        assert page.locator('#wm-dialog .wm-compact-reward[data-completed-book="' + book_id + '"]').count() == 1
        assert page.locator('#wm-dialog .city-tactics-board').count() == 0
        assert f'{len(finished)}／14' in page.locator('#wm-count').inner_text()
        assert page.evaluate('SutraZenWorldmap.getState().status.city.stage') == len(finished)
        assert bool(page.locator('#wm-dialog .wm-success').count()) == (book_id == 'six-senses')
        assert page.locator('#wm-dialog [data-wm-city]').evaluate('e=>e.href') == base + 'play/city/'
        page.locator('#wm-dialog img').evaluate_all('els=>Promise.all(els.map(i=>i.decode()))')
        if capture_feedback:
            page.screenshot(path=str(OUT / f'native-complete-{book_id}.png'), full_page=True)
        next_id = ORDER[len(finished)]
        page.locator('#wm-dialog [data-wm-read="' + next_id + '"]').click()
    page.wait_for_function('document.body?.dataset.collectionBook==="twelve-links"')
    assert page.locator('body').get_attribute('data-collection-index') == '0'
    page.locator('.collection-reader-return').click()
    page.wait_for_selector('.wm-world')
    assert page.url == base + 'game/'
    assert page.evaluate("localStorage.getItem('sutrazen.play.v1')") == 'release-preserve-v1'
    assert page.evaluate("localStorage.getItem('unrelated')") == 'release-preserve-other'
    page.screenshot(path=str(OUT / 'native-three-completed-game.png'), full_page=True)
    assert started_hashes == native_core_hashes(), 'Reading runtime changed during the native flow'
    trace = {'entry': '/game/', 'steps': 198, 'books': ORDER[:3],
        'completionOnlyOnExplicitLastAction': True, 'compactFeedback': True,
        'cityStages': [1, 2, 3], 'nextBook': 'twelve-links step0',
        'reloadAndReturnResume': 'Four Truths step5',
        'rotation': 'Five Aggregates step3 at390x844 and1024x768',
        'oldJourneyAndUnrelatedKeys': 'preserved',
        'artworkBoundary': 'City art was pending; no city-art screenshot claim belongs to this reading trace',
        'recordedAtUtc': datetime.now(timezone.utc).isoformat(),
        'nativeCoreHashes': native_core_hashes()}
    report['nativeFirstThree'] = trace
    (OUT / 'native-first-three.json').write_text(json.dumps(trace, ensure_ascii=False, indent=2) + '\n')
    context.close()


def reuse_native_first_three(report):
    trace = json.loads((OUT / 'native-first-three.json').read_text())
    assert trace['steps'] == 198 and trace['books'] == ORDER[:3]
    assert trace['nativeCoreHashes'] == native_core_hashes(), 'Reading runtime changed; repeat native198-step flow before release'
    report['nativeFirstThree'] = trace
    report['nativeTraceReuse'] = 'Earlier actual198-step run reused after exact runtime hash comparison; only final art/anchor/label checks are run again'


def check_public_views(browser, base, report):
    context = browser.new_context(reduced_motion='reduce')
    page = context.new_page()
    observe(page, base, report)
    for width, height in SIZES:
        page.set_viewport_size({'width': width, 'height': height})
        page.goto(base + 'game/?mode=free', wait_until='domcontentloaded')
        page.wait_for_selector('.wm-world')
        restore_fixture(page, fixture())
        assert page.locator('script[type="module"]').first.evaluate('e=>e.src') == base + 'play/worldmap-v4/worldmap.js'
        assert not page.locator('.wm-art-details').is_visible()
        assert '未發布' not in page.locator('body').inner_text() and '[object Object]' not in page.locator('body').inner_text()
        assert re.sub(r'\s+', '', page.locator('[data-landmark="breathing_grove"]').inner_text()) == '安那般那與止觀竹林'
        assert re.sub(r'\s+', '', page.locator('[data-landmark="recollection_lighthouse"]').inner_text()) == '六念燈塔'
        assert page.locator('.wm-landmark').count() == 32
        page.locator('.wm-background').evaluate('i=>i.decode()')
        no_overflow(page)
        page.screenshot(path=str(OUT / f'game-free-map-{width}x{height}.png'), full_page=True)
        page.locator('[data-wm-zoom]').click()
        landmarks = page.locator('.wm-landmark').evaluate_all('els=>els.map(e=>({id:e.dataset.landmark,book:e.dataset.book}))')
        for landmark in landmarks:
            page.locator('[data-wm-landmark="' + landmark['id'] + '"]').click(timeout=5000)
            page.wait_for_selector('#wm-dialog[open]')
            if landmark['book']:
                assert page.locator('#wm-dialog [data-wm-read="' + landmark['book'] + '"]').count() == 1
                assert page.locator('#wm-dialog [data-wm-guide]').evaluate('e=>e.href') == base + landmark['book'] + '/'
            page.locator('[data-wm-close]').click()
        assert page.evaluate('(key)=>JSON.parse(localStorage.getItem(key)).completed.length', COLLECTION_KEY) == 0
        # Shared published routes intentionally retain their existing /play paths.
        page.locator('[data-game-nav="city"]').click()
        page.wait_for_url('**/play/city/**')
        page.wait_for_selector('.tactics-label')
        restore_fixture(page, fixture(ORDER))
        assert '未發布' not in page.locator('body').inner_text() and '[object Object]' not in page.locator('body').inner_text()
        assert page.locator('[data-game-nav="map"]').evaluate('e=>e.href') == base + 'game/'
        assert page.locator('#city-back-map').evaluate('e=>e.href') == base + 'game/'
        board = page.locator('#city-scene-host .city-tactics-board')
        art = page.evaluate("async()=>{const m=await import('/play/visual-v2/city-tactics.js');return {art:m.TACTICS_ART,hair:m.CITY_LORD_HAIR}}")
        assert [art['art']['width'], art['art']['height']] == [1671, 941]
        page.locator('.tactics-art').evaluate('i=>i.decode()')
        page.locator('svg image').evaluate_all("els=>Promise.all(els.map(i=>new Promise((resolve,reject)=>{const image=new Image();image.onload=resolve;image.onerror=reject;image.src=i.href.baseVal})))")
        assert page.locator('.tactics-label').count() == 14 and page.locator('.tactics-gate-hotspot').count() == 6
        for part, text in [('plaza', '地水火風四大廣場'), ('messengers', '止・觀使者'), ('message', '如實消息・涅槃')]:
            assert re.sub(r'\s+', '', page.locator('[data-city-label="' + part + '"] .tactics-label-text').inner_text()) == text
        assert page.locator('.tactics-label-text').evaluate_all('els=>els.every(e=>getComputedStyle(e).userSelect==="text"&&e.scrollWidth<=e.clientWidth+1)')
        maths = board.evaluate("""b=>{
          const r=b.getBoundingClientRect(),im=b.querySelector('.tactics-art').getBoundingClientRect(),svg=b.querySelector('.tactics-label-lines'),v=svg.viewBox.baseVal;
          const labels=[...b.querySelectorAll('[data-city-label]')].map(e=>{const p=b.querySelector('[data-label-for="'+e.dataset.cityLabel+'"]'),q=p.getPointAtLength(p.getTotalLength()),z=e.getBoundingClientRect();return{id:e.dataset.cityLabel,error:Math.hypot(z.x+z.width/2-r.x-q.x/v.width*r.width,z.y+z.height/2-r.y-q.y/v.height*r.height),inside:z.left>=r.left-1&&z.right<=r.right+1&&z.top>=r.top-1&&z.bottom<=r.bottom+1}});
          const p=b.querySelector('[data-label-for=message]'),a=p.getPointAtLength(0),z=p.getPointAtLength(p.getTotalLength());
          return {world:[r.width,r.height],image:[im.x-r.x,im.y-r.y,im.width,im.height],view:[v.width,v.height],labels,message:{start:[a.x,a.y],end:[z.x,z.y],length:p.getTotalLength()}};
        }""")
        assert maths['view'] == [1671, 941]
        assert abs(maths['world'][0] / maths['world'][1] - 1671/941) < .001
        assert all(abs(n) < 1 for n in maths['image'][:2])
        assert all(abs(a-b) < 1 for a,b in zip(maths['world'], maths['image'][2:]))
        assert all(label['error'] < 1 and label['inside'] for label in maths['labels']), maths['labels']
        m = maths['message']
        assert min(sum((a-b)**2 for a,b in zip(point,[1081,465]))**.5 for point in [m['start'],m['end']]) < 1
        assert m['length'] < 250, 'message label leader is not local to the open scroll'
        assert board.locator('.tactics-lord-hair [data-lord-facial-hair]').count() == 1
        before = page.evaluate('(key)=>localStorage.getItem(key)', COLLECTION_KEY)
        parts = page.locator('.tactics-label').evaluate_all('els=>els.map(e=>e.dataset.cityLabel)')
        for part in parts:
            page.locator('[data-city-label="' + part + '"]').click(timeout=5000)
            page.wait_for_selector('#city-dialog[open]')
            assert page.locator('#city-dialog [data-city-reread]').count() == 1
            assert 'SN 35.245' in page.locator('#city-dialog').inner_text()
            if part == 'lord':
                assert page.locator('#city-dialog [data-lord-facial-hair]').count() == 1
                if width in [1280,390]:
                    page.screenshot(path=str(OUT / f'city-lord-composite-{width}x{height}.png'), full_page=True)
            page.locator('[data-city-close]').click()
        assert page.evaluate('(key)=>localStorage.getItem(key)', COLLECTION_KEY) == before
        page.locator('#city-label-toggle').click()
        assert page.locator('.tactics-label').count() == 0
        page.locator('#city-label-toggle').click()
        assert page.locator('.tactics-label').count() == 14
        no_overflow(page)
        page.evaluate('window.scrollTo(0,0)')
        page.screenshot(path=str(OUT / f'city-full-labels-{width}x{height}.png'), full_page=True)
        page.locator('[data-game-nav="shelf"]').click()
        page.wait_for_selector('[data-book-card]')
        assert page.locator('[data-book-card]').count() == 14
        assert page.locator('[data-game-nav="map"]').evaluate('e=>e.href') == base + 'game/'
        assert '未發布' not in page.locator('body').inner_text()
        no_overflow(page)
        page.evaluate('window.scrollTo(0,document.body.scrollHeight)')
        settle(page)
        assert page.locator('header.sz-game-header').bounding_box()['y'] >= -1
        page.locator('[data-game-nav="map"]').click()
        page.wait_for_url('**/game/**')
        page.wait_for_selector('.wm-world')
        report.setdefault('layouts', []).append({'viewport':[width,height], 'mapNativeDialogs':32, 'cityNativeDialogs':14, 'fullRequestedLabels':True, 'cityNativeFrame':[1671,941], 'sixGates':True, 'hairLayerInSceneAndLordDialog':True, 'scrollLeaderNativeLength':m['length'], 'scrollEndpoint':[1081,465], 'nativeReturnToGame':True, 'horizontalOverflow':'none'})
    # The source page is a shared existing route with a native return to /game/.
    page.goto(base + 'play/city/')
    page.wait_for_selector('.tactics-label')
    page.locator('[data-city-label="message"]').click()
    page.locator('#city-dialog a').filter(has_text='查看城喻原經').click()
    page.wait_for_url('**/play/sources.html')
    assert '未發布' not in page.locator('body').inner_text()
    assert page.locator('.sz-city__gate').count() == 6
    page.locator('a.back').first.click()
    page.wait_for_url('**/game/**')
    page.wait_for_selector('.wm-world')
    report['sharedPublicRoutes'] = {'map':'/game/', 'city':'/play/city/', 'shelf':'/play/visual-v2/shelf.html', 'sources':'/play/sources.html', 'allMapReturnLinks':'/game/'}
    context.close()


def check_mode_isolation(browser, base, report):
    context = browser.new_context(viewport={'width': 390, 'height': 844}, reduced_motion='reduce')
    page = context.new_page()
    observe(page, base, report)
    page.goto(base + 'game/')
    page.wait_for_selector('.wm-world')
    v1 = {'version':1,'replayBook':None,'positions':{'four-truths':28},'freePositions':{'six-senses':6},'completed':['four-truths'],'activeBook':'five-aggregates','orderedBook':'five-aggregates','mode':'ordered','settings':{'locale':'zh-Hant','reducedMotion':False}}
    assert page.evaluate("async s=>{const {store}=await import('/play/progress.js');return store.restoreBackup(JSON.stringify(s))}",v1)
    v1_before = page.evaluate("localStorage.getItem('sutrazen.play.v1')")
    page.locator('[data-wm-mode="free"]').click()
    page.locator('[data-landmark="senses_lake"]').click()
    page.locator('#wm-dialog [data-wm-read="six-senses"]').click()
    page.wait_for_function('document.body?.dataset.collectionBook==="six-senses"')
    assert page.locator('body').get_attribute('data-collection-index') == '0'
    page.locator('#next').click()
    page.wait_for_function('document.body?.dataset.collectionIndex==="1"')
    page.locator('.collection-reader-return').click()
    page.wait_for_url('**/game/**')
    page.wait_for_selector('.wm-world')
    assert '0／14' in page.locator('#wm-count').inner_text()
    assert page.evaluate("localStorage.getItem('sutrazen.play.v1')") == v1_before
    page.locator('[data-wm-next]').click()
    page.wait_for_function('document.body?.dataset.collectionBook==="six-senses"&&document.body?.dataset.collectionIndex==="1"')
    # Native free chapter selection is allowed; reaching the final step alone is not completion.
    menu = page.locator('.controls select')
    last_option = menu.locator('option').last.get_attribute('value')
    menu.select_option(last_option)
    page.wait_for_function('document.body?.dataset.collectionIndex==="114"')
    assert page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).completed.length',COLLECTION_KEY) == 0
    page.locator('#next').click()
    page.wait_for_url('**/game/**')
    page.wait_for_selector('#wm-dialog[open]')
    assert page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).completed',COLLECTION_KEY) == ['six-senses']
    assert '1／14' in page.locator('#wm-count').inner_text()
    assert page.locator('#wm-dialog [data-wm-read="four-truths"]').count() == 1
    page.locator('[data-wm-close]').click()
    collection_before = page.evaluate('(k)=>localStorage.getItem(k)',COLLECTION_KEY)
    page.goto(base + 'six-senses/book/?journey=free')
    page.wait_for_function('document.body?.dataset.playBook==="six-senses"')
    assert page.locator('body').get_attribute('data-play-index') == '6'
    page.locator('#next').click()
    page.wait_for_function('document.body?.dataset.playIndex==="7"')
    assert page.evaluate('(k)=>localStorage.getItem(k)',COLLECTION_KEY) == collection_before
    page.goto(base + 'four-truths/book/?collection=1')
    page.wait_for_function('document.body?.dataset.collectionBook==="four-truths"')
    assert page.locator('.collection-reader-return').evaluate('e=>e.href') == base + 'play/visual-v2/shelf.html'
    page.locator('#next').click()
    page.wait_for_function('document.body?.dataset.collectionIndex==="1"')
    page.locator('.collection-reader-return').click()
    page.wait_for_selector('[data-book-card]')
    assert '1／14' in page.locator('#collection-count').inner_text()
    assert page.locator('[data-game-nav="map"]').evaluate('e=>e.href') == base + 'game/'
    collection_before = page.evaluate('(k)=>localStorage.getItem(k)',COLLECTION_KEY)
    journey_before = page.evaluate("localStorage.getItem('sutrazen.play.v1')")
    for book_id in ORDER[:3]:
        page.goto(base + book_id + '/book/')
        page.wait_for_selector('#next')
        assert page.locator('.collection-reader-return,.play-reader-return').count() == 0
        first = page.locator('#position-text').inner_text()
        page.locator('#next').click()
        assert page.locator('#position-text').inner_text() != first
        page.locator('#previous').click()
        assert page.locator('#position-text').inner_text() == first
        assert page.locator('#next').evaluate('e=>getComputedStyle(e).touchAction') == 'manipulation'
    assert page.evaluate('(k)=>localStorage.getItem(k)',COLLECTION_KEY) == collection_before
    assert page.evaluate("localStorage.getItem('sutrazen.play.v1')") == journey_before
    # The old draft mount remains usable and keeps its explicit legacy return target.
    page.goto(base + 'play/worldmap-v4/')
    page.wait_for_selector('.wm-world')
    assert page.locator('.wm-art-details').is_visible()
    page.locator('[data-wm-next]').click()
    page.wait_for_function('document.body?.dataset.collectionBook==="four-truths"')
    assert 'collectionReturn=worldmap-v4' in page.url
    assert page.locator('.collection-reader-return').evaluate('e=>e.href') == base + 'play/worldmap-v4/'
    page.locator('.collection-reader-return').click()
    page.wait_for_url('**/play/worldmap-v4/**')
    report['modeIsolation'] = {'freeGame':'Open/Next/return keeps0; native final-chapter selection does not complete; explicit finish earns only Six Senses1/14 and recommends Four Truths',
        'oldV1':'Distinct valid prior Four Truths completion and Six Senses free bookmark6 preserved by/game; old free reader resumes6→7 without changing collection',
        'ordinaryCollection':'Still returns to the shared shelf; shelf sea link points/game',
        'standalone':'First3 native Next/Previous and touch-action unchanged, no opt-in UI, neither store rewritten',
        'legacyDraftMount':'/play/worldmap-v4/ remains usable with its own collectionReturn target'}
    context.close()


def check_city_reading_and_feedback(browser, base, report):
    context = browser.new_context(viewport={'width':390,'height':844}, reduced_motion='reduce')
    page = context.new_page()
    observe(page, base, report)
    page.goto(base + 'play/city/')
    page.wait_for_selector('.tactics-label')
    page.locator('[data-city-label="lord"]').click()
    page.locator('[data-city-reread="five-aggregates"]').click()
    page.wait_for_function('document.body?.dataset.collectionBook==="five-aggregates"')
    assert 'collectionReturn=game' in page.url
    page.locator('#next').click()
    page.wait_for_function('document.body?.dataset.collectionIndex==="1"')
    page.reload(wait_until='domcontentloaded')
    page.wait_for_function('document.body?.dataset.collectionIndex==="1"')
    page.locator('.collection-reader-return').click()
    page.wait_for_url('**/game/**')
    page.wait_for_selector('[data-game-nav="city"]')
    page.locator('[data-game-nav="city"]').click()
    page.wait_for_selector('#city-continue')
    assert page.locator('#city-continue').get_attribute('data-city-resume-at') == '1'
    assert '0／14' in page.locator('#city-progress').inner_text()
    page.locator('#city-continue').click()
    page.wait_for_function('document.body?.dataset.collectionBook==="five-aggregates"&&document.body?.dataset.collectionIndex==="1"')
    page.locator('.collection-reader-return').click()
    page.wait_for_url('**/game/**')
    page.wait_for_selector('.wm-world')
    # Current final-art completion cards are explicitly labelled saved-state fixtures.
    for book_id, completed in [('four-truths',ORDER[:1]),('five-aggregates',ORDER[:2]),('six-senses',ORDER[:3]),('four-fruits-ten-fetters',ORDER)]:
        restore_fixture(page, fixture(completed))
        page.goto(base + 'game/?completed=' + book_id)
        page.wait_for_selector('#wm-dialog.wm-completion-dialog[open]')
        assert page.locator('#wm-dialog .wm-compact-reward[data-completed-book="' + book_id + '"]').count() == 1
        assert page.locator('#wm-dialog .city-tactics-board').count() == 0
        assert page.locator('#wm-dialog [data-wm-city]').evaluate('e=>e.href') == base + 'play/city/'
        assert f'{len(completed)}／14' in page.locator('#wm-count').inner_text()
        assert '未發布' not in page.locator('#wm-dialog').inner_text()
        if book_id == 'five-aggregates':
            assert page.locator('#wm-dialog [data-lord-facial-hair]').count() == 1
        if len(completed) < 14:
            assert page.locator('#wm-dialog [data-wm-read="' + ORDER[len(completed)] + '"]').count() == 1
        else:
            assert page.locator('#wm-dialog [data-wm-ending]').count() == 1
        page.locator('#wm-dialog svg image').evaluate_all("els=>Promise.all(els.map(i=>new Promise((resolve,reject)=>{const image=new Image();image.onload=resolve;image.onerror=reject;image.src=i.href.baseVal})))")
        page.screenshot(path=str(OUT / f'fixture-final-art-feedback-{book_id}-390x844.png'), full_page=True)
        page.locator('[data-wm-close]').click()
    assert page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).completed.length', COLLECTION_KEY) == 14
    report['cityReadingAndFinalArtFeedback'] = {'nativeCityReread':'Five Aggregates0→1/reload1, back/game, city primary resumes1 without completion', 'feedbackFixtures':['four-truths','five-aggregates','six-senses','four-fruits-ten-fetters'], 'hairLayerInFiveAggregatesReward':True,'compactOptionalCityEntry':True,'noFifteenthBook':True}
    context.close()


def check_storage_edges(browser, base, report):
    raw = json.dumps(fixture(ORDER[::-1], {id:index for index,id in enumerate(ORDER)},ORDER[-1]),ensure_ascii=False,indent=1)
    context = browser.new_context(reduced_motion='reduce')
    context.add_init_script('localStorage.setItem('+json.dumps(COLLECTION_KEY)+','+json.dumps(raw)+');localStorage.setItem("sutrazen.play.v1","preserve-existing-v1");localStorage.setItem("unrelated","keep")')
    page = context.new_page()
    observe(page,base,report)
    page.goto(base+'game/')
    page.wait_for_selector('.wm-world')
    for selector in ['[data-wm-mode="free"]','[data-wm-lines]','[data-wm-zoom]','[data-game-nav="city"]']:
        page.locator(selector).click()
    page.wait_for_selector('#city-progress')
    assert '14／14' in page.locator('#city-progress').inner_text()
    assert page.evaluate('(k)=>localStorage.getItem(k)',COLLECTION_KEY)==raw
    assert page.evaluate("localStorage.getItem('sutrazen.play.v1')")=='preserve-existing-v1'
    assert page.evaluate("localStorage.getItem('unrelated')")=='keep'
    context.close()
    for issue in ['corrupt','unavailable']:
        context=browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce')
        if issue=='corrupt':
            context.add_init_script('localStorage.setItem('+json.dumps(COLLECTION_KEY)+',"{broken-json")')
        else:
            context.add_init_script("Object.defineProperty(window,'localStorage',{configurable:true,get(){throw new DOMException('blocked','SecurityError')}})")
        page=context.new_page();observe(page,base,report)
        page.goto(base+'game/');page.wait_for_selector('.wm-world')
        assert page.locator('#wm-storage-notice').is_visible()
        if issue=='corrupt':assert page.evaluate('(k)=>localStorage.getItem(k)',COLLECTION_KEY)=='{broken-json'
        page.locator('[data-wm-next]').click()
        page.wait_for_function('document.body?.dataset.collectionBook==="four-truths"')
        warning=page.locator('.collection-reader-storage')
        if warning.count() and warning.is_visible():warning.locator('button').click()
        page.locator('#next').click();page.wait_for_function('document.body?.dataset.collectionIndex==="1"')
        context.close()
    report['storageEdges']={'existingFourteenBookSave':'Exact raw string preserved through public map controls/city; no automatic migration or clearing','corrupt':'Untouched on initial read-only mount; warning and original reader remain usable','unavailable':'Warning and reader Next usable; persistence is not promised','oldV1AndUnrelatedKeys':'preserved'}


def check_release_files(report):
    subprocess.run(['python3','-B','scripts/build-game-entry.py','--check'],cwd=ROOT,check=True,capture_output=True,text=True)
    config=(ROOT/'_config.yml').read_text()
    excludes=[line.strip()[2:] for line in config.splitlines() if line.strip().startswith('- ')]
    assert excludes and all(path.startswith('docs/previews/') for path in excludes)
    manifest=json.loads((ROOT/'docs/play/game-release/generated-assets.json').read_text())
    assets=[]
    for entry in manifest['assets']:
        path=ROOT/entry['path'];im=Image.open(path)
        assert [im.width,im.height]==[entry['width'],entry['height']]
        assert im.mode==entry['mode']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==entry['sha256']
        assert not any(entry['path']==excluded or entry['path'].startswith(excluded+'/') for excluded in excludes)
        assets.append({'path':entry['path'],'size':[im.width,im.height],'mode':im.mode,'sha256':entry['sha256']})
    model=json.loads((OUT/'model-check.json').read_text());assert model['result']=='passed' and model['subsets']==16384
    report['releaseFiles']={'gameBuilderCheck':'passed; single shell shares one runtime/store','pagesConfig':'Only docs/previews QA artifacts excluded; runtime and original sources stay included','excludedQaDirectories':excludes,'generatedAssets':assets,'modelCompletionSubsets':16384,'productionProof':'Exact merge SHA Pages success and live smoke handled separately'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reuse-native-reading', action='store_true', help='Reuse actual198-step trace only when all guarded reading runtime hashes match')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    report = original_source_guard()
    report.update({'phase': 'Local pre-publication validation; production status requires separate exact-SHA evidence',
                   'javascriptErrors': [], 'httpErrors': [],
                   'physicalSafari': 'Not tested; Chromium viewport simulation only',
                   'fixtures': 'Valid backups in disposable browser contexts exercise presentation, separately from the native198-step flow'})
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}/'
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
            if args.reuse_native_reading:
                reuse_native_first_three(report)
            else:
                native_first_three(browser, base, report)
            check_public_views(browser, base, report)
            check_mode_isolation(browser, base, report)
            check_city_reading_and_feedback(browser, base, report)
            check_storage_edges(browser, base, report)
            browser.close()
    finally:
        server.shutdown()
    check_release_files(report)
    assert not report['javascriptErrors'] and not report['httpErrors'], [report['javascriptErrors'],report['httpErrors']]
    (OUT / 'validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'result': 'passed', 'report': str((OUT / 'validation.json').relative_to(ROOT)), 'actualReadingSteps':report['nativeFirstThree']['steps'],'viewports':len(report['layouts']),'mapNativeDialogs':sum(v['mapNativeDialogs'] for v in report['layouts']),'cityNativeDialogs':sum(v['cityNativeDialogs'] for v in report['layouts']),'javascriptErrors':[],'localHttpErrors':[]}, ensure_ascii=False))


if __name__ == '__main__':
    main()
