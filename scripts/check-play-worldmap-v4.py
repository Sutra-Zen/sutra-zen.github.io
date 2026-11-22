#!/usr/bin/env python3
"""Check the isolated map-v4 proposal against the author's r3/v4 handoffs.

Disposable browser save fixtures only exercise presentation. They are clearly
separate from the real primary-button reading flow below.
"""
from pathlib import Path
import functools
import hashlib
import http.server
import json
import subprocess
import threading

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/previews/play-worldmap-v4'
BASE = '4f4e1fd'
SIZES = [(1280, 900), (390, 844), (844, 390), (768, 1024), (1024, 768)]
COLLECTION_KEY = 'sutrazen.play.collection.v1'
ROUTE_KEY = 'sutrazen.play.route-metadata.v1'
ORDER = [
    'four-truths', 'five-aggregates', 'six-senses', 'twelve-links',
    'eightfold-path', 'four-purities-six-recollections', 'mindfulness',
    'right-effort', 'anapana', 'iddhipada', 'four-jhanas',
    'five-roots-powers', 'seven-factors', 'four-fruits-ten-fetters',
]

DATA_CHECK = r"""async () => {
  const d = await import('./data.js');
  const expectedColumns={faith:432,mindfulness:672,effort:912,concentration:1152,wisdom:1392};
  const assert=(ok,label)=>{if(!ok)throw new Error(label)};
  assert(JSON.stringify(d.WORLD)===JSON.stringify({width:1600,height:900}), 'world16:9');
  assert(JSON.stringify(d.COLUMNS)===JSON.stringify(expectedColumns), 'five exact columns');
  const all=[...d.LANDMARKS,...d.SECONDARY], ids=all.map(l=>l.id);
  assert(new Set(ids).size===ids.length, 'stable unique landmarks');
  const awakening=d.LANDMARKS.filter(l=>l.row==='awakening');
  const faculties=d.LANDMARKS.filter(l=>l.row==='faculties');
  const bridges=d.LANDMARKS.filter(l=>l.type==='bridge');
  assert(awakening.length===4&&awakening.every(l=>l.y===108&&l.x===expectedColumns[l.family]&&l.family!=='faith'),'four awakening anchors, no faith awakening');
  assert(faculties.length===5&&faculties.every(l=>l.y===243&&l.x===expectedColumns[l.family]),'five faculties anchors');
  assert(bridges.length===4&&bridges.every(l=>l.y===810&&l.x===expectedColumns[l.family]&&l.family!=='faith'),'four aligned bridges, no faith bridge');
  const road=d.LANDMARKS.find(l=>l.id==='path_road');
  assert(road.x===368&&road.y>=756&&road.y<=765&&road.bookId==='eightfold-path','road scroll not extra book/bridge');
  assert(d.LANDMARKS.filter(l=>l.type==='scroll').length===3,'two overview scrolls plus road scroll');
  assert(d.LANDMARKS.find(l=>l.id==='harbor').x===128&&d.LANDMARKS.find(l=>l.id==='harbor').y===423,'northwest harbor');
  assert(d.NODES.length===32&&d.EDGES.length===46,'original source graph preserved');
  assert(new Set(d.MEMBERS.map(m=>m.id)).size===d.MEMBERS.length,'compatibility member IDs unique');
  assert(d.MEMBERS.every(m=>m.provenance==='member-of-source-aggregate'&&d.NODES.some(n=>n.id===m.sourceParentId)),'compatibility members do not pretend original IDs');
  for(const parent of ['concentration-awakening-group','eightfold-action-group']) assert(d.MEMBERS.filter(m=>m.sourceParentId===parent).length===4,parent+' keeps allfour meanings');
  assert(d.MEMBERS.filter(m=>m.sourceParentId==='right-view-intention').length===2,'view/intention both kept');
  const books=[...new Set(all.map(l=>l.bookId).filter(Boolean))];
  assert(books.length===14,'fourteen books across many landmarks');
  const counts=Object.fromEntries(books.map(id=>[id,all.filter(l=>l.bookId===id).length]));
  assert(counts['eightfold-path']===8&&counts['right-effort']===1,'path eight landmarks, independent effort garden');
  return {world:d.WORLD,columns:d.COLUMNS,landmarks:d.LANDMARKS,secondary:d.SECONDARY,
    groups:d.LANDSCAPE_GROUPS,originalConcepts:d.NODES.length,originalRelations:d.EDGES.length,
    compatibilityMembers:d.MEMBERS.length,landmarksPerBook:counts};
}"""


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def copyfile(self, source, target):
        try:
            super().copyfile(source, target)
        except (BrokenPipeError, ConnectionResetError):
            pass


