#!/usr/bin/env python3

import datetime
import logging
import os
import time
from pathlib import Path
from typing import Dict, List, Optional

import requests
import yaml
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(
    format='%(levelname)s: %(name)s: %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('fetch_og')


def setup_environment() -> Path:
    """Initialize environment and return base directory."""
    base_dir = Path(os.getenv("BASEDIR", os.getcwd()))
    logger.info("Using base directory: %s", base_dir)
    return base_dir


def load_repository_config(base_dir: Path) -> List[Dict]:
    """Load repository configuration from repos.yml."""
    repos_file = base_dir / 'html/_data/repos.yml'
    try:
        with open(repos_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data.get('repositories', [])
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
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        if parse_html:
            soup = BeautifulSoup(response.text, 'html.parser')
            og_title = soup.find("meta", property="og:title")
            og_desc = soup.find("meta", property="og:description")
            og_image = soup.find("meta", property="og:image")

            # Log OpenGraph metadata findings
            logger.info("OpenGraph data for %s:", url)
            logger.info("  - title: %s", og_title["content"] if og_title else "Not found")
            logger.info("  - description: %s", og_desc["content"] if og_desc else "Not found")
            logger.info("  - image: %s", og_image["content"] if og_image else "Not found")

            return {
                "title": og_title["content"] if og_title else "",
                "description": og_desc["content"] if og_desc else "",
                "image_url": og_image["content"] if og_image else ""
            }
        return response.json()
    except Exception as e:
        logger.error("Failed to fetch data from %s: %s", url, e)
        return None


def fetch_github_data(owner: str, repo: str) -> Optional[Dict]:
    """Fetch repository data from GitHub API."""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    try:
        response = requests.get(url)
        if response.status_code == 404:
            logger.info("Repository %s/%s is private or not found", owner, repo)
            return None
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error("Error fetching GitHub data for %s/%s: %s", owner, repo, e)
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
        '/assets/images/ImageNotFound.png',
        '/assets/images/NoImageFound.png',
    ]

    def get_first_existing_fallback():
        for fallback in fallback_images:
            fallback_path = web_root / 'html' / fallback.lstrip('/')
            if fallback_path.exists():
                logger.warning("Using fallback image for %s: %s", repo_name, fallback)
                return fallback
        logger.error("No fallback image found for %s, using default path.", repo_name)
        return '/assets/images/projects/default.png'

    # If no image_url is provided, use fallback
    if not image_url:
        logger.warning("No image URL provided for %s", repo_name)
        return get_first_existing_fallback()

    # If image_url is a local path, verify it exists
    if image_url.startswith('/'):
        local_image_path = web_root / 'html' / image_url.lstrip('/')
        if local_image_path.exists():
            logger.debug("Using local image for %s: %s", repo_name, image_url)
            return image_url
        else:
            logger.error("Local image not found for %s: %s", repo_name, local_image_path)
            return get_first_existing_fallback()

    # For remote URLs, always cache the image
    image_dir = web_root / 'html/assets/images/projects'
    image_dir.mkdir(parents=True, exist_ok=True)
    image_path = image_dir / f"{repo_name}.png"

    try:
        time.sleep(1)  # Rate limiting
        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            logger.error(f"Invalid content type for {repo_name} image: {content_type}")
            # If a local image already exists, use it
            if image_path.exists():
                logger.warning("Keeping existing image for %s: %s", repo_name, image_path)
                return f'/assets/images/projects/{repo_name}.png'
            return get_first_existing_fallback()

        content = response.content
        if len(content) < 1000:  # Minimum size check
            logger.error(f"Image content too small for {repo_name}, likely an error response")
            if image_path.exists():
                logger.warning("Keeping existing image for %s: %s", repo_name, image_path)
                return f'/assets/images/projects/{repo_name}.png'
            return get_first_existing_fallback()

        # Only write the new image if it is valid
        with open(image_path, 'wb') as f:
            f.write(content)
            logger.info(f"Cached image for {repo_name}")

        return f'/assets/images/projects/{repo_name}.png'
    except requests.RequestException as e:
        logger.error(f"Error caching image for {repo_name}: {e}")
        # If a local image already exists, use it
        if image_path.exists():
            logger.warning("Keeping existing image for %s: %s", repo_name, image_path)
            return f'/assets/images/projects/{repo_name}.png'
        return get_first_existing_fallback()


def generate_project_files(project_data: Dict, base_dir: Path) -> bool:
    """Generate project page and blog entry if they don't already exist."""
    try:
        # Create project page
        project_dir = base_dir / 'html/projects'
        project_dir.mkdir(parents=True, exist_ok=True)

        # Create project-specific directories
        project_path = project_dir / project_data['name']
        project_path.mkdir(exist_ok=True)
        
        # Create _drafts directory for the project
        drafts_dir = project_path / '_drafts'
        drafts_dir.mkdir(exist_ok=True)

        # Create _posts directory for the project
        posts_dir = project_path / '_posts'
        posts_dir.mkdir(exist_ok=True)

        # Generate project page only if it doesn't exist
        project_page = project_dir / f"{project_data['name']}.md"
        if not project_page.exists():
            # Generate minimal project page content
            project_content = f"""---
layout: project
title: "{project_data['title']}"
category: {project_data['name']}
permalink: /projects/{project_data['name']}/
---

{project_data['description']}"""
            project_page.write_text(project_content)
            logger.info(f"Created project page for {project_data['name']}")
        else:
            logger.info(f"Project page for {project_data['name']} already exists, skipping...")

        # Generate draft template
        draft_template = drafts_dir / "template-blog-entry.md"
        if not draft_template.exists():
            draft_content = f"""---
layout: post
title: "New {project_data['title']} Update"
date: 2024-03-14
category: {project_data['name']}
tags: [development, update]
excerpt: "Brief introduction about this update"
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
            logger.info(f"Created draft template for {project_data['name']}")

        # Generate sample blog entry in _posts if it doesn't exist
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        sample_post = posts_dir / f"{current_date}-{project_data['name'].lower()}-introduction.md"
        if not sample_post.exists():
            sample_content = f"""---
layout: post
title: "Introducing {project_data['title']}"
date: {current_date}
category: {project_data['name']}
tags: [introduction, overview]
excerpt: "Welcome to the {project_data['title']} project blog. Here we'll share updates, insights, and progress on our development journey."
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
            logger.info(f"Created sample blog post for {project_data['name']}")

        logger.info(f"Generated project files for {project_data['name']}")
        return True
    except Exception as e:
        logger.error(f"Failed to generate project files for {project_data['name']}: {e}")
        return False


def write_projects_data(projects: List[Dict], base_dir: Path) -> bool:
    """Write processed projects data to github_projects.yml."""
    output_file = base_dir / 'html/_data/github_projects.yml'
    try:
        # Configure YAML dumper to use double quotes for strings
        class QuotedString(str):
            pass

        def quoted_presenter(dumper, data):
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')

        yaml.add_representer(QuotedString, quoted_presenter)

        # Convert long strings to QuotedString
        for project in projects:
            project['description'] = QuotedString(project['description'])

        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump({"projects": projects}, f, allow_unicode=True, default_flow_style=False)
        logger.info("Successfully wrote projects data")
        return True
    except Exception as e:
        logger.error("Failed to write projects data: %s", e)
        return False


def format_title(name: str) -> str:
    """Format repository name into a clean title.
    
    Args:
        name: Repository name to format
        
    Returns:
        Formatted title string
    """
    # Special case replacements (add more as needed)
    special_cases = {
        'macos': 'macOS',
        'cuda': 'CUDA',
        'mps': 'MPS',
        'cpu': 'CPU',
        'gpt': 'GPT',
        'chatgpt': 'ChatGPT',
        'ui': 'UI',
        'webui': 'WebUI',
        'llama': 'LLaMA',
        'venvutil': 'VenvUtil',
        'torchdevice': 'TorchDevice',
        'oobabooga': 'Oobabooga',
        'loggpt': 'LogGPT Chatlog Export',
        'unicodefix': 'UnicodeFix',
    }
    
    # First replace hyphens with spaces
    title = name.replace('-', ' ')
    
    # Split into words
    words = title.split()
    
    # Process each word
    formatted_words = []
    for word in words:
        word_lower = word.lower()
        # Check if it's a special case
        if word_lower in special_cases:
            formatted_words.append(special_cases[word_lower])
        else:
            # Otherwise capitalize normally
            formatted_words.append(word.capitalize())
    
    return ' '.join(formatted_words)


def create_project_entry(data: Optional[Dict], owner: str, name: str, base_dir: Path, repo_config: Dict) -> Dict:
    """Create a project entry from GitHub repository data or manual configuration."""
    # Check if project image already exists
    project_image = base_dir / 'html/assets/images/projects' / f"{name}.png"
    existing_image_url = None
    if project_image.exists():
        existing_image_url = f"/assets/images/projects/{name}.png"

    # If repo is private or GitHub data is not available, use manual data
    if data is None:
        manual_data = repo_config.get('manual_data', {})
        image_url = manual_data.get('image_url')
        if not image_url and existing_image_url:
            image_url = existing_image_url
        elif not image_url:
            image_url = '/assets/images/projects/default.png'
        
        # Always try to cache the image, even for private repos
        cached_image = cache_image(image_url, name, base_dir)
            
        return {
            "name": name,
            "owner": owner,
            "title": manual_data.get('title', format_title(name)),
            "description": manual_data.get('description', f"Private repository: {name}"),
            "image_url": cached_image,
            "page_url": f"/projects/{name}/",
            "visibility": "private"
        }

    # For public repos, use GitHub/OpenGraph data
    image_url = data.get('image_url', data.get('owner', {}).get('avatar_url', ''))
    if not image_url and existing_image_url:
        image_url = existing_image_url
    elif not image_url:
        image_url = '/assets/images/projects/default.png'
    
    logger.debug("Project %s image URL: %s", name, image_url)

    return {
        "name": name,
        "owner": owner,
        "title": format_title(name),
        "description": data.get('description', ''),
        "image_url": cache_image(image_url, name, base_dir),
        "repo_url": f"https://github.com/{owner}/{name}",
        "page_url": f"/projects/{name}/",
        "visibility": data.get('visibility', 'public')
    }


def main():
    """Main function to orchestrate the project data fetching and generation."""
    base_dir = setup_environment()
    repositories = load_repository_config(base_dir)
    processed_projects = []

    for repo in repositories:
        try:
            owner = repo['owner']
            name = repo['name']

            github_data = fetch_github_data(owner, name)
            if github_data is None and not repo.get('manual_data'):
                logger.info("Skipping %s/%s - no data available", owner, name)
                continue

            og_data = {}
            if github_data:  # Only fetch OG data for public repos
                og_data = fetch_og_metadata(f"https://github.com/{owner}/{name}") or {}

            # Merge GitHub and OpenGraph data, preferring OpenGraph for overlapping fields
            project_data = create_project_entry(
                data={**github_data, **og_data} if github_data else None,
                owner=owner,
                name=name,
                base_dir=base_dir,
                repo_config=repo
            )

            # Only generate files if project doesn't exist
            project_file = base_dir / 'html/projects' / f"{name}.md"
            if not project_file.exists():
                generate_project_files(project_data, base_dir)
            else:
                logger.info(f"Project {name} already exists, skipping file generation")

            processed_projects.append(project_data)

        except Exception as e:
            logger.error("Failed to process repository %s: %s", name, e)
            continue

    write_projects_data(processed_projects, base_dir)


if __name__ == "__main__":
    main()
