#!/usr/bin/env python3

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict


def extract_first_paragraph(content: str) -> str:
    """Extract the first paragraph of content after front matter."""
    # Remove front matter first
    content_without_fm = re.sub(r'^---.*?---\n', '', content, flags=re.DOTALL)
    
    # Find first non-empty paragraph
    paragraphs = content_without_fm.split('\n\n')
    for para in paragraphs:
        clean_para = para.strip()
        if clean_para and not clean_para.startswith('#') and '<!--more-->' not in clean_para:
            # Remove any markdown links
            clean_para = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean_para)
            return clean_para
    return ""


def get_default_fields(file_path: Path) -> Dict[str, str]:
    """Get default fields based on file path and content."""
    # Extract category from path for project posts
    category = None
    for parent in file_path.parents:
        if parent.name in ['_posts', '_drafts']:
            # Check if this is a project post
            project_dir = parent.parent
            if project_dir.parent.name == 'projects':
                category = project_dir.name
                break
    
    # If no category found from path, use 'blog'
    if not category:
        category = 'blog'
    
    return {
        'layout': 'post',
        'image': '/assets/images/default-og-image.png',
        'category': category,
        'tags': '[general]'
    }


def fix_frontmatter(file_path: Path) -> bool:
    """Fix front matter in a markdown file.
    
    Returns:
        bool: True if file was modified, False otherwise.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract front matter
        fm_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if not fm_match:
            return False

        front_matter = fm_match.group(1)
        
        # Parse existing front matter
        fm_data: Dict[str, str] = {}
        for line in front_matter.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if ':' not in line:
                continue
                
            key, value = [x.strip() for x in line.split(':', 1)]
            
            # Skip commented lines
            if key.startswith('#'):
                continue
            
            # Clean up values
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            
            # Don't overwrite first instance of a field
            if key not in fm_data:
                fm_data[key] = value

        # Get default fields
        defaults = get_default_fields(file_path)
        
        # Add missing required fields
        modified = False
        for key, default_value in defaults.items():
            if key not in fm_data:
                fm_data[key] = default_value
                modified = True

        # Fix specific fields
        if 'date' not in fm_data and any(parent.name in ['_posts', '_drafts'] for parent in file_path.parents):
            # Try to extract date from filename first
            date_match = re.match(r'(\d{4}-\d{2}-\d{2})', file_path.stem)
            if date_match:
                fm_data['date'] = date_match.group(1)
            else:
                # Use current date as fallback
                fm_data['date'] = datetime.now().strftime('%Y-%m-%d')
            modified = True

        if 'excerpt' not in fm_data:
            fm_data['excerpt'] = extract_first_paragraph(content)
            modified = True
        elif 'image:' in fm_data['excerpt']:
            fm_data['excerpt'] = extract_first_paragraph(content)
            modified = True

        if 'image' in fm_data and ('"' in fm_data['image'] or not fm_data['image'].startswith('/')):
            fm_data['image'] = fm_data['image'].strip('"')
            if not fm_data['image'].startswith('/'):
                fm_data['image'] = '/' + fm_data['image']
            modified = True

        # Rebuild front matter
        new_front_matter = '---\n'
        for key in sorted(fm_data.keys()):
            new_front_matter += f'{key}: {fm_data[key]}\n'
        new_front_matter += '---\n'
        
        # Get content after front matter, removing any duplicate excerpt/image lines
        content_after_fm = re.sub(r'^---\n.*?\n---\n(excerpt:.*?\nimage:.*?\n)?', '', content, flags=re.DOTALL)
        
        # Combine new front matter with content
        new_content = new_front_matter + content_after_fm
        
        if content != new_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed front matter in {file_path}")
            return True
        
        return modified

    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return False


def main() -> None:
    base_dir = Path(os.getenv("BASEDIR", os.getcwd()))
    posts_dir = base_dir / 'html'
    
    # Find all markdown files
    md_files = list(posts_dir.rglob('*.md'))
    fixed_count = 0
    file_count = 0
    
    print("\nFixing front matter in markdown files...")
    print("=" * 50)
    
    for file_path in md_files:
        file_count += 1
        if fix_frontmatter(file_path):
            fixed_count += 1
    
    print("\n" + "=" * 50)
    print("Fix complete:")
    print(f"- Files processed: {file_count}")
    print(f"- Files fixed: {fixed_count}")
    print(f"- Success rate: {(fixed_count / file_count * 100):.1f}%")


if __name__ == "__main__":
    main() 