def unchanged_originals():
    paths = ORDER + ['docs/' + book for book in ORDER] + [
        'index.html', 'shelf.css', 'reader-controls.css', 'reader-layout.js',
        'reader-restart.js', 'picture-panel-focus.js', 'picture-panel-focus.css',
        'sitemap.xml', 'robots.txt', 'googlee0c995331ec518ae.html',
        'play/collection/catalog.js', 'play/collection/store.js',
        'play/collection/reader.css', 'play/collection/shelf-text.js',
        'play/progress.js', 'play/reader-bridge.js',
        'play/app.js', 'play/visual-v2/network-data.js',
    ]
    changed = subprocess.check_output(
        ['git', 'diff', '--name-only', BASE, '--', *paths], cwd=ROOT, text=True,
    ).splitlines()
    assert not changed, {'protectedOriginalFilesChanged': changed}
    tracked = subprocess.check_output(
        ['git', 'ls-tree', '-r', '--name-only', BASE, '--', *paths],
        cwd=ROOT, text=True,
    ).splitlines()
    old_bridge = subprocess.check_output(
        ['git', 'show', BASE + ':play/collection/reader-bridge.js'],
        cwd=ROOT, text=True,
    )
    new_bridge = (ROOT / 'play/collection/reader-bridge.js').read_text()
    new_return = """  const requestedReturn = new URLSearchParams(location.search).get('collectionReturn');
  const worldmapReturn = requestedReturn === 'worldmap-v4';
  const gameReturn = requestedReturn === 'game';
  const shelfURL = new URL(gameReturn ? '../../game/' : worldmapReturn ? '../worldmap-v4/' : '../visual-v2/shelf.html', import.meta.url);
  const returnLabel = worldmapReturn || gameReturn ? (await import('../worldmap-v4/text.js')).T.returnJourney : text.returnShelf;"""
    assert new_bridge.count(new_return) == 1
    normalized = new_bridge.replace(new_return, "  const shelfURL = new URL('../visual-v2/shelf.html', import.meta.url);")
    normalized = normalized.replace('returnLink.textContent = returnLabel;', 'returnLink.textContent = text.returnShelf;')
    normalized = normalized.replace("returnLink.setAttribute('aria-label', returnLabel);", "returnLink.setAttribute('aria-label', text.returnShelf);")
    assert normalized == old_bridge, 'reader bridge change exceeds opt-in return URL and label'
    image_path = ROOT / 'play/worldmap-v4/assets/worldmap-master-concept.png'
    image = Image.open(image_path)
    return {
        'baseline': BASE,
        'protectedTrackedFiles': len(tracked),
        'originalSiteReadersCollectionStoreAndOldJourneyBridge': 'byte-for-byte unchanged',
        'collectionBridge': 'Only explicit collectionReturn=worldmap-v4/game whitelist, return URL and label differ; normalized bytes exactly match baseline',
        'originalFullReadingCoverage':
            'docs/previews/play-collection/validation.json: 1192 original reading steps; not repeated for an unchanged core',
        'worldmapMaster': {
            'path': str(image_path.relative_to(ROOT)),
            'size': list(image.size), 'mode': image.mode,
            'sha256': hashlib.sha256(image_path.read_bytes()).hexdigest(),
            'visualInspection': 'Generated concept base has no baked text, fog or locks; artwork remains an unapproved proposal',
        },
    }


def validate_generated_assets():
    manifest = json.loads((ROOT / 'docs/play/worldmap-v4/generated-assets.json').read_text())
    checked = []
    for entry in manifest['assets']:
        asset = ROOT / entry['path']
        image = Image.open(asset)
        assert list(image.size) == entry['nativeDimensions']
        assert image.mode == entry['mode']
        assert hashlib.sha256(asset.read_bytes()).hexdigest() == entry['sha256']
        checked.append({'path': entry['path'], 'size': list(image.size), 'sha256': entry['sha256']})
    return {'assets': checked, 'masterNative4K': False, 'detailsStitchable': False,
            'reviewStatus': 'Generated concept images, pending author confirmation'}


def fixture(completed=(), positions=None, active=None):
    return {'version': 1, 'completed': list(completed),
            'positions': positions or {}, 'activeBook': active or ORDER[0]}


def settle(page):
    page.evaluate('()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))')


def no_overflow(page):
    settle(page)
    assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1'), 'viewport overflow'


def restore_fixture(page, state):
    assert page.evaluate("""async state => {
      const {store} = await import('../collection/store.js');
      return store.restoreBackup(JSON.stringify(state));
    }""", state)
    settle(page)


def geometry(page):
    return page.evaluate("""() => {
      const world=document.querySelector('.wm-world'), wr=world.getBoundingClientRect();
      const relative=e=>{const r=e.getBoundingClientRect();return [r.x-wr.x,r.y-wr.y,r.width,r.height].map(n=>Math.round(n*100)/100)};
      return {world:[wr.width,wr.height].map(n=>Math.round(n*100)/100),
        image:{src:document.querySelector('.wm-background').getAttribute('src'),box:relative(document.querySelector('.wm-background'))},
        landmarks:[...document.querySelectorAll('.wm-landmark')].map(e=>({id:e.dataset.landmark,book:e.dataset.book,concept:e.dataset.concept,label:e.textContent,box:relative(e)}))};
    }""")


def compact_completion(page, book_id):
    """Check the approved concise reward, retaining the actual city-state proof."""
    reward = page.locator('#wm-dialog .wm-compact-reward')
    assert reward.count() == 1
    assert reward.get_attribute('data-completed-book') == book_id
    assert reward.locator('.wm-reward-feature-art').count() == 1
    assert reward.locator('p').inner_text().strip()
    assert page.locator('#wm-dialog .city-tactics-board').count() == 0
    assert page.locator('#wm-dialog [data-wm-city]').get_attribute('href') == '../city/'
    city = page.evaluate('SutraZenWorldmap.getState().status.city')
    expected = next(item for item in city['rewards'] if item['bookId'] == book_id)
    assert reward.get_attribute('data-reward-available') == str(expected['available']).lower()
    return city


