#!/usr/bin/env python3
"""Targeted independent-city / fixed-navigation / coastal-line regression QA.

The unchanged 1192-step readers and r3 model retain their prior full coverage.
This round performs one genuine Four Truths completion, not another full walk.
"""
from pathlib import Path
import functools
import hashlib
import http.server
import json
import subprocess
import threading

from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/previews/play-city-entry'
BASE = 'fd7d44c'
SIZES = [(1280, 900), (390, 844), (844, 390), (768, 1024), (1024, 768)]
ORDER = ['four-truths', 'five-aggregates', 'six-senses', 'twelve-links',
         'eightfold-path', 'four-purities-six-recollections', 'mindfulness',
         'right-effort', 'anapana', 'iddhipada', 'four-jhanas',
         'five-roots-powers', 'seven-factors', 'four-fruits-ten-fetters']
COLLECTION_KEY = 'sutrazen.play.collection.v1'
CITY_BOOKS = {
    **{gate: 'six-senses' for gate in ['eye', 'ear', 'nose', 'tongue', 'body', 'mind']},
    **{part: 'five-aggregates' for part in ['town', 'plaza', 'lord']},
    'guardian': 'mindfulness', 'messengers': 'anapana', 'message': 'six-senses',
    'road': 'eightfold-path', 'dock': 'four-truths',
}


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def copyfile(self, source, destination):
        try:
            super().copyfile(source, destination)
        except (BrokenPipeError, ConnectionResetError):
            pass


def protect_originals():
    paths = ORDER + ['docs/' + book for book in ORDER] + [
        'play/collection', 'play/route', 'play/visual-v2/network-data.js',
        'play/progress.js', 'play/reader-bridge.js', 'play/app.js',
        'index.html', 'shelf.css', 'reader-controls.css', 'reader-layout.js',
        'reader-restart.js', 'picture-panel-focus.js', 'picture-panel-focus.css',
        'sitemap.xml', 'robots.txt', 'googlee0c995331ec518ae.html',
    ]
    changed = subprocess.check_output(
        ['git', 'diff', '--name-only', BASE, '--', *paths], cwd=ROOT, text=True,
    ).splitlines()
    assert not changed, {'unexpectedProtectedChanges': changed}
    files = subprocess.check_output(
        ['git', 'ls-tree', '-r', '--name-only', BASE, '--', *paths],
        cwd=ROOT, text=True,
    ).splitlines()
    return {'baseline': BASE, 'protectedTrackedFiles': len(files),
            'originalFourteenBooksAndSourcePackages': 'byte-for-byte unchanged',
            'collectionStoreCatalogBridgeAndRoute': 'byte-for-byte unchanged',
            'rootHomepageSEOAndSharedReaderControls': 'byte-for-byte unchanged'}


def validate_city_art():
    manifest = json.loads((ROOT / 'docs/play/city-entry/generated-assets.json').read_text())
    checked = []
    for entry in manifest['assets']:
        asset = ROOT / entry['path']
        image = Image.open(asset)
        assert list(image.size) == entry['nativeDimensions']
        assert image.mode == entry['mode']
        assert hashlib.sha256(asset.read_bytes()).hexdigest() == entry['sha256']
        assert abs(image.width / image.height - 16/9) < .002
        checked.append({'path': entry['path'], 'size': list(image.size), 'sha256': entry['sha256']})
    return {'assets': checked, 'visualInspection': 'Six painted gates; crowned orange-tabby lord with moustache; guardian and black-white/calico messengers remain distinct; no baked name labels', 'native4K': False, 'status': 'Generated concept pending author confirmation'}


def fixture(completed=(), positions=None, active=None):
    return {'version': 1, 'completed': list(completed), 'positions': positions or {},
            'activeBook': active or ORDER[0]}


def settle(page):
    page.evaluate('()=>new Promise(done=>requestAnimationFrame(()=>requestAnimationFrame(done)))')


def no_overflow(page):
    settle(page)
    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'), 'viewport horizontal overflow'


def restore_fixture(page, state):
    assert page.evaluate("""async state => {
      const {store}=await import('/play/collection/store.js');
      return store.restoreBackup(JSON.stringify(state));
    }""", state)
    settle(page)


