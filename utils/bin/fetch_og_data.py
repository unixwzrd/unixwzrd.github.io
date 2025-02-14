#!/usr/bin/env python

import os
import requests
import yaml
import datetime
from bs4 import BeautifulSoup as BS
import logging

# Set up logging
logging.basicConfig(
    format='%(levelname)s: %(name)s: %(message)s',
    level=logging.INFO
)
mylog = logging.getLogger(os.path.basename(__file__).replace('.py', ''))

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
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "login": data["login"],
            "bio": data.get("bio", ""),
            "avatar_url": data["avatar_url"]
        }
    except requests.exceptions.RequestException as e:
        mylog.error(f"Failed to fetch GitHub profile data for {username}: {e}")
        return None

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
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BS(response.text, 'html.parser')

        og_title_tag = soup.find("meta", property="og:title")
        og_desc_tag = soup.find("meta", property="og:description")
        og_image_tag = soup.find("meta", property="og:image")

        og_title = og_title_tag["content"] if og_title_tag else "No title available"
        og_desc = og_desc_tag["content"] if og_desc_tag else "No description available."
        og_image = og_image_tag["content"] if og_image_tag else ""

        return {
            "title": og_title,
            "description": og_desc,
            "image_url": og_image
        }
    except requests.exceptions.RequestException as e:
        mylog.error(f"Failed to fetch Open Graph data from {url}: {e}")
        return None
    except Exception as e:
        mylog.error(f"Error parsing Open Graph data from {url}: {e}")
        return None

def cache_image(image_url, repo_name, web_root):
    """
    Cache the image at the given URL in the projects directory under BASEDIR.

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
    image_dir = os.path.join(web_root, "html/assets/images/projects/")
    os.makedirs(image_dir, exist_ok=True)
    image_path = os.path.join(image_dir, f"{repo_name}.png")

    # Cache the image locally if it doesn't already exist or overwrite the existing one
    if image_url:
        try:
            img_data = requests.get(image_url, timeout=10).content
            with open(image_path, 'wb') as handler:
                handler.write(img_data)
            mylog.info(f"Cached image for {repo_name}")
        except requests.exceptions.RequestException as e:
            mylog.error(f"Failed to download image for {repo_name}: {e}")
            # Return a placeholder or default image path
            return "/assets/images/projects/default.png"
    else:
        mylog.warning(f"No image URL for {repo_name}, using default image")
        # Return a placeholder or default image path
        return "/assets/images/projects/default.png"

    # Return the correct relative path for the HTML
    return f"/assets/images/projects/{repo_name}.png"

def create_project_intro(repo_name, description, repo_url, web_root):
    """
    Create a project introduction markdown file (projectname.md) if it doesn't exist.
    Acts as the index page for the project and lists its blog posts.
    """
    projects_dir = os.path.join(web_root, 'html/projects')
    os.makedirs(projects_dir, exist_ok=True)
    project_file_path = os.path.join(projects_dir, f"{repo_name}.md")

    if not os.path.exists(project_file_path):
        # Content of the project introduction file
        content = f"""---
layout: project
title: "{repo_name}"
category: {repo_name}
---

## {repo_name}

{description}

<!-- Placeholder for additional user supplied information >
## This is some optional additional information on {repo_name}

Some additional information as a placeholder for additional project information we can edit to appear on the page as well, in front of the blog entries.
<!-- Placeholder for additional user supplied information -->

* [View on GitHub]({repo_url}){{: target="_blank" rel="noopener noreferrer"}}

## Project Blog Entries

{{% for post in site.categories.{repo_name} %}}
<article class="post">
    <h3><a href="{{{{ post.url | relative_url }}}}">{{{{ post.title }}}}</a></h3>
    <span class="post-date">{{{{ post.date | date: "%B %d, %Y" }}}}</span>
    {{% assign excerpt = post.content | split: '<!--more-->' | first %}}
    {{{{ excerpt | truncatewords: 50 | markdownify }}}}
    <a href="{{{{ post.url | relative_url }}}}" class="btn">Read More</a>
</article>
{{% endfor %}}

{{% include join_us.html %}}

