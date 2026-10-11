#!/usr/bin/env python3
"""Small, isolated prepublication gate exercise. Requires Python 3 only."""

import argparse
import re
from pathlib import Path


def make_fixture(root: Path, scenario: str) -> None:
    if root.exists():
        raise ValueError(f"output already exists: {root}")
    root.mkdir(parents=True)
    (root / "images").mkdir()
    title = "" if scenario == "missing-title" else 'title: "An example article"\n'
    target = "missing.md" if scenario == "broken-link" else "about.md"
    image = "missing.svg" if scenario == "missing-image" else "cover.svg"
    (root / "index.md").write_text(
        f"---\n{title}image: /images/{image}\n---\n\n"
        f"Read the [about page]({target}).\n",
        encoding="utf-8",
    )
    (root / "about.md").write_text("---\ntitle: About\n---\n\nA second page.\n", encoding="utf-8")
    (root / "images" / "cover.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"/>\n',
        encoding="utf-8",
    )


def front_matter(root: Path) -> None:
    for page in root.glob("*.md"):
        text = page.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        if not match or not re.search(r"^title:\s*\S", match.group(1), re.M):
            raise ValueError(f"{page.name}: missing title in front matter")


def local_links(root: Path) -> None:
    for page in root.glob("*.md"):
        text = page.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
            if target.startswith(("http:", "https:", "#")):
                continue
            candidate = (page.parent / target).resolve()
            if not candidate.is_relative_to(root.resolve()) or not candidate.is_file():
                raise ValueError(f"{page.name}: missing local link {target}")


def image_paths(root: Path) -> None:
    for page in root.glob("*.md"):
        match = re.search(r"^image:\s*/(.+)$", page.read_text(encoding="utf-8"), re.M)
        if match and not (root / match.group(1)).is_file():
            raise ValueError(f"{page.name}: missing image {match.group(1)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path, help="new output directory; existing paths are refused")
    parser.add_argument(
        "--scenario",
        choices=("clean", "missing-title", "broken-link", "missing-image"),
        default="clean",
    )
    args = parser.parse_args()
    try:
        make_fixture(args.root, args.scenario)
        for name, check in (
            ("front matter", front_matter),
            ("local links", local_links),
            ("image paths", image_paths),
        ):
            print(f"Checking {name}...", flush=True)
            check(args.root)
            print(f"PASS: {name}", flush=True)
    except (OSError, ValueError) as exc:
        print(f"STOP: {exc}", flush=True)
        return 1
    print(f"PASS: all gates; fixture retained at {args.root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
