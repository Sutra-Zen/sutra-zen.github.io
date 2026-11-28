#!/usr/bin/env python3
"""Paginate the intact v3 narration using the established caption/image/scripture reader."""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs/mindfulness'


def caption_parts(text):
    """Keep every original character while fitting complete phrases into caption pages."""
    phrases = re.findall(r'[^，。；！？]*[，。；！？]|[^，。；！？]+$', text)
    parts = []
    for phrase in phrases:
        if parts and len(parts[-1]) + len(phrase) <= 64:
            parts[-1] += phrase
        else:
            parts.append(phrase)
    assert ''.join(parts) == text and max(map(len, parts)) <= 80
    return parts


def compile_book():
    story = json.loads((DOCS / 'storyboard.json').read_text())
    edits = json.loads((DOCS / 'reader-edits.json').read_text())

    def reader_narration(text):
        """Keep approved player copy separate from the original handoff/quotes."""
        for original, replacement in edits['narrationReplacements'].items():
            text = text.replace(original, replacement)
        return text

    catalog = json.loads((DOCS / 'scripture-catalog.json').read_text())['quotes']
    manifest = json.loads((DOCS / 'asset-manifest.json').read_text())
    split = json.loads((DOCS / 'SPLIT_MANIFEST.json').read_text())
    assert story['version'] == 3 and len(story['scenes']) == 25
    assert len(catalog) == 18 and sum(len(s['scriptureRefs']) for s in story['scenes']) == 27
    for row in split:
        data = (DOCS / row['path']).read_bytes()
        assert len(data) == row['size_bytes']
        assert hashlib.sha256(data).hexdigest() == row['sha256'], row['path']
    assets = {a['path']: a for a in manifest}
    quotes = {q['id']: q for q in catalog}
    scenes = []
    for scene in story['scenes']:
        summary = scene['id'] == 'S25'
        paragraphs = [] if summary else [dict(p, text=reader_narration(p['text']))
                                          for p in scene['narrationParagraphs']]
        if not summary:
            assert '\n\n'.join(p['text'] for p in paragraphs) == reader_narration(scene['narration'])
        groups = []
        for ref in scene['scriptureRefs']:
            indices = ref['narrationParagraphs']
            assert indices and max(indices) <= len(paragraphs)
            q = quotes[ref['quoteId']]
            for frame in q['evidenceFrames']:
                assert (DOCS / frame).is_file()
            # Consecutive groups of the same quote may share a card, preserving every mapping.
            if groups and groups[-1]['quoteId'] == ref['quoteId'] and groups[-1]['relation'] == ref['relation']:
                group = groups[-1]
            else:
                group = {'quoteId': ref['quoteId'], 'relation': ref['relation'], 'mappings': [],
                         'source': q['sourceLabelAsVideo'], 'text': q['videoText'],
                         'evidenceFrames': q['evidenceFrames'], 'afterParagraph': 0}
                groups.append(group)
            group['mappings'].append({'paragraphs': indices, 'focus': ref['focus']})
            group['afterParagraph'] = max(group['afterParagraph'], max(indices))
        asset = assets[scene['asset']]
        scenes.append({'id': scene['id'], 'title': scene['title'], 'image': scene['asset'],
                       'dimensions': [asset['width'], asset['height']], 'alt': scene['visual'],
                       'paragraphs': paragraphs, 'quotes': groups,
                       'artOverlay': scene['artOverlay'], 'bakedText': scene['bakedText'],
                       'summaryRows': scene.get('summaryRows', []),
                       'scrimOpacity': scene.get('scrimOpacity', 0), 'reference': scene['reference']})
    assert 'BD74B990' in scenes[2]['image']
    assert 'B8B53DDC' in scenes[17]['image'] and '3DF2D5E4' in scenes[20]['image']
    assert [(q['quoteId'], q['afterParagraph']) for q in scenes[9]['quotes']] == [('Q05', 2), ('Q06', 4)]
    assert not scenes[24]['paragraphs'] and not scenes[24]['quotes'] and len(scenes[24]['summaryRows']) == 4
    pages = []
    for scene in scenes:
        scene['start'] = len(pages)
        for number, paragraph in enumerate(scene['paragraphs'], 1):
            paired = [dict(q, mappings=[m for m in q['mappings'] if number in m['paragraphs']])
                      for q in scene['quotes'] if any(number in m['paragraphs'] for m in q['mappings'])]
            for part, text in enumerate(caption_parts(paragraph['text']), 1):
                pages.append({'scene': scene['id'], 'title': scene['title'], 'paragraphId': paragraph['id'],
                              'paragraphNumber': number, 'part': part, 'lines': [text], 'quotes': paired,
                              'image': '../../docs/mindfulness/' + scene['image'], 'dimensions': scene['dimensions']})
        if scene['summaryRows']:
            pages.append({'scene': scene['id'], 'title': scene['title'], 'lines': [], 'quotes': [],
                          'image': '../../docs/mindfulness/' + scene['image'], 'dimensions': scene['dimensions'],
                          'summary': True})
    pages.append({'scene': 'afterword', 'title': '製作說明｜走入經藏的起點', 'lines': [
        '本繪本所呈現的內容，係以《中阿含經》〈念處經〉為主，參照《中阿含經》〈念經〉、《雜阿含經》、《增壹阿含經》及《增支部》〈顛倒經〉所製作。',
        '為了讓讀者更親近佛法，我們以圖文並茂的方式，用白話語言說明經意。',
        '然而，繪本的詮釋難免簡略，無法完全涵蓋原經的深義。解讀仍請以原經文為準。',
        '我們誠摯地鼓勵讀者參閱原經文，細細品味佛陀的智慧與慈悲。',
        '也希望這本繪本能成為您走入經藏的起點。',
    ], 'quotes': [], 'image': None, 'dimensions': None, 'afterword': True})
    return '// Generated by scripts/build-mindfulness.py from the intact v3 handoff.\nconst BOOK = ' + json.dumps({
        'title': '四念處與四顛倒', 'version': 3, 'layout': 'caption-art-scripture', 'scenes': scenes, 'pages': pages,
    }, ensure_ascii=False, indent=2) + ';\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    target = ROOT / 'mindfulness/book/book-data.js'
    result = compile_book()
    if args.check:
        assert target.read_text() == result, 'Rebuild book data.'
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(result)
    print('v3: 25 scenes, 92 original narration paragraphs, 18 quotes, 27 mappings; 91 file hashes OK')
