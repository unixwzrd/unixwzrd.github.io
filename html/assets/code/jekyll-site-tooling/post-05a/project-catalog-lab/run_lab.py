#!/usr/bin/env python3
"""Exercise the site's frozen project generator without site data or network."""

import importlib.util
import sys
import tempfile
from argparse import ArgumentParser, Namespace
from pathlib import Path
from unittest import mock

import yaml


ROOT = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
SPEC = importlib.util.spec_from_file_location("fetch_og_lab", ROOT / "source/fetch_og.py")
fetch_og = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fetch_og)


def main():
    parser = ArgumentParser(description="Run the invented project catalog through the site's generator")
    parser.add_argument("--reorder", action="store_true", help="move QuietTool ahead of ExampleTool in the authored catalog")
    parser.add_argument("--show-hidden", action="store_true", help="change HiddenTool's authored visibility from none to public")
    args = parser.parse_args()
    repositories = [
        {"owner": "example", "name": "ExampleTool", "overrides": {"title": "Example Tool", "description": "An invented tool for the lab.", "visibility": "public"}},
        {"owner": "example", "name": "QuietTool", "overrides": {"title": "Quiet Tool", "description": "A private example.", "visibility": "private"}},
        {"owner": "example", "name": "HiddenTool", "overrides": {"title": "Hidden Tool", "visibility": "none"}},
    ]
    if args.reorder:
        repositories[0], repositories[1] = repositories[1], repositories[0]
    if args.show_hidden:
        repositories[2]["overrides"]["visibility"] = "public"
    metadata = {"ExampleTool": {"description": "A fetched description.", "visibility": "public", "language": "Python"}, "QuietTool": None, "HiddenTool": None}

    with tempfile.TemporaryDirectory(prefix="project-catalog-lab-") as scratch:
        base = Path(scratch)
        (base / "html/_data").mkdir(parents=True)
        with mock.patch.object(fetch_og, "setup_environment", return_value=base), \
             mock.patch.object(fetch_og, "load_repository_config", return_value=repositories), \
             mock.patch.object(fetch_og, "fetch_github_data", side_effect=lambda owner, name: metadata[name]), \
             mock.patch.object(fetch_og, "generate_project_card", return_value="/assets/images/projects/ExampleTool.png"), \
             mock.patch.object(fetch_og, "cache_image", side_effect=lambda url, name, base_dir: url), \
             mock.patch.object(fetch_og, "parse_args", return_value=Namespace(refresh_images=False)), \
             mock.patch.object(fetch_og.requests, "get", side_effect=AssertionError("network request attempted")):
            fetch_og.main()

        output = yaml.safe_load((base / "html/_data/github_projects.yml").read_text(encoding="utf-8"))["projects"]
        expected_order = ["QuietTool", "ExampleTool", "HiddenTool"] if args.reorder else ["ExampleTool", "QuietTool", "HiddenTool"]
        assert [p["name"] for p in output] == expected_order
        projects = {p["name"]: p for p in output}
        assert projects["ExampleTool"]["title"] == "Example Tool"
        assert projects["ExampleTool"]["description"] == "An invented tool for the lab."
        assert projects["ExampleTool"]["repo_url"] == "https://github.com/example/ExampleTool"
        assert projects["QuietTool"]["visibility"] == "private" and "repo_url" not in projects["QuietTool"]
        assert projects["HiddenTool"]["visibility"] == ("public" if args.show_hidden else "none")
        assert ("repo_url" in projects["HiddenTool"]) == args.show_hidden
        assert (base / "html/projects/ExampleTool.md").exists()
        assert (base / "html/projects/ExampleTool/_drafts/template-blog-entry.md").exists()
        intro = list((base / "html/projects/ExampleTool/_posts").glob("*.md"))
        assert len(intro) == 1 and "draft: true" in intro[0].read_text(encoding="utf-8")

        print("Generated data, in catalog order:")
        for project in output:
            print(f"  {project['name']}: {project['visibility']}; repo link: {'yes' if 'repo_url' in project else 'no'}")
        print(f"ExampleTool description: {projects['ExampleTool']['description']}")
        print("New ExampleTool files: landing page, _drafts/template-blog-entry.md, draft-marked _posts introduction")
        print("PASS: ordered projects, visibility, overrides, and new-project scaffolding")


if __name__ == "__main__":
    main()
