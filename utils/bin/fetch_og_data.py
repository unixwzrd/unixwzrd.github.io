#!/usr/bin/env python
# utils/bin/fetch_og_data.py

import os
import yaml
import requests
from pathlib import Path

# Load repository data
with open('html/_data/repos.yml', 'r') as f:
    repos_data = yaml.safe_load(f)

projects = []

for repo in repos_data['repositories']:
    owner = repo['owner']
    name = repo['name']
    repo_api_url = f'https://api.github.com/repos/{owner}/{name}'
    response = requests.get(repo_api_url)
    repo_data = response.json()

    project = {
        'name': repo_data['name'],
        'owner': owner,
        'repo_url': repo_data['html_url'],
        'description': repo_data.get('description', 'No description available.'),
        'image_url': f"/assets/images/projects/{repo_data['name']}.png",
        'page_url': f"/projects/{repo_data['name']}/"
    }
    projects.append(project)

    # Create project index file if it doesn't exist
    project_index_path = f'html/projects/{name}.md'
    if not os.path.exists(project_index_path):
        with open(project_index_path, 'w') as f:
            f.write(f"""---
title: "{name}"
layout: project
project_name: "{name}"
repo_url: "{project['repo_url']}"
image_url: "{project['image_url']}"
permalink: /projects/{name}/
---

## {name}

{project['description']}

- [View on GitHub]({project['repo_url']})

""")

    # Create blog directory and placeholder file if it doesn't exist
    blog_dir = f'html/projects/{name}'
    if not os.path.exists(blog_dir):
        os.makedirs(blog_dir)

    blog_post_path = os.path.join(blog_dir, f'{name}-project-blog-entry.md')
    if not os.path.exists(blog_post_path):
        with open(blog_post_path, 'w') as f:
            f.write(f"""---
title: "{name} Blog Entry"
layout: post
category: {name}
published: false
---

This is a placeholder for the project blog entry.

""")

# Write projects data to _data/github_projects.yml
with open('html/_data/github_projects.yml', 'w') as f:
    yaml.dump({'projects': projects}, f)