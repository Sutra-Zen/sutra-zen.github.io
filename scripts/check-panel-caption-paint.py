"""Regression: a panel mask must darken artwork without darkening narration.

Serve the repository and optionally set SUTRAZEN_TEST_URL / SUTRAZEN_TEST_ARTIFACTS.
Requires Pillow and Playwright. Compares white text pixels with/without masks.
"""
from io import BytesIO
import json
import os
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

BASE = os.environ.get('SUTRAZEN_TEST_URL', 'http://127.0.0.1:8012/')
OUT = Path(os.environ.get('SUTRAZEN_TEST_ARTIFACTS', '/tmp/picture-book-overlay-tests'))
OUT.mkdir(parents=True, exist_ok=True)
results = []


def pixels(image):
    data = image.convert('RGB').tobytes()
    return list(zip(data[0::3], data[1::3], data[2::3]))


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for name in ['five-aggregates', 'six-senses']:
        for width, height in [(390, 844), (844, 390), (768, 1024), (1024, 768)]:
            page = browser.new_page(viewport={'width': width, 'height': height})
            page.goto(BASE + name + '/book/', wait_until='domcontentloaded')
            page.locator('#page-select').select_option('2')
            for _ in range(1 if name == 'five-aggregates' else 3):
                page.locator('#next').click()
            page.wait_for_function('document.querySelector("#art").complete')
            mask = page.locator('.picture-panel-focus')
            mask.evaluate('(e)=>e.hidden=true')
            before = Image.open(BytesIO(page.locator('#caption').screenshot()))
            mask.evaluate('(e)=>e.hidden=false')
            after = Image.open(BytesIO(page.locator('#caption').screenshot()))
            assert before.size == after.size
            bright = [index for index, rgb in enumerate(pixels(before)) if min(rgb) > 245]
            after_pixels = pixels(after)
            assert len(bright) > 20
            assert all(min(after_pixels[index]) > 243 for index in bright), (name, width, 'narration dimmed')
            results.append({'book': name, 'width': width, 'height': height, 'status': 'pass'})
            print(f'PASS {name} {width}x{height}: narration remains white above image mask', flush=True)
            page.close()
    browser.close()
(OUT / 'caption-paint-results.json').write_text(json.dumps({'status': 'pass', 'checks': results}, indent=2) + '\n')
