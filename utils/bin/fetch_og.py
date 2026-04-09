#!/usr/bin/env python3

import argparse
import datetime
import html
import json
import logging
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional

import requests
import yaml
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(format="%(levelname)s: %(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger("fetch_og")


DEFAULT_HEADERS = {
    "User-Agent": "unixwzrd-site-fetch-og/1.0 (+https://unixwzrd.ai)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/*;q=0.8,*/*;q=0.7",
}

REFRESH_EXISTING_IMAGES = False
CARD_STYLE_VERSION = 8


def should_refresh_existing_images() -> bool:
    """Return True when remote image refresh is explicitly requested."""
    return REFRESH_EXISTING_IMAGES


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh project metadata and thumbnails.")
    parser.add_argument(
        "--refresh-images",
        action="store_true",
        help="Force regeneration of locally generated project thumbnail PNGs.",
    )
    args, _ = parser.parse_known_args()
    return args


def format_count(value: Optional[int]) -> str:
    """Format numeric stats for compact display."""
    if value is None:
        return "0"
    if value >= 1000000:
        return f"{value / 1000000:.1f}M".rstrip("0").rstrip(".")
    if value >= 1000:
        return f"{value / 1000:.1f}K".rstrip("0").rstrip(".")
    return str(value)


def language_color(language: str) -> str:
    """Pick a stable accent color from the primary language."""
    palette = {
        "Python": "#3572A5",
        "Swift": "#ff9f43",
        "JavaScript": "#f7df1e",
        "TypeScript": "#3178c6",
        "Shell": "#89e051",
        "Ruby": "#cc342d",
        "C": "#a8b9cc",
        "C++": "#649ad2",
        "HTML": "#e34c26",
        "CSS": "#563d7c",
        "Makefile": "#427819",
        "Jupyter Notebook": "#da5b0b",
        "Jinja": "#a52a22",
        "Go": "#00add8",
        "Rust": "#dea584",
        "Java": "#b07219",
        "SCSS": "#c6538c",
        "Objective-C": "#438eff",
        "Objective-C++": "#6866fb",
        "CMake": "#064f8c",
        "Lua": "#000080",
        "Perl": "#0298c3",
        "PHP": "#4f5d95",
        "Dockerfile": "#384d54",
        "Vue": "#41b883",
        "Kotlin": "#a97bff",
        "Markdown": "#083fa1",
    }
    if language in palette:
        return palette[language]

    # Stable fallback so unknown languages don't all collapse to the same color.
    fallback_palette = [
        "#0ea5e9",
        "#10b981",
        "#f59e0b",
        "#ef4444",
        "#8b5cf6",
        "#14b8a6",
        "#f97316",
        "#3b82f6",
    ]
    if not language:
        return "#0ea5e9"
    index = sum(ord(char) for char in language) % len(fallback_palette)
    return fallback_palette[index]


def fetch_top_languages(owner: str, repo: str, top_n: int = 3) -> List[Dict[str, str]]:
    """Fetch the top languages for a repository ordered by bytes of code."""
    url = f"https://api.github.com/repos/{owner}/{repo}/languages"
    try:
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=10)
        if response.status_code in {403, 404}:
            return []
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict) or not payload:
            return []

        total = sum(payload.values()) or 1
        items = sorted(payload.items(), key=lambda item: item[1], reverse=True)[:top_n]
        return [
            {
                "name": language,
                "share": f"{round((count / total) * 100)}%",
                "color": language_color(language),
            }
            for language, count in items
        ]
    except requests.RequestException:
        return []


