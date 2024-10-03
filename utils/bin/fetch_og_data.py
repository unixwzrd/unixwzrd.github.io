#!/usr/bin/env python

"""
This script fetches Open Graph data from a given URL and caches the image
in the projects directory located at BASEDIR. It then writes the projects data to
projects.yml in the _data directory for Jekyll.
"""

import os
import requests
import yaml
from bs4 import BeautifulSoup


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

def cache_image(image_url, repo_name, base_dir):
    """
    Cache the image at the given URL in the projects directory under BASEDIR.

    Parameters
    ----------
    image_url : str
        URL of the image to cache.
    repo_name : str
        Name of the repository the image is associated with.
    base_dir : str
        Base directory where the image will be cached.

    Returns
    -------
    image_path : str
        Relative path to the cached image (for HTML use).
    """
    # Store the image in BASEDIR/html/assets/images/projects/
    image_dir = os.path.join(base_dir, "html/assets/images/projects/")
    os.makedirs(image_dir, exist_ok=True)
    image_path = os.path.join(image_dir, f"{repo_name}.png")

    # Cache the image locally if it doesn't already exist
    if not os.path.exists(image_path):
        img_data = requests.get(image_url, timeout=10 ).content
        with open(image_path, 'wb') as handler:
            handler.write(img_data)
    
    # Return the correct relative path for the HTML
    return f"/assets/images/projects/{repo_name}.png"

def get_base_dir():
    """
    Get the base directory from an environment variable or default to current working directory.

    Returns
    -------
    base_dir : str
        The base directory to use for storing images.
    """
    return os.getenv("BASEDIR", os.getcwd())

def main():
    """
    Main function.

    Loads repositories from html/_data/repos.yml, fetches OpenGraph data for each,
    caches the image, and writes the projects data to html/_data/github_projects.yml.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    # Get the base directory from environment or fallback
    base_dir = get_base_dir()

    # Path to repos.yml inside _data
    repos_file_path = os.path.join(base_dir, 'html/_data/repos.yml')

    # Path to save projects.yml inside _data
    projects_file_path = os.path.join(base_dir, 'html/_data/github_projects.yml')

    # Load the repos.yml data
    with open(repos_file_path, 'r', encoding="utf-8") as f:
        repos = yaml.safe_load(f)['repositories']

    projects = []

    for repo in repos:
        repo_url = f"https://github.com/{repo['owner']}/{repo['name']}"
        og_data = fetch_og_data(repo_url)
        image_path = cache_image(og_data["image_url"], repo['name'], base_dir)

        # Extract the repo name for a cleaner title
        repo_name = repo['name']

        projects.append({
            "title": repo_name,  # Only the repo name in the title
            "description": og_data["description"],  # Keep the fetched description
            "image_url": image_path,
            "repo_url": repo_url
        })

    # Write the github_projects.yml in the _data directory
    with open(projects_file_path, 'w', encoding="utf-8") as f:
        yaml.dump({"projects": projects}, f)

if __name__ == "__main__":
    main()