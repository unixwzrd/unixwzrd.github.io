#!/usr/bin/env python3
"""
Test script for external link checking functionality
"""

import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urlparse


def is_internal_unixwzrd_url(url: str) -> bool:
    """Return True if URL host is unixwzrd.ai or one of its subdomains."""
    try:
        hostname = urlparse(url).hostname
    except ValueError:
        return False

    if not hostname:
        return False

    hostname = hostname.lower()
    return hostname == "unixwzrd.ai" or hostname.endswith(".unixwzrd.ai")


def test_external_link_extraction():
    """Test extracting external links from a page."""
    print("🧪 Testing external link extraction...")

    # Test with a simple page
    test_url = "https://unixwzrd.ai/"

    try:
        response = requests.get(test_url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        external_links = []

        # Find all links
        for link in soup.find_all("a", href=True):
            href = link["href"]

            # Skip internal links, anchors, javascript, mailto, etc.
            if (
                href.startswith("#")
                or href.startswith("javascript:")
                or href.startswith("mailto:")
                or href.startswith("tel:")
                or href.startswith("/")
                or is_internal_unixwzrd_url(href)
                or not href.startswith(("http://", "https://"))
            ):
                continue

            external_links.append(href)

        # Also check for external links in content
        content = response.text
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, content)

        for url in urls:
            if not is_internal_unixwzrd_url(url):
                external_links.append(url)

        external_links = list(set(external_links))  # Remove duplicates

        print(f"✅ Found {len(external_links)} external links:")
        for link in external_links[:5]:  # Show first 5
            print(f"   - {link}")
        if len(external_links) > 5:
            print(f"   ... and {len(external_links) - 5} more")

        return external_links

    except Exception as e:
        print(f"❌ Error extracting links: {e}")
        return []


def test_external_link_checking():
    """Test checking external links."""
    print("\n🧪 Testing external link checking...")

    # Test with some known good and bad links
    test_links = [
        "https://www.google.com",
        "https://httpbin.org/status/404",
        "https://httpbin.org/status/500",
        "https://httpbin.org/delay/2",  # Slow link
        "https://nonexistent-domain-12345.com",  # Bad link
    ]

    for link in test_links:
        try:
            start_time = time.time()
            response = requests.head(link, timeout=10, allow_redirects=True)
            response_time = time.time() - start_time

            if response.status_code < 400:
                status = "working"
                if response_time > 5.0:
                    status = "slow"
                print(f"✅ {link}: {status} ({response_time:.2f}s)")
            else:
                print(f"❌ {link}: broken ({response.status_code})")

        except requests.exceptions.Timeout:
            print(f"❌ {link}: timeout")
        except requests.exceptions.ConnectionError:
            print(f"❌ {link}: connection error")
        except Exception as e:
            print(f"❌ {link}: error - {e}")


if __name__ == "__main__":
    print("🔗 External Link Testing")
    print("=" * 40)

    # Test link extraction
    links = test_external_link_extraction()

    # Test link checking
    test_external_link_checking()

    print("\n✅ External link testing completed!")

