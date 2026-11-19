"""Check window alignment, requested labels, verse layout and open sources."""
import json
import os
from pathlib import Path
import re
import subprocess

from lxml import html
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get('SUTRAZEN_TEST_URL', 'http://127.0.0.1:8013/')
OUT = Path(os.environ.get('SUTRAZEN_TEST_ARTIFACTS', '/tmp/reader-polish-tests'))
OUT.mkdir(parents=True, exist_ok=True)
BASELINE = 'f01ffa80e6936c81572f8b9d29e99bb084ab26e5'
story = json.loads((ROOT / 'docs/eightfold-path/storyboard.json').read_text())
sources = json.loads((ROOT / 'docs/eightfold-path/verified-sources.json').read_text())
poem = next(row for row in sources if row['id'] == 'sa771')
assert len(poem['displayExcerpt'].splitlines()) == 4
assert re.sub(r'\s+', '', poem['excerpt']) == re.sub(r'\s+', '', poem['displayExcerpt'])
assert '\u3000' not in poem['displayExcerpt']
assert next(o for o in story['scenes'][3]['presentation']['overlays'] if o['id'] == 'unwholesome-br')['lines'] == ['心不定']
assert all('正業' not in line for o in story['scenes'][5]['presentation']['overlays'] for line in o['lines'])
assert len(story['scenes']) == 13 and sum(len(s['subtitles']) for s in story['scenes']) == 110
names = ['four-truths', 'five-aggregates', 'six-senses', 'twelve-links', 'eightfold-path']
for name in names:
    before = html.fromstring(subprocess.check_output(['git', 'show', BASELINE + ':' + name + '/index.html'], cwd=ROOT))
    after = html.fromstring((ROOT / name / 'index.html').read_bytes())
    assert not after.xpath('//details')
    assert before.xpath('//a/@href') == after.xpath('//a/@href')
    normalized = lambda node: re.sub(r'\s+', '', node.text_content())
    assert [normalized(q) for q in before.xpath('//blockquote')] == [normalized(q) for q in after.xpath('//blockquote')]
print('PASS requested text changes, 13 original scenes/110 subtitles, whitespace-only poem formatting and all five open scripture guides', flush=True)

results = []
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width, height in [(390, 844), (844, 390), (768, 1024), (1024, 768)]:
        page = browser.new_page(viewport={'width': width, 'height': height}, has_touch=True)
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto(BASE + 'six-senses/book/', wait_until='domcontentloaded')
        page.locator('#page-select').select_option('1')
        for offset in range(19):
            if offset:
                page.locator('#next').click()
            page.wait_for_function('document.querySelector("#art").complete && document.querySelector("#art").naturalWidth>0')
            labels = page.locator('.window-label')
            image = page.locator('#art').bounding_box()
            layout = page.evaluate('scenes[1].windowLayout')
            for label in labels.all():
                column = layout['windows'][int(label.get_attribute('data-window'))]
                box = label.bounding_box()
                center = (box['x'] + box['width']/2 - image['x']) / image['width'] * 100
                assert abs(center - column['centerX']) < .1
                assert box['x'] >= image['x'] + image['width']*column['left']/100 - 1
                assert box['x'] + box['width'] <= image['x'] + image['width']*column['right']/100 + 1
                assert box['y'] >= image['y'] + image['height']*column['top']/100 - 1
                assert box['y'] + box['height'] <= image['y'] + image['height']*column['bottom']/100 + 1
            if offset == 18:
                assert labels.count() == 18
                page.screenshot(path=str(OUT / f'eighteen-windows-{width}.png'))
        assert not errors, errors
        page.goto(BASE + 'eightfold-path/book/', wait_until='domcontentloaded')
        page.locator('#page-select').select_option('4')
        for _ in range(4):
            page.locator('#next').click()
        assert page.locator('.art-overlay p').all_text_contents() == ['心不定']
        page.screenshot(path=str(OUT / f'quiet-mind-{width}.png'))
        page.locator('#page-select').select_option('6')
        boxes = []
        for offset in range(8):
            if offset:
                page.locator('#next').click()
            page.evaluate('()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))')
            assert '正業' not in page.locator('#art-overlays').inner_text()
            assert page.locator('#panel-mask .active').count() == 1
            boxes.append(page.locator('#art-frame').bounding_box())
        assert page.locator('#art-overlays > div').count() == 0
        assert all(abs(box[key]-boxes[0][key]) < 1 for box in boxes for key in ['x','y','width','height'])
        page.screenshot(path=str(OUT / f'wholesome-rest-{width}.png'))
        page.locator('#page-select').select_option('13')
        assert page.locator('#verse').text_content().split('\n',1)[1] == poem['displayExcerpt']
        page.locator('#verse').scroll_into_view_if_needed()
        page.screenshot(path=str(OUT / f'poem-{width}.png'))
        page.locator('#page-select').select_option('14')
        assert page.locator('#position-text').inner_text() == '111 / 111 頁'
        assert page.locator('#next').is_disabled()
        assert '以原經文為準' in page.locator('#narration').inner_text()
        assert '溫柔起點' in page.locator('#narration').inner_text()
        page.locator('#narration p').last.scroll_into_view_if_needed()
        page.screenshot(path=str(OUT / f'afterword-{width}.png'))
        position = page.locator('#position-text').inner_text()
        page.set_viewport_size({'width': height, 'height': width})
        assert page.locator('#position-text').inner_text() == position
        page.set_viewport_size({'width': width, 'height': height})
        page.locator('.reading-links a').click()
        page.wait_for_url('**/eightfold-path/#sources', wait_until='domcontentloaded')
        assert not page.locator('#sources details').count()
        assert page.locator('#sa771 .source-poem').inner_text() == poem['displayExcerpt']
        page.locator('.book-cover').click()
        assert page.locator('#position-text').inner_text() == position
        for name in names:
            page.goto(BASE + name + '/#sources', wait_until='domcontentloaded')
            assert page.locator('details').count() == 0
            for quote in page.locator('blockquote').all():
                assert quote.is_visible()
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        assert not errors, errors
        results.append({'width': width, 'height': height, 'status': 'pass'})
        print(f'PASS {width}x{height}: all window label states/bounds, corrected labels, steady scene6, four-line poem, afterword/return, five open sources', flush=True)
        page.close()
    browser.close()
(OUT/'polish-results.json').write_text(json.dumps({'baseline': BASELINE, 'viewports': results, 'originalSubtitles':110,'afterwordPage':111,'sourceGuides':5,'realIPadSafari':'not tested'}, indent=2)+'\n')