def check_layouts(browser, base, report):
    context = browser.new_context(reduced_motion='reduce')
    context.add_init_script("localStorage.setItem('sutrazen.play.v1','worldmap-layout-preserve-v1');localStorage.setItem('unrelated-site-setting','keep');")
    page = context.new_page()
    page.on('pageerror', lambda e: report['javascriptErrors'].append(str(e)))
    page.on('response', lambda r: report['httpErrors'].append(r.url) if r.url.startswith(base) and r.status >= 400 else None)
    page.goto(base + 'play/worldmap-v4/', wait_until='domcontentloaded')
    page.wait_for_selector('.wm-world')
    data = page.evaluate(DATA_CHECK)
    report['mapData'] = data
    page.evaluate("async()=>{const {routeMetadata}=await import('../route/metadata.js');routeMetadata.reset()}")
    for width, height in SIZES:
        page.set_viewport_size({'width': width, 'height': height})
        page.goto(base + 'play/worldmap-v4/', wait_until='domcontentloaded')
        page.wait_for_selector('.wm-world')
        restore_fixture(page, fixture())
        # Mode changes never create completion or write the original collection.
        page.locator('[data-wm-mode="route"]').click()
        if not page.locator('.wm-viewport').get_attribute('class').endswith('is-overview'):
            page.locator('[data-wm-zoom]').click()
        page.locator('.wm-background').evaluate('i=>i.decode()')
        assert page.locator('.wm-landmark').count() == len(data['landmarks'])
        assert page.locator('.wm-world').get_attribute('data-world-size') == '1600x900'
        assert page.locator('.wm-landmark[data-landmark="truth_wheel_ruin"]').get_attribute('data-unlocked') == 'true'
        assert page.locator('.wm-fog[data-fog-for="truth_wheel_ruin"]').count() == 0
        assert page.locator('.wm-fog').count() > 0
        assert '尚未揭曉的旅程' in page.locator('[data-landmark="fruition_valley"]').inner_text()
        assert '四向四果' not in page.locator('[data-landmark="fruition_valley"]').get_attribute('aria-label')
        assert page.locator('.wm-world [class*="lock"],.wm-world [data-lock]').count() == 0
        no_overflow(page)
        assert page.locator('.wm-label').evaluate_all("""els=>els.every(e=>{
          const r=e.getBoundingClientRect(),w=e.closest('.wm-world').getBoundingClientRect();
          return r.left>=w.left-1&&r.right<=w.right+1&&r.top>=w.top-1&&r.bottom<=w.bottom+1;
        })"""), 'overview label clipped by world boundary'
        page.screenshot(path=str(OUT / f'initial-overview-{width}x{height}.png'), full_page=True)
        restore_fixture(page, fixture(ORDER))
        assert page.locator('.wm-fog').count() == 0
        assert '14／14' in page.locator('#wm-count').inner_text()
        assert page.locator('[data-path-active]').count() == 1 and page.locator('[data-irrigation-active]').count() == 1
        # Toggle exact original relation layer without exchanging geography.
        if page.evaluate('SutraZenWorldmap.getState().links') != 'none':
            if page.evaluate('SutraZenWorldmap.getState().links') == 'direct':
                page.locator('[data-wm-lines]').click()
            page.locator('[data-wm-lines]').click()
        before = geometry(page)
        page.locator('[data-wm-lines]').click()
        assert page.locator('.wm-relation:not(.is-hidden)').count() == 46
        assert page.locator('[data-layout-guides] [data-column]').count() == 5
        assert page.locator('[data-layout-guides] [data-column="faith"]').get_attribute('d') == 'M432 243V540'
        assert geometry(page) == before, 'lines toggle changed image or anchor geometry'
        if width in [1280, 390]:
            page.screenshot(path=str(OUT / f'all-fourteen-lines-{width}x{height}.png'), full_page=True)
        page.locator('[data-wm-lines]').click()
        assert page.locator('.wm-relation:not(.is-hidden)').count() == 0
        assert geometry(page) == before, 'hiding lines changed labels or geometry'
        page.screenshot(path=str(OUT / f'all-fourteen-overview-{width}x{height}.png'), full_page=True)
        # Inspect at useful physical label sizes rather than clicking microtext.
        page.locator('[data-wm-zoom]').click()
        assert page.locator('.wm-world').bounding_box()['width'] == 1600
        for landmark in data['landmarks']:
            page.locator('[data-wm-landmark="' + landmark['id'] + '"]').click(timeout=5000)
            page.wait_for_selector('#wm-dialog[open]')
            if landmark['bookId']:
                assert page.locator('#wm-dialog [data-wm-read="' + landmark['bookId'] + '"]').count() == 1
                guide = page.locator('#wm-dialog [data-wm-guide]').get_attribute('href')
                assert guide == base + landmark['bookId'] + '/'
            page.locator('[data-wm-close]').click()
        page.locator('[data-wm-locate]').click()
        # All complete: no invented next book; still no external overflow.
        no_overflow(page)
        assert page.evaluate("localStorage.getItem('sutrazen.play.v1')") == 'worldmap-layout-preserve-v1'
        assert page.evaluate("localStorage.getItem('unrelated-site-setting')") == 'keep'
        report.setdefault('layouts', []).append({
            'viewport': [width, height], 'nativeLandmarkDialogs': len(data['landmarks']),
            'sameBaseAndGeometryWithLinesOnOff': True,
            'originalRelationPaths': 46, 'initialFourTruthsReadableWithoutFog': True,
            'allFourteenNoFog': True, 'viewportOverflow': 'none',
        })
    # Native locate in an incomplete route must pan to the actual next anchor.
    page.set_viewport_size({'width': 390, 'height': 844})
    restore_fixture(page, fixture(ORDER[:3]))
    page.locator('[data-wm-locate]').click()
    settle(page)
    assert page.locator('[data-landmark="dependent_origination_court"]').get_attribute('class').find('is-selected') >= 0
    assert page.locator('[data-wm-next]').get_attribute('data-next-book') == 'twelve-links'
    box = page.locator('[data-landmark="dependent_origination_court"]').bounding_box()
    viewport = page.locator('.wm-viewport').bounding_box()
    assert box['x'] + box['width']/2 >= viewport['x'] and box['x'] + box['width']/2 <= viewport['x'] + viewport['width']
    page.locator('[data-wm-next]').scroll_into_view_if_needed()
    page.screenshot(path=str(OUT / 'mobile-locate-next-390x844.png'), full_page=True)
    context.close()


