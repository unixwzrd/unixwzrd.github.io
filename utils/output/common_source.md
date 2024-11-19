## genmd Settings

| Variable               | Value                                                                 |
|------------------------|-----------------------------------------------------------------------|
| GENMD_FILE_EXCLUDES | *.ico *.svg *.png *.pdf *.jpg *.htaccess *.webp *.jekyll .DS_Store combined_source.md *.JPG professional.md *.png |
| GENMD_DIR_EXCLUDES | tmp .git _site .jekyll new_files _includes |
| GENMD_PATTERN_EXCLUDES |  |
| GENMD_FILE_INCLUDES |  |
| GENMD_BASE | /Users/mps/projects/AI-PROJECTS/DTS-WebSite/unixwzrd.github.io |
| output_filename | /Users/mps/projects/AI-PROJECTS/DTS-WebSite/unixwzrd.github.io/utils/output/common_source.md |
| dry_run | false |
| debug_level | 4 |
| verbose | false |



## Project filesystem directory structure
```text
Root Directory
├── CNAME
├── Gemfile
├── Gemfile.lock
├── _config.yml
├── file_layout.txt
├── genmd_env.sh
├── html/
│   ├── 404.html
│   ├── _data/
│   │   ├── countries.yml
│   │   ├── github_projects.yml
│   │   └── repos.yml
│   ├── _drafts/
│   ├── _layouts/
│   │   ├── blog.html
│   │   ├── home.html
│   │   ├── page.html
│   │   ├── post.html
│   │   └── project.html
│   ├── _pages/
│   ├── _plugins/
│   │   └── remove_headings_filter.rb
│   ├── _posts/
│   │   ├── 2024-08-16-Testing-markdown-formatting-with-our-changes.md
│   │   ├── 2024-09-02-AI-Coding-Assistants.md
│   │   └── 2024-09-27-Building-This-Site-With-AI.md
│   ├── about/
│   │   ├── resume.md
│   │   └── sullivan-michael-creds.md
│   ├── about.md
│   ├── assets/
│   │   ├── css/
│   │   │   ├── _base.scss
│   │   │   ├── _components.scss
│   │   │   ├── _layout.scss
│   │   │   ├── _overrides.scss
│   │   │   ├── _variables.scss
│   │   │   ├── mineokai.scss
│   │   │   ├── monokai.scss
│   │   │   └── style.scss
│   │   ├── documents/
│   │   ├── icons/
│   │   ├── images/
│   │   │   └── projects/
│   │   ├── js/
│   │   │   └── email-obfuscation.js
│   │   └── minima-social-icons.liquid
│   ├── blog.md
│   ├── collaborate/
│   │   └── community.md
│   ├── collaborate.md
│   ├── contact.md
│   ├── faq.md
│   ├── hidden/
│   │   └── sitemap.md
│   ├── index.md
│   ├── projects/
│   │   ├── TokenSecure/
│   │   │   └── TokenSecure-project-blog-entry.md
│   │   ├── TokenSecure.md
│   │   ├── TorchDevice/
│   │   │   └── TorchDevice-project-blog-entry.md
│   │   ├── TorchDevice.md
│   │   ├── oobabooga-macOS/
│   │   │   └── oobabooga-macOS-project-blog-entry.md
│   │   ├── oobabooga-macOS.md
│   │   ├── text-generation-webui-macos/
│   │   │   └── text-generation-webui-macos-project-blog-entry.md
│   │   ├── text-generation-webui-macos.md
│   │   ├── venvutil/
│   │   │   └── venvutil-project-blog-entry.md
│   │   └── venvutil.md
│   ├── projects.md
│   ├── resources/
│   │   └── emergency-resources.md
│   ├── resources.md
│   ├── robots.txt
│   └── site.webmanifest
└── utils/
    ├── bin/
    │   ├── fetch_og_data.py
    │   ├── jekyll-service
    │   ├── push-social-media
    │   ├── push-twitter
    │   ├── screenscraper.py
    │   └── update_structure.sh
    ├── etc/
    │   ├── combined_source.grc
    │   └── jekyll.pid
    └── output/
        └── common_source.md

```


## Filename ==>  ./html/assets/minima-social-icons.liquid
```text
---
permalink: /assets/minima-social-icons.svg
layout: none
---

<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
{% comment %}
  Iterate through {{ site.minima.social_links }} and render platform related SVG-symbol
  unless the platform is "rss" because we need the "rss" symbol for the `Subscribe` link
  in the footer and therefore inject the "rss" icon outside the iteration loop.
{% endcomment %}
{% for entry in site.minima.social_links %}
  {%- assign symbol_id = entry.platform -%}
  {%- unless symbol_id == "rss" -%}
    {%- include svg_symbol.html key = symbol_id -%}
  {% endunless %}
{%- endfor -%}
  {%- include svg_symbol.html key = "rss" -%}
</svg>

```


## Filename ==>  ./utils/bin/push-social-media
```bash
#!/usr/bin/env bash

# Source tokens and credentials
if [ -f ~/.tokens/tokens.txt ]; then
  source ~/.tokens/tokens.txt
fi

# Define the social media services you're using
services=("twitter" "linkedin" "reddit")

# Loop through the services and execute their individual posting scripts
for service in "${services[@]}"; do
  if [ -f "./social_media/${service}_post.sh" ]; then
    bash "./social_media/${service}_post.sh"
  else
    echo "No script found for $service"
  fi
done
```
