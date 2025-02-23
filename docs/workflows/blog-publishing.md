# Blog Publishing Guide

## Overview
This guide covers the process of creating and publishing blog posts, both for general blogs and project-specific blogs.

## Directory Structure
```
html/
├── _posts/                    # General blog posts
│   └── YYYY-MM-DD-title.md   # Format for general posts
└── projects/
    └── ProjectName/
        ├── _drafts/          # Work in progress posts
        │   └── draft.md
        └── _posts/           # Published project posts
            └── YYYY-MM-DD-project-name-title.md
```

## Creating a New Post

### General Blog Post
1. Create file in `html/_posts/` with format:
   ```
   YYYY-MM-DD-descriptive-title.md
   ```

2. Add front matter:
   ```yaml
   ---
   layout: post
   title: "Your Post Title"
   date: YYYY-MM-DD HH:MM:SS -0500
   categories: [category1, category2]
   tags: [tag1, tag2]
   ---
   ```

3. Add content with excerpt marker:
   ```markdown
   Brief introduction (this will appear in previews).

   <!--more-->

   Rest of your post content...
   ```

### Project Blog Post
1. Create draft in `html/projects/ProjectName/_drafts/`:
   ```
   descriptive-title.md
   ```

2. Add front matter:
   ```yaml
   ---
   layout: post
   title: "Your Project Post Title"
   date: YYYY-MM-DD HH:MM:SS -0500
   category: ProjectName
   tags: [tag1, tag2]
   ---
   ```

3. When ready to publish, move to `_posts/` with date prefix:
   ```bash
   mv _drafts/title.md _posts/YYYY-MM-DD-project-name-title.md
   ```

## Post Guidelines

### Content Structure
1. Start with brief introduction
2. Use `<!--more-->` to mark excerpt end
3. Use clear headings (h2, h3)
4. Include relevant links
5. Add images if helpful

### Formatting
1. Use markdown for formatting
2. Include code blocks with syntax highlighting:
   ````markdown
   ```python
   def example():
       print("Hello, World!")
   ```
   ````
3. Use lists and tables as needed
4. Add images with alt text:
   ```markdown
   ![Alt text](/path/to/image.png)
   ```

### Categories and Tags
- Use relevant categories
- Add descriptive tags
- Be consistent with naming
- Check existing tags for ideas

## Publishing Process

1. **Draft Stage**
   - Write post in _drafts
   - Preview locally
   - Get feedback if needed

2. **Pre-publish Checks**
   - Run spell check
   - Verify front matter
   - Check links
   - Test code samples

3. **Publishing**
   - Move to _posts with date
   - Run pre-commit checks
   - Commit changes
   - Push to repository

4. **Post-publish**
   - Verify on site
   - Check links work
   - Share on social media

## Common Issues

### Front Matter
- Missing required fields
- Incorrect date format
- Invalid categories/tags

### Content
- Missing excerpt marker
- Broken links
- Invalid markdown
- Missing alt text

### Build
- Date in future
- Duplicate permalinks
- Invalid front matter

## Tips and Tricks
1. Use templates for consistency
2. Preview locally before publishing
3. Keep drafts organized
4. Use meaningful file names
5. Follow naming conventions 