## genmd Settings

| Variable               | Value                                                                 |
|------------------------|-----------------------------------------------------------------------|
| GENMD_FILE_EXCLUDES | *.JPG |
| GENMD_DIR_EXCLUDES | .git |
| GENMD_PATTERN_EXCLUDES |  |
| GENMD_FILE_INCLUDES | css |
| GENMD_BASE | /Users/mps/projects/AI-PROJECTS/DTS-WebSite/unixwzrd.github.io |
| output_filename | /Users/mps/projects/AI-PROJECTS/DTS-WebSite/unixwzrd.github.io/utils/output/my_test_file.md |
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
│   ├── about/
│   │   ├── resume.md
│   │   └── sullivan-michael-creds.md
│   ├── about.md
│   ├── android-chrome-192x192.png
│   ├── android-chrome-512x512.png
│   ├── apple-touch-icon.png
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
│   │   │   └── SullivanMichael_IT_AI_ML_Unix_42020819.pdf
│   │   ├── icons/
│   │   ├── images/
│   │   │   ├── IMG_1887.JPG
│   │   │   ├── child-with-robot.png
│   │   │   ├── child-with-robot.webp
│   │   │   └── some-image.webp
│   │   └── minima-social-icons.liquid
│   ├── blog.md
│   ├── collaborate/
│   │   ├── community.md
│   │   └── professional.md
│   ├── collaborate.md
│   ├── contact.md
│   ├── faq.md
│   ├── favicon-16x16.png
│   ├── favicon-32x32.png
│   ├── favicon.ico
│   ├── hidden/
│   │   └── sitemap.md
│   ├── index.md
│   ├── projects.md
│   ├── resources/
│   │   └── emergency-resources.md
│   ├── resources.md
│   ├── robots.txt
│   └── site.webmanifest
├── new_files/
│   ├── _layouts/
│   └── assets/
│       └── css/
│           ├── _base.scss
│           ├── _components.scss
│           ├── _layout.scss
│           ├── _overrides.scss
│           ├── _variables.scss
│           └── style.scss
└── outfile.txt

```


## Filename ==>  ./html/assets/css/_base.scss
```scss
// assets/css/_base.scss

body {
  color: $text-color;
  background-color: $background-color;
}

a {
  color: $link-color;
  text-decoration: none;
}

.wrapper {
  margin: 0 auto;
  max-width: $wrapper-max-width;
  padding: $wrapper-padding;
}

// Highlighter Rouge Overrides
.highlighter-rouge {
  .highlight pre {
    background: $code-background;
  }
  pre,
  code {
    background: $code-background;
  }
}
```


## Filename ==>  ./html/assets/css/_components.scss
```scss
// assets/css/_components.scss

// Blockquote Styling
blockquote {
  color: #60c0ee !important;
  background: #000000;
  border-left-color: #5592b4;
}

// Table Styling
table {
  border: 1px solid $border-color;

  th {
    background-color: $header-color !important;
    border: 1px solid $border-color;
    font-weight: bold !important;
    padding: 12px;
  }

  tr {
    border: 1px;
  }

  td {
    border: 1px solid $border-color;
    padding: 12px;
  }

  // Odd and Even Row Backgrounds
  .odd td {
    background-color: $odd-row-color;
  }
  .even td {
    background-color: $even-row-color;
  }

  // Cell Border Adjustments
  td:empty {
    border-top: none;
    border-bottom: none;
  }
  td:first-child {
    border-bottom: none;
  }
  tr:last-of-type td:first-child:not(:empty) {
    border-bottom: 1px;
  }
}

// Code Blocks
pre,
code {
  background: $code-background;
}

// Post Styling
.post {
  h3 {
    font-size: $h3-font-size;
    line-height: 1.2;
    margin-bottom: 0rem;
    margin-top: 0.2rem;
  }

  .post-date {
    font-size: $post-date-font-size;
    color: #aaaaaa;
    display: inline-block;
    margin-bottom: 0.5rem;
  }

  .post-excerpt {
    margin-left: 10px;
    margin-bottom: 0.2rem;
  }

  .p {
    font-size: 1.1rem;
    line-height: 1.5rem;
    margin-bottom: 1.2rem;
  }

  .btn {
    margin-top: 0.0rem;
    margin-bottom: 1.0rem;
    display: inline-block;
    font-size: $btn-font-size;
  }
}