def check_resume_modes(browser, base, report):
    context = browser.new_context(viewport={'width': 390, 'height': 844}, reduced_motion='reduce')
    page = context.new_page()
    page.on('pageerror', lambda e: report['javascriptErrors'].append(str(e)))
    page.goto(base + 'play/worldmap-v4/')
    page.wait_for_selector('.wm-world')
    page.locator('[data-wm-mode="free"]').click()
    page.locator('[data-landmark="jhana_water_garden"]').click()
    page.locator('#wm-dialog [data-wm-read="four-jhanas"]').click()
    page.wait_for_function('document.body?.dataset.collectionBook==="four-jhanas"')
    for index in range(1, 6):
        page.locator('#next').click()
        page.wait_for_function('(n)=>document.body?.dataset.collectionIndex===String(n)', arg=index)
    page.locator('.collection-reader-return').click()
    page.wait_for_selector('.wm-world')
    assert page.locator('[data-wm-next]').get_attribute('data-next-book') == 'four-jhanas'
    assert page.evaluate('SutraZenWorldmap.getState().status.nextBookId') == 'four-truths'
    assert '0／14' in page.locator('#wm-count').inner_text()
    page.locator('[data-wm-next]').click()
    page.wait_for_function('document.body?.dataset.collectionBook==="four-jhanas"&&document.body?.dataset.collectionIndex==="5"')
    page.reload(wait_until='domcontentloaded')
    page.wait_for_function('document.body?.dataset.collectionIndex==="5"')
    page.locator('.collection-reader-return').click()
    page.wait_for_selector('.wm-world')
    # Re-reading an earned cover still keeps a new partial bookmark, with no double count.
    restore_fixture(page, fixture(['four-truths'], {'four-truths': 28}))
    page.locator('[data-landmark="truth_wheel_ruin"]').click()
    page.locator('#wm-dialog [data-wm-read="four-truths"]').click()
    page.wait_for_function('document.body?.dataset.collectionBook==="four-truths"&&document.body?.dataset.collectionIndex==="0"')
    for index in range(1, 6):
        page.locator('#next').click()
        page.wait_for_function('(n)=>document.body?.dataset.collectionIndex===String(n)', arg=index)
    page.locator('.collection-reader-return').click()
    page.wait_for_selector('.wm-world')
    assert page.locator('[data-wm-next]').get_attribute('data-next-book') == 'four-truths'
    assert page.evaluate('SutraZenWorldmap.getState().status.nextBookId') == 'five-aggregates'
    page.locator('[data-wm-next]').click()
    page.wait_for_function('document.body?.dataset.collectionIndex==="5"')
    for index in range(6, 29):
        page.locator('#next').click()
        page.wait_for_function('(n)=>document.body?.dataset.collectionIndex===String(n)', arg=index)
    page.locator('#next').click()
    page.wait_for_selector('#wm-dialog[open]')
    compact_completion(page, 'four-truths')
    assert page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).completed', COLLECTION_KEY) == ['four-truths']
    assert '1／14' in page.locator('#wm-count').inner_text()
    report['primaryResume'] = 'Actual free Four Jhanas Next0→5, return and primary resume5/reload5 while recommendation remains Four Truths; earned Four Truths reread0→5, return/resume5 and explicit re-finish leaves count1'
    context.close()


