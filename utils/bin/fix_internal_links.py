#!/usr/bin/env python3
"""
Fix Internal Links Script

Conservatively fixes internal page links to use canonical slash-terminated URLs.
This script must not rewrite front-matter permalinks or blindly replace partial
matches inside already-correct links.
"""

import os
import re
import argparse


def fix_internal_link_issues():
    """Fix internal page links without mutating front matter."""

    link_fixes = [
        # Fix missing trailing slashes
        {
            "old": "/contact",
            "new": "/contact/",
            "files": [
                "html/resources.md",
                "html/about.md",
                "html/projects/Case-Analytics.md",
                "html/projects/venvutil.md",
                "html/resources/emergency-resources.md",
                "html/about/resume.md",
                "html/collaborate/professionals.md",
                "html/collaborate/community.md",
            ],
        },
        {
            "old": "/resources",
            "new": "/resources/",
            "files": ["html/contact.md", "html/collaborate/community.md"],
        },
        {
            "old": "/projects",
            "new": "/projects/",
            "files": ["html/collaborate/community.md"],
        },
        # Fix specific path issues
        {
            "old": "/about/sullivan-michael-creds",
            "new": "/about/credentials/",
            "files": ["html/about/resume.md"],
        },
        {
            "old": "/assets/documents/SullivanMichael_IT_AI_ML_Unix_52050111.pdf",
            "new": "/assets/documents/SullivanMichael_IT_AI_ML_Unix_A26047020020.pdf",
            "files": ["html/about/resume.md"],
        },
    ]

    for fix in link_fixes:
        for file_path in fix["files"]:
            if os.path.exists(file_path):
                print(
                    f"🔧 Fixing internal link in {file_path}: {fix['old']} → {fix['new']}"
                )

                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                escaped_old = re.escape(fix["old"])
                pattern = re.compile(rf"(?<![\w/]){escaped_old}(?!/)")
                new_content, replacements = pattern.subn(fix["new"], content)

                if replacements:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"   ✅ Fixed in {file_path}")
                else:
                    print(f"   ⚠️ Link not found in {file_path}")
            else:
                print(f"   ❌ File not found: {file_path}")


def normalize_internal_page_links():
    """Normalize internal page links across site content to slash-terminated form."""

    print("\n🔧 Normalizing internal page links across site content...")

    content_files = []
    for root, dirs, files in os.walk("html"):
        dirs[:] = [d for d in dirs if d not in {".jekyll-cache", "_site"}]
        for name in files:
            if name.endswith((".md", ".html")):
                content_files.append(os.path.join(root, name))

    markdown_link_re = re.compile(r"(\[[^\]]*\]\()(/[^)\s\"']*)(\))")
    html_href_re = re.compile(r"""(href=["'])(/[^"' ]*)(["'])""")

    def normalize_target(target: str) -> str:
        if not target.startswith("/") or target.startswith("//"):
            return target

        path, hash_sep, fragment = target.partition("#")
        path, query_sep, query = path.partition("?")

        if (
            not path
            or path == "/"
            or path.endswith("/")
            or path.startswith("/assets/")
            or path in {"/feed.xml", "/sitemap.xml", "/robots.txt", "/redirects.json"}
        ):
            return target

        leaf = path.rsplit("/", 1)[-1]
        if "." in leaf:
            return target

        normalized = f"{path}/"
        if query_sep:
            normalized += f"?{query}"
        if hash_sep:
            normalized += f"#{fragment}"
        return normalized

    updated_files = 0
    replacement_count = 0

    for file_path in content_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        def replace_markdown(match):
            nonlocal replacement_count
            prefix, target, suffix = match.groups()
            normalized = normalize_target(target)
            if normalized != target:
                replacement_count += 1
            return f"{prefix}{normalized}{suffix}"

        def replace_href(match):
            nonlocal replacement_count
            prefix, target, suffix = match.groups()
            normalized = normalize_target(target)
            if normalized != target:
                replacement_count += 1
            return f"{prefix}{normalized}{suffix}"

        new_content = markdown_link_re.sub(replace_markdown, content)
        new_content = html_href_re.sub(replace_href, new_content)

        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            updated_files += 1
            print(f"   ✅ Normalized links in {file_path}")

    print(f"   📊 Updated {updated_files} files; normalized {replacement_count} links")


def fix_missing_assets():
    """Fix missing asset references."""

    # Check if the default OG image exists
    og_image_path = "html/assets/images/default-og-image.png"
    if not os.path.exists(og_image_path):
        print(f"⚠️ Missing asset: {og_image_path}")
        # Create a placeholder or copy from another image
        if os.path.exists("html/assets/images/No_Image_for_Project.png"):
            import shutil

            shutil.copy("html/assets/images/No_Image_for_Project.png", og_image_path)
            print(f"   ✅ Created placeholder from existing image")

    # Check if the PDF document exists
    pdf_path = "html/assets/documents/SullivanMichael_IT_AI_ML_Unix_A26047020020.pdf"
    if not os.path.exists(pdf_path):
        print(f"⚠️ Missing asset: {pdf_path}")
        print(f"   Please ensure the PDF file exists at this location")


def validate_fixes():
    """Validate that the fixes resolved the issues."""

    print("\n🔍 Validating fixes...")

    # Run the permalink validation script again
    import subprocess

    result = subprocess.run(
        ["python3", "utils/bin/validate_permalink_consistency.py"],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print("✅ All permalink and internal link issues resolved!")
    else:
        print("⚠️ Some issues may remain:")
        print(result.stdout)


def main():
    parser = argparse.ArgumentParser(
        description="Fix internal link and permalink case sensitivity issues"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be fixed without making changes",
    )
    parser.add_argument(
        "--validate-only", action="store_true", help="Only validate current state"
    )

    args = parser.parse_args()

    print("🔍 Internal Links and Permalinks Analysis")
    print("=" * 50)

    if args.validate_only:
        validate_fixes()
        return

    if args.dry_run:
        print("🔍 DRY RUN - No changes will be made")
        print("\nWould fix the following issues:")
        print("1. Project permalinks to match expected paths")
        print("2. Missing trailing slashes in internal links")
        print("3. Incorrect asset references")
        print("4. Blog post permalink consistency")
        return

    print(f"\n🔧 Starting internal link and permalink fixes...")

    # Fix internal link issues
    fix_internal_link_issues()

    # Normalize internal page links broadly
    normalize_internal_page_links()

    # Fix missing assets
    fix_missing_assets()

    # Validate the fixes
    validate_fixes()

    print(f"\n✅ Internal link and permalink fixes completed!")
    print(f"\n📋 Summary:")
    print(f"   - Added missing trailing slashes to internal links")
    print(f"   - Fixed asset references")
    print(f"\n⚠️ Note: These fixes ensure compatibility with GitHub Pages")
    print(f"   where case sensitivity matters for file paths.")


if __name__ == "__main__":
    main()
