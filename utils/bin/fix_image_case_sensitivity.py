#!/usr/bin/env python3
"""
Fix case sensitivity issues with image references in Jekyll site.

This script scans all markdown and HTML files for image references and
corrects case mismatches between the reference and the actual file name.
This is particularly important when developing on macOS (case-insensitive)
and deploying to Linux servers (case-sensitive).
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple


class ImageCaseFixer:
    def __init__(self, site_root: str = "html"):
        self.site_root = Path(site_root)
        self.actual_files: Dict[str, str] = {}  # normalized path -> actual filename
        self.fixes_made: List[Tuple[str, str, str]] = []  # file, old_ref, new_ref

    def scan_actual_files(self) -> None:
        """Scan all image files and build a mapping of normalized paths to actual filenames."""
        print("Scanning actual image files...")

        # Scan assets/images
        assets_path = self.site_root / "assets" / "images"
        if assets_path.exists():
            self._scan_directory(assets_path, "/assets/images/")

        # Scan project-specific images
        projects_path = self.site_root / "projects"
        if projects_path.exists():
            for project_dir in projects_path.iterdir():
                if project_dir.is_dir():
                    project_images = project_dir / "images"
                    if project_images.exists():
                        project_path = f"/projects/{project_dir.name}/images/"
                        self._scan_directory(project_images, project_path)

        print(f"Found {len(self.actual_files)} image files")

    def _scan_directory(self, directory: Path, base_path: str) -> None:
        """Scan a directory for image files and add to mapping."""
        for file_path in directory.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in [
                ".png",
                ".jpg",
                ".jpeg",
                ".gif",
                ".webp",
                ".svg",
            ]:
                # Create normalized path (lowercase) for lookup
                relative_path = file_path.relative_to(directory)
                normalized_path = base_path + str(relative_path).lower()
                actual_path = base_path + str(relative_path)

                self.actual_files[normalized_path] = actual_path

    def find_image_references(self) -> Dict[str, List[Tuple[int, str, str]]]:
        """Find all image references in markdown and HTML files."""
        print("Scanning for image references...")

        references: Dict[str, List[Tuple[int, str, str]]] = {}

        # Patterns to match image references
        patterns = [
            r"!\[([^\]]*)\]\(([^)]+)\)",  # Markdown images
            r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>',  # HTML img tags
            r"image:\s*([^\s\n]+)",  # Front matter image fields
        ]

        # Find all markdown and HTML files
        for ext in ["*.md", "*.html"]:
            for file_path in self.site_root.rglob(ext):
                if file_path.is_file():
                    content = file_path.read_text(encoding="utf-8")
                    file_refs = []

                    for pattern in patterns:
                        for match in re.finditer(pattern, content, re.IGNORECASE):
                            if match.group(1) and match.group(1).startswith("/"):
                                # This is a local image reference
                                normalized_ref = match.group(1).lower()
                                if normalized_ref in self.actual_files:
                                    actual_ref = self.actual_files[normalized_ref]
                                    if normalized_ref != actual_ref:
                                        file_refs.append(
                                            (match.start(), match.group(1), actual_ref)
                                        )

                    if file_refs:
                        references[str(file_path)] = file_refs

        return references

    def fix_references(self, references: Dict[str, List[Tuple[int, str, str]]]) -> None:
        """Fix case sensitivity issues in image references."""
        print("Fixing case sensitivity issues...")

        for file_path, refs in references.items():
            print(f"Processing {file_path}...")

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Sort references by position (reverse order to avoid offset issues)
            refs.sort(key=lambda x: x[0], reverse=True)

            modified = False
            for start_pos, old_ref, new_ref in refs:
                if old_ref != new_ref:
                    # Find the exact match in the content
                    content_before = content[:start_pos]
                    content_after = content[start_pos:]

                    # Replace the first occurrence after the start position
                    if old_ref in content_after:
                        content_after = content_after.replace(old_ref, new_ref, 1)
                        content = content_before + content_after
                        modified = True
                        self.fixes_made.append((file_path, old_ref, new_ref))
                        print(f"  Fixed: {old_ref} -> {new_ref}")

            if modified:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)

    def verify_references(
        self, references: Dict[str, List[Tuple[int, str, str]]]
    ) -> None:
        """Verify that each referenced image file exists at the exact path and case."""
        print("\nVerifying image references...")
        for file_path, refs in references.items():
            for _, ref, _ in refs:
                # Remove query strings/fragments if present
                ref_clean = ref.split("?")[0].split("#")[0]
                # Remove leading slash for Path
                rel_path = ref_clean.lstrip("/")
                abs_path = (self.site_root / rel_path).resolve()
                if not abs_path.exists():
                    # Try case-insensitive match in the same directory
                    parent = abs_path.parent
                    suggestion = None
                    if parent.exists():
                        for f in parent.iterdir():
                            if f.name.lower() == abs_path.name.lower():
                                suggestion = f.name
                                break
                    if suggestion:
                        print(
                            f"[CASE MISMATCH] {file_path}: '{ref}' → Did you mean: '{parent}/{suggestion}'?"
                        )
                    else:
                        print(f"[MISSING] {file_path}: '{ref}' not found.")
                else:
                    print(f"[OK] {file_path}: '{ref}' exists.")

    def run(self) -> None:
        """Run the complete image case sensitivity fix process."""
        print("Starting image case sensitivity fix...")

        self.scan_actual_files()
        references = self.find_image_references()

        if references:
            print(
                f"Found {sum(len(refs) for refs in references.values())} potential case sensitivity issues"
            )
            self.fix_references(references)

            print(f"\nFixed {len(self.fixes_made)} case sensitivity issues:")
            for file_path, old_ref, new_ref in self.fixes_made:
                print(f"  {file_path}: {old_ref} -> {new_ref}")
            # Verification step
            self.verify_references(references)
        else:
            print("No case sensitivity issues found.")

    def dry_run(self) -> None:
        """Show what would be fixed without making changes."""
        print("DRY RUN - No changes will be made")

        self.scan_actual_files()
        references = self.find_image_references()

        if references:
            print(
                f"Would fix {sum(len(refs) for refs in references.values())} case sensitivity issues:"
            )
            for file_path, refs in references.items():
                print(f"\n{file_path}:")
                for _, old_ref, new_ref in refs:
                    print(f"  {old_ref} -> {new_ref}")
            # Verification step
            self.verify_references(references)
        else:
            print("No case sensitivity issues found.")


def main():
    import sys

    dry_run = "--dry-run" in sys.argv
    target_file = None

    # Check for --target-file option
    for i, arg in enumerate(sys.argv):
        if arg == "--target-file" and i + 1 < len(sys.argv):
            target_file = sys.argv[i + 1]
            break

    fixer = ImageCaseFixer()

    if target_file:
        # Process only the specified file
        print(f"Processing single file: {target_file}")
        fixer.scan_actual_files()
        references = fixer.find_image_references()

        # Filter to only the target file
        if target_file in references:
            target_refs = {target_file: references[target_file]}
            if dry_run:
                print(
                    f"Would fix {len(target_refs[target_file])} case sensitivity issues in {target_file}"
                )
                for _, old_ref, new_ref in target_refs[target_file]:
                    print(f"  {old_ref} -> {new_ref}")
            else:
                fixer.fix_references(target_refs)
                print(
                    f"Fixed {len(fixer.fixes_made)} case sensitivity issues in {target_file}"
                )

            # Verification step
            fixer.verify_references(target_refs)
        else:
            print(f"No image references found in {target_file}")
    else:
        # Process all files (original behavior)
        if dry_run:
            fixer.dry_run()
        else:
            fixer.run()


if __name__ == "__main__":
    main()
