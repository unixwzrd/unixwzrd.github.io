# File Watchers

This directory contains scripts that are automatically run by the general file watcher when files change.

## How It Works

The general file watcher (`utils/bin/file_watcher.py`) monitors the `html/` directory for file changes and automatically runs all Python scripts in this directory.

## Dynamic Reloading

**No restart required!** The file watcher automatically detects when you add, modify, or remove scripts in this directory and reloads them immediately. You'll see messages like:
- `🆕 New watcher script detected: my_new_watcher.py`
- `🔄 Watcher script modified: existing_watcher.py`
- `🗑️ Watcher script removed: old_watcher.py`

## Adding a New Watcher

1. Create a new Python script in this directory
2. The script should accept two command-line arguments:
   - `file_path`: Path to the changed file
   - `event_type`: Type of event (modified, created, deleted)
3. The script will receive these environment variables:
   - `WATCHER_FILE`: Path to the changed file
   - `WATCHER_EVENT`: Type of event
   - `WATCHER_NAME`: Name of the watcher script

## Example Watcher Script

```python
#!/usr/bin/env python3
"""
Example Watcher

This is an example watcher script that shows the basic structure.
"""

import os
import sys

def main():
    file_path = sys.argv[1]
    event_type = sys.argv[2]
    
    # Only process specific file types
    if not file_path.endswith('.md'):
        return
    
    # Your watcher logic here
    print(f"Processing {file_path} (event: {event_type})")
    
    # Example: run some command
    # subprocess.run(['some', 'command', file_path])

if __name__ == "__main__":
    main()
```

## Available Watchers

- **image_path_fixer.py**: Automatically fixes image paths in Markdown files when they are modified

## Running the File Watcher

```bash
# Start the file watcher
python utils/bin/file_watcher.py

# List available watchers
python utils/bin/file_watcher.py --list-watchers

# Watch a different directory
python utils/bin/file_watcher.py --target-dir some/other/dir
```

## Best Practices

1. **Debouncing**: The watcher automatically debounces events (1 second), so don't worry about multiple rapid events
2. **Error Handling**: Always handle errors gracefully in your watcher scripts
3. **File Filtering**: Check file extensions or paths to only process relevant files
4. **Output**: Use `print()` for success messages, the watcher will display them
5. **Exit Codes**: Return 0 for success, non-zero for failure

## Disabling a Watcher

To temporarily disable a watcher, rename it to start with an underscore (e.g., `_disabled_watcher.py`). 