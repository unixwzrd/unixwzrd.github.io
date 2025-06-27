#!/usr/bin/env python3
"""
Test Watcher Script

This script is used for testing the file watcher system.
It simply logs that it was executed.
"""

import os
import sys

def main():
    file_path = sys.argv[1]
    event_type = sys.argv[2]
    
    # Only process test files
    if not file_path.endswith('test_file.md'):
        return
    
    print(f"Test watcher executed for {file_path} (event: {event_type})")
    
if __name__ == "__main__":
    main()
