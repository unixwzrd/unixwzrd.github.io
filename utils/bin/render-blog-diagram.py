#!/usr/bin/env python3
"""Render a DOT or Mermaid source to the SVG and PNG used by a blog figure."""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


def normalize_mermaid_svg(path: Path) -> None:
    """Give an mmdc SVG intrinsic dimensions for the site's image viewer."""
    svg = path.read_text(encoding="utf-8")
    root = re.search(r"<svg\b[^>]*>", svg)
    if root is None:
        raise ValueError(f"Mermaid output has no SVG root: {path}")
    opening = root.group()
    view_box = re.search(
        r'\bviewBox="[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)"', opening
    )
    if view_box is None:
        raise ValueError(f"Mermaid output has no numeric viewBox: {path}")
    width, height = view_box.groups()
    if 'width="100%"' not in opening:
        raise ValueError(f"Unexpected Mermaid SVG width; review before publishing: {path}")
    opening = opening.replace('width="100%"', f'width="{width}" height="{height}"', 1)
    path.write_text(svg[: root.start()] + opening + svg[root.end() :], encoding="utf-8")


def render(source: Path, output_stem: Path) -> None:
    source = source.resolve(strict=True)
    if source.suffix not in {".dot", ".mmd"}:
        raise ValueError("Source must have a .dot or .mmd extension")
    output_stem = output_stem.resolve()
    output_stem.parent.mkdir(parents=True, exist_ok=True)
    renderer = "dot" if source.suffix == ".dot" else "mmdc"
    if shutil.which(renderer) is None:
        raise RuntimeError(f"{renderer} is required to render {source.name}; install it and try again")

    with tempfile.TemporaryDirectory(prefix="diagram-render-", dir=output_stem.parent) as scratch:
        svg = Path(scratch) / "figure.svg"
        png = Path(scratch) / "figure.png"
        if renderer == "dot":
            commands = [
                ["dot", "-Tsvg", str(source), "-o", str(svg)],
                ["dot", "-Tpng", "-Gdpi=150", str(source), "-o", str(png)],
            ]
        else:
            commands = [
                ["mmdc", "-i", str(source), "-o", str(svg), "-t", "dark", "-b", "transparent", "-q"],
                ["mmdc", "-i", str(source), "-o", str(png), "-t", "dark", "-b", "transparent", "-w", "1600", "-s", "1.5", "-q"],
            ]
        for command in commands:
            subprocess.run(command, check=True)
        if renderer == "mmdc":
            normalize_mermaid_svg(svg)
        ET.parse(svg)
        if not svg.stat().st_size or not png.stat().st_size:
            raise ValueError("Renderer produced an empty output")
        os.replace(svg, Path(f"{output_stem}.svg"))
        os.replace(png, Path(f"{output_stem}.png"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="editable .dot or .mmd file")
    parser.add_argument("output_stem", type=Path, help="output path without .svg or .png")
    args = parser.parse_args()
    try:
        render(args.source, args.output_stem)
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"render-blog-diagram: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote {args.output_stem}.svg and {args.output_stem}.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