def observe(page, base, report):
    page.on('pageerror', lambda e: report['javascriptErrors'].append(str(e)))
    page.on('response', lambda r: report['httpErrors'].append(r.url) if r.url.startswith(base) and r.status >= 400 else None)


def check_navigation(browser, base, report):
    context = browser.new_context(reduced_motion='reduce')
    page = context.new_page()
    observe(page, base, report)
    for width, height in SIZES:
        page.set_viewport_size({'width': width, 'height': height})
        for path, active in [('play/worldmap-v4/', 'map'), ('play/city/', 'city'), ('play/visual-v2/shelf.html', 'shelf')]:
            page.goto(base + path, wait_until='domcontentloaded')
            page.wait_for_selector('header.sz-game-header [data-game-nav="city"]')
            assert '[object Object]' not in page.locator('body').inner_text()
            header = page.locator('header.sz-game-header')
            nav = header.locator('.sz-game-nav')
            assert nav.locator('[data-game-nav]').evaluate_all('els=>els.map(e=>e.dataset.gameNav)') == ['map', 'mindmap', 'city', 'shelf']
            assert nav.locator('[data-game-nav="' + active + '"]').get_attribute('aria-current') == 'page'
            assert nav.locator('[data-game-nav="city"] svg.sz-game-nav__castle').count() == 1
            assert nav.locator('[data-game-nav="city"] svg path').count() > 0
            assert nav.locator('[data-game-nav="city"]').get_attribute('href') == base + 'play/city/'
            assert nav.locator('[data-game-nav="map"]').get_attribute('href') == base + 'play/worldmap-v4/'
            assert nav.locator('[data-game-nav="mindmap"]').get_attribute('href') == base + 'index.html#map-heading'
            assert nav.locator('[data-game-nav="shelf"]').get_attribute('href') == base + 'play/visual-v2/shelf.html'
            assert nav.locator('[data-game-nav]').evaluate_all('els=>els.every(e=>{const r=e.getBoundingClientRect();return r.width>=43&&r.height>=43})')
            no_overflow(page)
            initial = header.bounding_box()
            page.evaluate('window.scrollTo(0,document.body.scrollHeight)')
            settle(page)
            after = header.bounding_box()
            assert initial['y'] >= -1 and after['y'] >= -1, 'game header scrolls out of view'
            assert abs(after['y'] - initial['y']) < 2
            assert after['height'] < height / 2
            # Follow the actual city entry; it is a separate page, never an embedded map dialog.
            nav.locator('[data-game-nav="city"]').click()
            page.wait_for_url('**/play/city/**')
            page.wait_for_selector('#city-scene-host .city-tactics-board')
            assert page.locator('#city-dialog[open]').count() == 0
            report.setdefault('navigation', []).append({'viewport': [width, height], 'origin': active, 'fourLinksAndCastleSvg': True, 'headerVisibleAfterScroll': True, 'nativeCityEntry': 'independent /play/city/ page', 'viewportOverflow': 'none'})
    context.close()