// Project Components
.project-table {
  width: 100%;
  margin-bottom: 20px;
  border-spacing: 20px;
  border: none !important;
  padding: 5px;
}

.project-image {
  width: 50%;
  vertical-align: top;
  border: none !important;
  padding-left: none !important;
}

.project-preview {
  width: 100%;
  height: auto;
  max-height: 150px;
  object-fit: cover;
  border-radius: 0 !important;
  border: none !important;
}

.project-details {
  width: 50%;
  vertical-align: top;
  padding-left: 10px;
  padding-top: 0px !important;
  margin-top: 0px !important;
  border: none !important;
}

.project-details h2 {
  font-size: $project-details-h2-font-size;
  margin-bottom: 10px;
  margin-top: 0 !important;
}

.github-link,
.project-blog-link {
  font-size: 1rem;
  color: $link-color;
  text-decoration: none;
  padding: 5px;
}

// Links Row
.links-row {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

// Obfuscated Email Link
#obfuscated-email a {
  color: #0000CC;
  text-decoration: underline;
}

#contact-link {
  cursor: pointer;
}

.social-icons {
  display: flex;
  gap: 10px; // Space between icons
  align-items: center;

  img {
    width: 24px; // Adjust size as needed
    height: 24px;
    transition: transform 0.3s;

    &:hover {
      transform: scale(1.1); // Slight zoom on hover
    }
  }
}
```


## Filename ==>  ./html/assets/css/_layout.scss
```scss
// assets/css/_layout.scss

// Header and Site Title
.header,
.site-title,
.site-header {
  color: $text-color !important;
  background: $header-background !important;
}

.site-header {
  border-top: 1px !important;
}

// Brand Graphic Styling
.brand-graphic {
  width: $brand-graphic-width;
  height: auto;
  margin-right: $brand-graphic-margin-right;
  vertical-align: middle;
}
```


## Filename ==>  ./html/assets/css/_overrides.scss
```scss
// assets/css/_overrides.scss

@media (prefers-color-scheme: dark) {
  // Import Monokai Theme for Syntax Highlighting
  @import "mineokai";

  // Override Body Styles
  body {
    color: $text-color !important;
    background-color: $background-color !important;
  }

  // Header and Site Title
  .header,
  .site-title,
  .site-header {
    color: $text-color !important;
    background: $header-background !important;
  }

  // Blockquote Styling
  blockquote {
    color: #60c0ee !important;
    background: #000000;
    border-left-color: #5592b4;
  }

  // Code Blocks
  pre,
  code {
    background: $code-background;
  }

  // Highlighter Rouge Overrides (Repeated for Dark Mode)
  .highlighter-rouge {
    .highlight pre {
      background: $code-background;
    }
    pre,
    code {
      background: $code-background;
    }
  }
}
```


## Filename ==>  ./html/assets/css/_variables.scss
```scss
// assets/css/_variables.scss

// Color Variables
$primary-color: #00fcbb;
$secondary-color: #66d9ef;
$text-color: #cacaca;
$background-color: #141414;
$header-background: #141414;
$link-color: #00f;
$border-color: #cacaca;

// Table Colors
$header-color: #000040;
$odd-row-color: darken($header-color, 5%);
$even-row-color: lighten($header-color, 2%);

// Dimensions
$brand-graphic-width: 45px;
$brand-graphic-margin-right: 20px;
$wrapper-max-width: 900px;
$wrapper-padding: 20px;

// Font Sizes
$h3-font-size: 1.5rem;
$post-date-font-size: 0.9rem;
$btn-font-size: 0.9rem;
$project-details-h2-font-size: 1.6rem;

// Other Variables
$code-background: #000000;
```


## Filename ==>  ./html/assets/css/mineokai.scss
```scss