def check_storage_and_original_modes(browser, base, report):
    # A pre-existing complete save must be consumed byte-for-byte, never rewritten on view changes.
    saved = fixture(ORDER[::-1], {id: index for index, id in enumerate(ORDER)}, ORDER[-1])
    raw = json.dumps(saved, ensure_ascii=False, indent=1)
    context = browser.new_context(reduced_motion='reduce')
    context.add_init_script('localStorage.setItem(' + json.dumps(COLLECTION_KEY) + ',' + json.dumps(raw) + ');localStorage.setItem("sutrazen.play.v1","legacy-keep");')
    page = context.new_page()
    page.goto(base + 'play/worldmap-v4/')
    page.wait_for_selector('.wm-world')
    for selector in ['[data-wm-lines]', '[data-wm-zoom]', '[data-wm-labels]', '[data-wm-mode="free"]', '[data-wm-mode="route"]']:
        page.locator(selector).click()
    assert page.evaluate('(k)=>localStorage.getItem(k)', COLLECTION_KEY) == raw
    assert page.evaluate('SutraZenWorldmap.getState().status.endingAvailable')
    assert page.evaluate("localStorage.getItem('sutrazen.play.v1')") == 'legacy-keep'
    context.close()
    for broken in ['corrupt', 'blocked']:
        context = browser.new_context(viewport={'width': 390, 'height': 844}, reduced_motion='reduce')
        if broken == 'corrupt':
            context.add_init_script('localStorage.setItem(' + json.dumps(COLLECTION_KEY) + ',"{broken-json");')
        else:
            context.add_init_script("Object.defineProperty(window,'localStorage',{configurable:true,get(){throw new DOMException('blocked','SecurityError')}})")
        page = context.new_page()
        page.on('pageerror', lambda e: report['javascriptErrors'].append(str(e)))
        page.goto(base + 'play/worldmap-v4/')
        page.wait_for_selector('.wm-world')
        assert page.locator('#wm-storage-notice').is_visible()
        if broken == 'corrupt':
            assert page.evaluate('(k)=>localStorage.getItem(k)', COLLECTION_KEY) == '{broken-json'
        page.locator('[data-wm-next]').click()
        page.wait_for_function('document.body?.dataset.collectionBook==="four-truths"')
        warning = page.locator('.collection-reader-storage')
        if warning.count() and warning.is_visible():
            warning.locator('button').click()
        page.locator('#next').click()
        page.wait_for_function('document.body?.dataset.collectionIndex==="1"')
        context.close()
    context = browser.new_context(reduced_motion='reduce')
    page = context.new_page()
    for book_id in ORDER[:3]:
        page.goto(base + book_id + '/book/', wait_until='domcontentloaded')
        page.wait_for_selector('#next')
        assert page.locator('.collection-reader-return').count() == 0
        assert page.locator('body').get_attribute('data-collection-book') is None
        old = page.locator('#position-text').inner_text()
        page.locator('#next').click()
        page.wait_for_function('(old)=>document.querySelector("#position-text").textContent!==old', arg=old)
        page.locator('#previous').click()
        assert page.locator('#position-text').inner_text() == old
        assert page.locator('#next').evaluate('e=>getComputedStyle(e).touchAction') == 'manipulation'
        assert page.locator('.reading-links a').count() >= 2
    page.goto(base + 'four-truths/book/?collection=1')
    page.wait_for_selector('.collection-reader-return')
    assert page.locator('.collection-reader-return').inner_text() == '回收集書架'
    assert page.locator('.collection-reader-return').get_attribute('href') == base + 'play/visual-v2/shelf.html'
    page.locator('.collection-reader-return').click()
    page.wait_for_selector('[data-book-card]')
    assert page.locator('[data-book-card]').count() == 14
    context.close()
    report['storageAndModeIsolation'] = {
        'existingAllFourteenSave': 'Exact original raw string preserved by world render, view switches and line/label controls; immediately ending eligible',
        'corrupt': 'Raw malformed value preserved on map view; visible notice and reader Next still work',
        'blocked': 'Visible storage notice; reader Next remains usable',
        'standalone': 'First3 original readers Next/Previous/links/touch-action unchanged without opt-in',
        'ordinaryCollectionReturn': 'Still returns to legacy collection shelf; only collectionReturn=worldmap-v4 uses new destination',
    }


