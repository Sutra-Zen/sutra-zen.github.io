#!/usr/bin/env python3
"""Apply/check only the 15 guide heads, sitemap, robots and Google file hash."""
import argparse
import hashlib
import json
from site_seo import ROOT, DATA, apply_page_seo, pages, sitemap, robots


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = {}
    for row in pages():
        path = ROOT / row["source_path"]
        outputs[path] = apply_page_seo(path.read_text(), row["source_path"]).encode()
    outputs[ROOT / "sitemap.xml"] = sitemap()
    path = ROOT / "robots.txt"
    outputs[path] = robots(path.read_text() if path.exists() else None).encode()
    verification = json.loads((DATA / "site-verification.json").read_text())
    raw = (ROOT / verification["filename"]).read_bytes()
    assert len(raw) == verification["bytes"]
    assert hashlib.sha256(raw).hexdigest() == verification["sha256"], "Keep the Google original file unchanged."
    for path, content in outputs.items():
        if args.check:
            assert path.read_bytes() == content, f"Stale SEO metadata: {path.relative_to(ROOT)}"
        elif not path.exists() or path.read_bytes() != content:
            path.write_bytes(content)
    print("2026-11-21-r2: 15 page heads / 15 sitemap URLs / robots / original Google file: OK")


if __name__ == "__main__":
    main()
