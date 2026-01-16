#!/usr/bin/env python3
import os
import re
import argparse

# Regex patterns
IMAGE_RE = re.compile(r"^(image:\s+)(/[^\s]+|https?://[^\s]+)$")
MD_IMAGE_RE = re.compile(r"(!\[([^\]]*)\]\(([^)]+)\))")
HTML_DIV_RE = re.compile(r"<div[^>]*>")
HTML_CLOSE_DIV_RE = re.compile(r"</div>")


def convert_md_image_to_html(match):
    """Convert Markdown image to HTML img tag"""
    alt_text = match.group(2)
    src = match.group(3)
    return f'<img src="{src}" alt="{alt_text}">'


def fix_image_paths(file_path, base_url=None, absolute_path_only=False, dry_run=False):
    with open(file_path, "r") as f:
        content = f.read()

    changes = []

    # Fix front matter image URLs
    def fix_front_matter_image(match):
        current_path = match.group(2)
        if current_path.startswith("http"):
            path_part = "/" + "/".join(current_path.split("/")[3:])
        else:
            path_part = current_path

        if absolute_path_only:
            new_url = path_part  # Just use the absolute path
        else:
            new_url = f"{base_url}{path_part}"

        if current_path != new_url:
            changes.append(f"Front matter: {current_path} -> {new_url}")
            return f"{match.group(1)}{new_url}"
        return match.group(0)

    content = IMAGE_RE.sub(fix_front_matter_image, content)

    # Fix Markdown images and convert those inside HTML blocks
    lines = content.split("\n")
    in_html_block = False
    new_lines = []

    for i, line in enumerate(lines):
        # Check if we're entering/exiting HTML blocks
        if HTML_DIV_RE.search(line):
            in_html_block = True
        elif HTML_CLOSE_DIV_RE.search(line):
            in_html_block = False

        # Process Markdown images
        if MD_IMAGE_RE.search(line):

            def process_md_image(match):
                alt_text = match.group(2)
                current_url = match.group(3)

                # Fix URL
                if current_url.startswith("http"):
                    path_part = "/" + "/".join(current_url.split("/")[3:])
                else:
                    path_part = current_url

                if absolute_path_only:
                    new_url = path_part  # Just use the absolute path
                else:
                    new_url = f"{base_url}{path_part}"

                if in_html_block:
                    # Convert to HTML img tag
                    changes.append(f"Line {i+1}: Converted Markdown to HTML img tag")
                    return f'<img src="{new_url}" alt="{alt_text}">'
                else:
                    # Keep as Markdown but fix URL
                    if current_url != new_url:
                        changes.append(f"Line {i+1}: {current_url} -> {new_url}")
                    return f"![{alt_text}]({new_url})"

            new_line = MD_IMAGE_RE.sub(process_md_image, line)
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    content = "\n".join(new_lines)

    if changes:
        if dry_run:
            print(f"\nWould fix image paths in: {file_path}")
            for change in changes:
                print(f"  {change}")
        else:
            with open(file_path, "w") as f:
                f.write(content)
            print(f"Fixed image paths in: {file_path}")
            for change in changes:
                print(f"  {change}")
        return True
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Fix image paths and convert Markdown images in HTML blocks to HTML img tags."
    )
    parser.add_argument(
        "--base-url",
        help="Base URL (e.g., http://localhost:4000 or https://unixwzrd.ai)",
    )
    parser.add_argument(
        "--absolute-path-only",
        action="store_true",
        help="Use absolute paths only (no hostname)",
    )
    parser.add_argument(
        "--target-dir", default="html", help="Directory to scan (default: html)"
    )
    parser.add_argument(
        "--file-filter", help="Only process files containing this string"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview changes without making them"
    )
    args = parser.parse_args()

    if not args.absolute_path_only and not args.base_url:
        parser.error("Either --base-url or --absolute-path-only must be specified")

    processed_files = 0
    changed_files = 0

    for root, dirs, files in os.walk(args.target_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)

                if (
                    args.file_filter
                    and args.file_filter.lower() not in file_path.lower()
                ):
                    continue

                processed_files += 1
                if fix_image_paths(
                    file_path, args.base_url, args.absolute_path_only, args.dry_run
                ):
                    changed_files += 1

    print(
        f"\nSummary: Processed {processed_files} files, {'would change' if args.dry_run else 'changed'} {changed_files} files"
    )


if __name__ == "__main__":
    main()
