#!/usr/bin/env python

import os
import requests
import yaml
from bs4 import BeautifulSoup
from logging import Logger

mylog = Logger(__name__)
mylog.setLevel("INFO")

def fetch_github_profile(username):
    """
    Fetch GitHub profile data using GitHub API.

    Parameters
    ----------
    username : str
        GitHub username to fetch profile data for.

    Returns
    -------
    profile_data : dict
        GitHub profile data including the avatar URL, bio, and login.
    """
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "login": data["login"],
            "bio": data["bio"],
            "avatar_url": data["avatar_url"]
        }
    else:
        raise Exception(f"Failed to fetch GitHub profile data for {username}")

def fetch_og_data(url):
    """
    Fetch Open Graph data from the given URL.

    Parameters
    ----------
    url : str
        URL to fetch Open Graph data from.

    Returns
    -------
    og_data : dict
        Open Graph data containing the title, description, and image_url.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    og_title = soup.find("meta", property="og:title")["content"]
    og_desc = soup.find("meta", property="og:description")["content"]
    og_image = soup.find("meta", property="og:image")["content"]

    return {
        "title": og_title,
        "description": og_desc,
        "image_url": og_image
    }

def cache_image(image_url, repo_name, web_root):
    """
    Cache the image at the given URL in the projects directory under BASE_DIR.

    Parameters
    ----------
    image_url : str
        URL of the image to cache.
    repo_name : str
        Name of the repository the image is associated with.
    web_root : str
        Base directory where the image will be cached.

    Returns
    -------
    image_path : str
        Relative path to the cached image (for HTML use).
    """
    # Store the image in {web_root}/assets/images/projects/
    image_dir = os.path.join(web_root, "assets/images/projects/")
    os.makedirs(image_dir, exist_ok=True)
    image_path = os.path.join(image_dir, f"{repo_name}.png")

    # Cache the image locally if it doesn't already exist
    if not os.path.exists(image_path):
        img_data = requests.get(image_url, timeout=10).content
        with open(image_path, 'wb') as handler:
            handler.write(img_data)
    
    # Return the correct relative path for the HTML
    return f"/assets/images/projects/{repo_name}.png"


def create_project_intro(repo_name, description, repo_url, web_root):
    """
    Create a project introduction markdown file (projectname.md) if it doesn't exist.
    Acts as the index page for the project and lists its blog posts.
    """
    projects_dir = os.path.join(web_root, 'projects')
    os.makedirs(projects_dir, exist_ok=True)
    project_file_path = os.path.join(projects_dir, f"{repo_name}.md")

    if not os.path.exists(project_file_path):
        # Content of the project introduction file
        content = f"""---
title: "{repo_name}"
layout: project
permalink: /projects/{repo_name}/
---


## {repo_name}

{description}

- [View on GitHub]({repo_url})

## Project Blog Entries

{{% for post in site.categories.{repo_name} %}}
  <article class="post">
    <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
    <span class="post-date">{{ post.date | date: "%B %d, %Y" }}</span>
    {{% assign excerpt = post.content | split: '<!--more-->' | first %}}
    {{ excerpt | truncatewords: 50 | markdownify | process_heading }}
    <a href="{{ post.url | relative_url }}" class="btn">Read More</a>
  </article>
{{% endfor %}}


{{% include join_us.html %}}

{{% include getintouch.html %}}

"""
        with open(project_file_path, 'w', encoding="utf-8") as f:
            f.write(content)
    else:
        mylog.warning(f"Project page for {repo_name} already exists, skipping...")

def create_project_blog_entry(repo_name, web_root):
    """
    Create a placeholder project blog entry if it doesn't exist in the project directory.
    """
    blog_dir = os.path.join(web_root, 'projects', repo_name)
    os.makedirs(blog_dir, exist_ok=True)
    blog_file_path = os.path.join(blog_dir, f"{repo_name}-project-blog-entry.md")

    if not os.path.exists(blog_file_path):
        content = f"""---
title: "{repo_name} Blog Entry"
layout: post
category: {repo_name}
published: false
---

This is a placeholder for the project blog entry.
"""
        with open(blog_file_path, 'w', encoding="utf-8") as f:
            f.write(content)
    else:
        mylog.warning(f"Blog entry for {repo_name} already exists, skipping...")

def get_base_dir():
    """
    Get the base directory from an environment variable or default to current working directory.
    """
    return os.getenv("BASE_DIR", os.getcwd())

def main():
    """
    Main function.

    Loads repositories from {web_root}/_data/repos.yml, fetches OpenGraph data for each,
    caches the image, and writes the projects data to {web_root}/_data/github_projects.yml.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    mylog.info("Fetching OpenGraph data for repositories...")
    # Get the base directory from environment or fallback
    base_dir = get_base_dir()
    web_root = os.path.join(base_dir, 'html')

    # Path to repos.yml inside _data
    repos_file_path = os.path.join(web_root, '_data/repos.yml')

    # Path to save projects.yml inside _data
    projects_file_path = os.path.join(web_root, '_data/github_projects.yml')

    # Load the repos.yml data
    mylog.info("Loading repositories from " + repos_file_path)
    with open(repos_file_path, 'r', encoding="utf-8") as f:
        repos = yaml.safe_load(f)['repositories']

    projects = []

    for repo in repos:
        if repo['name'] == '':  # GitHub profile
            profile_data = fetch_github_profile(repo['owner'])
            image_path = cache_image(profile_data["avatar_url"], repo['owner'], web_root)

            projects.append({
                "title": "GitHub Profile: " + profile_data["login"],
                "description": profile_data["bio"] or "GitHub profile for " + profile_data["login"],
                "image_url": image_path,
                "repo_url": f"https://github.com/{repo['owner']}"
            })
        else:
            repo_url = f"https://github.com/{repo['owner']}/{repo['name']}"
            og_data = fetch_og_data(repo_url)
            image_path = cache_image(og_data["image_url"], repo['name'], web_root)

            # Create project introduction and blog entries
            create_project_intro(repo['name'], og_data["description"], repo_url, web_root)
            create_project_blog_entry(repo['name'], web_root)

            projects.append({
                "title": repo['name'],
                "description": og_data["description"],
                "image_url": image_path,
                "repo_url": repo_url
            })

    # Write the github_projects.yml in the _data directory
    mylog.info("Writing projects data to _data/github_projects.yml...")
    with open(projects_file_path, 'w', encoding="utf-8") as f:
        yaml.dump({"projects": projects}, f)
    
    mylog.info("Fetching OpenGraph data for repositories... Completed!")


if __name__ == "__main__":
    main()
