#!/usr/bin/env python3
"""Check static site references; optionally compare reachable files to deployment."""
import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urlencode, urljoin, urlsplit
from urllib.request import urlopen


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = set()
        self.refs = []
        self.errors = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            identifier = values["id"]
            if identifier in self.ids:
                self.errors.append(f"duplicate id: {identifier}")
            self.ids.add(identifier)
        for key in ("src", "href", "poster"):
            if values.get(key):
                self.refs.append(values[key])


def check(root, base_url=None, cache_tag="verify"):
    root = Path(root).resolve()
    errors = []
    queue = [root / "index.html"]
    visited = set()
    pages = {}
    anchors = []

    def add_ref(parent, reference):
        parts = urlsplit(reference)
        if parts.scheme or parts.netloc:
            return
        if not parts.path:
            target = parent
        elif parts.path.startswith("/"):
            target = root / unquote(parts.path).lstrip("/")
        else:
            target = parent.parent / unquote(parts.path)
        target = target.resolve()
        if not target.is_relative_to(root):
            errors.append(f"reference leaves site root: {parent.relative_to(root)} -> {reference}")
            return
        if target.is_dir():
            target /= "index.html"
        if not target.is_file():
            errors.append(f"missing resource: {parent.relative_to(root)} -> {reference}")
            return
        if parts.fragment and target.suffix.lower() == ".html":
            anchors.append((parent, target, unquote(parts.fragment)))
        queue.append(target)

    while queue:
        path = queue.pop()
        if path in visited:
            continue
        if not path.is_file():
            errors.append(f"missing required file: {path.name}")
            continue
        visited.add(path)
        suffix = path.suffix.lower()
        if suffix not in {".html", ".css", ".js"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError) as error:
            errors.append(f"cannot read {path.relative_to(root)}: {error}")
            continue
        if suffix == ".html":
            page = Page(text)
            pages[path] = page
            errors.extend(f"{path.relative_to(root)}: {message}" for message in page.errors)
            for reference in page.refs:
                add_ref(path, reference)
        elif suffix == ".css":
            for reference in re.findall(r"url\(\s*['\"]?([^'\")\s]+)", text):
                add_ref(path, reference)
        else:
            # Best effort only: dynamic expressions and JS execution need a browser.
            for reference in re.findall(r"['\"](assets/[^'\"\s]+)['\"]", text):
                add_ref(root / "index.html", reference)
    for parent, target, anchor in anchors:
        if target in pages and anchor not in pages[target].ids:
            errors.append(f"missing HTML anchor: {parent.relative_to(root)} -> {target.relative_to(root)}#{anchor}")

    # Catalogs are provenance, not necessarily referenced or published by HTML.
    for path in sorted(root.rglob("*.json")):
        if any(part.startswith(".") or part in {"node_modules", "vendor"} for part in path.relative_to(root).parts):
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, OSError) as error:
            errors.append(f"invalid JSON {path.relative_to(root)}: {error}")
            continue
        entries = data if isinstance(data, list) else []
        for entry in entries:
            if isinstance(entry, dict) and isinstance(entry.get("cover"), str):
                reference = entry["cover"]
                if not urlsplit(reference).scheme and not urlsplit(reference).netloc:
                    parent = root / "index.html" if reference.startswith("assets/") else path
                    add_ref(parent, reference)
    # Catalog references are checked locally but are not automatically remote targets.
    if base_url:
        parsed = urlsplit(base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.query or parsed.fragment:
            errors.append("base-url must be an http(s) site root with no query/fragment")
        else:
            for path in sorted(visited):
                relative = path.relative_to(root).as_posix()
                url = urljoin(base_url.rstrip("/") + "/", quote(relative))
                url += "?" + urlencode({"verify": cache_tag})
                try:
                    with urlopen(url, timeout=20) as response:
                        actual = response.read()
                    if actual != path.read_bytes():
                        errors.append(f"deployment differs: {relative}")
                except OSError as error:
                    errors.append(f"cannot fetch {relative}: {error}")
    return visited, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", type=Path)
    parser.add_argument("--base-url")
    parser.add_argument("--cache-tag", default="verify")
    args = parser.parse_args()
    root = args.site.resolve()
    if not root.is_dir():
        parser.error("site must be a directory")
    files, errors = check(root, args.base_url, args.cache_tag)
    for error in errors:
        print("ERROR: " + error, file=sys.stderr)
    print(f"Checked {len(files)} reachable files; {len(errors)} issue(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
