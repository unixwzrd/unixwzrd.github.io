# Blog System and Templates

## Overview

The blog system consists of several components that work together to display posts across the site:

1. **Post Layout**: The main template for displaying individual blog posts
2. **Blog List Component**: A reusable component for displaying lists of blog posts
3. **Pagination**: System for breaking up long lists of posts into pages
4. **Project Blog Integration**: Special handling for project-specific blog posts

## Post Layout

The post layout (`_layouts/post.html`) is used to render individual blog posts. It handles:

- Post title and metadata display
- Content formatting
- Author information
- Date formatting
- Footer content

### Important Variables

When working with the post layout, remember that all frontmatter variables are accessed through the `page` object:

```liquid
{{ page.title }}
{{ page.date }}
{{ page.author }}
{{ page.categories }}
{{ page.tags }}
```

### Common Issues

- Using `post.` variables instead of `page.` variables in the layout
- Missing frontmatter in blog posts
- Incorrect date formatting

## Blog List Component

The blog list component (`_includes/blog_list.html`) provides a consistent way to display lists of blog posts across the site. It can be included in any page with parameters:

```liquid
{% include blog_list.html 
   heading="Latest Posts" 
   limit=5 
   category="project-name" 
%}
```

### Parameters

- `heading`: The heading to display above the list (optional)
- `limit`: Maximum number of posts to display (default: 5)
- `category`: Filter posts by category (optional)
- `tag`: Filter posts by tag (optional)

## Pagination

Pagination is configured in `_config.yml`:

```yaml
paginate: 5
paginate_path: "/blog/page:num/"
```

To use pagination, the template must be an HTML file (not Markdown) and must include pagination logic:

```liquid
{% if paginator.total_pages > 1 %}
<div class="pagination">
  {% if paginator.previous_page %}
    <a href="{{ paginator.previous_page_path | relative_url }}">&laquo; Prev</a>
  {% endif %}
  
  {% for page in (1..paginator.total_pages) %}
    {% if page == paginator.page %}
      <span class="current-page">{{ page }}</span>
    {% else %}
      <a href="{% if page == 1 %}{{ '/blog/' | relative_url }}{% else %}{{ site.paginate_path | relative_url | replace: ':num', page }}{% endif %}">{{ page }}</a>
    {% endif %}
  {% endfor %}
  
  {% if paginator.next_page %}
    <a href="{{ paginator.next_page_path | relative_url }}">Next &raquo;</a>
  {% endif %}
</div>
{% endif %}
```

## Project Blog Integration

Project blogs are integrated through:

1. Project-specific blog directories: `projects/[project-name]/_posts/`
2. Category-based filtering: `{% include blog_list.html category=page.category %}`
3. Consistent styling through shared CSS classes

### Project Blog Structure

```
projects/
├── Project1/
│   ├── _drafts/
│   │   └── template-blog-entry.md
│   └── _posts/
│       └── YYYY-MM-DD-project1-title.md
```

## Troubleshooting

### Post Title Not Displaying

Check that:
- The post has proper frontmatter with a title
- The layout is using `page.title` (not `post.title`)
- There are no Liquid syntax errors in the template

### Pagination Not Working

Ensure that:
- The template file is HTML (not Markdown)
- Pagination is enabled in `_config.yml`
- The paginator object is being used correctly

### Blog List Not Showing Posts

Verify that:
- Posts have the correct category/tag if filtering is used
- Posts have proper frontmatter
- Posts are in the correct directory
- Posts have a future date if `future: false` is set in config 