{{% include getintouch.html %}}
"""
        try:
            with open(project_file_path, 'w', encoding="utf-8") as f:
                f.write(content)
            mylog.info(f"Created project introduction page for {repo_name}")
        except Exception as e:
            mylog.error(f"Failed to create project introduction page for {repo_name}: {e}")
    else:
        mylog.info(f"Project page for {repo_name} already exists, skipping...")

def create_project_blog_entry(repo_name, web_root):
    """
    Create a placeholder project blog entry if it doesn't exist in the project directory.
    """
    blog_dir = os.path.join(web_root, 'html/projects', repo_name)
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

<!--more-->

{{% include join_us.html %}}

{{% include getintouch.html %}}
"""
        try:
            with open(blog_file_path, 'w', encoding="utf-8") as f:
                f.write(content)
            mylog.info(f"Created placeholder blog entry for {repo_name}")
        except Exception as e:
            mylog.error(f"Failed to create blog entry for {repo_name}: {e}")
    else:
        mylog.info(f"Blog entry for {repo_name} already exists, skipping...")

def get_base_dir():
    """
    Get the base directory from an environment variable or default to current working directory.
    """
    return os.getenv("BASEDIR", os.getcwd())

def archive_project_data(project_data, web_root):
    """
    Add project to the archived projects YAML file with archive date.
    """
    archive_data_file = os.path.join(web_root, '_data/archived_projects.yml')
    
    # Load existing archived projects
    archived_projects = []
    if os.path.exists(archive_data_file):
        try:
            with open(archive_data_file, 'r', encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if data and 'projects' in data:
                    archived_projects = data['projects']
        except Exception as e:
            mylog.error(f"Failed to load archived projects data: {e}")

    # Add archive date to project data
    project_data['archive_date'] = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Add to archived projects if not already there
    if not any(p['name'] == project_data['name'] for p in archived_projects):
        archived_projects.append(project_data)

    # Write updated archive data
    try:
        with open(archive_data_file, 'w', encoding="utf-8") as f:
            header = f"""---
# DO NOT EDIT THIS FILE BY HAND - it was generated by the site automation
# script {os.path.basename(__file__)} at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
---
"""
            f.write(header)
            yaml.dump({'projects': archived_projects}, f)
            mylog.info(f"Updated archived projects data for {project_data['name']}")
    except Exception as e:
        mylog.error(f"Failed to write archived projects data: {e}")

def archive_unused_projects(web_root, active_projects):
    """
    Move inactive projects to an archive directory structure.
    
    Archive structure:
    html/
    ├── _archives/
    │   └── projects/
    │       ├── project1/
    │       │   ├── project1.md
    │       │   └── project1-blog-entry.md
    │       ├── includes/
    │       │   └── project1.html
    │       └── images/
    │           └── project1.png
    """
    archive_root = os.path.join(web_root, '_archives')
    archive_projects = os.path.join(archive_root, 'projects')
    archive_images = os.path.join(archive_root, 'projects/images')
    archive_includes = os.path.join(archive_root, 'projects/includes')
    
    # Create archive directories
    os.makedirs(archive_projects, exist_ok=True)
    os.makedirs(archive_images, exist_ok=True)
    os.makedirs(archive_includes, exist_ok=True)

    projects_dir = os.path.join(web_root, 'projects')
    if not os.path.exists(projects_dir):
        return

    # Move inactive project files and directories
    for item in os.listdir(projects_dir):
        item_path = os.path.join(projects_dir, item)
        project_name = item.replace('.md', '')
        
        if project_name not in active_projects:
            if os.path.isfile(item_path):
                try:
                    import shutil
                    shutil.move(item_path, os.path.join(archive_projects, item))
                    mylog.info(f"Archived project file: {item}")
                except Exception as e:
                    mylog.error(f"Failed to archive {item}: {e}")
            elif os.path.isdir(item_path):
                try:
                    import shutil
                    shutil.move(item_path, os.path.join(archive_projects, item))
                    mylog.info(f"Archived project directory: {item}")
                except Exception as e:
                    mylog.error(f"Failed to archive directory {item}: {e}")

    # Move inactive project images
    images_dir = os.path.join(web_root, "assets/images/projects/")
    if os.path.exists(images_dir):
        for image in os.listdir(images_dir):
            if image.endswith('.png'):
                project_name = image.replace('.png', '')
                if project_name not in active_projects:
                    try:
                        import shutil
                        shutil.move(os.path.join(images_dir, image), 
                                os.path.join(archive_images, image))
                        mylog.info(f"Archived project image: {image}")
                    except Exception as e:
                        mylog.error(f"Failed to archive image {image}: {e}")

    # Move inactive project includes
    includes_dir = os.path.join(web_root, "_includes/projects/")
    if os.path.exists(includes_dir):
        for include in os.listdir(includes_dir):
            if include.endswith('.html'):
                project_name = include.replace('.html', '')
                if project_name not in active_projects:
                    try:
                        import shutil
                        shutil.move(os.path.join(includes_dir, include), 
                                os.path.join(archive_includes, include))
                        mylog.info(f"Archived project include: {include}")
                    except Exception as e:
                        mylog.error(f"Failed to archive include {include}: {e}")

def main():
    """
    Main function.

    Loads repositories from {web_root}/_data/repos.yml, fetches OpenGraph data for each,
    caches the image, and writes the projects data to {web_root}/_data/github_projects.yml.
    """
    mylog.info("Fetching OpenGraph data for repositories...")
    # Get the base directory from environment or fallback
    base_dir = get_base_dir()
    web_root = base_dir

    # Path to repos.yml inside _data
    repos_file_path = os.path.join(web_root, 'html/_data/repos.yml')

    # Path to save projects.yml inside _data
    projects_file_path = os.path.join(web_root, 'html/_data/github_projects.yml')

    # Load the repos.yml data
    mylog.info("Loading repositories from " + repos_file_path)
    try:
        with open(repos_file_path, 'r', encoding="utf-8") as f:
            repos = yaml.safe_load(f)['repositories']
    except Exception as e:
        mylog.error(f"Failed to load repositories from {repos_file_path}: {e}")
        return

    # Get list of active project names
    active_projects = [repo['name'] for repo in repos if repo['name']]
    
    # Archive unused projects before generating new ones
    archive_unused_projects(web_root, active_projects)

    projects = []

    for repo in repos:
        if repo['name'] == '':  # GitHub profile
            profile_data = fetch_github_profile(repo['owner'])
            if profile_data:
                image_path = cache_image(profile_data["avatar_url"], repo['owner'], web_root)

                projects.append({
                    "name": profile_data["login"],
                    "title": "GitHub Profile: " + profile_data["login"],
                    "description": profile_data["bio"] or "GitHub profile for " + profile_data["login"],
                    "image_url": image_path,
                    "repo_url": f"https://github.com/{repo['owner']}",
                    "page_url": f"/projects/{profile_data['login']}/"
                })
            else:
                mylog.warning(f"Skipping GitHub profile for {repo['owner']} due to previous errors.")
                continue
        else:
            repo_url = f"https://github.com/{repo['owner']}/{repo['name']}"
            og_data = fetch_og_data(repo_url)
            if og_data:
                image_path = cache_image(og_data["image_url"], repo['name'], web_root)

                # Create project introduction and blog entries
                create_project_intro(repo['name'], og_data["description"], repo_url, web_root)
                create_project_blog_entry(repo['name'], web_root)

                projects.append({
                    "name": repo['name'],
                    "owner": repo['owner'],
                    "repo_url": repo_url,
                    "description": og_data["description"],
                    "image_url": image_path,
                    "page_url": f"/projects/{repo['name']}/",
                    "title": repo['name']
                })
            else:
                mylog.warning(f"Skipping repository {repo['owner']}/{repo['name']} due to previous errors.")
                continue

    # Write the github_projects.yml in the _data directory
    mylog.info("Writing projects data to _data/github_projects.yml...")
    try:
        with open(projects_file_path, 'w', encoding="utf-8") as f:
            yaml.dump({"projects": projects}, f)
        mylog.info("Successfully wrote projects data to github_projects.yml")
    except Exception as e:
        mylog.error(f"Failed to write projects data to {projects_file_path}: {e}")

    mylog.info("Fetching OpenGraph data for repositories... Completed!")

if __name__ == "__main__":
    main()