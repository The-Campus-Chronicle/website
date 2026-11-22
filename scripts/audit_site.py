#!/usr/bin/env python3
"""Audit generated HTML assets and (optionally) internal link targets; never probes external hosts."""
import argparse
import collections
import html.parser
import pathlib
import re
import urllib.parse


class Page(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.media = []
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if attr.get("id"):
            self.ids.add(attr["id"])
        if tag == "a" and attr.get("href"):
            self.links.append(attr["href"])
        if tag == "img" and attr.get("src"):
            self.media.append(attr["src"])
        if attr.get("style") and "background-image" in attr["style"]:
            for match in re.finditer(r"""url\(\s*(?:(['"])(.*?)\1|([^)]*))\s*\)""", attr["style"], flags=re.I):
                image = (match[2] or match[3] or "").strip()
                if image:
                    self.media.append(image)


def site_url(root, file):
    return "/" + file.relative_to(root).as_posix().removesuffix("index.html")


def destination(root, path):
    file = root / urllib.parse.unquote(path).lstrip("/")
    for option in (file, file / "index.html", pathlib.Path(f"{file}.html")):
        if option.is_file() and option.resolve().is_relative_to(root):
            return option
    return None


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("site", type=pathlib.Path)
    cli.add_argument("--host", default="ucvts-campus-chronicle.com")
    cli.add_argument("--links", action="store_true")
    cli.add_argument("--require-images", action="store_true", help="Fail if a local image target is missing")
    args = cli.parse_args()
    root = args.site.resolve()
    pages = {}
    for file in sorted(root.rglob("*.html")):
        item = Page()
        item.feed(file.read_text(encoding="utf-8", errors="replace"))
        pages[file] = item

    counts = collections.Counter()
    assets, remote = set(), set()
    missing_images = collections.defaultdict(set)
    missing_links = collections.defaultdict(set)
    for file, page in pages.items():
        origin = f"https://{args.host}{site_url(root, file)}"
        for kind, items in (("image", page.media), ("link", page.links if args.links else [])):
            for raw in items:
                try:
                    url = urllib.parse.urlsplit(urllib.parse.urljoin(origin, raw))
                except ValueError:
                    continue
                if url.scheme not in {"http", "https"}:
                    continue
                if url.hostname != args.host:
                    if kind == "image":
                        remote.add(url.geturl())
                    continue
                result = destination(root, url.path)
                if kind == "image":
                    counts["local image references"] += 1
                    assets.add(url.path)
                    if result is None:
                        missing_images[url.path].add(site_url(root, file))
                elif result is None or (url.fragment and result in pages and urllib.parse.unquote(url.fragment) not in pages[result].ids):
                    target = url.path + (f"#{url.fragment}" if url.fragment else "")
                    missing_links[target].add(site_url(root, file))

    print(f"{len(pages)} HTML pages, {counts['local image references']} local image references, "
          f"{len(assets)} unique local image URLs, {len(remote)} unique external image URLs")
    for title, entries in (("Missing local image targets", missing_images), ("Missing internal link/anchor targets", missing_links)):
        if title.startswith("Missing internal") and not args.links:
            continue
        print(f"{title}: {len(entries)} across {len(set().union(*entries.values())) if entries else 0} pages")
        for target, sources in sorted(entries.items()):
            print(f"  {target} ({len(sources)} pages; e.g. {min(sources)})")
    for url in sorted(remote):
        print(f"External image: {url}")
    if args.require_images and missing_images:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
