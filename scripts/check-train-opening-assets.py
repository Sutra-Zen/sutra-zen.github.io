#!/usr/bin/env python3
"""Require the exact author-supplied train illustration before release."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'docs/play/train-opening/assets.json'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--allow-pending', action='store_true', help='Only for explicitly labelled missing-art development checks.')
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text())
    data = (ROOT / 'play/opening/data.js').read_text()
    ready = re.search(r'\bready:\s*(true|false)', data).group(1) == 'true'
    if not ready or manifest.get('status') != 'imported':
        if args.allow_pending:
            print('PENDING: author train illustration is not imported; fallback checks only, not a release approval.')
            return
        raise SystemExit('Formal release blocked: import the author train illustration and record its original/runtime hashes first.')

    def local(path):
        result = (ROOT / path).resolve()
        assert result.is_relative_to(ROOT) and result.is_file(), path
        return result

    original, runtime = manifest['original'], manifest['runtime']
    source_path = local(original['path'])
    source_bytes = source_path.read_bytes()
    assert hashlib.sha256(source_bytes).hexdigest() == original['sha256']
    if source_path.suffix.lower() == '.zip':
        with zipfile.ZipFile(io.BytesIO(source_bytes)) as archive:
            assert archive.testzip() is None
            original_image = archive.read(original['member'])
    else:
        original_image = source_bytes
    runtime_path = local(runtime['path'])
    image_bytes = runtime_path.read_bytes()
    assert image_bytes == original_image, 'Do not silently redraw or re-encode the author illustration.'
    assert len(image_bytes) == runtime['bytes']
    assert hashlib.sha256(image_bytes).hexdigest() == runtime['sha256']
    asset = re.search(r"url:new URL\('([^']+)'", data).group(1)
    assert (ROOT / 'play/opening' / asset).resolve() == runtime_path
    with Image.open(io.BytesIO(image_bytes)) as image:
        assert image.size == (runtime['width'], runtime['height'])
    print('PASS: author original, runtime bytes, dimensions and configured train asset match exactly.')


if __name__ == '__main__':
    main()