def check_coastal_relation(browser, base, report):
    context = browser.new_context(viewport={'width': 1280, 'height': 900}, reduced_motion='reduce')
    page = context.new_page()
    observe(page, base, report)
    page.goto(base + 'play/worldmap-v4/')
    page.wait_for_selector('.wm-world')
    restore_fixture(page, fixture(ORDER))
    page.locator('.wm-background').evaluate('i=>i.decode()')
    before = page.locator('.wm-landmark').evaluate_all('els=>els.map(e=>({id:e.dataset.landmark,x:e.style.getPropertyValue("--x"),y:e.style.getPropertyValue("--y"),label:e.textContent}))')
    page.locator('[data-wm-lines]').click()
    actual = page.locator('.wm-relation').evaluate_all('els=>els.map(e=>({id:e.dataset.sourceEdge,from:e.dataset.from,to:e.dataset.to}))')
    expected = page.evaluate("async()=>{const {EDGES}=await import('./data.js');return EDGES.map(e=>({id:e.id,from:String(e.from),to:String(e.to)}))}")
    assert actual == expected and len(actual) == 46
    target_id = 'overview-branch-road-overview-eightfold-overview'
    path = page.locator('[data-source-edge="' + target_id + '"]')
    sample = path.evaluate("""p=>{
      const n=p.getTotalLength(),xy=t=>{const q=p.getPointAtLength(t);return [q.x,q.y]};
      const points=Array.from({length:121},(_,i)=>xy(n*i/120));
      return {d:p.getAttribute('d'),start:xy(0),end:xy(n),interiorCrossings:points.filter(([x,y])=>x>300&&x<1100&&y>350&&y<720).length};
    }""")
    endpoints = sorted([sample['start'], sample['end']])
    assert all(abs(a - b) < 1 for actual_point, expected_point in zip(endpoints, [[128, 423], [1480, 693]]) for a, b in zip(actual_point, expected_point))
    assert sample['interiorCrossings'] == 0, 'harbor/path branch still cuts diagonally through central scenery'
    assert sample['d'] != 'M128 423L1480 693'
    after = page.locator('.wm-landmark').evaluate_all('els=>els.map(e=>({id:e.dataset.landmark,x:e.style.getPropertyValue("--x"),y:e.style.getPropertyValue("--y"),label:e.textContent}))')
    assert before == after, 'line repair changed geography or label anchors'
    assert not any(e['from'] == 'road-overview' and e['to'] in ['iddhipada', 'four-jhanas'] for e in actual)
    extra = page.locator('[data-display-route="harbor-concentration-access"]')
    assert extra.count() == 1 and extra.get_attribute('data-is-source-relation') == 'false'
    assert extra.get_attribute('data-route-kind') == 'author-geographic-access'
    assert extra.get_attribute('data-source-edge') is None
    access = extra.evaluate("""p=>{const length=p.getTotalLength(),point=t=>{const q=p.getPointAtLength(t);return[q.x,q.y]};return{start:point(0),via:point(99),end:point(length)}}""")
    assert access['start'] == [1152, 630] and access['via'] == [1152, 531] and access['end'] == [128, 423]
    page.screenshot(path=str(OUT / 'coastal-relations-1280x900.png'), full_page=True)
    page.locator('[data-landmark="jhana_water_garden"]').click()
    assert page.locator('#wm-dialog [data-wm-select="harbor"]').count() == 0
    page.locator('[data-wm-close]').click()
    report['coastalLine'] = {'originalEdges': 46, 'sourceIdentityPreserved': True, 'target': target_id, 'displayPath': sample['d'], 'originalEndpointPair': [sample['start'], sample['end']], 'centralDiagonalCrossings': 0, 'landmarkAnchors': 'unchanged', 'noInventedHarborIddhipadaJhanaEdges': True, 'separateGeographicAccess': access, 'geographicAccessIsNotSemanticNeighbour': True}
    context.close()