def check_city_r3(browser, base, report):
    context = browser.new_context(reduced_motion='reduce')
    page = context.new_page()
    page.on('pageerror', lambda e: report['javascriptErrors'].append(str(e)))
    page.on('response', lambda r: report['httpErrors'].append(r.url) if r.url.startswith(base) and r.status >= 400 else None)
    page.goto(base + 'play/worldmap-v4/')
    page.wait_for_selector('.wm-world')
    for width, height in SIZES:
        page.set_viewport_size({'width': width, 'height': height})
        for name, completed, stage, count, gates in [
            ('initial', [], 0, 0, 0),
            ('dock', ORDER[:1], 1, 1, 0),
            ('body', ORDER[:2], 2, 4, 0),
            ('gates', ORDER[:3], 3, 10, 6),
            ('all', ORDER, 3, 14, 6),
        ]:
            page.goto(base + 'play/worldmap-v4/')
            page.wait_for_selector('.wm-world')
            restore_fixture(page, fixture(completed))
            page.goto(base + 'play/city/')
            page.wait_for_selector('.city-tactics-board')
            board = page.locator('.city-tactics-board')
            assert board.get_attribute('data-city-stage') == str(stage)
            assert page.locator('[data-city-state-source="collection"]').count() == 1
            # All fourteen labels remain inspectable before acquisition; the
            # availability flags, not the existence of labels, prove progress.
            assert page.locator('.city-spot[data-spot]').count() == 14
            assert page.locator('.city-spot[data-city-label]').count() == 14
            assert page.locator('.city-spot[data-feature-available="true"]').count() == count
            assert page.locator('.city-spot[data-feature-available="false"]').count() == 14 - count
            assert page.locator('.tactics-gate-hotspot').count() == 6
            assert page.locator('.tactics-gate-hotspot[data-feature-available="true"]').count() == gates
            assert page.locator('.tactics-road-light.is-active').count() == int('eightfold-path' in completed)
            assert page.locator('.tactics-plaza-light.is-active').count() == int('five-aggregates' in completed)
            assert not page.locator('#city-review-options').evaluate('e=>e.open')
            page.locator('#city-scene-host img').evaluate_all('els=>Promise.all(els.map(i=>i.decode()))')
            no_overflow(page)
            if name in ['initial', 'all'] and width in [1280, 390]:
                page.screenshot(path=str(OUT / f'city-actual-{name}-{width}x{height}.png'), full_page=True)
            if name == 'all':
                spot_ids = page.locator('.city-spot[data-spot]').evaluate_all('els=>els.map(e=>e.dataset.spot)')
                for spot_id in spot_ids:
                    page.locator('.city-spot[data-spot="' + spot_id + '"]').click(timeout=5000)
                    assert 'SN 35.245' in page.locator('#city-dialog').inner_text()
                    assert page.locator('#city-dialog a[href="' + base + 'play/sources.html"]').count() == 1
                    page.locator('#city-dialog [data-city-close]').click()
            report.setdefault('cities', []).append({'viewport': [width, height], 'fixture': name, 'stage': stage, 'realSourceHotspots': 14, 'availableSourceHotspots': count, 'sixGateHotspots': 6, 'availableGateHotspots': gates, 'viewportOverflow': 'none'})
        before = page.evaluate('(k)=>localStorage.getItem(k)', COLLECTION_KEY)
        page.locator('#city-review-options > summary').click()
        page.locator('[data-city-review="0"]').click()
        assert page.locator('[data-city-state-source="review"]').count() == 1
        assert '不會新增、刪除或清空' in page.locator('#city-review-options').inner_text()
        page.locator('[data-city-review="all"]').click()
        assert page.evaluate('(k)=>localStorage.getItem(k)', COLLECTION_KEY) == before
        page.locator('[data-city-review="real"]').click()
        assert page.locator('[data-city-state-source="collection"]').count() == 1
    # Earn a late role first: pending preview exists without falsely creating a body.
    for completed, pending, guardian, messengers in [
        (['mindfulness'], ['mindfulness_guard'], False, False),
        (['anapana'], ['calm_insight_messengers'], False, False),
        (['mindfulness', 'anapana', 'five-aggregates', 'six-senses'], [], True, True),
    ]:
        page.goto(base + 'play/worldmap-v4/')
        page.wait_for_selector('.wm-world')
        restore_fixture(page, fixture(completed))
        page.goto(base + 'play/city/')
        page.wait_for_selector('.city-tactics-board')
        assert page.locator('.city-tactics-board').get_attribute('data-city-guardian') == str(guardian).lower()
        assert page.locator('.city-tactics-board').get_attribute('data-city-messengers') == str(messengers).lower()
        for reward_id in pending:
            assert page.locator('[data-preview-reward="' + reward_id + '"]').count() == 1
        assert page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).completed.length', COLLECTION_KEY) == len(completed)
    report['earnedPendingCityRoles'] = 'Early mindfulness/anapana rewards preview without placing or fabricating body/gates; completing body+gates later auto-places both without rereading'
    # Legacy bookmarks still lead to the new page. Valid read-only review
    # parameters must survive; unrelated/invalid parameters are not promoted.
    before = page.evaluate('(k)=>localStorage.getItem(k)', COLLECTION_KEY)
    for review, expected_query, expected_stage, source in [
        ('all', '?review=all', '3', 'review'),
        ('0', '?review=0', '0', 'review'),
        ('invalid', '', '3', 'collection'),
    ]:
        page.goto(base + 'play/visual-v2/?view=city&review=' + review)
        page.wait_for_url(base + 'play/city/' + expected_query)
        page.wait_for_selector('.city-tactics-board')
        assert page.locator('.city-tactics-board').get_attribute('data-city-stage') == expected_stage
        assert page.locator('[data-city-state-source="' + source + '"]').count() == 1
        assert page.evaluate('(k)=>localStorage.getItem(k)', COLLECTION_KEY) == before
    report['legacyCityRedirect'] = 'Standalone city destination; valid review=all/0 preserved, invalid review ignored, actual collection unchanged'
    context.close()