.highlight .bp { color: #7799ff } /* Name.Builtin.Pseudo */
.highlight .c { color: #008800; font-style: italic } /* Comment */
.highlight .c1 { color: #008800; font-style: italic } /* Comment.Single */
.highlight .ch { color: #8b949e; font-style: italic } /* Comment.Hashbang */
.highlight .cm { color: #008800; font-style: italic } /* Comment.Multiline */
.highlight .cp { color: #008800; font-style: italic } /* Comment.Preproc */
.highlight .cpf { color: #8b949e; font-style: italic } /* Comment.PreprocFile */
.highlight .cs { color: #008800; font-style: italic } /* Comment.Special */
.highlight .dl { color: #79c0ff } /* Literal.String.Delimiter */
.highlight .err { color: #960050; background-color: #1e0010 } /* Error */
.highlight .esc { color: #e6edf3 } /* Escape */
.highlight .fm { color: #d2a8ff; font-weight: bold } /* Name.Function.Magic */
.highlight .g { color: #e6edf3 } /* Generic */
.highlight .g-Underline { color: #e6edf3; text-decoration: underline } /* Generic.Underline */
.highlight .gd { color: #f92672; } /* Generic.Deleted & Diff Deleted */
.highlight .ge { font-weight: bold; font-style: italic } /* Generic.Emph */
.highlight .ges { color: #e6edf3; font-weight: bold; font-style: italic } /* Generic.EmphStrong */
.highlight .gh {color: #79c0ff; font-weight: bold } /* Generic Heading & Diff Header */
.highlight .gi { color: #a6e22e } /* Generic.Inserted & Diff Inserted */
.highlight .go { color: #8b949e } /* Generic.Output */
.highlight .gp { color: #8b949e } /* Generic.Prompt & Diff Changed */
.highlight .gr { color: #ffa198 } /* Generic.Error */
.highlight .gs { font-weight: bold } /* Generic.Strong */
.highlight .gt { color: #ff7b72 } /* Generic.Traceback */
.highlight .gu { color: #75715e; } /* Generic.Subheading & Diff Unified/Comment? */
.highlight .hll { background-color: #272822; }
.highlight .il { color: #ae81ff } /* Literal.Number.Integer.Long */
.highlight .k { color: #66aadd } /* Keyword */
.highlight .kc { color: #66d9ef } /* Keyword.Constant */
.highlight .kd { color: #66d9ef } /* Keyword.Declaration */
.highlight .kn { color: #ee80cc } /* Keyword.Namespace */
.highlight .kp { color: #66d9ef } /* Keyword.Pseudo */
.highlight .kr { color: #66d9ef } /* Keyword.Reserved */
.highlight .kt { color: #66d9ef } /* Keyword.Type */
.highlight .l { color: #ae81ff } /* Literal */
.highlight .ld { color: #e6db74 } /* Literal.Date */
.highlight .m { color: #ae81ff } /* Literal.Number */
.highlight .mb { color: #a5d6ff } /* Literal.Number.Bin */
.highlight .mf { color: #ae81ff } /* Literal.Number.Float */
.highlight .mh { color: #ae81ff } /* Literal.Number.Hex */
.highlight .mi { color: #ffff00 } /* Literal.Number.Integer */
.highlight .mo { color: #ae81ff } /* Literal.Number.Oct */
.highlight .n { color: #00fcbb } /* Name */
.highlight .na { color: #a6e22e } /* Name.Attribute */
.highlight .nb { color: #88ddee } /* Name.Builtin */
.highlight .nc { color: #88ff88 } /* Name.Class */
.highlight .nd { color: #a6e22e } /* Name.Decorator */
.highlight .ne { color: #a6e22e } /* Name.Exception */
.highlight .nf { color: #a6e22e } /* Name.Function */
.highlight .ni { color: #f8f8f2 } /* Name.Entity */
.highlight .nl { color: #f8f8f2 } /* Name.Label */
.highlight .nn { color: #f8f8f2 } /* Name.Namespace */
.highlight .no { color: #66d9ef } /* Name.Constant */
.highlight .nt { color: #f92672 } /* Name.Tag */
.highlight .nv { color: #f8f8f2 } /* Name.Variable */
.highlight .nx { color: #a6e22e } /* Name.Other */
.highlight .o { color: #ffff00 } /* Operator */
.highlight .ow { color: #dd8866 } /* Operator.Word */
.highlight .p { color: #ffff00 } /* Punctuation */
.highlight .pm { color: #e6edf3 } /* Punctuation.Marker */
.highlight .py { color: #f8f8f2 } /* Name.Property */
.highlight .s { color: #e6db74 } /* Literal.String */
.highlight .s1 { color: #e6db74 } /* Literal.String.Single */
.highlight .s2 { color: #e6db74 } /* Literal.String.Double */
.highlight .sa { color: #79c0ff } /* Literal.String.Affix */
.highlight .sb { color: #e6db74 } /* Literal.String.Backtick */
.highlight .sc { color: #e6db74 } /* Literal.String.Char */
.highlight .sd { color: #e6db74 } /* Literal.String.Doc */
.highlight .se { color: #ae81ff } /* Literal.String.Escape */
.highlight .sh { color: #e6db74 } /* Literal.String.Heredoc */
.highlight .si { color: #e6db74 } /* Literal.String.Interpol */
.highlight .sr { color: #e6db74 } /* Literal.String.Regex */
.highlight .ss { color: #e6db74 } /* Literal.String.Symbol */
.highlight .sx { color: #e6db74 } /* Literal.String.Other */
.highlight .vc { color: #f8f8f2 } /* Name.Variable.Class */
.highlight .vg { color: #f8f8f2 } /* Name.Variable.Global */
.highlight .vi { color: #f8f8f2 } /* Name.Variable.Instance */
.highlight .vm { color: #79c0ff } /* Name.Variable.Magic */
.highlight .w { color: #f8f8f2 } /* Text.Whitespace */
.highlight .x { color: #e6edf3 } /* Other */
```


## Filename ==>  ./html/assets/css/monokai.scss
```scss
.highlight pre { background-color: #272822; }
.highlight .hll { background-color: #272822; }
.highlight .c { color: #75715e } /* Comment */
.highlight .err { color: #960050; background-color: #1e0010 } /* Error */
.highlight .k { color: #66d9ef } /* Keyword */
.highlight .l { color: #ae81ff } /* Literal */
.highlight .n { color: #f8f8f2 } /* Name */
.highlight .o { color: #f92672 } /* Operator */
.highlight .p { color: #f8f8f2 } /* Punctuation */
.highlight .cm { color: #75715e } /* Comment.Multiline */
.highlight .cp { color: #75715e } /* Comment.Preproc */
.highlight .c1 { color: #75715e } /* Comment.Single */
.highlight .cs { color: #75715e } /* Comment.Special */
.highlight .ge { font-style: italic } /* Generic.Emph */
.highlight .gs { font-weight: bold } /* Generic.Strong */
.highlight .kc { color: #66d9ef } /* Keyword.Constant */
.highlight .kd { color: #66d9ef } /* Keyword.Declaration */
.highlight .kn { color: #f92672 } /* Keyword.Namespace */
.highlight .kp { color: #66d9ef } /* Keyword.Pseudo */
.highlight .kr { color: #66d9ef } /* Keyword.Reserved */
.highlight .kt { color: #66d9ef } /* Keyword.Type */
.highlight .ld { color: #e6db74 } /* Literal.Date */
.highlight .m { color: #ae81ff } /* Literal.Number */
.highlight .s { color: #e6db74 } /* Literal.String */
.highlight .na { color: #a6e22e } /* Name.Attribute */
.highlight .nb { color: #f8f8f2 } /* Name.Builtin */
.highlight .nc { color: #a6e22e } /* Name.Class */
.highlight .no { color: #66d9ef } /* Name.Constant */
.highlight .nd { color: #a6e22e } /* Name.Decorator */
.highlight .ni { color: #f8f8f2 } /* Name.Entity */
.highlight .ne { color: #a6e22e } /* Name.Exception */
.highlight .nf { color: #a6e22e } /* Name.Function */
.highlight .nl { color: #f8f8f2 } /* Name.Label */
.highlight .nn { color: #f8f8f2 } /* Name.Namespace */
.highlight .nx { color: #a6e22e } /* Name.Other */
.highlight .py { color: #f8f8f2 } /* Name.Property */
.highlight .nt { color: #f92672 } /* Name.Tag */
.highlight .nv { color: #f8f8f2 } /* Name.Variable */
.highlight .ow { color: #f92672 } /* Operator.Word */
.highlight .w { color: #f8f8f2 } /* Text.Whitespace */
.highlight .mf { color: #ae81ff } /* Literal.Number.Float */
.highlight .mh { color: #ae81ff } /* Literal.Number.Hex */
.highlight .mi { color: #ae81ff } /* Literal.Number.Integer */
.highlight .mo { color: #ae81ff } /* Literal.Number.Oct */
.highlight .sb { color: #e6db74 } /* Literal.String.Backtick */
.highlight .sc { color: #e6db74 } /* Literal.String.Char */
.highlight .sd { color: #e6db74 } /* Literal.String.Doc */
.highlight .s2 { color: #e6db74 } /* Literal.String.Double */
.highlight .se { color: #ae81ff } /* Literal.String.Escape */
.highlight .sh { color: #e6db74 } /* Literal.String.Heredoc */
.highlight .si { color: #e6db74 } /* Literal.String.Interpol */
.highlight .sx { color: #e6db74 } /* Literal.String.Other */
.highlight .sr { color: #e6db74 } /* Literal.String.Regex */
.highlight .s1 { color: #e6db74 } /* Literal.String.Single */
.highlight .ss { color: #e6db74 } /* Literal.String.Symbol */
.highlight .bp { color: #f8f8f2 } /* Name.Builtin.Pseudo */
.highlight .vc { color: #f8f8f2 } /* Name.Variable.Class */
.highlight .vg { color: #f8f8f2 } /* Name.Variable.Global */
.highlight .vi { color: #f8f8f2 } /* Name.Variable.Instance */
.highlight .il { color: #ae81ff } /* Literal.Number.Integer.Long */

.highlight .gh { } /* Generic Heading & Diff Header */
.highlight .gu { color: #75715e; } /* Generic.Subheading & Diff Unified/Comment? */
.highlight .gd { color: #f92672; } /* Generic.Deleted & Diff Deleted */
.highlight .gi { color: #a6e22e; } /* Generic.Inserted & Diff Inserted */
```


## Filename ==>  ./html/assets/css/style.scss
```scss
// assets/css/style.scss
---
---
@import
  "minima/skins/{{ site.minima.skin | default: 'auto' }}",
  "minima/initialize",
  "variables",
  "base",
  "layout",
  "components",
  "overrides";
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


## Filename ==>  ./new_files/assets/css/_base.scss
```scss
// assets/css/_base.scss

body {
  color: $text-color;
  background-color: $background-color;
}

a {
  color: $link-color;
  text-decoration: none;
}

.wrapper {
  margin: 0 auto;
  max-width: $wrapper-max-width;
  padding: $wrapper-padding;
}

// Highlighter Rouge Overrides
.highlighter-rouge {
  .highlight pre {
    background: $code-background;
  }
  pre,
  code {
    background: $code-background;
  }
}
```


## Filename ==>  ./new_files/assets/css/_components.scss
```scss
// assets/css/_components.scss

// Blockquote Styling
blockquote {
  color: #60c0ee !important;
  background: #000000;
  border-left-color: #5592b4;
}

// Table Styling
table {
  border: 1px solid $border-color;

  th {
    background-color: $header-color !important;
    border: 1px solid $border-color;
    font-weight: bold !important;
    padding: 12px;
  }

  tr {
    border: 1px;
  }

  td {
    border: 1px solid $border-color;
    padding: 12px;
  }

  // Odd and Even Row Backgrounds
  .odd td {
    background-color: $odd-row-color;
  }
  .even td {
    background-color: $even-row-color;
  }

  // Cell Border Adjustments
  td:empty {
    border-top: none;
    border-bottom: none;
  }
  td:first-child {
    border-bottom: none;
  }
  tr:last-of-type td:first-child:not(:empty) {
    border-bottom: 1px;
  }
}

// Code Blocks
pre,
code {
  background: $code-background;
}

// Post Styling
.post {
  h3 {
    font-size: $h3-font-size;
    line-height: 1.2;
    margin-bottom: 0rem;
    margin-top: 0.2rem;
  }

  .post-date {
    font-size: $post-date-font-size;
    color: #aaaaaa;
    display: inline-block;
    margin-bottom: 0.5rem;
  }

  .post-excerpt {
    margin-left: 10px;
    margin-bottom: 0.2rem;
  }

  .p {
    font-size: 1.1rem;
    line-height: 1.5rem;
    margin-bottom: 1.2rem;
  }

  .btn {
    margin-top: 0.0rem;
    margin-bottom: 1.0rem;
    display: inline-block;
    font-size: $btn-font-size;
  }
}

// Project Components
.project-table {
  width: 100%;
  margin-bottom: 20px;
  border-spacing: 20px;
  border: none !important;
  padding: 5px;
}

.project-image {
  width: 50%;
  vertical-align: top;
  border: none !important;
  padding-left: none !important;
}

.project-preview {
  width: 100%;
  height: auto;
  max-height: 150px;
  object-fit: cover;
  border-radius: 0 !important;
  border: none !important;
}

.project-details {
  width: 50%;
  vertical-align: top;
  padding-left: 10px;
  padding-top: 0px !important;
  margin-top: 0px !important;
  border: none !important;
}

.project-details h2 {
  font-size: $project-details-h2-font-size;
  margin-bottom: 10px;
  margin-top: 0 !important;
}

.github-link,
.project-blog-link {
  font-size: 1rem;
  color: $link-color;
  text-decoration: none;
  padding: 5px;
}

// Links Row
.links-row {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

// Obfuscated Email Link
#obfuscated-email a {
  color: #0000CC;
  text-decoration: underline;
}

#contact-link {
  cursor: pointer;
}
```


## Filename ==>  ./new_files/assets/css/_layout.scss
```scss
// assets/css/_layout.scss

// Header and Site Title
.header,
.site-title,
.site-header {
  color: $text-color !important;
  background: $header-background !important;
}

.site-header {
  border-top: 1px !important;
}

// Wrapper Adjustments
.wrapper {
  margin-left: 80px auto;
  margin-right: 80px auto;
  max-width: $wrapper-max-width;
  padding: $wrapper-padding;
}

// Brand Graphic Styling
.brand-graphic {
  width: $brand-graphic-width;
  height: auto;
  margin-right: $brand-graphic-margin-right;
  vertical-align: middle;
}
```


## Filename ==>  ./new_files/assets/css/_overrides.scss
```scss
// assets/css/_overrides.scss

@media (prefers-color-scheme: dark) {
  // Import Monokai Theme for Syntax Highlighting
  @import "mineokai";

  // Override Body Styles
  body {
    color: $text-color !important;
    background-color: $background-color !important;
  }

  // Header and Site Title
  .header,
  .site-title,
  .site-header {
    color: $text-color !important;
    background: $header-background !important;
  }

  // Blockquote Styling
  blockquote {
    color: #60c0ee !important;
    background: #000000;
    border-left-color: #5592b4;
  }

  // Code Blocks
  pre,
  code {
    background: $code-background;
  }

  // Highlighter Rouge Overrides (Repeated for Dark Mode)
  .highlighter-rouge {
    .highlight pre {
      background: $code-background;
    }
    pre,
    code {
      background: $code-background;
    }
  }
}
```


## Filename ==>  ./new_files/assets/css/_variables.scss
```scss
// assets/css/_variables.scss

// Color Variables
$primary-color: #00fcbb;
$secondary-color: #66d9ef;
$text-color: #cacaca;
$background-color: #141414;
$header-background: #141414;
$link-color: #00f;
$border-color: #cacaca;

// Table Colors
$header-color: #000040;
$odd-row-color: darken($header-color, 5%);
$even-row-color: lighten($header-color, 2%);

// Dimensions
$brand-graphic-width: 45px;
$brand-graphic-margin-right: 20px;
$wrapper-max-width: 900px;
$wrapper-padding: 20px;

// Font Sizes
$h3-font-size: 1.5rem;
$post-date-font-size: 0.9rem;
$btn-font-size: 0.9rem;
$project-details-h2-font-size: 1.6rem;

// Other Variables
$code-background: #000000;
```


## Filename ==>  ./new_files/assets/css/style.scss
```scss
// assets/css/style.scss

---
---

@import
  "minima/skins/{{ site.minima.skin | default: 'auto' }}",
  "minima/initialize",
  "variables",
  "base",
  "layout",
  "components",
  "overrides";
```