def generate_project_card(
    data: Dict, owner: str, name: str, title: str, description: str, base_dir: Path
) -> Optional[str]:
    """Generate a local 1200x600 PNG thumbnail from repository metadata."""
    image_dir = base_dir / "html/assets/images/projects"
    image_dir.mkdir(parents=True, exist_ok=True)
    image_path = image_dir / f"{name}.png"
    meta_path = image_dir / f"{name}.card-meta.json"

    card_metadata = {
        "card_style_version": CARD_STYLE_VERSION,
        "owner": owner,
        "name": name,
        "title": title,
        "description": description,
        "language": data.get("language") or "",
        "top_languages": data.get("top_languages", []),
        "contributors_count": data.get("contributors_count", 0),
        "stargazers_count": data.get("stargazers_count", 0),
        "forks_count": data.get("forks_count", 0),
        "open_issues_count": data.get("open_issues_count", 0),
        "updated_at": data.get("updated_at") or "",
    }

    if image_path.exists() and meta_path.exists() and not should_refresh_existing_images():
        try:
            existing_metadata = json.loads(meta_path.read_text(encoding="utf-8"))
            if existing_metadata == card_metadata:
                logger.info("Using existing cached image for %s: %s", name, image_path)
                return f"/assets/images/projects/{name}.png"
        except (OSError, json.JSONDecodeError) as e:
            logger.warning("Could not read card metadata for %s: %s", name, e)

    renderer = shutil.which("wkhtmltoimage")
    if not renderer:
        logger.warning("wkhtmltoimage not available; cannot generate card for %s", name)
        if image_path.exists():
            return f"/assets/images/projects/{name}.png"
        return None

    language = data.get("language") or "Repository"
    accent = language_color(language)
    contributors = format_count(data.get("contributors_count"))
    stars = format_count(data.get("stargazers_count"))
    forks = format_count(data.get("forks_count"))
    issues = format_count(data.get("open_issues_count"))
    updated_raw = data.get("updated_at", "")
    updated_label = updated_raw[:10] if updated_raw else "n/a"
    repo_label = f"{owner}/{name}"
    safe_description = html.escape((description or "").strip())
    safe_repo_label = html.escape(repo_label)
    top_languages = data.get("top_languages") or []
    if not top_languages:
        top_languages = [{"name": language, "share": "", "color": accent}]
    language_markup = "".join(
        f'<div class="lang-row"><span class="lang-dot" style="background:{html.escape(item["color"])}"></span>'
        f'<span class="lang-name">{html.escape(item["name"])}</span>'
        f'<span class="lang-share">{html.escape(item["share"])}</span></div>'
        for item in top_languages[:3]
    )

    html_content = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    html, body {{
      margin: 0;
      width: 1200px;
      height: 600px;
      overflow: hidden;
      background: #eef2f6;
      font-family: "Avenir Next", "Helvetica Neue", Arial, sans-serif;
    }}
    .card {{
      position: relative;
      width: 1200px;
      height: 600px;
      box-sizing: border-box;
      padding: 42px 48px;
      color: #1e2b39;
      background-color: #f2f6fa;
      border: 1px solid rgba(180, 192, 205, 0.98);
      box-shadow:
        0 18px 38px rgba(0, 0, 0, 0.20),
        inset 0 1px 0 rgba(255,255,255,0.85);
    }}
    .frame {{
      position: absolute;
      inset: 18px;
      border: 1px solid rgba(205, 215, 225, 0.98);
      border-radius: 26px;
      pointer-events: none;
    }}
    .brand {{
      position: absolute;
      left: 48px;
      top: 40px;
      display: block;
      padding: 0;
      border-radius: 0;
      font-size: 27px;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      white-space: nowrap;
      color: #25374d;
      background: transparent;
      border: 0;
      font-weight: 700;
    }}
    .repo {{
      position: absolute;
      left: 48px;
      top: 132px;
      margin: 0;
      width: 780px;
      font-size: 68px;
      line-height: 1.02;
      font-weight: 700;
      color: #223148;
      letter-spacing: -0.03em;
    }}
    .description {{
      position: absolute;
      left: 48px;
      top: 270px;
      width: 930px;
      margin: 0;
      font-size: 34px;
      line-height: 1.3;
      color: #263c55;
      font-weight: 600;
    }}
    .stats {{
      position: absolute;
      left: 48px;
      right: 48px;
      bottom: 38px;
      height: 164px;
    }}
    .stat {{
      display: inline-block;
      width: 138px;
      height: 138px;
      margin-right: 12px;
      padding: 16px 16px 14px 16px;
      box-sizing: border-box;
      border-radius: 18px;
      background: rgba(255,255,255,0.98);
      border: 1px solid rgba(182, 194, 207, 1);
      vertical-align: top;
    }}
    .stat-label {{
      font-size: 18px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: #33485f;
      font-weight: 700;
    }}
    .stat-value {{
      margin-top: 10px;
      font-size: 40px;
      line-height: 1;
      color: #0f2134;
      font-weight: 700;
    }}
    .language {{
      display: inline-block;
      width: 486px;
      height: 150px;
      padding: 14px 18px;
      box-sizing: border-box;
      border-radius: 18px;
      background: rgba(255,255,255,0.98);
      border: 1px solid rgba(182, 194, 207, 1);
      vertical-align: top;
      text-align: left;
    }}
    .languages {{
      display: block;
    }}
    .lang-row {{
      display: block;
      margin-bottom: 7px;
      color: #203247;
      font-size: 17px;
      font-weight: 700;
      line-height: 1.2;
    }}
    .lang-dot {{
      display: inline-block;
      width: 12px;
      height: 12px;
      margin-right: 8px;
      border-radius: 50%;
      vertical-align: middle;
    }}
    .lang-name {{
      vertical-align: middle;
    }}
    .lang-share {{
      margin-left: 8px;
      color: #49627d;
      font-weight: 600;
      vertical-align: middle;
    }}
    .updated {{
      margin-top: 14px;
      font-size: 24px;
      color: #2f4963;
      font-weight: 600;
    }}
    .bar {{
      position: absolute;
      left: 0;
      right: 0;
      bottom: 0;
      height: 10px;
      background: linear-gradient(90deg, {accent} 0%, {accent} 70%, #b8c3ce 70%, #b8c3ce 100%);
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="frame"></div>
    <div class="brand">Distributed Thinking Systems LLC</div>
    <div class="repo">{safe_repo_label}</div>
    <p class="description">{safe_description}</p>
    <div class="stats">
      <div class="stat">
        <div class="stat-label">Contrib</div>
        <div class="stat-value">{contributors}</div>
      </div>
      <div class="stat">
        <div class="stat-label">Issues</div>
        <div class="stat-value">{issues}</div>
      </div>
      <div class="stat">
        <div class="stat-label">Stars</div>
        <div class="stat-value">{stars}</div>
      </div>
      <div class="stat">
        <div class="stat-label">Forks</div>
        <div class="stat-value">{forks}</div>
      </div>
      <div class="language">
        <div class="languages">{language_markup}</div>
        <div class="updated">Updated {html.escape(updated_label)}</div>
      </div>
    </div>
    <div class="bar"></div>
  </div>
</body>
</html>
"""

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        html_path = tmpdir_path / f"{name}.html"
        output_path = tmpdir_path / f"{name}.png"
        html_path.write_text(html_content, encoding="utf-8")

        try:
            subprocess.run(
                [
                    renderer,
                    "--width",
                    "1200",
                    "--height",
                    "600",
                    "--format",
                    "png",
                    "--disable-smart-width",
                    str(html_path),
                    str(output_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            shutil.copyfile(output_path, image_path)
            meta_path.write_text(
                json.dumps(card_metadata, indent=2, sort_keys=True),
                encoding="utf-8",
            )
            logger.info("Generated project card for %s", name)
            return f"/assets/images/projects/{name}.png"
        except subprocess.CalledProcessError as e:
            logger.error("Failed to generate project card for %s: %s", name, e.stderr.strip())
            if image_path.exists():
                logger.warning("Keeping existing image for %s: %s", name, image_path)
                return f"/assets/images/projects/{name}.png"
            return None


def setup_environment() -> Path:
    """Initialize environment and return base directory."""
    base_dir = Path(os.getenv("BASEDIR", os.getcwd()))
    logger.info("Using base directory: %s", base_dir)
    return base_dir


def load_repository_config(base_dir: Path) -> List[Dict]:
    """Load repository configuration from repos.yml."""
    repos_file = base_dir / "html/_data/repos.yml"
    try:
        with open(repos_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data.get("repositories", [])
    except Exception as e:
        logger.error("Failed to load repository config: %s", e)
        return []


def fetch_url_data(url: str, parse_html: bool = False) -> Optional[Dict]:
    """Fetch data from a URL, optionally parsing HTML for OpenGraph metadata.

    Args:
        url: URL to fetch data from
        parse_html: If True, parse response as HTML and extract OpenGraph metadata
    """
    try:
        response = requests.get(url, timeout=10, headers=DEFAULT_HEADERS)
        response.raise_for_status()

        if parse_html:
            soup = BeautifulSoup(response.text, "html.parser")
            og_title = soup.find("meta", property="og:title")
            og_desc = soup.find("meta", property="og:description")
            og_image = soup.find("meta", property="og:image")

            logger.info("OpenGraph data for %s:", url)
            logger.info(
                "  - title: %s", og_title["content"] if og_title else "Not found"
            )
            logger.info(
                "  - description: %s",
                og_desc["content"] if og_desc else "Not found",
            )
            logger.info(
                "  - image: %s", og_image["content"] if og_image else "Not found"
            )

            return {
                "title": og_title["content"] if og_title else "",
                "description": og_desc["content"] if og_desc else "",
                "image_url": og_image["content"] if og_image else "",
            }
        return response.json()
    except Exception as e:
        logger.error("Failed to fetch data from %s: %s", url, e)
        return None


def fetch_github_data(owner: str, repo: str) -> Optional[Dict]:
    """Fetch repository data from GitHub API."""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    try:
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=10)
        if response.status_code == 404:
            logger.info("Repository %s/%s is private or not found", owner, repo)
            return None
        response.raise_for_status()
        data = response.json()
        contributors_count = fetch_contributors_count(owner, repo)
        if contributors_count is not None:
            data["contributors_count"] = contributors_count
        data["top_languages"] = fetch_top_languages(owner, repo)
        return data
    except requests.RequestException as e:
        logger.error("Error fetching GitHub data for %s/%s: %s", owner, repo, e)
        return None


def fetch_contributors_count(owner: str, repo: str) -> Optional[int]:
    """Fetch contributor count using GitHub pagination headers when available."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors?per_page=1&anon=1"
    try:
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=10)
        if response.status_code in {403, 404}:
            return None
        response.raise_for_status()

        link_header = response.headers.get("Link", "")
        if 'rel="last"' in link_header:
            for part in link_header.split(","):
                if 'rel="last"' in part:
                    fragment = part.split(";")[0].strip()
                    if "page=" in fragment:
                        page_token = fragment.split("page=")[-1].split(">")[0]
                        if page_token.isdigit():
                            return int(page_token)

        payload = response.json()
        if isinstance(payload, list):
            return len(payload)
        return None
    except requests.RequestException:
        return None


def fetch_og_metadata(url: str) -> Optional[Dict]:
    """Fetch Open Graph metadata from URL."""
    data = fetch_url_data(url, parse_html=True)
    if data:
        logger.debug("Retrieved OpenGraph data for %s", url)
    return data


def cache_image(image_url, repo_name, web_root):
    """Cache the image at the given URL in the projects directory under BASEDIR.

    Args:
        image_url: URL or local path to the image
        repo_name: Name of the repository the image is associated with
        web_root: Base directory where the image will be cached
    """
    fallback_images = [
        "/assets/images/ImageNotFound.png",
        "/assets/images/NoImageFound.png",
    ]

    def get_first_existing_fallback():
        for fallback in fallback_images:
            fallback_path = web_root / "html" / fallback.lstrip("/")
            if fallback_path.exists():
                logger.warning("Using fallback image for %s: %s", repo_name, fallback)
                return fallback
        logger.error("No fallback image found for %s, using default path.", repo_name)
        return "/assets/images/projects/default.png"

    if not image_url:
        logger.warning("No image URL provided for %s", repo_name)
        return get_first_existing_fallback()

    if image_url.startswith("/"):
        local_image_path = web_root / "html" / image_url.lstrip("/")
        if local_image_path.exists():
            logger.debug("Using local image for %s: %s", repo_name, image_url)
            return image_url
        logger.error("Local image not found for %s: %s", repo_name, local_image_path)
        return get_first_existing_fallback()

    image_dir = web_root / "html/assets/images/projects"
    image_dir.mkdir(parents=True, exist_ok=True)
    image_path = image_dir / f"{repo_name}.png"

    if image_path.exists() and not should_refresh_existing_images():
        logger.info("Using existing cached image for %s: %s", repo_name, image_path)
        return f"/assets/images/projects/{repo_name}.png"

    try:
        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            time.sleep(1)
            response = requests.get(
                image_url, stream=True, headers=DEFAULT_HEADERS, timeout=20
            )

            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                wait_seconds = int(retry_after) if retry_after and retry_after.isdigit() else attempt * 2
                logger.warning(
                    "Rate limited while caching image for %s (attempt %s/%s). Waiting %ss.",
                    repo_name,
                    attempt,
                    max_attempts,
                    wait_seconds,
                )
                if attempt < max_attempts:
                    time.sleep(wait_seconds)
                    continue

            response.raise_for_status()
            break

        content_type = response.headers.get("content-type", "")
        if not content_type.startswith("image/"):
            logger.error("Invalid content type for %s image: %s", repo_name, content_type)
            if image_path.exists():
                logger.warning("Keeping existing image for %s: %s", repo_name, image_path)
                return f"/assets/images/projects/{repo_name}.png"
            return get_first_existing_fallback()

        content = response.content
        if len(content) < 1000:
            logger.error(
                "Image content too small for %s, likely an error response", repo_name
            )
            if image_path.exists():
                logger.warning("Keeping existing image for %s: %s", repo_name, image_path)
                return f"/assets/images/projects/{repo_name}.png"
            return get_first_existing_fallback()

        with open(image_path, "wb") as f:
            f.write(content)
            logger.info("Cached image for %s", repo_name)

        return f"/assets/images/projects/{repo_name}.png"
    except requests.RequestException as e:
        if getattr(getattr(e, "response", None), "status_code", None) == 429:
            logger.warning("Skipping image refresh for %s due to rate limiting: %s", repo_name, e)
        else:
            logger.error("Error caching image for %s: %s", repo_name, e)
        if image_path.exists():
            logger.warning("Keeping existing image for %s: %s", repo_name, image_path)
            return f"/assets/images/projects/{repo_name}.png"
        return get_first_existing_fallback()


def generate_project_files(project_data: Dict, base_dir: Path) -> bool:
    """Generate project page and blog entry if they don't already exist."""
    try:
        image_dir = base_dir / "html/assets/images/projects" / project_data["name"]
        image_dir.mkdir(parents=True, exist_ok=True)
        gitkeep_file = image_dir / ".gitkeep"
        if not gitkeep_file.exists():
            gitkeep_file.write_text("", encoding="utf-8")

        project_dir = base_dir / "html/projects"
        project_dir.mkdir(parents=True, exist_ok=True)

        project_path = project_dir / project_data["name"]
        project_path.mkdir(exist_ok=True)

        drafts_dir = project_path / "_drafts"
        drafts_dir.mkdir(exist_ok=True)

        posts_dir = project_path / "_posts"
        posts_dir.mkdir(exist_ok=True)

        project_page = project_dir / f"{project_data['name']}.md"
        if not project_page.exists():
            project_content = f"""---
layout: project
title: \"{project_data['title']}\"
category: {project_data['name']}
permalink: /projects/{project_data['name']}/
---

{project_data['description']}"""
            project_page.write_text(project_content)
            logger.info("Created project page for %s", project_data["name"])
        else:
            logger.info(
                "Project page for %s already exists, skipping...",
                project_data["name"],
            )

        draft_template = drafts_dir / "template-blog-entry.md"
        if not draft_template.exists():
            draft_content = f"""---
layout: post
title: \"New {project_data['title']} Update\"
date: 2024-03-14
category: {project_data['name']}
tags: [development, update]
excerpt: \"Brief introduction about this update\"
image: /assets/images/projects/{project_data['name']}.png
# author: Michael Sullivan
# For drafts, use either:
# published: false  (won't show up at all)
# draft: true      (will show up with --drafts flag)
draft: true
published: true
---

Brief introduction about this update (this will appear in previews).

<!--more-->

## Current Status

- Point 1
- Point 2
- Point 3

## New Features

### Feature 1
Description of feature 1

### Feature 2
Description of feature 2

## Technical Details

Technical information about the implementation.

## Next Steps

- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## Get Involved

How users can participate or provide feedback.
"""
            draft_template.write_text(draft_content)
            logger.info("Created draft template for %s", project_data["name"])

        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        sample_post = posts_dir / f"{current_date}-{project_data['name'].lower()}-introduction.md"
        if not sample_post.exists():
            sample_content = f"""---
layout: post
title: \"Introducing {project_data['title']}\"
date: {current_date}
category: {project_data['name']}
tags: [introduction, overview]
excerpt: \"Welcome to the {project_data['title']} project blog. Here we'll share updates, insights, and progress on our development journey.\"
image: /assets/images/projects/{project_data['name']}.png
# author: Michael Sullivan
# For drafts, use either:
# published: false  (won't show up at all)
# draft: true      (will show up with --drafts flag)
draft: true
published: true
---

Welcome to the {project_data['title']} project blog. Here we'll share updates, insights, and progress on our development journey.

<!--more-->

## About {project_data['title']}

{project_data['description']}

## Current Features

- Feature 1
- Feature 2
- Feature 3

## Roadmap

Our planned development roadmap includes:

1. Phase 1
2. Phase 2
3. Phase 3

## Get Involved

We welcome contributions and feedback. Here's how you can get involved:

- Review our documentation
- Test new features
- Provide feedback
- Contribute to development

[Contact us](/contact) to learn more about participating in this project.
"""
            sample_post.write_text(sample_content)
            logger.info("Created sample blog post for %s", project_data["name"])

        logger.info("Generated project files for %s", project_data["name"])
        return True
    except Exception as e:
        logger.error("Failed to generate project files for %s: %s", project_data["name"], e)
        return False


def write_projects_data(projects: List[Dict], base_dir: Path) -> bool:
    """Write processed projects data to github_projects.yml."""
    output_file = base_dir / "html/_data/github_projects.yml"
    try:
        class LiteralStr(str):
            pass

        def literal_presenter(dumper, data):
            if len(data) > 60:
                return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
            return dumper.represent_scalar("tag:yaml.org,2002:str", data, style='"')

        yaml.add_representer(LiteralStr, literal_presenter)

        for project in projects:
            if len(project.get("description", "")) > 60:
                project["description"] = LiteralStr(project["description"])

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(
                {"projects": projects},
                f,
                allow_unicode=True,
                default_flow_style=False,
                indent=2,
                sort_keys=False,
            )
        logger.info("Successfully wrote projects data")
        return True
    except Exception as e:
        logger.error("Failed to write projects data: %s", e)
        return False


def format_title(name: str) -> str:
    """Format repository name into a clean title."""
    special_cases = {
        "macos": "macOS",
        "cuda": "CUDA",
        "mps": "MPS",
        "cpu": "CPU",
        "gpt": "GPT",
        "chatgpt": "ChatGPT",
        "ui": "UI",
        "webui": "WebUI",
        "llama": "LLaMA",
        "venvutil": "VenvUtil",
        "torchdevice": "TorchDevice",
        "oobabooga": "Oobabooga",
        "loggpt": "LogGPT Chatlog Export",
        "unicodefix": "UnicodeFix",
        "llm": "LLM",
    }

    title = name.replace("-", " ")
    words = title.split()

    formatted_words = []
    for word in words:
        word_lower = word.lower()
        if word_lower in special_cases:
            formatted_words.append(special_cases[word_lower])
        else:
            formatted_words.append(word.capitalize())

    return " ".join(formatted_words)


def normalize_description(description: str, owner: str, name: str) -> str:
    """Strip GitHub repo suffix noise from descriptions."""
    if not description:
        return description

    suffix = f" - {owner}/{name}"
    if description.endswith(suffix):
        return description[: -len(suffix)].rstrip()

    return description


def create_project_entry(
    data: Optional[Dict], owner: str, name: str, base_dir: Path, repo_config: Dict
) -> Dict:
    """Create a project entry from GitHub repository data or manual configuration."""
    project_image = base_dir / "html/assets/images/projects" / f"{name}.png"
    existing_image_url = None
    if project_image.exists():
        existing_image_url = f"/assets/images/projects/{name}.png"

    overrides = repo_config.get("overrides")
    if overrides is None:
        overrides = repo_config.get("manual_data", {})

    visibility = overrides.get("visibility")
    if visibility is None:
        if data is None:
            visibility = "private"
        else:
            visibility = data.get("visibility", "public")
    else:
        visibility = visibility.lower()

    if data is None:
        image_url = overrides.get("image_url")
        if not image_url and existing_image_url:
            image_url = existing_image_url
        elif not image_url:
            image_url = "/assets/images/projects/default.png"

        cached_image = cache_image(image_url, name, base_dir)
        banner_image_url = overrides.get("banner_image_url", cached_image)

        entry = {
            "name": name,
            "owner": owner,
            "title": overrides.get("title", format_title(name)),
            "description": overrides.get("description", f"Private repository: {name}"),
            "image_url": cached_image,
            "banner_image_url": banner_image_url,
            "page_url": f"/projects/{name}/",
            "visibility": visibility,
        }

        if visibility == "public":
            entry["repo_url"] = f"https://github.com/{owner}/{name}"

        return entry

    title = overrides.get("title") or format_title(name)
    description = overrides.get("description") or normalize_description(
        data.get("description", ""), owner, name
    )
    override_image_url = overrides.get("image_url")
    if override_image_url:
        cached_image = cache_image(override_image_url, name, base_dir)
    else:
        cached_image = generate_project_card(data, owner, name, title, description, base_dir)
        if not cached_image:
            image_url = data.get("image_url", data.get("owner", {}).get("avatar_url", ""))
            if not image_url and existing_image_url:
                image_url = existing_image_url
            elif not image_url:
                image_url = "/assets/images/projects/default.png"
            cached_image = cache_image(image_url, name, base_dir)
    banner_image_url = overrides.get("banner_image_url", cached_image)

    entry = {
        "name": name,
        "owner": owner,
        "title": title,
        "description": description,
        "image_url": cached_image,
        "banner_image_url": banner_image_url,
        "page_url": f"/projects/{name}/",
        "visibility": visibility,
    }

    if visibility == "public":
        entry["repo_url"] = f"https://github.com/{owner}/{name}"

    return entry


def main():
    """Main function to orchestrate the project data fetching and generation."""
    global REFRESH_EXISTING_IMAGES
    args = parse_args()
    REFRESH_EXISTING_IMAGES = args.refresh_images

    base_dir = setup_environment()
    repositories = load_repository_config(base_dir)
    processed_projects = []

    for repo in repositories:
        try:
            owner = repo["owner"]
            name = repo["name"]

            github_data = fetch_github_data(owner, name)
            if github_data is None:
                logger.info(
                    "Using fallback scaffolding for %s/%s - GitHub data unavailable",
                    owner,
                    name,
                )

            project_data = create_project_entry(
                data=github_data,
                owner=owner,
                name=name,
                base_dir=base_dir,
                repo_config=repo,
            )

            project_file = base_dir / "html/projects" / f"{name}.md"
            if not project_file.exists():
                generate_project_files(project_data, base_dir)
            else:
                logger.info("Project %s already exists, skipping file generation", name)

            processed_projects.append(project_data)

        except Exception as e:
            logger.error("Failed to process repository %s: %s", name, e)
            continue

    write_projects_data(processed_projects, base_dir)


if __name__ == "__main__":
    main()
