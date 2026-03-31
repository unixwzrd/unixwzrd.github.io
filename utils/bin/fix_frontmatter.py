#!/usr/bin/env python3

import os
import re
from pathlib import Path


def extract_first_paragraph(content):
    """Extract the first paragraph of content after front matter."""
    # Remove front matter first
    content_without_fm = re.sub(r"^---.*?---\n", "", content, flags=re.DOTALL)

    # Find first non-empty paragraph
    paragraphs = content_without_fm.split("\n\n")
    for para in paragraphs:
        clean_para = para.strip()
        if (
            clean_para
            and not clean_para.startswith("#")
            and "<!--more-->" not in clean_para
        ):
            # Remove any markdown links
            clean_para = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", clean_para)
            return clean_para
    return ""


def fix_frontmatter(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract front matter
    fm_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not fm_match:
        return False

    front_matter = fm_match.group(1)

    # Parse the front matter
    fm_lines = []
    excerpt_found = False
    image_found = False

    for line in front_matter.split("\n"):
        if line.startswith("excerpt:"):
            # Skip this line - we'll add a proper excerpt later
            excerpt_found = True
            continue
        elif line.startswith("image:"):
            if not image_found:  # Only keep the first image line
                # Clean up the image path - remove any quotes and fix the path
                image_path = line.split(":", 1)[1].strip().strip('"')
                fm_lines.append(f"image: {image_path}")
                image_found = True
        else:
            fm_lines.append(line)

    # Extract first paragraph for excerpt
    excerpt = extract_first_paragraph(content)
    fm_lines.append(f'excerpt: "{excerpt}"')

    # Add default image if missing
    if not image_found:
        fm_lines.append("image: /assets/images/default-og-image.png")

    # Rebuild front matter
    new_front_matter = "---\n" + "\n".join(fm_lines) + "\n---\n"

    # Get content after front matter, removing any duplicate excerpt/image lines
    content_after_fm = re.sub(
        r"^---\n.*?\n---\n(excerpt:.*?\nimage:.*?\n)?", "", content, flags=re.DOTALL
    )

    # Combine new front matter with content
    new_content = new_front_matter + content_after_fm

    if content != new_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Fixed front matter in {file_path}")
        return True

    return False


def main():
    base_dir = Path(os.getenv("BASEDIR", os.getcwd()))
    posts_dir = base_dir / "html"

    # Find all markdown files
    md_files = list(posts_dir.rglob("*.md"))
    fixed_count = 0

    for file_path in md_files:
        if fix_frontmatter(file_path):
            fixed_count += 1

    print(f"\nFixed {fixed_count} files with duplicate front matter")


if __name__ == "__main__":
    main()
