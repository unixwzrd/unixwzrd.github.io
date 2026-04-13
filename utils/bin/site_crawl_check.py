#!/usr/bin/env python
"""
Remote/local site crawl checker.

Checks the site as served over HTTP:
- loads sitemap.xml
- verifies each sitemap page returns 200
- verifies same-site links return non-404 responses
- verifies same-site images return non-404 responses

This is intentionally separate from the heavier reliability monitor:
- no source-derived unpublished pages
- no external-link noise
- no email/monitoring state
"""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from collections import deque
from dataclasses import dataclass
from typing import Iterable
from urllib.parse import urljoin, urlparse, urldefrag

import requests
from bs4 import BeautifulSoup

TIMEOUT = 10
USER_AGENT = "unixwzrd-site-crawl-check/1.0 (+https://unixwzrd.ai)"
SITEMAP_PATH = "/sitemap.xml"


@dataclass(frozen=True)
class Failure:
    kind: str
    source: str
    target: str
    status: str


def normalize_base_url(base_url: str) -> str:
    return base_url.rstrip("/")


def is_same_host(url: str, host: str) -> bool:
    parsed = urlparse(url)
    return parsed.netloc == host


def is_http_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https")


def canonicalize_url(url: str) -> str:
    clean, _fragment = urldefrag(url)
    return clean


def should_check_asset(url: str, host: str) -> bool:
    parsed = urlparse(url)
    return is_http_url(url) and parsed.netloc == host


def fetch(session: requests.Session, url: str) -> requests.Response:
    return session.get(url, timeout=TIMEOUT, allow_redirects=True)


def parse_sitemap(session: requests.Session, sitemap_url: str) -> list[str]:
    response = fetch(session, sitemap_url)
    response.raise_for_status()
    root = ET.fromstring(response.text)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [loc.text.strip() for loc in root.findall(".//sm:loc", ns) if loc.text]
    return urls


def extract_same_site_links(
    page_url: str, html: str, host: str
) -> tuple[set[str], set[str]]:
    soup = BeautifulSoup(html, "html.parser")
    links: set[str] = set()
    images: set[str] = set()

    for tag in soup.find_all("a", href=True):
        href = tag.get("href", "").strip()
        if not href or href.startswith("#"):
            continue
        absolute = canonicalize_url(urljoin(page_url, href))
        if should_check_asset(absolute, host):
            links.add(absolute)

    for tag in soup.find_all("img", src=True):
        src = tag.get("src", "").strip()
        if not src:
            continue
        absolute = canonicalize_url(urljoin(page_url, src))
        if should_check_asset(absolute, host):
            images.add(absolute)

    return links, images


def summarize_failures(failures: Iterable[Failure]) -> None:
    for failure in failures:
        print(
            f"❌ {failure.kind}: {failure.target} (from {failure.source}) [{failure.status}]"
        )


def run(base_url: str, verbose: bool = False) -> int:
    base_url = normalize_base_url(base_url)
    host = urlparse(base_url).netloc
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    sitemap_url = base_url + SITEMAP_PATH
    print(f"🔎 Crawling site from sitemap: {sitemap_url}")

    try:
        sitemap_pages = parse_sitemap(session, sitemap_url)
    except Exception as exc:
        print(f"❌ Failed to load sitemap: {exc}")
        return 1

    pages_to_check = [canonicalize_url(url) for url in sitemap_pages if is_same_host(url, host)]
    page_failures: list[Failure] = []
    link_failures: list[Failure] = []
    image_failures: list[Failure] = []

    checked_pages: set[str] = set()
    checked_links: set[str] = set()
    checked_images: set[str] = set()

    queue = deque(pages_to_check)

    while queue:
        page_url = queue.popleft()
        if page_url in checked_pages:
            continue
        checked_pages.add(page_url)

        try:
            response = fetch(session, page_url)
            status = response.status_code
            if status >= 400:
                page_failures.append(Failure("page", "sitemap", page_url, f"HTTP {status}"))
                continue
            if verbose:
                print(f"✅ page: {page_url} [{status}]")
        except Exception as exc:
            page_failures.append(Failure("page", "sitemap", page_url, str(exc)))
            continue

        links, images = extract_same_site_links(page_url, response.text, host)

        for link_url in sorted(links):
            if link_url in checked_links:
                continue
            checked_links.add(link_url)
            try:
                link_response = fetch(session, link_url)
                if link_response.status_code >= 400:
                    link_failures.append(
                        Failure("link", page_url, link_url, f"HTTP {link_response.status_code}")
                    )
                elif verbose:
                    print(f"✅ link: {link_url} [{link_response.status_code}]")
            except Exception as exc:
                link_failures.append(Failure("link", page_url, link_url, str(exc)))

        for image_url in sorted(images):
            if image_url in checked_images:
                continue
            checked_images.add(image_url)
            try:
                image_response = fetch(session, image_url)
                if image_response.status_code >= 400:
                    image_failures.append(
                        Failure("image", page_url, image_url, f"HTTP {image_response.status_code}")
                    )
                elif verbose:
                    print(f"✅ image: {image_url} [{image_response.status_code}]")
            except Exception as exc:
                image_failures.append(Failure("image", page_url, image_url, str(exc)))

    print(
        f"📋 Checked {len(checked_pages)} pages, {len(checked_links)} internal links, "
        f"and {len(checked_images)} images"
    )

    failures = page_failures + link_failures + image_failures
    if failures:
        summarize_failures(failures)
        print(
            f"❌ Crawl failed: {len(page_failures)} page errors, "
            f"{len(link_failures)} link errors, {len(image_failures)} image errors"
        )
        return 1

    print("✅ Crawl passed with no internal page, link, or image failures.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Crawl a local or remote site from sitemap.xml")
    parser.add_argument("--base-url", required=True, help="Base site URL, e.g. https://unixwzrd.ai")
    parser.add_argument("--verbose", action="store_true", help="Print every successful page/link/image check")
    args = parser.parse_args()
    return run(args.base_url, verbose=args.verbose)


if __name__ == "__main__":
    sys.exit(main())