def check_presentation_states(browser, base, report):
    context = browser.new_context(viewport={'width': 1280, 'height': 900}, reduced_motion='reduce')
    page = context.new_page()
    page.on('pageerror', lambda e: report['javascriptErrors'].append(str(e)))
    page.on('response', lambda r: report['httpErrors'].append(r.url) if r.url.startswith(base) and r.status >= 400 else None)
    page.goto(base + 'play/worldmap-v4/')
    page.wait_for_selector('.wm-world')
    for name, completed, path, garden, irrigation in [
        ('none', [], False, False, False),
        ('path-only', ['eightfold-path'], True, False, False),
        ('effort-only', ['right-effort'], False, True, False),
        ('path-and-effort', ['eightfold-path', 'right-effort'], True, True, True),
    ]:
        restore_fixture(page, fixture(completed))
        assert page.locator('[data-path-active]').count() == int(path)
        assert page.locator('[data-irrigation-active]').count() == int(irrigation)
        assert page.locator('[data-landmark="effort_garden"]').get_attribute('data-completed') == str(garden).lower()
        assert page.locator('[data-landmark="wholesome_lake"]').get_attribute('data-completed') == str(path).lower()
        if completed:
            assert f'{len(completed)}／14' in page.locator('#wm-count').inner_text()
            page.screenshot(path=str(OUT / f'fixture-{name}-1280x900.png'), full_page=True)
    for name, completed, positions, revealed, ending, next_id in [
        ('initial', [], {}, False, False, ORDER[0]),
        ('final-bookmark-zero', [], {ORDER[-1]: 0}, True, False, ORDER[0]),
        ('final-only', [ORDER[-1]], {}, True, False, ORDER[0]),
        ('random-thirteen', ORDER[1:], {}, True, False, ORDER[0]),
        ('first-thirteen', ORDER[:-1], {}, True, False, ORDER[-1]),
        ('all-fourteen', ORDER[::-1], {}, True, True, None),
    ]:
        page.evaluate("async()=>{const {routeMetadata}=await import('../route/metadata.js');routeMetadata.reset()}")
        restore_fixture(page, fixture(completed, positions))
        s = page.evaluate('SutraZenWorldmap.getState().status')
        assert s['count'] == len(completed) and s['finalChapterRevealed'] == revealed and s['endingAvailable'] == ending
        assert page.locator('[data-wm-next]').get_attribute('data-next-book') == (next_id or '')
        actual = page.locator('[data-landmark="fruition_valley"]').inner_text()
        assert ('四向四果' in actual) == revealed
        if ending:
            page.locator('[data-wm-next]').click()
            assert '回到城中，學會放下' in page.locator('#wm-dialog-title').inner_text()
            assert '完整終章演出仍待製作' in page.locator('#wm-dialog').inner_text()
            assert '《雜阿含經》第262經' in page.locator('#wm-dialog').inner_text()
            assert '不生世間無見' in page.locator('#wm-dialog blockquote').inner_text()
            page.screenshot(path=str(OUT / 'ending-direction-not-complete-story-1280x900.png'), full_page=True)
            page.locator('[data-wm-close]').click()
        report.setdefault('finalStates', []).append({'fixture': name, 'count': len(completed), 'revealed': revealed, 'endingEligible': ending, 'next': next_id})
    # Free reading is genuinely accessible and never itself creates completion.
    restore_fixture(page, fixture())
    before = page.evaluate('(key)=>localStorage.getItem(key)', COLLECTION_KEY)
    page.locator('[data-wm-mode="free"]').click()
    assert '四向四果' in page.locator('[data-landmark="fruition_valley"]').inner_text()
    assert page.locator('.wm-fog').count() == 0
    page.locator('[data-landmark="fruition_valley"]').click()
    assert page.locator('#wm-dialog [data-wm-read="' + ORDER[-1] + '"]').count() == 1
    page.locator('[data-wm-close]').click()
    assert page.evaluate('(key)=>localStorage.getItem(key)', COLLECTION_KEY) == before
    assert '0／14' in page.locator('#wm-count').inner_text()
    page.locator('[data-wm-mode="route"]').click()
    report['freeMode'] = 'All14 readable; switching/inspecting does not modify completion or positions'
    context.close()


