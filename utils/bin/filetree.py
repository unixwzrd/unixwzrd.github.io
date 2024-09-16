#!/usr/bin/env python
"""
Generate a tree structure of the current directory excluding specific
directories/files.

Example usage:

    python filetree.py --exclude node_modules __pycache__

"""
import os
import argparse as Ap
from rich.console import Console
from rich.tree import Tree

def is_ignored(item_name):
    """
    Check if the item should be ignored based on the arguments given.

    :param item_name: The name of the item to check.
    :return: True if the item should be ignored, False otherwise.
    """
    return item_name.startswith(('.', '_')) or item_name in args.exclude

def add_items(root_dir, parent_tree):
    """
    Recursively add items in the file system to the tree structure.

    :param root_dir: The root directory to start from.
    :param parent_tree: The parent tree node to add items to.
    """
    for item_name in sorted(os.listdir(root_dir)):
        if is_ignored(item_name):
            continue

        item_path = os.path.join(root_dir, item_name)
        if os.path.isdir(item_path):
            # Add directory with custom format and recursively add subdirectories
            dir_branch = parent_tree.add(f"{item_name}/")
            add_items(item_path, dir_branch)
        elif item_name.endswith(('.html', '.md', '.py', '.js', '.css', '.sass', '.scss')):
            # Add file with custom format for files
            parent_tree.add(item_name)

def generate_tree():
    """
    Generate a tree structure of the current directory excluding specific
    directories/files.
    """
    console = Console()
    tree = Tree("Root Directory")
    add_items(".", tree)
    console.print(tree)

# Argument parser setup to allow exclusions from command line
parser = Ap.ArgumentParser(description="Generate a tree structure excluding specific directories/files.")
parser.add_argument( '--exclude', nargs='+',  default=[],
                     help='Whitespace-separated list of directories/files to exclude.')
args = parser.parse_args()

if __name__ == "__main__":
    generate_tree()
