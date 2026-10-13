#!/usr/bin/env python3
"""Serve a tiny site on loopback and check its public-side HTTP contracts."""

import argparse
import threading
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class Images(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            source = dict(attrs).get("src")
            if source:
                self.sources.append(source)


def make_handler(scenario):
    class TinySite(BaseHTTPRequestHandler):
        def do_GET(self):
            base = f"http://127.0.0.1:{self.server.server_port}"
            if self.path == "/sitemap.xml":
                body = (
                    '<?xml version="1.0" encoding="UTF-8"?>'
                    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                    f"<url><loc>{base}/</loc></url>"
                    f"<url><loc>{base}/article/</loc></url>"
                    "</urlset>"
                ).encode()
                self.respond(200, body, "application/xml")
            elif self.path == "/":
                self.respond(200, b'<a href="/article/">Article</a>', "text/html")
            elif self.path == "/article/":
                self.respond(
                    200,
                    b'<h1>Article</h1><img src="/assets/diagram.svg" alt="Diagram">'
                    b'<a href="/old-article/">Old address</a>',
                    "text/html",
                )
            elif self.path == "/old-article/":
                self.send_response(302)
                self.send_header(
                    "Location", "/" if scenario == "wrong-redirect" else "/article/"
                )
                self.end_headers()
            elif self.path == "/assets/diagram.svg" and scenario != "missing-image":
                self.respond(
                    200,
                    b'<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"/>',
                    "image/svg+xml",
                )
            else:
                self.respond(404, b"Missing", "text/plain")

        def respond(self, status, body, content_type):
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, _format, *_args):
            pass

    return TinySite


def fetch(url):
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            return response.status, response.url, response.read()
    except urllib.error.HTTPError as error:
        return error.code, error.url, error.read()


def check(base):
    status, _final, sitemap = fetch(base + "/sitemap.xml")
    if status != 200:
        print(f"FAIL sitemap: HTTP {status}")
        return False

    root = ET.fromstring(sitemap)
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    pages = [node.text for node in root.findall(".//sm:loc", namespace)]
    good = True
    images = set()

    for page in pages:
        page_status, _final, body = fetch(page)
        print(f"{'PASS' if page_status == 200 else 'FAIL'} page {urllib.parse.urlparse(page).path}: HTTP {page_status}")
        good &= page_status == 200
        if page_status == 200:
            parser = Images()
            parser.feed(body.decode("utf-8"))
            images.update(urllib.parse.urljoin(page, src) for src in parser.sources)

    for image in sorted(images):
        image_status, _final, _body = fetch(image)
        print(f"{'PASS' if image_status == 200 else 'FAIL'} image {urllib.parse.urlparse(image).path}: HTTP {image_status}")
        good &= image_status == 200

    old_status, destination, _body = fetch(base + "/old-article/")
    final_path = urllib.parse.urlparse(destination).path
    correct_destination = old_status == 200 and final_path == "/article/"
    print(
        f"{'PASS' if correct_destination else 'FAIL'} old URL: "
        f"HTTP {old_status}, final path {final_path!r}, expected '/article/'"
    )
    good &= correct_destination
    return good


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scenario",
        choices=("healthy", "missing-image", "wrong-redirect"),
        default="healthy",
    )
    scenario = parser.parse_args().scenario
    server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(scenario))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        print(f"Scenario: {scenario}")
        return 0 if check(f"http://127.0.0.1:{server.server_port}") else 1
    finally:
        server.shutdown()
        thread.join()
        server.server_close()


if __name__ == "__main__":
    raise SystemExit(main())