def real_first_three_flow(browser, base):
    """Never mutate a reading index or completion set in this real-player flow."""
    context = browser.new_context(
        viewport={'width': 1280, 'height': 900}, reduced_motion='reduce',
    )
    context.add_init_script("""
      localStorage.setItem('sutrazen.play.v1','worldmap-qa-preserve-original-journey');
      localStorage.setItem('unrelated-site-setting','preserve-unrelated');
    """)
    page = context.new_page()
    javascript_errors, http_errors = [], []
    page.on('pageerror', lambda e: javascript_errors.append(str(e)))
    page.on('response', lambda r: http_errors.append(r.url) if r.url.startswith(base) and r.status >= 400 else None)
    page.goto(base + 'play/worldmap-v4/', wait_until='domcontentloaded')
    page.wait_for_selector('.wm-world')
    assert '0／14' in page.locator('#wm-count').inner_text()
    page.locator('[data-wm-next]').click()
    finished = []
    stages = []
    for book_id, steps in zip(ORDER[:3], [29, 54, 115]):
        page.wait_for_function(
            '(id)=>document.body?.dataset.collectionBook===id', arg=book_id,
        )
        assert page.locator('body').get_attribute('data-collection-index') == '0'
        assert 'collectionReturn=worldmap-v4' in page.url
        assert page.locator('.collection-reader-return').inner_text() == '回繪本旅程'
        for index in range(1, steps):
            page.locator('#next').click()
            page.wait_for_function(
                '(i)=>document.body?.dataset.collectionIndex===String(i)', arg=index,
            )
            if book_id == 'four-truths' and index == 5:
                page.reload(wait_until='domcontentloaded')
                page.wait_for_function('document.body?.dataset.collectionIndex==="5"')
                page.locator('.collection-reader-return').click()
                page.wait_for_selector('.wm-world')
                assert '0／14' in page.locator('#wm-count').inner_text()
                page.locator('[data-wm-next]').click()
                page.wait_for_function('document.body?.dataset.collectionIndex==="5"')
            if book_id == 'five-aggregates' and index == 3:
                page.screenshot(path=str(OUT / 'actual-reader-five-aggregates-1280x900.png'), full_page=True)
                page.set_viewport_size({'width': 390, 'height': 844})
                settle(page)
                no_overflow(page)
                assert page.locator('body').get_attribute('data-collection-index') == '3'
                page.screenshot(path=str(OUT / 'actual-reader-five-aggregates-390x844.png'), full_page=True)
                page.set_viewport_size({'width': 1280, 'height': 900})
        assert page.locator('#next').inner_text().strip() == '完成這本'
        assert page.evaluate(
            '(key)=>JSON.parse(localStorage.getItem(key)).completed', COLLECTION_KEY,
        ) == finished, 'arrival at last page must not mark completion'
        page.locator('#next').click()
        page.wait_for_url('**/play/worldmap-v4/**')
        page.wait_for_selector('#wm-dialog[open]')
        finished.append(book_id)
        assert page.evaluate(
            '(key)=>JSON.parse(localStorage.getItem(key)).completed', COLLECTION_KEY,
        ) == finished
        assert f'{len(finished)}／14' in page.locator('#wm-count').inner_text()
        city = compact_completion(page, book_id)
        assert city['stage'] == len(finished)
        stages.append(str(city['stage']))
        if len(finished) == 1:
            assert city['features']['truth_dock']
            assert not city['features']['city_body']
        else:
            assert city['features']['city_body']
        assert not city['features']['mindfulness_guard']
        assert not city['features']['calm_insight_messengers']
        page.locator('#wm-dialog img').evaluate_all('els=>Promise.all(els.map(i=>i.decode()))')
        page.screenshot(path=str(OUT / f'actual-feedback-{book_id}-1280x900.png'), full_page=True)
        # The one salient completion action advances to the next actual reader.
        page.locator('#wm-dialog button.primary').first.click()
    page.wait_for_function('document.body?.dataset.collectionBook==="twelve-links"')
    assert page.locator('body').get_attribute('data-collection-index') == '0'
    page.locator('.collection-reader-return').click()
    page.wait_for_selector('.wm-world')
    assert '3／14' in page.locator('#wm-count').inner_text()
    assert page.evaluate("localStorage.getItem('sutrazen.play.v1')") == 'worldmap-qa-preserve-original-journey'
    assert page.evaluate("localStorage.getItem('unrelated-site-setting')") == 'preserve-unrelated'
    page.screenshot(path=str(OUT / 'actual-after-first-three-1280x900.png'), full_page=True)
    assert not javascript_errors and not http_errors, [javascript_errors, http_errors]
    context.close()
    return {'actualReadingSteps': 198, 'books': ORDER[:3],
            'progressChangesOnlyOnExplicitFinish': True, 'cityStages': stages,
            'reloadAndReturnResume': 'Four Truths step5',
            'rotationPreservesPosition': 'Five Aggregates step3',
            'nextAfterThird': 'twelve-links', 'priorJourneyAndUnrelatedKeys': 'preserved',
            'javascriptErrors': javascript_errors, 'httpErrors': http_errors}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report = unchanged_originals()
    report['generatedAssets'] = validate_generated_assets()
    report.update({
        'specifications': ['2026-11-22-map-v4', '2026-11-22-r3'],
        'publication': 'Local review only; not merged or publicly deployed',
        'fixtures': 'Valid collection backups in isolated disposable browser contexts; no product completion shortcuts',
        'physicalSafari': 'Not tested; Chromium viewport simulation only',
        'javascriptErrors': [], 'httpErrors': [],
    })
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
            check_layouts(browser, base, report)
            check_presentation_states(browser, base, report)
            check_resume_modes(browser, base, report)
            check_storage_and_original_modes(browser, base, report)
            check_city_r3(browser, base, report)
            report['actualFirstThree'] = real_first_three_flow(browser, base)
            browser.close()
    finally:
        server.shutdown()
    assert not report['javascriptErrors'] and not report['httpErrors'], [report['javascriptErrors'], report['httpErrors']]
    model = json.loads((OUT / 'route-model-validation.json').read_text())
    assert model['model']['result'] == 'passed'
    report['routeModel'] = {'report': 'route-model-validation.json', 'completionSubsets': model['model']['exhaustiveCompletionSubsets'], 'assertions': model['model']['assertionCount']}
    (OUT / 'validation.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n',
    )
    print(json.dumps({'result': 'passed', 'report': str((OUT / 'validation.json').relative_to(ROOT)),
                      'viewports': len(report['layouts']), 'nativeMapDialogs': sum(x['nativeLandmarkDialogs'] for x in report['layouts']),
                      'cityStates': len(report['cities']), 'actualReadingSteps': report['actualFirstThree']['actualReadingSteps'],
                      'completionSubsets': report['routeModel']['completionSubsets'], 'javascriptErrors': [], 'localHttpErrors': []}, ensure_ascii=False))


if __name__ == '__main__':
    main()