def check_city_layout_and_components(browser, base, report):
    context = browser.new_context(reduced_motion='reduce')
    context.add_init_script("localStorage.setItem('sutrazen.play.v1','city-qa-preserve-v1');localStorage.setItem('unrelated','keep')")
    page = context.new_page()
    observe(page, base, report)
    for width, height in SIZES:
        page.set_viewport_size({'width': width, 'height': height})
        page.goto(base + 'play/city/', wait_until='domcontentloaded')
        page.wait_for_selector('.tactics-label')
        restore_fixture(page, fixture(ORDER))
        page.locator('.tactics-art').evaluate('i=>i.decode()')
        assert '[object Object]' not in page.locator('body').inner_text()
        board = page.locator('#city-scene-host .city-tactics-board')
        assert board.get_attribute('data-city-labels') == 'true'
        assert page.locator('.tactics-label[data-city-label]').count() == 14
        assert page.locator('.tactics-label.tactics-gate-hotspot').count() == 6
        assert page.locator('.tactics-label-text').evaluate_all('els=>els.every(e=>getComputedStyle(e).userSelect==="text"&&e.textContent.trim())')
        maths = board.evaluate("""b=>{
          const r=b.getBoundingClientRect(),i=b.querySelector('.tactics-art').getBoundingClientRect(),svg=b.querySelector('.tactics-label-lines');
          const box=[r.width,r.height],image=[i.x-r.x,i.y-r.y,i.width,i.height],view=svg.viewBox.baseVal;
          const labels=[...b.querySelectorAll('[data-city-label]')].map(e=>{
            const id=e.dataset.cityLabel,p=b.querySelector('[data-label-for="'+id+'"]'),q=p.getPointAtLength(p.getTotalLength()),lr=e.getBoundingClientRect();
            return{id,xError:Math.abs(lr.x+lr.width/2-r.x-q.x/view.width*r.width),yError:Math.abs(lr.y+lr.height/2-r.y-q.y/view.height*r.height),inside:lr.left>=r.left-1&&lr.right<=r.right+1&&lr.top>=r.top-1&&lr.bottom<=r.bottom+1};
          });return{box,image,view:[view.width,view.height],labels};
        }""")
        assert maths['view'] == [1672, 941]
        assert abs(maths['box'][0] / maths['box'][1] - 1672/941) < .002
        assert abs(maths['image'][0]) < 1 and abs(maths['image'][1]) < 1
        assert abs(maths['image'][2] - maths['box'][0]) < 1 and abs(maths['image'][3] - maths['box'][1]) < 1
        assert all(p['xError'] < 1 and p['yError'] < 1 and p['inside'] for p in maths['labels']), maths['labels']
        original_save = page.evaluate('(key)=>localStorage.getItem(key)', COLLECTION_KEY)
        for part, book_id in CITY_BOOKS.items():
            page.locator('[data-city-label="' + part + '"]').click(timeout=5000)
            page.wait_for_selector('#city-dialog[open]')
            assert 'SN 35.245' in page.locator('#city-dialog').inner_text()
            assert page.locator('#city-dialog [data-city-reread="' + book_id + '"]').count() == 1
            assert len(page.locator('#city-dialog').inner_text()) < 1500
            page.locator('[data-city-close]').click()
        page.locator('#city-label-toggle').click()
        assert page.locator('.tactics-label').count() == 0 and page.locator('.tactics-label-lines').count() == 0
        page.locator('#city-label-toggle').click()
        assert page.locator('.tactics-label').count() == 14
        page.locator('#city-overview-toggle').click()
        assert 'city-explore' in page.locator('#city-scene-host').get_attribute('class')
        assert page.locator('.city-tactics-board').bounding_box()['width'] >= 1250
        page.locator('[data-city-label="lord"]').click(timeout=5000)
        page.locator('[data-city-close]').click()
        page.locator('#city-overview-toggle').click()
        assert page.evaluate('(key)=>localStorage.getItem(key)', COLLECTION_KEY) == original_save
        assert page.evaluate("localStorage.getItem('sutrazen.play.v1')") == 'city-qa-preserve-v1'
        no_overflow(page)
        page.evaluate('window.scrollTo(0,0)')
        page.screenshot(path=str(OUT / f'city-all-labels-{width}x{height}.png'), full_page=True)
        if width == 390:
            page.locator('[data-city-label="lord"]').click()
            assert not page.locator('#city-dialog .tactics-character-preview figcaption').is_visible()
            page.screenshot(path=str(OUT / 'city-lord-meaning-390x844.png'), full_page=True)
            page.locator('[data-city-close]').click()
        report.setdefault('cityLayouts', []).append({'viewport': [width, height], 'htmlLabels': 14, 'gates': 6, 'nativeComponentDialogs': 14, 'leaderEndpointsFollowLabels': True, 'imageAndOverlayFrame': [1672, 941], 'completeImageNotCropped': True, 'labelsSelectable': True, 'progressUnchangedByInspection': True, 'viewportOverflow': 'none'})
    context.close()


