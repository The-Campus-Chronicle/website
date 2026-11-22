#!/usr/bin/env python3
"""Smoke-check the public search and article metadata produced by Jekyll."""
import argparse
import json
import pathlib
import re
import urllib.parse
import xml.etree.ElementTree as ET
from audit_site import destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", type=pathlib.Path)
    parser.add_argument("--origin", default="https://ucvts-campus-chronicle.com")
    args = parser.parse_args()
    root = args.site.resolve()
    stories = json.loads((root / "search-index.json").read_text(encoding="utf-8"))
    assert stories and len({story["url"] for story in stories}) == len(stories)
    for story in stories:
        uri = urllib.parse.urlsplit(story["url"])
        assert not uri.netloc and uri.path.startswith("/")
        page = destination(root, uri.path)
        assert page, story["url"]
        source = page.read_text(encoding="utf-8")
        assert source.count("<title>") == 1, story["url"]
        states = re.findall(r'<script type="application/ld\+json">\s*(.*?)</script>', source, flags=re.S)
        schema, = map(json.loads, states)
        assert schema["@type"] == "NewsArticle", story["url"]
        assert schema["headline"] == story["title"], story["url"]
        # Jekyll may encode Unicode in absolute_url while the search index retains it.
        assert urllib.parse.unquote(schema["mainEntityOfPage"]) == args.origin + urllib.parse.unquote(uri.path), story["url"]
        for author in schema.get("author", []):
            if "url" in author:
                link = urllib.parse.urlsplit(author["url"])
                assert destination(root, link.path), author["url"]

    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap = ET.parse(root / "sitemap.xml")
    urls = [node.text for node in sitemap.findall(".//s:loc", ns)]
    assert urls and all(url.startswith(args.origin + "/") for url in urls)
    assert all(not url.endswith(("/404.html", "/search.html", "/search-index.json")) for url in urls)
    for name in ("404.html", "search.html"):
        assert 'content="noindex, follow"' in (root / name).read_text(encoding="utf-8")
    assert f"Sitemap: {args.origin}/sitemap.xml" in (root / "robots.txt").read_text(encoding="utf-8")
    assert not re.search(r'\bhttp://ucvts-campus-chronicle\.com/', (root / "feed.xml").read_text(encoding="utf-8"))
    print(f"Verified {len(stories)} indexed article routes and metadata; {len(urls)} HTTPS sitemap URLs.")


if __name__ == "__main__":
    main()
