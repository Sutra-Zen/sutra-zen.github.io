#!/usr/bin/env python3
"""Reuse the existing worldmap shell at /game/; never copy its runtime or data.

Only five shell differences are intentional: base URL, title, brand destination,
public-trial badge and hidden internal art-review controls. All asset and module
URLs continue to use the one source.
"""
import argparse
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'play/worldmap-v4/index.html'
TARGET = ROOT / 'game/index.html'


def render_entry():
    shell = SOURCE.read_text()
    assert '<base ' not in shell, 'Source acquired a base URL; review shell mounting explicitly.'
    assert shell.count('<head>') == 1
    shell = shell.replace('<head>', '<head><base href="../play/worldmap-v4/">', 1)
    shell, titles = re.subn(r'<title>.*?</title>', '<title>SutraZen 繪本旅程｜試玩版</title>', shell, count=1)
    shell, brands = re.subn(r'(<header\b[^>]*>\s*<a )href="[^"]*"', r'\1href="../../game/"', shell, count=1)
    shell, badges = re.subn(r'<span class="proposal-stamp">.*?</span>', '<span class="proposal-stamp">試玩版</span>', shell, count=1)
    assert titles == brands == badges == 1
    assert shell.count('<details class="wm-art-details">') == 1
    shell = shell.replace('<details class="wm-art-details">', '<details class="wm-art-details" hidden>', 1)
    assert '<meta name="robots" content="noindex,nofollow">' in shell, 'Public trial stays deliberately noindex.'
    return shell


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    output = render_entry()
    if args.check:
        assert TARGET.read_text() == output, 'Run python3 scripts/build-game-entry.py to sync the public entry shell.'
    else:
        TARGET.parent.mkdir(parents=True, exist_ok=True)
        TARGET.write_text(output)
    print('/game/ shell shares worldmap runtime/data; base/title/brand/trial badge/hidden art-review controls: OK')


if __name__ == '__main__':
    main()
