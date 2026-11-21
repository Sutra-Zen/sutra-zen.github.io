#!/usr/bin/env python3
"""Independently verify r2 metadata, preserved content, HTTP and build outputs."""
import argparse
import ast
import functools
import hashlib
import http.server
import importlib.util
import json
import re
import subprocess
import threading
import urllib.request
from pathlib import Path
from urllib import robotparser
from xml.etree import ElementTree as ET

from lxml import html
from PIL import Image
from site_seo import ROOT, DATA, apply_page_seo, pages, robots

BASELINE = "db3a882b4ec2d4dd7647cbbeef9f4622a214cb84"
OUT = ROOT / "docs/previews/seo-r2"


def old(path):
    return subprocess.check_output(["git", "show", BASELINE + ":" + path], cwd=ROOT)


def inspect_page(raw, row):
    tree = html.fromstring(raw)
    head = tree.find("head")
    assert head.xpath("./title/text()") == [row["seo_title"]], row["source_path"]
    assert head.xpath('./meta[translate(@name,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz")="description"]/@content') == [row["meta_description"]]
    assert head.xpath('./link[@rel="canonical"]/@href') == [row["canonical_url"]]
    assert not head.xpath('./meta[contains(translate(@content,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"noindex")]')
    assert head.xpath('./meta[@property="og:title"]/@content') == [row["seo_title"]]
    assert head.xpath('./meta[@property="og:description"]/@content') == [row["meta_description"]]
    assert head.xpath('./meta[@property="og:url"]/@content') == [row["canonical_url"]]
    assert head.xpath('./meta[@name="twitter:title"]/@content') == [row["seo_title"]]
    image = head.xpath('./meta[@property="og:image"]/@content')
    assert len(image) == 1 and image[0].startswith("https://sutra-zen.github.io/")
    assert not image[0].startswith("data:")
    json_nodes = head.xpath('./script[@type="application/ld+json"]')
    assert len(json_nodes) == 1
    graph = json.loads(json_nodes[0].text)
    types = [node["@type"] for node in graph["@graph"]]
    assert types == (["WebSite", "WebPage"] if row["order"] == 0 else ["WebPage"])
    webpage = graph["@graph"][-1]
    assert webpage["url"] == row["canonical_url"] and webpage["name"] == row["seo_title"]
    assert webpage["description"] == row["meta_description"]
    assert not any(key in webpage for key in ["datePublished", "dateModified", "uploadDate"])
    return tree, image[0]


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def copyfile(self, source, output):
        try:
            super().copyfile(source, output)
        except (BrokenPipeError, ConnectionResetError):
            pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    rows = pages()
    subprocess.run(["python3", "-B", "scripts/build-seo.py", "--check"], cwd=ROOT, check=True)
    report = {"handoff_revision": "2026-11-21-r2", "baseline": BASELINE,
              "pages": [], "guideGenerators": [], "bodyBytesUnchanged": True,
              "readerArtworkAndOtherCodeUnchanged": True, "browser": None}
    for row in rows:
        name = row["source_path"]
        raw, before = (ROOT / name).read_bytes(), old(name)
        tree, image = inspect_page(raw, row)
        assert raw.split(b"</head>", 1)[1] == before.split(b"</head>", 1)[1], name
        # Preserve styles, executable scripts, charset, viewport and crawler directives.
        a, b = html.fromstring(before).find("head"), tree.find("head")
        for path in ["./style", './script[not(@type="application/ld+json")]',
                     './meta[@name="robots" or @name="googlebot" or @charset]',
                     './meta[@name="viewport"]', './link[@rel="stylesheet"]']:
            assert [html.tostring(e, with_tail=False) for e in a.xpath(path)] == [html.tostring(e, with_tail=False) for e in b.xpath(path)], (name, path)
        assert apply_page_seo(raw.decode(), name).encode() == raw, "Not idempotent: " + name
        record = dict(row)
        record.update({"titleDescriptionCanonical": "passed", "body": "byte-identical",
                       "bodySha256": hashlib.sha256(raw.split(b"</head>", 1)[1]).hexdigest(),
                       "ogImage": image, "jsonLd": "valid WebSite/WebPage only"})
        report["pages"].append(record)
    # Exercise duplicates and policy retention independently of the existing simple heads.
    fixture = (ROOT / "index.html").read_text().replace("</head>", '<title>stale</title><meta NAME="DESCRIPTION" content="stale"><link rel="canonical" href="https://old.invalid/"></head>', 1)
    inspect_page(apply_page_seo(fixture, "index.html").encode(), rows[0])
    policy = "User-agent: GPTBot\nDisallow: /\n\nUser-agent: OAI-SearchBot\nAllow: /\n"
    result = robots(policy)
    assert result.startswith(policy) and robots(result) == result
    report["duplicateTagsAndExistingCrawlerPolicy"] = "passed"
    changed = subprocess.check_output(["git", "diff", "--name-only", BASELINE], cwd=ROOT, text=True).splitlines()
    allowed = {r["source_path"] for r in rows} | {"AGENTS.md", "README.md", "docs/PROJECT.md", "docs/HANDOFF.md", "scripts/site_seo.py", "scripts/build-seo.py", "scripts/check-seo.py", "sitemap.xml", "robots.txt", "googlee0c995331ec518ae.html"} | {"scripts/build-" + name + ".py" for name in ["anapana", "four-jhanas", "five-roots-powers", "seven-factors"]}
    assert all(path in allowed or path.startswith(("docs/seo/", "docs/previews/seo-r2/")) for path in changed), changed
    assert (ROOT / "docs/right-effort/verified-sources.json").read_bytes() == old("docs/right-effort/verified-sources.json")
    assert "《相應部》49.23–34（節錄）｜依戒修習四正勤" in (ROOT / "right-effort/index.html").read_text()
    home = html.parse(str(ROOT / "index.html"))
    assert home.xpath('//h1/text()') == ["三十七道品修道地圖"]
    assert len(home.xpath('//ol[contains(@class,"sz-books")]/li')) == 14
    dhamma = json.loads(re.search(r"const dhammaData = (.*?);\s*\n", (ROOT / "index.html").read_text())[1])
    assert len(dhamma) == 32 and all(html.fragment_fromstring(v["content"], create_parent=True).xpath('.//a[contains(@class,"sz-topic-resource")]') for v in dhamma.values())
    report["shelfBooks"] = 14
    report["mapNodes"] = 32
    for slug, function in [("anapana", "compile_guide"), ("four-jhanas", "guide"), ("five-roots-powers", "guide"), ("seven-factors", "guide")]:
        path = ROOT / "scripts" / ("build-" + slug + ".py")
        spec = importlib.util.spec_from_file_location("builder_" + slug.replace("-", "_"), path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if slug == "anapana":
            content = module.compile_guide(json.loads((ROOT / "docs/anapana/verified-sources.json").read_text()))
        else:
            _, content = module.guide()
        row = next(row for row in rows if row["source_path"] == slug + "/index.html")
        inspect_page(content.encode(), row)
        assert content == (ROOT / row["source_path"]).read_text(), slug
        # The reader-producing functions themselves were not edited.
        before = ast.parse(old(str(path.relative_to(ROOT))))
        after = ast.parse(path.read_text())
        for node in before.body:
            if isinstance(node, ast.FunctionDef) and node.name in ["book", "compile_book"]:
                new = next(n for n in after.body if isinstance(n, ast.FunctionDef) and n.name == node.name)
                assert ast.dump(node) == ast.dump(new), slug
        report["guideGenerators"].append({"source_path": row["source_path"], "output": "matches committed HTML including SEO", "readerFunction": "unchanged"})
    urls = [r["canonical_url"] for r in rows]
    xml = ET.parse(ROOT / "sitemap.xml")
    locs = [node.text for node in xml.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    assert locs == urls and len(set(locs)) == 15
    assert not xml.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod")
    policy_text = (ROOT / "robots.txt").read_text()
    rp = robotparser.RobotFileParser()
    rp.parse(policy_text.splitlines())
    assert (rp.site_maps() or []).count("https://sutra-zen.github.io/sitemap.xml") == 1
    for bot in ["Googlebot", "Bingbot", "OAI-SearchBot"]:
        assert all(rp.can_fetch(bot, url) for url in urls)
    report["sitemap"] = {"xml": "valid", "exactCanonicalUrls": 15, "lastmod": "omitted"}
    report["robots"] = "Existing absence of restrictions preserved; search/training bot policy not changed"
    verification = json.loads((DATA / "site-verification.json").read_text())
    verification_raw = (ROOT / verification["filename"]).read_bytes()
    assert len(verification_raw) == 53 and hashlib.sha256(verification_raw).hexdigest() == verification["sha256"]
    report["googleVerification"] = verification | {"originalBytes": "passed"}
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}/"
    try:
        image_urls = set()
        for record in report["pages"]:
            relative = record["canonical_url"].removeprefix("https://sutra-zen.github.io/")
            with urllib.request.urlopen(base + relative) as response:
                raw = response.read()
                assert response.status == 200
            _, image = inspect_page(raw, record)
            assert raw == (ROOT / record["source_path"]).read_bytes()
            record["localHttp"] = 200
            image_urls.add(image)
        for name in ["sitemap.xml", "robots.txt", verification["filename"]]:
            with urllib.request.urlopen(base + name) as response:
                assert response.status == 200 and response.read() == (ROOT / name).read_bytes()
        for url in sorted(image_urls):
            name = url.removeprefix("https://sutra-zen.github.io/")
            with urllib.request.urlopen(base + name) as response:
                assert response.status == 200 and response.read() == (ROOT / name).read_bytes()
            with Image.open(ROOT / name) as image:
                image.verify()
        report["sharingImages"] = {"uniqueFiles": len(image_urls), "localHttpAndImageDecode": "passed; existing files only"}
        if args.browser:
            from playwright.sync_api import sync_playwright
            errors, http_errors, browser_pages = [], [], []
            with sync_playwright() as p:
                browser = p.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
                page = browser.new_page(viewport={"width": 1280, "height": 900})
                page.route("https://www.youtube.com/**", lambda route: route.abort())
                page.route("https://cdn.tailwindcss.com/**", lambda route: route.fulfill(content_type="application/javascript", body=Path("/tmp/tailwind-site.js").read_bytes()))
                page.route("https://unpkg.com/**", lambda route: route.fulfill(content_type="application/javascript", body=Path("/tmp/migration-lucide.min.js").read_bytes()))
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.on("response", lambda response: http_errors.append(response.url) if response.url.startswith(base) and response.status >= 400 else None)
                for row in rows:
                    relative = row["canonical_url"].removeprefix("https://sutra-zen.github.io/")
                    page.goto(base + relative, wait_until="domcontentloaded")
                    assert page.title() == row["seo_title"]
                    assert page.locator('head meta[name="description"]').get_attribute("content") == row["meta_description"]
                    assert page.locator('head link[rel="canonical"]').get_attribute("href") == row["canonical_url"]
                    baseline_h1 = html.fromstring(old(row["source_path"])).xpath("//h1")[0].text_content()
                    assert page.locator("h1").inner_text() == baseline_h1
                    browser_pages.append({"url": relative or "/", "headAndOriginalH1": "passed"})
                browser.close()
            assert not errors and not http_errors, (errors, http_errors)
            report["browser"] = {"pages": browser_pages, "jsErrors": errors, "localHttpErrors": http_errors,
                                 "scope": "head and unchanged H1; no visible content/navigation changed",
                                 "cdn": "existing cached script copies; external CDN/playback not tested",
                                 "physicalSafari": "not tested"}
    finally:
        server.shutdown()
    (OUT / "validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print("PASS: 15 heads + unchanged bodies, 4 guide generators, 15 sitemap URLs, robots, Google original and HTTP" + (" + 15 browser pages" if args.browser else ""))


if __name__ == "__main__":
    main()
