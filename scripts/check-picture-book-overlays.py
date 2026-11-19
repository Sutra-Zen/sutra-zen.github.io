"""Verify image topics, panel focus, content retention and reader interactions.

Run with a server at SUTRAZEN_TEST_URL (repository root URL); defaults to the
current workspace server. Requires Playwright, lxml and Pillow.
"""
import json
import os
import re
from pathlib import Path
import subprocess
from urllib.parse import urlsplit

from lxml import html
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get('SUTRAZEN_TEST_URL', 'http://127.0.0.1:8012/')
OUT = Path(os.environ.get('SUTRAZEN_TEST_ARTIFACTS', '/tmp/picture-book-overlay-tests'))
OUT.mkdir(parents=True, exist_ok=True)
BASELINE = 'f01ffa80e6936c81572f8b9d29e99bb084ab26e5'


def published(path):
    return subprocess.check_output(['git', 'show', BASELINE + ':' + path], cwd=ROOT, text=True)


def variable(source, name):
    import re
    match = re.search(r'const\s+' + name + r'\s*=\s*', source)
    return json.JSONDecoder().raw_decode(source[match.end():])[0]


book = variable((ROOT / 'eightfold-path/book/book-data.js').read_text(), 'BOOK')
old = variable(published('eightfold-path/book/book-data.js'), 'BOOK')
assert len(book['pages']) == 111
assert book['pages'][-1].get('afterword') and '溫柔起點' in book['pages'][-1]['lines'][-1]
for before, after in zip(old['pages'], book['pages']):
    expected = {k: v for k, v in before.items() if k != 'note'}
    if before['scene'] == 13:
        expected['verse'] = next(r for r in json.loads((ROOT / 'docs/eightfold-path/verified-sources.json').read_text()) if r['id'] == 'sa771')['displayExcerpt']
    assert expected == after
assert old['summary'] == book['summary']
handoff = json.loads((ROOT / 'docs/eightfold-path/storyboard.json').read_text())
source_handoff = json.loads(published('docs/eightfold-path/storyboard.json'))
for scene in handoff['scenes']:
    scene = dict(scene)
    scene.pop('presentation')
    original = dict(source_handoff['scenes'][scene['scene'] - 1])
    original.pop('presentation', None)
    assert scene == original
assert handoff['scenes'][0]['presentation']['overlays'] == []
assert handoff['scenes'][12]['presentation']['overlays'] == []
assert handoff['scenes'][2]['presentation']['overlays'][0]['lines'] == [
    '八正道：正志', '十善業道：不貪，不瞋恚']
for scene in handoff['scenes']:
    plan = scene['presentation']
    assert plan['coordinateBasis'] == 'displayed-image-percent'
    for overlay in plan['overlays']:
        assert all(key in overlay for key in ['lines', 'x', 'y', 'width', 'align', 'portrait'])

legacy = {}
for name, count in [('five-aggregates', 54), ('six-senses', 115)]:
    path = name + '/book/index.html'
    source = (ROOT / path).read_text()
    before = published(path)
    actual_scenes, original_scenes = variable(source, 'scenes'), variable(before, 'scenes')
    comparable = json.loads(json.dumps(actual_scenes))
    if name == 'six-senses':
        comparable[1].pop('windowLayout', None)
        for actual, original in zip(comparable[1]['pages'], original_scenes[1]['pages']):
            assert [o['text'] for o in actual['overlays']] == [o['text'] for o in original['overlays']]
            actual['overlays'] = original['overlays']
    assert comparable == original_scenes
    # Includes every byte of the existing embedded Six Senses images.
    assert variable(source, 'previewImages') == variable(before, 'previewImages')
    old_tree, new_tree = html.fromstring(before), html.fromstring(source)
    assert [html.tostring(e) for e in old_tree.xpath('//noscript')] == [html.tostring(e) for e in new_tree.xpath('//noscript')]
    scenes = variable(source, 'scenes')
    assert sum(len(s['pages']) for s in scenes) == count
    legacy[name] = scenes

assert (ROOT / 'index.html').read_text() == published('index.html')
for name in ['four-truths', 'twelve-links']:
    for path in subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASELINE, name], cwd=ROOT, text=True).splitlines():
        if path in ['four-truths/index.html', 'twelve-links/index.html']:
            continue  # Canonical source content is checked below after unfolding.
        assert (ROOT / path).read_bytes() == subprocess.check_output(['git', 'show', BASELINE + ':' + path], cwd=ROOT)
