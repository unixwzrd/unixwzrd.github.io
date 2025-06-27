#!/usr/bin/env python3
"""
Image Path Fixer Watcher

Automatically fixes image paths in Markdown files when they are modified.
This script is designed to be run by the general file watcher.

Environment variables provided by the watcher:
- WATCHER_FILE: Path to the modified file
- WATCHER_EVENT: Type of event (modified, created, etc.)
- WATCHER_NAME: Name of this watcher script
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    if len(sys.argv) < 3:
        print("Usage: image_path_fixer.py <file_path> <event_type>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    event_type = sys.argv[2]
    
    # Only process Markdown files
    if not file_path.endswith('.md'):
        return
    
    # Get the filename for filtering
    filename = Path(file_path).name
    
    # Determine base URL based on environment
    base_url = "http://localhost:4000"  # Default for development
    
    # Run the image path fixer on this specific file
    try:
        cmd = [
            sys.executable, "utils/bin/fix_image_paths.py",
            "--base-url", base_url,
            "--target-dir", "html",
            "--file-filter", filename
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            if "would change" in result.stdout or "changed" in result.stdout:
                print(f"Fixed image paths in {filename}")
            else:
                print(f"No image path issues found in {filename}")
        else:
            print(f"Error fixing image paths: {result.stderr}")
            
    except Exception as e:
        print(f"Failed to run image path fixer: {e}")

if __name__ == "__main__":
    main() 