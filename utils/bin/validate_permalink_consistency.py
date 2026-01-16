#!/usr/bin/env python3
"""
Validate permalink consistency in Jekyll site.

This script checks that permalinks are consistent with file paths and reports
any inconsistencies without making changes. This helps identify case sensitivity
issues that could cause problems on case-sensitive servers.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class PermalinkValidator:
    def __init__(self, site_root: str = "html"):
        self.site_root = Path(site_root)
        self.issues: List[Dict] = []

    def extract_permalink_from_frontmatter(self, content: str) -> str:
        """Extract permalink from frontmatter."""
        permalink_match = re.search(r"permalink:\s*([^\s\n]+)", content)
        if permalink_match:
            return permalink_match.group(1).strip()
        return None

    def extract_title_from_frontmatter(self, content: str) -> str:
        """Extract title from frontmatter."""
        title_match = re.search(r'title:\s*["\']([^"\']+)["\']', content)
        if title_match:
            return title_match.group(1).strip()
        return None

    def validate_permalinks(self) -> List[Dict]:
        """Validate permalink consistency across all markdown files."""
        print("Validating permalink consistency...")

        for file_path in self.site_root.rglob("*.md"):
            if file_path.is_file():
                content = file_path.read_text(encoding="utf-8")
                permalink = self.extract_permalink_from_frontmatter(content)
                title = self.extract_title_from_frontmatter(content)

                if permalink:
                    # Check for potential issues
                    issue = self.analyze_permalink(file_path, permalink, title, content)
                    if issue:
                        self.issues.append(issue)

        return self.issues

    def analyze_permalink(
        self, file_path: Path, permalink: str, title: str, content: str
    ) -> Dict:
        """Analyze a permalink for potential issues."""
        issue = {
            "file": str(file_path),
            "permalink": permalink,
            "title": title,
            "problems": [],
        }

        # Check 1: Permalink starts and ends with /
        if not permalink.startswith("/") or not permalink.endswith("/"):
            issue["problems"].append("Permalink should start and end with /")

        # Check 2: Permalink matches file structure expectations
        expected_base = self.get_expected_permalink_base(file_path)
        if expected_base and permalink != expected_base:
            issue["problems"].append(
                f"Permalink '{permalink}' doesn't match expected '{expected_base}'"
            )

        # Check 3: Look for internal links that might be inconsistent
        internal_links = self.find_internal_links(content)
        for link in internal_links:
            if link.startswith("/") and not self.is_valid_internal_link(link):
                issue["problems"].append(f"Internal link '{link}' may not exist")

        return issue if issue["problems"] else None

    def get_expected_permalink_base(self, file_path: Path) -> str:
        """Get the expected permalink base based on file location."""
        relative_path = file_path.relative_to(self.site_root)

        # Handle special cases
        if relative_path.name == "index.md":
            return f"/{relative_path.parent}/"
        elif relative_path.name == "404.md":
            return "/404.html"
        elif relative_path.name in [
            "Policies.md",
            "General_Privacy.md",
            "General_ToS.md",
            "Privacy_LogGPT_for_Safari.md",
        ]:
            # These have specific permalinks that should be preserved
            return None
        elif relative_path.parts[0] == "projects":
            # Project files should have /projects/ProjectName/ permalinks
            stem = relative_path.stem
            return f"/projects/{stem}/"
        else:
            # Regular files
            stem = relative_path.stem
            return f"/{stem}/"

    def find_internal_links(self, content: str) -> List[str]:
        """Find internal links in content."""
        links = []

        # Markdown links
        md_links = re.findall(r"\[([^\]]*)\]\(([^)]+)\)", content)
        for _, url in md_links:
            if url.startswith("/"):
                links.append(url)

        # HTML links
        html_links = re.findall(r'href=["\']([^"\']+)["\']', content)
        for url in html_links:
            if url.startswith("/"):
                links.append(url)

        return links

    def is_valid_internal_link(self, link: str) -> bool:
        """Check if an internal link likely exists."""
        # Remove trailing slash and query parameters
        clean_link = link.rstrip("/").split("?")[0].split("#")[0]

        # Check if it's a known valid path
        valid_paths = [
            "/",
            "/about/",
            "/blog/",
            "/projects/",
            "/contact/",
            "/resources/",
            "/Policies/",
            "/Policies/General_Privacy/",
            "/Policies/General_ToS/",
            "/Policies/Privacy_LogGPT_for_Safari/",
            "/collaborate/",
            "/faq/",
            "/archive/",
            "/404.html",
            # Project paths
            "/projects/LogGPT/",
            "/projects/Case-Analytics/",
            "/projects/UnicodeFix/",
            "/projects/text-generation-webui-macos/",
            "/projects/oobabooga-macOS/",
            "/projects/TorchDevice/",
            "/projects/venvutil/",
        ]

        return clean_link in valid_paths

    def run(self) -> None:
        """Run the validation process."""
        print("Starting permalink consistency validation...")

        issues = self.validate_permalinks()

        if issues:
            print(f"\nFound {len(issues)} files with permalink issues:")
            for issue in issues:
                print(f"\n📄 {issue['file']}")
                print(f"   Permalink: {issue['permalink']}")
                if issue["title"]:
                    print(f"   Title: {issue['title']}")
                print("   Problems:")
                for problem in issue["problems"]:
                    print(f"     ❌ {problem}")
        else:
            print("✅ No permalink consistency issues found!")

        return issues


def main():
    validator = PermalinkValidator()
    issues = validator.run()

    if issues:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