for name in ['four-truths', 'five-aggregates', 'six-senses', 'twelve-links', 'eightfold-path']:
    old_guide = html.fromstring(published(name + '/index.html'))
    new_guide = html.fromstring((ROOT / name / 'index.html').read_bytes())
    normalize = lambda text: re.sub(r'\s+', '', text)
    assert [normalize(e.text_content()) for e in old_guide.xpath('//blockquote')] == [normalize(e.text_content()) for e in new_guide.xpath('//blockquote')]
    assert old_guide.xpath('//a/@href') == new_guide.xpath('//a/@href')
    assert not new_guide.xpath('//details')
print('PASS original 110/54/115 pages retained; added one afterword; all guide scripture visible with words/links preserved', flush=True)


def overlaps(a, b):
    return a['x'] < b['x'] + b['width'] - .5 and a['x'] + a['width'] > b['x'] + .5 and a['y'] < b['y'] + b['height'] - .5 and a['y'] + a['height'] > b['y'] + .5


def swipe(locator, dx=-140, dy=0):
    locator.evaluate('''(element, delta) => {
      element.dispatchEvent(new TouchEvent('touchstart', {bubbles:true,
        touches:[new Touch({identifier:0,target:element,clientX:220,clientY:100})]}));
      element.dispatchEvent(new TouchEvent('touchend', {bubbles:true,
        changedTouches:[new Touch({identifier:0,target:element,clientX:220+delta[0],clientY:100+delta[1]})]}));
    }''', [dx, dy])


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width, height in [(390, 844), (844, 390), (768, 1024), (1024, 768)]:
        for name, count in [('eightfold-path', 111), ('five-aggregates', 54), ('six-senses', 115)]:
            g = browser.new_page(viewport={'width': width, 'height': height}, has_touch=True)
            errors = []
            g.on('pageerror', lambda error: errors.append(str(error)))
            g.goto(BASE + name + '/book/', wait_until='domcontentloaded')
            g.locator('#next').wait_for(state='visible')
            last_scene = None
            last_boxes = None
            last_ids = None
            for index in range(count):
                if index:
                    g.locator('#next').click()
                assert g.locator('#position-text').inner_text() == f'{index+1} / {count} 頁'
                image_visible = g.locator('#art-frame').is_visible()
                if image_visible:
                    g.wait_for_function('document.querySelector("#art").complete && document.querySelector("#art").naturalWidth>0')
                if name == 'eightfold-path':
                    item = book['pages'][index]
                    assert g.locator('#narration > p').all_text_contents() == item['lines']
                    expected = item['verseLabel'] + '\n' + item['verse'] if item['verse'] else ''
                    assert g.locator('#verse').text_content() == expected
                    plan = handoff['scenes'][item['scene']-1]['presentation'] if item['scene'] <= 13 else {'overlays': []}
                    overlays = [o for o in plan['overlays'] if o['fromSubtitle'] <= item['subtitle'] <= o['throughSubtitle']]
                    assert g.locator('#art-overlays > div').count() == len(overlays)
                    assert not g.locator('#chapter-note').count()
                    if overlays:
                        # Wait for the responsive band/image observer to settle.
                        g.evaluate('()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))')
                        frame = g.locator('#art-frame').bounding_box()
                        boxes = []
                        for position, overlay in enumerate(overlays):
                            element = g.locator('.art-overlay').nth(position)
                            assert element.locator('p').all_text_contents() == overlay['lines']
                            box = element.bounding_box()
                            variant = {**overlay, **(overlay['portrait'] if width < height else {})}
                            for coordinate in ['x', 'y', 'width']:
                                normalized = (box[coordinate] - frame[coordinate]) / frame['width' if coordinate != 'y' else 'height'] * 100 if coordinate in ['x', 'y'] else box['width'] / frame['width'] * 100
                                assert abs(normalized - variant[coordinate]) < .1, (name, index, coordinate)
                            assert box['y'] + box['height'] <= frame['y'] + frame['height'] + 1, (index, box, frame)
                            assert element.evaluate('(e)=>e.scrollWidth<=e.clientWidth+1'), (index, element.inner_text())
                            assert not overlaps(box, g.locator('#caption').bounding_box())
                            assert not overlaps(box, g.locator('.scripture').bounding_box())
                            for button in ['#previous', '#next', '.position']:
                                assert not overlaps(box, g.locator(button).bounding_box()), (width, height, item['scene'], index, overlay['id'], button, box, g.locator(button).bounding_box())
                            if item['scene'] == 3:
                                assert element.locator('p').count() == 2
                                for region in plan['protectedRegions']:
                                    protected = {'x': frame['x'] + frame['width'] * region['x']/100, 'y': frame['y'] + frame['height'] * region['y']/100, 'width': frame['width'] * region['width']/100, 'height': frame['height'] * region['height']/100}
                                    assert not overlaps(box, protected), (region['name'], width, index)
                            boxes.append(box)
                        ids = [overlay['id'] for overlay in overlays]
                        if last_scene == item['scene'] and last_boxes and ids == last_ids:
                            for before, after in zip(last_boxes, boxes):
                                assert all(abs(before[key]-after[key]) < 1 for key in ['x','y','width','height']), (width, height, item['scene'], index, before, after)
                        last_boxes = boxes
                        last_ids = ids
                    else:
                        last_boxes = None
                    last_scene = item['scene']
                    expected_focus = item['focusPanel']
                    mask = g.locator('#panel-mask')
                    if expected_focus:
                        assert mask.locator('.active').get_attribute('data-panel') == expected_focus
                        assert mask.locator('span:not(.active)').count() == 3
                    else:
                        assert mask.is_hidden()
                else:
                    entry = g.evaluate('pages[current]')
                    source_scene = legacy[name][entry['sceneIndex']]
                    mask = g.locator('.picture-panel-focus')
                    expected_verse = source_scene.get('heart') or entry['verse']
                    assert g.locator('#verse').text_content() == expected_verse
                    definition = g.evaluate('PANEL_FOCUS.scenes[pages[current].sceneIndex+1] || null')
                    if definition:
                        assert mask.is_visible()
                        local = index - g.evaluate('sceneStarts[pages[current].sceneIndex]')
                        assert mask.locator('.active').get_attribute('data-panel') == definition['pages'][local]
                        assert mask.locator('span:not(.active)').count() == len(definition['panels']) - 1
                        g.evaluate('()=>new Promise(resolve=>requestAnimationFrame(resolve))')
                        actual = g.locator('#art').evaluate('''e=>{const r=e.getBoundingClientRect(),s=Math.min(r.width/e.naturalWidth,r.height/e.naturalHeight);return {x:r.x+(r.width-e.naturalWidth*s)/2,y:r.y+(r.height-e.naturalHeight*s)/2,width:e.naturalWidth*s,height:e.naturalHeight*s}}''')
                        rect = mask.bounding_box()
                        assert all(abs(actual[key]-rect[key]) < 1 for key in actual), (name, width, index)
                    else:
                        assert mask.is_hidden()
                assert g.evaluate('document.documentElement.scrollWidth <= innerWidth')
            assert g.locator('#next').is_disabled()
            target = '3' if name == 'eightfold-path' else '2'
            g.locator('#page-select').select_option(target)
            g.locator('#next').click()
            position = g.locator('#position-text').inner_text()
            g.set_viewport_size({'width': height, 'height': width})
            assert g.locator('#position-text').inner_text() == position
            g.set_viewport_size({'width': width, 'height': height})
            g.locator('#next').press('ArrowRight')
            before = g.evaluate('current')
            swipe(g.locator('#art-frame'))
            assert g.evaluate('current') == before + 1
            if width > height:
                g.locator('#open-verse').click()
                assert g.locator('#dialog-verse').text_content() == g.locator('#verse').text_content()
                g.locator('#verse-dialog button').click()
            assert not errors, errors
            g.screenshot(path=str(OUT / f'{name}-{width}.png'))
            print(f'PASS {name} {width}x{height}: {count} pages, all overlay/focus states, image bounds, stable positions, controls/rotation/dialog', flush=True)
            g.close()
    browser.close()
(OUT/'results.json').write_text(json.dumps({'baseline':BASELINE,'books':{'eightfold-path':111,'five-aggregates':54,'six-senses':115},'viewports':[[390,844],[844,390],[768,1024],[1024,768]],'totalPageChecks':1120,'status':'pass','realIPadSafari':'not tested'},indent=2)+'\n')
