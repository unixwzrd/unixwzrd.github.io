# Blog Listing & Pagination

[← Back to Site Operations Guide](site-operations.md)

- [Blog Listing \& Pagination](#blog-listing--pagination)
  - [Configuration](#configuration)
  - [Excerpt \& Image Handling](#excerpt--image-handling)
  - [Client-Side Pagination](#client-side-pagination)
  - [Styling](#styling)

This section covers how blog listings and pagination work, including configuration, customization, and client-side navigation.

## Blog Listing & Pagination
- The main blog page now lists all posts (main + project) with unified styling.
- Blog and project blog post limits are configurable in `_config.yml` (`site_blogs_count`, `project_blog_count`) and can be overridden in page front matter.
- Excerpts are auto-generated from post content, strip images, and are truncated to a configurable word count (`excerpt_word_limit`).
- Pagination is handled client-side via JavaScript and Liquid, not by Jekyll's built-in `paginate` feature. The number of posts per page is configurable, and navigation is smooth with URL updates (e.g., `?page=2`).
- Pagination controls are styled for dark backgrounds and accessibility.

### Configuration
- Set `site_blogs_count` and `project_blog_count` in `_config.yml` to control the number of posts per page for the main blog and project blogs.
- Set `excerpt_word_limit` in `_config.yml` to control the number of words in each excerpt.
- You can override these values in the front matter of individual pages.

### Excerpt & Image Handling
- Excerpts are generated from the first part of the post content.
- All image tags (Markdown and HTML) are stripped from excerpts.
- Excerpts are truncated to the configured word limit.

### Client-Side Pagination
- Pagination is implemented with JavaScript and Liquid.
- The page number is reflected in the URL as `?page=2`.
- Navigation is smooth and does not reload the page.

### Styling
- Pagination controls are styled for dark backgrounds.
- Buttons and page info are spaced and accessible. 