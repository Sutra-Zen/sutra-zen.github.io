#!/usr/bin/env python3
"""Build book 07 from the author's storyboard, overlays and verified sources."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs/four-purities-six-recollections'


def compile_book():
    story = json.loads((DOCS / 'storyboard.json').read_text())
    sources = json.loads((DOCS / 'verified-sources.json').read_text())
    assets = json.loads((DOCS / 'assets-manifest.json').read_text())
    art = {a['path']: a for a in assets if a['role'] == 'illustration'}
    assert len(art) == 8
    for a in assets:
        raw = (DOCS / a['path']).read_bytes()
        assert len(raw) == a['bytes']
        assert hashlib.sha256(raw).hexdigest() == a['sha256'], a['path']
    corrections_path = DOCS / 'editorial-corrections.json'
    corrections = json.loads(corrections_path.read_text()) if corrections_path.exists() else []
    assignments = json.loads((DOCS / 'image-assignments.json').read_text())
    pages, scenes = [], []
    for scene in story['scenes']:
        end = scene['id'] == 'END'
        asset = assignments.get(scene['id'], scene['asset'])
        scenes.append({'id': scene['id'], 'title': scene['title'], 'start': len(pages),
                       'topSubtitleLayout': {'align': 'left', 'color': 'black'},
                       'artOverlay': scene['artOverlay']})
        cues = scene['topSubtitle']['cues']
        if end:
            cues = [{'startSec': scene['startSec'], 'text': ''}]
        for number, cue in enumerate(cues, 1):
            quote_key = 'S06b' if scene['id'] == 'S06' and cue['startSec'] >= 351 else scene['id']
            quote = sources['quotes'].get(quote_key, {})
            text = cue['text']
            for correction in corrections:
                if correction['scene'] == scene['id'] and correction['startSec'] == cue['startSec']:
                    assert text == correction['original']
                    text = correction['replacement']
            pages.append({'scene': scene['id'], 'subtitle': number, 'atSec': cue['startSec'],
                          'title': scene['title'], 'lines': [text] if text else [],
                          'image': '../../docs/four-purities-six-recollections/' + asset,
                          'dimensions': [art[asset]['width'], art[asset]['height']],
                          'verse': '\n\n'.join(quote.get('blocks', [])),
                          'verseLabel': quote.get('label', ''),
                          'source': '../#' + quote['canon'].replace('.', '-') if quote else None,
                          'quoteKey': quote_key if quote else None, 'end': end})
    assert sum(len(s['topSubtitle']['cues']) for s in story['scenes']) == 93
    assert len(pages) == 94
    scenes.append({'id': 'afterword', 'title': '製作說明｜溫柔的起點', 'start': len(pages),
                   'topSubtitleLayout': {'align': 'left', 'color': 'white'}, 'artOverlay': []})
    pages.append({'scene': 'afterword', 'subtitle': 1, 'atSec': None,
                  'title': '製作說明｜溫柔的起點', 'lines': [
                      '本繪本所呈現的內容，係以《相應部》55.1〈轉輪王經〉為主，參照《雜阿含經》第61、554、843經所製作。',
                      '為了讓讀者更親近佛法，我們以圖文並茂的方式，用白話語言說明經意。',
                      '然而，繪本的詮釋難免簡略，無法完全涵蓋原經的深義。解讀仍請以原經文為準。',
                      '我們誠摯地鼓勵讀者參閱原經文，細細品味佛陀的智慧與慈悲。',
                      '也希望這本繪本能成為您走入經藏的起點。'],
                  'image': None, 'dimensions': None, 'verse': '', 'verseLabel': '', 'source': None,
                  'afterword': True})
    return '// Generated from the original handoff by scripts/build-four-purities-six-recollections.py\nconst BOOK = ' + json.dumps({
        'title': story['title'], 'videoId': story['videoId'], 'scenes': scenes, 'pages': pages,
    }, ensure_ascii=False, indent=2) + ';\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    target = ROOT / 'four-purities-six-recollections/book/book-data.js'
    result = compile_book()
    if args.check:
        assert target.read_text() == result
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(result)
    print('8 illustrations / 93 original captions / closing artwork / afterword = 95 pages; hashes OK')
