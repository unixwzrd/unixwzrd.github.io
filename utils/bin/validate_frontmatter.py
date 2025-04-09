#!/usr/bin/env python3

import os
import re
import sys
from pathlib import Path
from typing import Dict, List


def validate_frontmatter(file_path: Path) -> List[str]:
    """Validate front matter in a markdown file.
    
    Returns:
        List of error messages. Empty list means no errors.
    """
    errors = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if file starts with front matter
        if not content.startswith('---\n'):
            errors.append("File does not start with front matter markers (---).")
            return errors

        # Extract front matter
        fm_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if not fm_match:
            errors.append("Front matter is not properly closed with ---")
            return errors

        front_matter = fm_match.group(1)
        
        # Check for duplicate front matter after the closing ---
        if re.search(r'^---\n.*?\n---\n(excerpt:.*?\nimage:.*?\n)', content, re.DOTALL):
            errors.append("Found duplicate front matter content after closing ---")

        # Required fields based on file location
        required_fields: Dict[str, type] = {
            'layout': str,
            'title': str,
            'image': str,
            'excerpt': str
        }
        
        # Additional required fields for posts
        if any(parent.name in ['_posts', '_drafts'] for parent in file_path.parents):
            required_fields.update({
                'date': str,
                'category': str,
                'tags': str  # Changed from list to str since we validate format separately
            })

        # Parse and validate each line
        fm_data = {}
        for line in front_matter.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            if ':' not in line:
                errors.append(f"Invalid front matter line: {line}")
                continue
                
            key, value = [x.strip() for x in line.split(':', 1)]
            
            # Skip commented lines
            if key.startswith('#'):
                continue
                
            # Validate tags format
            if key == 'tags':
                if not (value.startswith('[') and value.endswith(']')):
                    errors.append(f"Tags must be in array format [tag1, tag2]. Found: {value}")
                    
            # Clean up values
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            
            fm_data[key] = value

        # Check for required fields
        for field, field_type in required_fields.items():
            if field not in fm_data:
                errors.append(f"Missing required field: {field}")

        # Validate specific fields
        if 'image' in fm_data:
            image_path = fm_data['image']
            if '"' in image_path:
                errors.append(f"Image path contains quotes: {image_path}")
            if not image_path.startswith('/'):
                errors.append(f"Image path must start with /: {image_path}")

        if 'excerpt' in fm_data:
            excerpt = fm_data['excerpt']
            if 'image:' in excerpt:
                errors.append("Excerpt contains 'image:' text, likely incorrect content")

        # Check for duplicate fields
        field_counts: Dict[str, int] = {}
        for line in front_matter.split('\n'):
            if ':' in line:
                field = line.split(':', 1)[0].strip()
                if not field.startswith('#'):
                    field_counts[field] = field_counts.get(field, 0) + 1
                    if field_counts[field] > 1:
                        errors.append(f"Duplicate field in front matter: {field}")

    except Exception as e:
        errors.append(f"Error processing file: {str(e)}")

    return errors


def main() -> None:
    base_dir = Path(os.getenv("BASEDIR", os.getcwd()))
    posts_dir = base_dir / 'html'
    
    # Find all markdown files
    md_files = list(posts_dir.rglob('*.md'))
    error_count = 0
    file_count = 0
    
    print("\nValidating front matter in markdown files...")
    print("=" * 50)
    
    for file_path in md_files:
        file_count += 1
        errors = validate_frontmatter(file_path)
        if errors:
            error_count += 1
            print(f"\nFile: {file_path}")
            for error in errors:
                print(f"  - {error}")
    
    print("\n" + "=" * 50)
    print("Validation complete:")
    print(f"- Files checked: {file_count}")
    print(f"- Files with errors: {error_count}")
    print(f"- Success rate: {((file_count - error_count) / file_count * 100):.1f}%")
    
    # Return non-zero exit code if there were errors
    sys.exit(1 if error_count > 0 else 0)


if __name__ == "__main__":
    main() 