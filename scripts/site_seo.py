"""Shared head-only metadata for the 2026-11-21-r2 handoff.

Do not parse/serialize the document body: existing inline readers, artwork and
scripture must remain byte-for-byte intact. Guide generators call this last.
"""
import json
import re
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "docs/seo"
ORIGIN = "https://sutra-zen.github.io/"
HEAD = re.compile(r"(<head\b[^>]*>)(.*?)(</head\s*>)", re.I | re.S)
TITLE = re.compile(r"<title\b[^>]*>.*?</title\s*>", re.I | re.S)
META = re.compile(r"<meta\b[^>]*>", re.I)
LINK = re.compile(r"<link\b[^>]*>", re.I)
SCRIPT = re.compile(r"<script\b[^>]*>.*?</script\s*>", re.I | re.S)


class _Attributes(HTMLParser):
    def handle_starttag(self, tag, attrs):
        self.attrs = dict(attrs)


def attributes(tag):
    parser = _Attributes()
    parser.feed(tag)
    return parser.attrs


def pages():
    data = json.loads((DATA / "seo_pages.json").read_text())
    assert data["handoff_revision"] == "2026-11-21-r2"
    rows = data["pages"]
    assert len(rows) == 15 and {r["order"] for r in rows} == set(range(15))
    assert len({r["source_path"] for r in rows}) == 15
    assert len({r["canonical_url"] for r in rows}) == 15
    for row in rows:
        path = Path(row["source_path"])
        assert not path.is_absolute() and ".." not in path.parts
        assert path.name == "index.html" and "book" not in path.parts
        assert row["canonical_url"] == urljoin(ORIGIN, str(path.parent) + "/")
        assert row["seo_title"].strip() and row["meta_description"].strip()
    return rows


def _upsert(head, pattern, predicate, replacement):
    """Replace the first matching tag and remove only additional duplicates."""
    found = False

    def update(match):
        nonlocal found
        if not predicate(match[0]):
            return match[0]
        if found:
            return ""
        found = True
        return replacement

    head = pattern.sub(update, head)
    return head if found else head + "\n" + replacement


def apply_page_seo(document, source_path):
    row = next(r for r in pages() if r["source_path"] == source_path)
    match = HEAD.search(document)
    assert match, f"Missing head: {source_path}"
    head = match[2]
    head = _upsert(head, TITLE, lambda tag: True,
                   "<title>" + escape(row["seo_title"]) + "</title>")

    def meta(name, value, attribute="name"):
        nonlocal head
        head = _upsert(
            head, META,
            lambda tag: (attributes(tag).get(attribute) or "").lower() == name,
            f'<meta {attribute}="{name}" content="{escape(value, quote=True)}">',
        )

    meta("description", row["meta_description"])
    head = _upsert(
        head, LINK,
        lambda tag: "canonical" in (attributes(tag).get("rel") or "").lower().split(),
        f'<link rel="canonical" href="{escape(row["canonical_url"], quote=True)}">',
    )
    for name, value in {
        "og:type": "website", "og:site_name": "SutraZen", "og:locale": "zh_TW",
        "og:title": row["seo_title"], "og:description": row["meta_description"],
        "og:url": row["canonical_url"],
    }.items():
        meta(name, value, "property")
    image = json.loads((DATA / "sharing-images.json").read_text())[source_path]
    assert (ROOT / image["path"]).is_file()
    image_url = urljoin(ORIGIN, image["path"])
    meta("og:image", image_url, "property")
    meta("og:image:alt", image["alt"], "property")
    for name, value in {
        "twitter:card": "summary_large_image", "twitter:title": row["seo_title"],
        "twitter:description": row["meta_description"], "twitter:image": image_url,
        "twitter:image:alt": image["alt"],
    }.items():
        meta(name, value)
    website = {"@type": "WebSite", "@id": ORIGIN + "#website", "url": ORIGIN,
               "name": "SutraZen", "inLanguage": "zh-Hant-TW"}
    webpage = {"@type": "WebPage", "@id": row["canonical_url"] + "#webpage",
               "url": row["canonical_url"], "name": row["seo_title"],
               "description": row["meta_description"], "inLanguage": "zh-Hant-TW",
               "isPartOf": {"@id": website["@id"]}}
    graph = {"@context": "https://schema.org", "@graph":
             [website, webpage] if row["order"] == 0 else [webpage]}
    payload = json.dumps(graph, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    head = _upsert(
        head, SCRIPT,
        lambda tag: attributes(tag.split(">", 1)[0] + ">").get("id") == "sutrazen-seo",
        '<script type="application/ld+json" id="sutrazen-seo">' + payload + '</script>',
    )
    # Keep the original whitespace around </head> stable across repeated builds.
    return document[:match.start(2)] + head + document[match.end(2):]


def sitemap():
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", namespace)
    root = ET.Element("{" + namespace + "}urlset")
    for row in pages():
        url = ET.SubElement(root, "{" + namespace + "}url")
        ET.SubElement(url, "{" + namespace + "}loc").text = row["canonical_url"]
    ET.indent(root, space="  ")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"


def robots(current=None):
    """Retain every existing crawler rule; only upsert this site's sitemap line."""
    if current is None:
        current = "User-agent: *\nAllow: /\n"
    lines = [line for line in current.splitlines()
             if not re.match(r"\s*Sitemap\s*:\s*https://sutra-zen\.github\.io/sitemap\.xml\s*$", line, re.I)]
    return "\n".join(lines).rstrip() + "\n\nSitemap: " + ORIGIN + "sitemap.xml\n"