def export_current_world(browser, base, report):
    """Render actual HTML/SVG at3x; this does not create native4K artwork."""
    context = browser.new_context(viewport={'width': 1280, 'height': 900}, device_scale_factor=3, reduced_motion='reduce')
    page = context.new_page()
    observe(page, base, report)
    page.goto(base + 'play/worldmap-v4/?mode=free')
    page.wait_for_selector('.wm-world')
    page.locator('.wm-background').evaluate('i=>i.decode()')
    export_css = """
      .proposal-header,.wm-heading,.wm-tools,.wm-notes,#wm-route-strip,.wm-art-details{display:none!important}
      .wm-page main{padding:0!important;margin:0!important;max-width:none!important}
      .wm-viewport{max-height:none!important;border:0!important;border-radius:0!important;overflow:visible!important}
      .wm-world{width:1280px!important;height:720px!important}
    """
    exports = []
    for enabled, filename in [(False, 'worldmap-3840x2160-no-lines.png'), (True, 'worldmap-3840x2160-with-lines.png')]:
        if enabled:
            page.locator('[data-wm-lines]').click()
            assert page.locator('.wm-relation:not(.is-hidden)').count() == 46
        style = page.add_style_tag(content=export_css)
        settle(page)
        frame = page.locator('.wm-world').bounding_box()
        assert frame['width'] == 1280 and frame['height'] == 720
        path = OUT / filename
        page.locator('.wm-world').screenshot(path=str(path))
        assert list(Image.open(path).size) == [3840, 2160]
        style.evaluate('e=>e.remove()')
        exports.append({'path': str(path.relative_to(ROOT)), 'pixels': [3840, 2160], 'linesVisible': enabled, 'cssWorld': [1280, 720], 'originalSourceEdges': 46})
    assert page.evaluate('(k)=>localStorage.getItem(k)', COLLECTION_KEY) is None
    context.close()
    report['highResolutionExport'] = {'method': 'Actual world-element browser screenshots at deviceScaleFactor3; page chrome hidden only for export', 'nativeBackground': [1672, 941], 'native4KArtwork': False, 'progressFixture': 'Free exploration in an empty disposable browser, no completion record written', 'exports': exports}


def check_native_resume(browser, base, report):
    context = browser.new_context(viewport={'width': 390, 'height': 844}, reduced_motion='reduce')
    context.add_init_script("localStorage.setItem('sutrazen.play.v1','city-native-preserve');localStorage.setItem('unrelated','keep')")
    page = context.new_page()
    observe(page, base, report)
    page.goto(base + 'play/city/')
    page.wait_for_selector('.tactics-label')
    page.locator('[data-city-label="lord"]').click()
    page.locator('[data-city-reread="five-aggregates"]').click()
    page.wait_for_function('document.body?.dataset.collectionBook==="five-aggregates"')
    assert page.locator('body').get_attribute('data-collection-index') == '0'
    for index in range(1, 4):
        page.locator('#next').click()
        page.wait_for_function('(n)=>document.body?.dataset.collectionIndex===String(n)', arg=index)
    page.reload(wait_until='domcontentloaded')
    page.wait_for_function('document.body?.dataset.collectionIndex==="3"')
    page.locator('.collection-reader-return').click()
    page.wait_for_selector('[data-game-nav="city"]')
    page.locator('[data-game-nav="city"]').click()
    page.wait_for_selector('#city-continue')
    assert page.locator('#city-continue').get_attribute('data-city-primary-book') == 'five-aggregates'
    assert page.locator('#city-continue').get_attribute('data-city-resume-at') == '3'
    assert '0／14' in page.locator('#city-progress').inner_text()
    page.set_viewport_size({'width': 844, 'height': 390})
    page.wait_for_function('document.querySelector("[data-city-label=lord] .tactics-label-text")?.textContent==="識・城主"')
    assert page.locator('#city-continue').get_attribute('data-city-resume-at') == '3'
    page.locator('#city-continue').click()
    page.wait_for_function('document.body?.dataset.collectionBook==="five-aggregates"&&document.body?.dataset.collectionIndex==="3"')
    page.locator('#next').click()
    page.wait_for_function('document.body?.dataset.collectionIndex==="4"')
    assert page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).completed.length', COLLECTION_KEY) == 0
    page.locator('.collection-reader-return').click()
    page.wait_for_selector('[data-game-nav="city"]')
    page.locator('[data-game-nav="city"]').click()
    page.wait_for_selector('#city-continue')
    # A completed-book fixture is explicitly separated from the real unfinished-book flow above.
    restore_fixture(page, fixture(['five-aggregates'], {'five-aggregates': 53}, 'five-aggregates'))
    page.locator('[data-city-label="lord"]').click()
    page.locator('[data-city-reread="five-aggregates"]').click()
    page.wait_for_function('document.body?.dataset.collectionIndex==="0"')
    page.locator('#next').click()
    page.wait_for_function('document.body?.dataset.collectionIndex==="1"')
    page.reload(wait_until='domcontentloaded')
    page.wait_for_function('document.body?.dataset.collectionIndex==="1"')
    page.locator('.collection-reader-return').click()
    page.wait_for_selector('[data-game-nav="city"]')
    page.locator('[data-game-nav="city"]').click()
    page.wait_for_selector('#city-continue')
    assert page.locator('#city-continue').get_attribute('data-city-resume-at') == '1'
    assert '1／14' in page.locator('#city-progress').inner_text()
    assert page.evaluate("localStorage.getItem('sutrazen.play.v1')") == 'city-native-preserve'
    assert page.evaluate("localStorage.getItem('unrelated')") == 'keep'
    report['nativeCityReading'] = {'componentBook': 'lord→five-aggregates', 'actualNext': '0→1→2→3, reload3, city primary resume3, Next4 without completing', 'resizePreservesBookmark': '390x844→844x390', 'rereadFixture': 'Earned book restarts0, Next1/reload1, city primary resumes1 with count1', 'originalJourneyAndUnrelatedKeys': 'preserved'}
    context.close()


