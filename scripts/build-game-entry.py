#!/usr/bin/env python3
"""Mount the shared immersive game shell at /game/ without a <base> hash trap.

HTML asset/navigation URLs are root-absolute. Runtime, original readers and
artwork remain single-source; title-art readiness reflects the supplied file.
"""
import argparse
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'play/worldmap-v4/index.html'
TARGET = ROOT / 'game/index.html'
TITLE_ART = ROOT / 'play/assets/CC1A7C32-0620-4DB2-BCD2-A9457A83C259.jpeg'


def render_entry():
    shell = SOURCE.read_text()
    assert '<base' not in shell.lower(), 'Do not reintroduce a base URL for hash navigation.'
    for value in re.findall(r'(?<![\w-])(?:href|src)="([^"]*)"', shell):
        assert value.startswith(('/', '#', 'https://', 'http://', 'data:')), value
    assert shell.count('data-title-art-ready="pending"') == 1
    shell = shell.replace('data-title-art-ready="pending"', f'data-title-art-ready="{str(TITLE_ART.is_file()).lower()}"', 1)
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
    print('/game/ immersive shell shares runtime/data; absolute URLs, title readiness and hidden art-review controls: OK')


if __name__ == '__main__':
    main()
