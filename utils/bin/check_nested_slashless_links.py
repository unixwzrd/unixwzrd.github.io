#!/usr/bin/env python3
"""
Fail when built HTML contains internal page links that omit the trailing slash.

Static hosting can be inconsistent about resolving directory permalinks without the
trailing slash. We enforce slash-terminated internal page links so the generated site
matches the canonical permalink form.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


LINK_RE = re.compile(r"""(?:href|src)=["']([^"'#]+(?:#[^"']*)?)["']""", re.IGNORECASE)


def is_risky_path(raw: str) -> bool:
    if not raw.startswith("/"):
        return False
    if raw.startswith("//"):
        return False
    if raw.startswith("/assets/"):
        return False
    if raw in {"/", "/feed.xml", "/sitemap.xml", "/robots.txt", "/redirects.json"}:
        return False

    path = raw.split("#", 1)[0].split("?", 1)[0]
    if not path or path == "/" or path.endswith("/"):
        return False

    leaf = path.rsplit("/", 1)[-1]
    if "." in leaf:
        return False

    return True


def main() -> int:
    site_dir = Path("_site")
    if not site_dir.exists():
        print("❌ _site directory does not exist.", file=sys.stderr)
        return 1

    failures: list[tuple[str, str]] = []
    for html_file in site_dir.rglob("*.html"):
        try:
            content = html_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = html_file.read_text(encoding="utf-8", errors="ignore")

        for match in LINK_RE.finditer(content):
            target = match.group(1)
            if is_risky_path(target):
                failures.append((str(html_file), target))

    if failures:
        print("❌ Found internal page links without trailing slashes:")
        for file_path, target in failures:
            print(f"   - {file_path}: {target}")
        return 1

    print("✅ No internal page links without trailing slashes found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