def assert_compact_feedback(page, completed_book, next_book, count):
    dialog = page.locator('#wm-dialog.wm-completion-dialog[open]')
    assert dialog.count() == 1
    assert dialog.locator('.wm-compact-reward[data-completed-book="' + completed_book + '"]').count() == 1
    assert dialog.locator('.city-tactics-board,.wm-reward-city').count() == 0
    assert dialog.locator('.wm-completion-actions a[data-wm-city]').get_attribute('href') == '../city/'
    assert dialog.locator('[data-wm-city]').inner_text() == '看看城池'
    if next_book:
        assert dialog.locator('.wm-completion-actions button.primary[data-wm-read="' + next_book + '"]').count() == 1
    else:
        assert dialog.locator('.wm-completion-actions button.primary[data-wm-ending]').count() == 1
    assert f'{count}／14' in page.locator('#wm-count').inner_text()
    assert f'{count}／14' in dialog.locator('.wm-completion-count').inner_text()
    assert '[object Object]' not in dialog.inner_text()


def check_actual_completion(browser, base, report):
    context = browser.new_context(viewport={'width': 390, 'height': 844}, reduced_motion='reduce')
    context.add_init_script("localStorage.setItem('sutrazen.play.v1','completion-preserve-v1')")
    page = context.new_page()
    observe(page, base, report)
    page.goto(base + 'play/worldmap-v4/')
    page.wait_for_selector('.wm-world')
    page.locator('[data-wm-next]').click()
    page.wait_for_function('document.body?.dataset.collectionBook==="four-truths"')
    for index in range(1, 29):
        page.locator('#next').click()
        page.wait_for_function('(n)=>document.body?.dataset.collectionIndex===String(n)', arg=index)
        if index == 5:
            page.reload(wait_until='domcontentloaded')
            page.wait_for_function('document.body?.dataset.collectionIndex==="5"')
    assert page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).completed.length', COLLECTION_KEY) == 0
    assert page.locator('#next').inner_text().strip() == '完成這本'
    page.locator('#next').click()
    page.wait_for_url('**/play/worldmap-v4/**')
    page.wait_for_selector('#wm-dialog[open]')
    assert_compact_feedback(page, 'four-truths', 'five-aggregates', 1)
    for width, height in SIZES:
        page.set_viewport_size({'width': width, 'height': height})
        settle(page)
        no_overflow(page)
        assert_compact_feedback(page, 'four-truths', 'five-aggregates', 1)
        action = page.locator('.wm-completion-actions')
        assert action.locator('button.primary').is_visible()
        assert action.locator('[data-wm-city]').is_visible()
        assert action.locator('button.primary,a[data-wm-city]').evaluate_all("""els=>els.every(e=>{
          const r=e.getBoundingClientRect(),d=e.closest('dialog').getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);
          return r.top>=d.top&&r.bottom<=d.bottom+1&&r.left>=d.left&&r.right<=d.right&&Boolean(hit&&e.contains(hit));
        })"""), 'compact actions are clipped or covered'
        assert page.locator('#wm-dialog').bounding_box()['height'] <= height - 20
        if width in [1280, 390, 844]:
            page.screenshot(path=str(OUT / f'actual-compact-four-truths-{width}x{height}.png'), full_page=True)
    page.locator('#wm-dialog [data-wm-read="five-aggregates"]').click()
    page.wait_for_function('document.body?.dataset.collectionBook==="five-aggregates"&&document.body?.dataset.collectionIndex==="0"')
    assert page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).completed', COLLECTION_KEY) == ['four-truths']
    page.locator('.collection-reader-return').click()
    page.wait_for_selector('[data-game-nav="city"]')
    page.locator('[data-game-nav="city"]').click()
    page.wait_for_selector('#city-progress')
    assert '1／14' in page.locator('#city-progress').inner_text()
    assert page.locator('.city-tactics-board').get_attribute('data-city-stage') == '1'
    assert page.evaluate("localStorage.getItem('sutrazen.play.v1')") == 'completion-preserve-v1'
    report['actualCompletion'] = {'book': 'four-truths', 'nativeReadingSteps': 29, 'reload': 'step5', 'arrivalAtLastPageDoesNotComplete': True, 'explicitFinishCount': '1/14', 'destination': '/play/worldmap-v4/', 'reward': 'compact optional city entry, no full city embed', 'primaryNext': 'five-aggregates step0', 'cityViaHeader': 'independent page stage1/count1'}
    # A valid restored final-page bookmark tests the new final feedback only.
    page.goto(base + 'play/worldmap-v4/')
    page.wait_for_selector('.wm-world')
    restore_fixture(page, fixture(ORDER[:-1], {ORDER[-1]: 74}, ORDER[-1]))
    page.locator('[data-wm-next]').click()
    page.wait_for_function('document.body?.dataset.collectionBook==="four-fruits-ten-fetters"&&document.body?.dataset.collectionIndex==="74"')
    assert page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).completed.length', COLLECTION_KEY) == 13
    page.locator('#next').click()
    page.wait_for_selector('#wm-dialog[open]')
    assert_compact_feedback(page, ORDER[-1], None, 14)
    page.screenshot(path=str(OUT / 'fixture-final-compact-1024x768.png'), full_page=True)
    page.locator('#wm-dialog [data-wm-city]').click()
    page.wait_for_url('**/play/city/**')
    page.wait_for_selector('#city-progress')
    assert '14／14' in page.locator('#city-progress').inner_text()
    assert len(page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).completed', COLLECTION_KEY)) == 14
    report['lastBookFeedbackFixture'] = 'Valid restored final-book bookmark74 with13completed; explicit last action adds only final to14, compact ending action and optional native city link work; no fifteenth book'
    context.close()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report = protect_originals()
    report['cityArt'] = validate_city_art()
    report.update({'javascriptErrors': [], 'httpErrors': [],
                   'publication': 'Local review only; not merged or deployed',
                   'physicalSafari': 'Not tested; Chromium viewport simulation only',
                   'fixtureBoundary': 'Disposable valid browser backups exercise presentation; genuine completion is separately verified with native Next buttons'})
    server = http.server.ThreadingHTTPServer(
        ('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)),
    )
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}/'
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                executable_path='/usr/bin/chromium', args=['--no-sandbox'],
            )
            check_navigation(browser, base, report)
            check_coastal_relation(browser, base, report)
            check_city_layout_and_components(browser, base, report)
            check_native_resume(browser, base, report)
            check_actual_completion(browser, base, report)
            export_current_world(browser, base, report)
            browser.close()
    finally:
        server.shutdown()
    assert not report['javascriptErrors'] and not report['httpErrors'], [report['javascriptErrors'], report['httpErrors']]
    (OUT / 'validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'result': 'passed', 'report': str((OUT / 'validation.json').relative_to(ROOT)), 'viewports': len(report['cityLayouts']), 'nativeCityDialogs': sum(x['nativeComponentDialogs'] for x in report['cityLayouts']), 'navigationCases': len(report['navigation']), 'actualReadingSteps': report['actualCompletion']['nativeReadingSteps'], 'originalSourceEdges': 46, 'javascriptErrors': [], 'localHttpErrors': []}, ensure_ascii=False))


if __name__ == '__main__':
    main()
