

## Project filesystem directory structure
```text
Root Directory
├── CNAME
├── Gemfile
├── Gemfile.lock
├── _config.yml
├── errout.txt
├── file_layout.txt
├── genmd_env.sh
├── histfile.txt.xz
├── html/
│   ├── 404.html
│   ├── _data/
│   │   ├── countries.yml
│   │   ├── github_projects.yml
│   │   └── repos.yml
│   ├── _drafts/
│   ├── _includes/
│   │   ├── codeium_stats.html
│   │   ├── custom-head.html
│   │   ├── disclaimer.html
│   │   ├── footer.html
│   │   ├── getintouch.html
│   │   ├── head.html
│   │   ├── header.html
│   │   ├── join_us.html
│   │   ├── navigation.html
│   │   ├── projects/
│   │   │   ├── TokenSecure.html
│   │   │   ├── TorchDevice.html
│   │   │   ├── oobabooga-macOS.html
│   │   │   ├── text-generation-webui-macos.html
│   │   │   └── venvutil.html
│   │   ├── projects_list.html
│   │   ├── rss_feed_sub.html
│   │   ├── social-icons/
│   │   │   ├── amazon-pay-svgrepo-com.svg
│   │   │   ├── amazon.svg
│   │   │   ├── amazonpay.svg
│   │   │   ├── apple-alt-svgrepo-com.svg
│   │   │   ├── apple-pay-svgrepo-com.svg
│   │   │   ├── apple-svgrepo-com.svg
│   │   │   ├── apple.svg
│   │   │   ├── applepay.svg
│   │   │   ├── bitcoin-2.svg
│   │   │   ├── bitcoin-svgrepo-com.svg
│   │   │   ├── bitcoin.png
│   │   │   ├── bitcoin.svg
│   │   │   ├── buymeacoffee.svg
│   │   │   ├── cocos.svg
│   │   │   ├── codeium.svg
│   │   │   ├── creativecommons.svg
│   │   │   ├── devdotto.svg
│   │   │   ├── devto.svg
│   │   │   ├── discord.svg
│   │   │   ├── disqus.svg
│   │   │   ├── dribbble.svg
│   │   │   ├── facebook.svg
│   │   │   ├── flickr.svg
│   │   │   ├── geeksforgeeks.svg
│   │   │   ├── git.svg
│   │   │   ├── github.svg
│   │   │   ├── githubpages.svg
│   │   │   ├── gitlab.svg
│   │   │   ├── godaddy.svg
│   │   │   ├── google_scholar.svg
│   │   │   ├── huggingface.svg
│   │   │   ├── instagram.svg
│   │   │   ├── ios.svg
│   │   │   ├── jekyll.svg
│   │   │   ├── jupyter.svg
│   │   │   ├── keybase.svg
│   │   │   ├── linkedin-svgrepo-com.svg
│   │   │   ├── linkedin.svg
│   │   │   ├── linux.svg
│   │   │   ├── macos.svg
│   │   │   ├── mastodon.svg
│   │   │   ├── medium.png
│   │   │   ├── medium.svg
│   │   │   ├── meta.svg
│   │   │   ├── microdotblog.svg
│   │   │   ├── numpy.svg
│   │   │   ├── openai.svg
│   │   │   ├── opensourceinitiative.svg
│   │   │   ├── pandas.svg
│   │   │   ├── patreon-2.svg
│   │   │   ├── patreon.png
│   │   │   ├── patreon.svg
│   │   │   ├── paypal-1-svgrepo-com.svg
│   │   │   ├── paypal-svgrepo-com.svg
│   │   │   ├── paypal.svg
│   │   │   ├── pinterest.svg
│   │   │   ├── python.svg
│   │   │   ├── pytorch.svg
│   │   │   ├── ray.svg
│   │   │   ├── react.svg
│   │   │   ├── rss.svg
│   │   │   ├── ruby.svg
│   │   │   ├── scipy.svg
│   │   │   ├── snapchat.svg
│   │   │   ├── sourceforge.svg
│   │   │   ├── square.svg
│   │   │   ├── stackoverflow.svg
│   │   │   ├── stripe-svgrepo-com-2.svg
│   │   │   ├── stripe-svgrepo-com.svg
│   │   │   ├── telegram.svg
│   │   │   ├── tensorflow.svg
│   │   │   ├── twitter-bird-svgrepo-com.svg
│   │   │   ├── twitter-svgrepo-com.svg
│   │   │   ├── twitter.svg
│   │   │   ├── wandb.svg
│   │   │   └── youtube.svg
│   │   ├── social-item.html
│   │   ├── social.html
│   │   ├── svg_symbol.html
│   │   └── wand_accred.html
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
│   │   │   ├── projects/
│   │   │   │   ├── TokenSecure.png
│   │   │   │   ├── TorchDevice.png
│   │   │   │   ├── oobabooga-macOS.png
│   │   │   │   ├── text-generation-webui-macos.png
│   │   │   │   └── venvutil.png
│   │   │   └── some-image.webp
│   │   ├── js/
│   │   │   └── email-obfuscation.js
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
└── outfile.txt

```


## Filename ==>  ./html/404.html
```html
     1	---
     2	permalink: /404.html
     3	layout: page
     4	---
     5	<style type="text/css" media="screen">
     6	  .container {
     7	    margin: 10px auto;
     8	    max-width: 600px;
     9	    text-align: center;
    10	  }
    11	  h1 {
    12	    margin: 30px 0;
    13	    font-size: 4em;
    14	    line-height: 1;
    15	    letter-spacing: -1px;
    16	  }
    17	</style>
    18	<div class="container">
    19	  <h1>404</h1>
    20	  <h2><strong>Page not found 🤷</strong></h2>
    21	  <p>The requested page could not be found.</p>
    22	  <p><b>If you're in crisis, please visit our <a href="emergency-resources">Emergency Resources</a> page for immediate help.</b></p>
    23	</div>

```


## Filename ==>  ./html/_includes/codeium_stats.html
```html
     1	### Codeium Statistics
     2	Follow the link to see my public Codeium profile.
     3	<div class="codeium-stats">
     4	    <a href="https://codeium.com/profile/unixwzrd" target="_blank"><img src="https://codeium.com/profile/unixwzrd/card.png" alt="My Codeium Profile With Statistics" title="My Codeium" /></a>
     5	  </div>

```


## Filename ==>  ./html/_includes/custom-head.html
```html
     1	<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
     2	<link rel="apple-touch-icon" sizes="180x180" href="/favicon-32x32.png">
     3	<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
     4	<link rel="manifest" href="/site.webmanifest">

```


## Filename ==>  ./html/_includes/disclaimer.html
```html
     1	<p class="disclaimer">
     2	    <br>
     3	    <strong>Disclaimer:</strong> The information on this website is for general informational purposes only. Distributed Thinking Systems makes no representations or warranties about the accuracy or completeness of any content. All use of our site and services is at your own risk. <br>
     4	    For any legal advice, please contact a licensed attorney.
     5	  </p>

```


## Filename ==>  ./html/_includes/footer.html
```html
     1	<!-- _includes/footer.html -->
     2	<footer class="site-footer h-card">
     3	  <data class="u-url" href="{{ "/" | relative_url }}"></data>
     4	  <div class="wrapper">
     5	    <div class="footer-col-wrapper">
     6	      <div class="footer-col">
     7	        <p class="feed-subscribe">
     8	          <a href="{{ site.feed.path | default: 'feed.xml' | absolute_url }}">
     9	            <svg class="svg-icon orange">
    10	              <use xlink:href="{{ 'assets/minima-social-icons.svg#rss' | relative_url }}"></use>
    11	            </svg><span>Subscribe</span>
    12	          </a>
    13	        </p>
    14	      {%- if site.author %}
    15	        <ul class="contact-list">
    16	          {% if site.author.name -%}
    17	            <li class="p-name">{{ site.author.name | escape }}</li>
    18	          {% endif -%}
    19	          {% if site.author.email -%}
    20	          <a href="mailto:{{ site.author.email | encode_email }}" title="Email Us">Email Us</a>
    21	          {%- endif %}
    22	        </ul>
    23	      {%- endif %}
    24	      </div>
    25	      <div class="footer-col">
    26	        <p>{{ site.description | safe }}</p>
    27	      </div>
    28	    </div>
    29	    <div class="social-links">
    30	      {%- include social.html -%}
    31	    </div>
    32	    {% include disclaimer.html %}
    33	  </div>
    34	  <script src="{{ '/assets/js/email-obfuscation.js' | relative_url }}"></script>
    35	</footer>

```


## Filename ==>  ./html/_includes/getintouch.html
```html
     1	---
     2	### Get In Touch
     3	We’re always looking to collaborate with professionals, families, and organizations seeking **AI-driven solutions** for **parental alienation** or other high-conflict situations.
     4	If you have questions, ideas, or want to contribute, you can [get in touch](/contact) with us directly. Alternatively, you can join discussions on our [GitHub Discussions](https://github.com/unixwzrd/unixwzrd.github.io/discussions) or follow us on social media (links in the footer).
     5	Your involvement helps us make a greater impact.
     6	<br>

```


## Filename ==>  ./html/_includes/head.html
```html
     1	<head>
     2	  <meta charset="utf-8">
     3	  <meta http-equiv="X-UA-Compatible" content="IE=edge">
     4	  <meta name="viewport" content="width=device-width, initial-scale=1">
     5	  {%- seo -%}
     6	  <link rel="stylesheet" href="{{ "/assets/css/style.css" | relative_url }}">
     7	  {%- feed_meta -%}
     8	  {%- if jekyll.environment == 'production' and site.google_analytics -%}
     9	    {%- include google-analytics.html -%}
    10	  {%- endif -%}
    11	  {%- include custom-head.html -%}
    12	</head>

```


## Filename ==>  ./html/_includes/header.html
```html
     1	<header class="site-header">
     2	  {% include custom-head.html %}
     3	  <div class="wrapper">
     4	    {%- assign default_paths = site.pages | map: "path" -%}
     5	    {%- assign page_paths = site.header_pages | default: default_paths -%}
     6	    {%- assign titles_size = site.pages | map: 'title' | join: '' | size -%}
     7	    <a class="site-title" rel="author" href="{{ "/" | relative_url }}">
     8	      <img src="{{ "/favicon-32x32.png" | relative_url }}" alt="Brand Graphic" class="brand-graphic">
     9	    </a>
    10	    <a class="site-title" rel="author" href="{{ "/" | relative_url }}">{{ site.title | escape }}</a>
    11	    {%- if titles_size > 0 -%}
    12	      {%- include navigation.html -%}
    13	    {%- endif -%}
    14	  </div>
    15	</header>

```


## Filename ==>  ./html/_includes/join_us.html
```html
     1	<br>
     2	---
     3	### Join Our Mission
     4	Join **Distributed Thinking Systems** in our development, community, support, and outreach efforts.
     5	- [**Operational Support**](/support/sponsorship):  If you find our resources useful, consider subscribing or making a one-time payment to help maintain and expand our projects. Your support allows us to continue developing valuable tools and innovations.
     6	- [**Collaborative Support**](/support/collaborate): Join the missionn, contribute data, provide expertise, or participate in building AI-driven solutions.
     7	- [**Products and Services**](/support/services): Assistance with AI projects, system architecture, or support for distributed Unix/Linux/macOS computing environments.
     8	Supporting us keeps vital resources available to the community and accessible to those who need them most. **You make a difference by helpingus make a difference.**

```


## Filename ==>  ./html/_includes/navigation.html
```html
     1	      <nav class="site-nav">
     2	        <input type="checkbox" id="nav-trigger" class="nav-trigger" />
     3	        <label for="nav-trigger">
     4	          <span class="menu-icon">
     5	            <svg viewBox="0 0 18 15" width="18px" height="15px">
     6	              <path d="M18,1.484c0,0.82-0.665,1.484-1.484,1.484H1.484C0.665,2.969,0,2.304,0,1.484l0,0C0,0.665,0.665,0,1.484,0 h15.032C17.335,0,18,0.665,18,1.484L18,1.484z M18,7.516C18,8.335,17.335,9,16.516,9H1.484C0.665,9,0,8.335,0,7.516l0,0 c0-0.82,0.665-1.484,1.484-1.484h15.032C17.335,6.031,18,6.696,18,7.516L18,7.516z M18,13.516C18,14.335,17.335,15,16.516,15H1.484 C0.665,15,0,14.335,0,13.516l0,0c0-0.82,0.665-1.483,1.484-1.483h15.032C17.335,12.031,18,12.695,18,13.516L18,13.516z"/>
     7	            </svg>
     8	          </span>
     9	        </label>
    10	        <div class="trigger">
    11	          {%- for path in page_paths -%}
    12	            {%- assign my_page = site.pages | where: "path", path | first -%}
    13	            {%- if my_page.title -%}
    14	            <a class="page-link" href="{{ my_page.url | relative_url }}">{{ my_page.menu_item | escape }}</a>
    15	            {%- endif -%}
    16	          {%- endfor -%}
    17	        </div>
    18	      </nav>

```


## Filename ==>  ./html/_includes/projects/TokenSecure.html
```html
     1	<h2><a href="https://github.com/unixwzrd/TokenSecure">TokenSecure</a></h2>
     2	<p>A safer way to store access tokens in an encrypted file and access them in your scripts without relying on environment files which could be accidentally be uploaded into a public repository. - unix...</p>
     3	<a class="github-link" href="https://github.com/unixwzrd/TokenSecure">View on GitHub</a>
     4	<a class="project-blog-link" href="/projects/TokenSecure/blog/">Project Blog</a>

```


## Filename ==>  ./html/_includes/projects/TorchDevice.html
```html
     1	<h2><a href="https://github.com/unixwzrd/TorchDevice">TorchDevice</a></h2>
     2	<p>Module contains class TorchDevice abstracting CUDA/MPS/CPU, intercepting, and redirecting calls to the available device to assist in porting code from CUDA to MPS. - unixwzrd/TorchDevice</p>
     3	<a class="github-link" href="https://github.com/unixwzrd/TorchDevice">View on GitHub</a>
     4	<a class="project-blog-link" href="/projects/TorchDevice/blog/">Project Blog</a>

```


## Filename ==>  ./html/_includes/projects/oobabooga-macOS.html
```html
     1	<h2><a href="https://github.com/unixwzrd/oobabooga-macOS">oobabooga-macOS</a></h2>
     2	<p>Optimizing performance, building and installing packages required for oobabooga, AI and Data Science on Apple Silicon GPU. The goal is to optimize wherever possible, from the ground up. - unixwzrd/...</p>
     3	<a class="github-link" href="https://github.com/unixwzrd/oobabooga-macOS">View on GitHub</a>
     4	<a class="project-blog-link" href="/projects/oobabooga-macOS/blog/">Project Blog</a>

```


## Filename ==>  ./html/_includes/projects/text-generation-webui-macos.html
```html
     1	<h2><a href="https://github.com/unixwzrd/text-generation-webui-macos">text-generation-webui-macos</a></h2>
     2	<p>A macOS version of the oobabooga gradio web UI for running Large Language Models like LLaMA, llama.cpp, GPT-J, Pythia, OPT, and GALACTICA. - unixwzrd/text-generation-webui-macos</p>
     3	<a class="github-link" href="https://github.com/unixwzrd/text-generation-webui-macos">View on GitHub</a>
     4	<a class="project-blog-link" href="/projects/text-generation-webui-macos/blog/">Project Blog</a>

```


## Filename ==>  ./html/_includes/projects/venvutil.html
```html
     1	<h2><a href="https://github.com/unixwzrd/venvutil">venvutil</a></h2>
     2	<p>Python virtual environment management functions and script to build and manage performance, compatibility, and regression test venv builds mostly for AI - unixwzrd/venvutil</p>
     3	<a class="github-link" href="https://github.com/unixwzrd/venvutil">View on GitHub</a>
     4	<a class="project-blog-link" href="/projects/venvutil/blog/">Project Blog</a>

```


## Filename ==>  ./html/_includes/projects_list.html
```html
     1	<!-- _includes/projects_list.html -->
     2	<div class="projects-list">
     3	  {% for project in site.data.github_projects.projects %}
     4	    <table class="project-table">
     5	      <tr>
     6	        <!-- First column: Image -->
     7	        <td class="project-image">
     8	          <a href="{{ project.repo_url }}">
     9	            <img class="project-preview" src="{{ project.image_url }}" alt="{{ project.title }} image">
    10	          </a>
    11	        </td>
    12	        <!-- Second column: Text (Title, Description, GitHub link) -->
    13	        <td class="project-details">
    14	          <h2><a href="{{ project.repo_url }}">{{ project.title }}</a></h2>
    15	          <p>{{ project.description }}</p>
    16	          <!-- Nested row for links: Project Blog and GitHub -->
    17	          <div class="links-row">
    18	            <a class="project-blog-link" href="/projects/{{ project.title }}">Project Blog</a>
    19	            <a class="github-link" href="{{ project.repo_url }}">View on GitHub</a>
    20	          </div>
    21	        </td>
    22	      </tr>
    23	    </table>
    24	  {% endfor %}
    25	</div>

```


## Filename ==>  ./html/_includes/rss_feed_sub.html
```html
     1	    <-- Subscribe to our RSS feed >
     2	        </p        <p class="feed-subscribe">
     3	          <a href="{{ site.feed.path | default: 'feed.xml' | absolute_url }}">
     4	            <svg class="svg-icon orange">
     5	              <use xlink:href="{{ '/assets/minima-social-icons.svg#rss' | relative_url }}"></use>
     6	            </svg><span>Subscribe</span>
     7	          </a>
     8	        </p>>

```


## Filename ==>  ./html/_includes/social-item.html
```html
     1	<!-- _includes/social-item.html -->
     2	<li>
     3	  {% assign entry = include.item %}
     4	  <a {% unless entry.platform == 'rss' %}rel="me" {% endunless %}href="{{ entry.user_url }}" target="_blank" title="{{ entry.title | default: entry.platform }}">
     5	    <svg class="svg-icon grey">
     6	      <use xlink:href="{{ '/assets/minima-social-icons.svg#' | append: entry.platform | relative_url }}"></use>
     7	    </svg>
     8	  </a>
     9	</li>

```


## Filename ==>  ./html/_includes/social.html
```html
     1	<ul class="social-media-list">
     2	{%- for entry in site.minima.social_links -%}
     3	  {%- include social-item.html item = entry -%}
     4	{%- endfor -%}
     5	</ul>

```


## Filename ==>  ./html/_includes/svg_symbol.html
```html
     1	<symbol id="{{ include.key }}" fill-rule="evenodd" clip-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="1.414" viewBox="0 0 16 16">
     2	  {%- include social-icons/{{ include.key }}.svg -%}
     3	</symbol>

```


## Filename ==>  ./html/_includes/wand_accred.html
```html
     1	<div class="accreditaion-s-certifications">
     2	    <a href="https://www.credential.net/600b14c6-39ee-4090-b501-b24c989772c9" target="_blank"><img src="https://api.accredible.com/v1/frontend/credential_website_embed_image/certificate/116814134" alt="Weights and Biases - 101" title="Weights and Bisese - 101" /></a>
     3	  </div>

```


## Filename ==>  ./html/_layouts/blog.html
```html
     1	---
     2	layout: page
     3	---
     4	<div class="blog-posts">
     5	  {{ content }}
     6	</div>

```


## Filename ==>  ./html/_layouts/home.html
```html
     1	---
     2	layout: default
     3	---
     4	<div class="home">
     5	  {%- if page.title -%}
     6	    <h1 class="post-title">{{ page.title }}</h1>
     7	  {%- endif -%}
     8	  {{ content }}
     9	  {% if site.paginate %}
    10	    {% assign posts = paginator.posts %}
    11	  {% else %}
    12	    {% assign posts = site.posts %}
    13	  {% endif %}
    14	  {%- if posts.size > 0 -%}
    15	    {%- if page.list_title -%}
    16	      <h2 class="post-list-heading">{{ page.list_title }}</h2>
    17	    {%- endif -%}
    18	    <ul class="post-list">
    19	      {%- assign date_format = site.minima.date_format | default: "%b %-d, %Y" -%}
    20	      {%- for post in posts -%}
    21	      <li>
    22	        <span class="post-meta">{{ post.date | date: date_format }}</span>
    23	        <h3>
    24	          <a class="post-link" href="{{ post.url | relative_url }}">
    25	            {{ post.title | escape }}
    26	          </a>
    27	        </h3>
    28	        {%- if site.show_excerpts -%}
    29	          {{ post.excerpt }}
    30	        {%- endif -%}
    31	      </li>
    32	      {%- endfor -%}
    33	    </ul>
    34	    {% if site.paginate %}
    35	      <div class="pager">
    36	        <ul class="pagination">
    37	        {%- if paginator.previous_page %}
    38	          <li><a href="{{ paginator.previous_page_path | relative_url }}" class="previous-page">{{ paginator.previous_page }}</a></li>
    39	        {%- else %}
    40	          <li><div class="pager-edge">•</div></li>
    41	        {%- endif %}
    42	          <li><div class="current-page">{{ paginator.page }}</div></li>
    43	        {%- if paginator.next_page %}
    44	          <li><a href="{{ paginator.next_page_path | relative_url }}" class="next-page">{{ paginator.next_page }}</a></li>
    45	        {%- else %}
    46	          <li><div class="pager-edge">•</div></li>
    47	        {%- endif %}
    48	        </ul>
    49	      </div>
    50	    {%- endif %}
    51	  {%- endif -%}
    52	</div>

```


## Filename ==>  ./html/_layouts/page.html
```html
     1	---
     2	layout: default
     3	---
     4	<article class="post">
     5	  <header class="page-heading">
     6	    <h1 class="post-title">{{ page.title | escape }}</h1>
     7	  </header>
     8	  <div class="post-content">
     9	    {{ content }}
    10	  </div>
    11	</article>

```


## Filename ==>  ./html/_layouts/post.html
```html
     1	---
     2	layout: default
     3	---
     4	<article class="post h-entry" itemscope itemtype="http://schema.org/BlogPosting">
     5	  <header class="post-header">
     6	    <h1 class="post-title p-name" itemprop="name headline">{{ page.title | escape }}</h1>
     7	    <p class="post-meta">
     8	      {%- assign date_format = site.minima.date_format | default: "%b %-d, %Y" -%}
     9	      <time class="dt-published" datetime="{{ page.date | date_to_xmlschema }}" itemprop="datePublished">
    10	        {{ page.date | date: date_format }}
    11	      </time>
    12	      {%- if page.modified_date -%}
    13	        ~
    14	        {%- assign mdate = page.modified_date | date_to_xmlschema -%}
    15	        <time class="dt-modified" datetime="{{ mdate }}" itemprop="dateModified">
    16	          {{ mdate | date: date_format }}
    17	        </time>
    18	      {%- endif -%}
    19	      {%- if page.author -%}
    20	        • {% for author in page.author %}
    21	          <span itemprop="author" itemscope itemtype="http://schema.org/Person">
    22	            <span class="p-author h-card" itemprop="name">{{ author }}</span></span>
    23	            {%- if forloop.last == false %}, {% endif -%}
    24	        {% endfor %}
    25	      {%- endif -%}</p>
    26	  </header>
    27	  <div class="post-content e-content" itemprop="articleBody">
    28	    {{ content }}
    29	  </div>
    30	  {%- if site.disqus.shortname -%}
    31	    {%- include disqus_comments.html -%}
    32	  {%- endif -%}
    33	  <a class="u-url" href="{{ page.url | relative_url }}" hidden></a>
    34	</article>

```


## Filename ==>  ./html/_layouts/project.html
```html
     1	<!-- _layouts/project.html -->
     2	---
     3	layout: default
     4	---
     5	<article class="project">
     6	  <header class="project-header">
     7	    <h1 class="project-title">{{ page.title | escape }}</h1>
     8	    {% if page.repo_url %}
     9	      <p class="project-meta">
    10	        GitHub: <a href="{{ page.repo_url }}">{{ page.repo_url }}</a>
    11	      </p>
    12	    {% endif %}
    13	  </header>
    14	  <div class="project-content">
    15	    {% if page.image_url %}
    16	      <img src="{{ page.image_url }}" alt="{{ page.title }} image" class="project-image">
    17	    {% endif %}
    18	    {{ content }}
    19	  </div>
    20	  {% if site.categories[page.project_name] %}
    21	    <h2>Project Blog Entries</h2>
    22	    {% for post in site.categories[page.project_name] %}
    23	      <article class="post">
    24	        <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
    25	        <span class="post-date">{{ post.date | date: "%B %d, %Y" }}</span>
    26	        {% assign excerpt = post.content | split: '<!--more-->' | first %}
    27	        {{ excerpt | markdownify | process_heading }}
    28	        <a href="{{ post.url | relative_url }}" class="btn">Read More</a>
    29	      </article>
    30	    {% endfor %}
    31	  {% endif %}
    32	</article>

```


## Filename ==>  ./html/about.md
```markdown
     1	---
     2	title: "About Us"
     3	layout: page
     4	menu_item: About
     5	permalink: /about/
     6	---
     7	### Our Mission
     8	Our primary technical focus is on **AI** and **distributed computing**. We are dedicated to applying these skills in ways that make a **positive societal impact**, particularly in **parental alienation**, a damaging form of child abuse where one parent manipulates a child to reject the other parent, sometimes creating false narratives or accusations. Utilizing **AI-driven insights** and **data analytics**, we work to detect and address early signs of alienation, preventing **emotional and psychological damage** before it takes root.
     9	At **Distributed Thinking Systems**, we also leverage our technical expertise across sectors to drive **responsible AI innovation**. Our work extends beyond family law to include custom **AI solutions** for various industries, from **digital forensics** to **distributed computing systems** architecture, ensuring technology serves the greater good. This combination of social responsibility and cutting-edge technology drives our mission forward.
    10	We believe **responsible AI** should not only solve today’s problems, but anticipate and prevent future harm. This core value drives everything we do: supporting AI in **Unix/Linux/macOS environments**, developing and integrating systems which prioritize **ethics**, and ensuring technology is both accessible and beneficial for everyone.
    11	We firmly believe all children need both parents in their lives. Forcing a child to reject one parent erases part of their personality and past without giving them the chance to understand why. Our mission is to ensure no child ever endures this experience again. **Children deserve to grow up free from abuse**, with the care and support of both parents.
    12	### Our Team
    13	- **[Michael Sullivan:](/about/resume)** Founder, with over 30 years of experience providing distributed computing, database, and infrastructure solutions across diverse industries. Now focusing on Artificial Intelligence, Data Analytics, and Distributed AI Solutions for businesses, Michael brings a wealth of technical expertise. As a parent personally affected by alienation for more than five years, experiencing the emotional impact this can have on families, and is committed to creating solutions that help prevent it.
    14	{% include join_us.html %}
    15	{% include getintouch.html %}

```


## Filename ==>  ./html/blog.md
```html
     1	---
     2	title: "Distributed Thinking Systems Blog"
     3	layout: page
     4	menu_item: Blog
     5	permalink: /blog/
     6	---
     7	Welcome to the **Distributed Thinking Systems Blog**, where we delve into topics at the intersection of **AI development**, **distributed computing**, and **technology innovations** in **Unix/Linux/macOS environments**.
     8	Beyond tech, we explore real-world applications of these advancements, such as addressing societal challenges like **parental alienation**. Dive into our latest articles and stay informed about our projects, research, and technical explorations.
     9	{% for post in site.posts %}
    10	  <article class="post">
    11	    <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
    12	    <span class="post-date">{{ post.date | date: "%B %d, %Y" }}</span>
    13	    {% assign excerpt = post.content | split: '<!--more-->' | first %}
    14	    {{ excerpt | truncatewords: 50 | markdownify | process_heading }}
    15	    <a href="{{ post.url | relative_url }}" class="btn">Read More</a>
    16	  </article>
    17	{% endfor %}
    18	{% include join_us.html %}
    19	{% include getintouch.html %}

```


## Filename ==>  ./html/collaborate.md
```markdown
     1	---
     2	layout: page
     3	title: "Collaborate and Join the Community"
     4	menu_item: Collaborate
     5	permalink: /collaborate/
     6	---
     7	### Build With Us: Become Part of the Community
     8	**Distributed Thinking Systems** is about building a collaborative community where professionals and individuals come together to contribute their expertise, participate in projects, or support our work.
     9	Whether you're a **legal professional**, a **researcher**, or someone who wants to help push our mission forward, your involvement is invaluable.
    10	#### Two Ways to Get Involved:
    11	- **For Professionals**: If you’re seeking our services, sponsorship opportunities, or want to hire us for AI development, data analysis, or consulting, head over to our [Professional Services](/collaborate/professionals) page.
    12	- **For Contributors & Participants**: Interested in joining our community, contributing data, collaborating on research, or getting involved with ongoing projects? Visit our [Community Collaboration](/collaborate/community) page.
    13	Join us in making an impact on the future of AI, parental alienation solutions, and technology.
    14	{% include getintouch.html %}

```


## Filename ==>  ./html/collaborate/community.md
```markdown
     1	---
     2	layout: page
     3	title: "Join Our Community"
     4	menu_item: Community
     5	permalink: /collaborate/community/
     6	---
     7	### Join Our Community: Research, Projects & Contributions
     8	We’re building a thriving community of individuals who share their experiences, contribute to research, or collaborate on new and innovative tech projects.
     9	#### How You Can Get Involved:
    10	- **Share Your Experience**: If you’ve been impacted by parental alienation, share your story with us to help raise awareness and build our data for research. Your insights could make a difference.
    11	- **Contribute to Research**: Are you a researcher or academic interested in contributing to our AI-based parental alienation tools? We need data, feedback, and insights to refine our models.
    12	- **Collaborate on Projects**: If you’re a developer, technologist, or individual who wants to participate in building AI solutions, join one of our open-source or private projects.
    13	#### Your Role in the Community:
    14	- **Researchers**: Provide data or collaborate with our AI teams.
    15	- **Participants**: Join ongoing projects or support us through your involvement.
    16	- **Community Members**: Stay informed and contribute to discussions that drive our work forward.
    17	Ready to get involved? [Contact Us](/contact) or visit our [Projects Page](/projects) for more details on current initiatives.
    18	---
    19	#### If You Like What We Do:
    20	Show your appreciation for my projects and the work I’m doing. Help keep the community growing and the projects going through any of the following ways:
    21	- **[Ko-fi](https://ko-fi.com/unixwzrd)** – Make one-time donations or monthly support.
    22	- **[Patreon](https://patreon.com/unixwzrd)** – Subscribe for exclusive updates and perks.
    23	{% include getintouch.html %}

```


## Filename ==>  ./html/collaborate/professional.md
```markdown
     1	---
     2	layout: page
     3	title: "Professional Services & Sponsorship"
     4	menu_item: Professionals
     5	permalink: /collaborate/professionals/
     6	---
     7	### Professional Services & Sponsorship Opportunities
     8	We work with legal professionals, trial consultants, mental health experts, and tech companies who are looking for solutions for difficult problems using technology for good.
     9	#### How You Can Work With Us:
    10	- **Hire Us**: We bring more than 30 years experience providing AI-driven analysis, digital forensics, Unix/Linux/macOS consulting, with systems and AI tool development. If you need our expertise, [Contact Us](/contact) directly to discuss your needs.
    11	- **Sponsorship Opportunities**: Support our work through sponsorship and have your business featured in our professional directory. Your sponsorship helps us keep our AI tools and research accessible.
    12	#### Services We Offer:
    13	- **AI/ML Development, and Data Analytics**
    14	- **Digital Forensics, Audio Restoration**
    15	- **Unix/Linux Systems Support**
    16	- **Custom Technology Solutions**
    17	Ready to work with us? [Contact Us](/contact) today.
    18	{% include getintouch.html %}

```


## Filename ==>  ./html/contact.md
```markdown
     1	---
     2	layout: page
     3	title: "Contact Us"
     4	menu_item: Contact
     5	permalink: /contact/
     6	---
     7	### Get in Touch
     8	For inquiries or to discuss a project, please use the following contact details:
     9	- **Email**: [Request Information Here](mailto:{{ site.author.email | encode_email }})
    10	- **Phone**: +1-901-471-0896 (Text only)
    11	- **Telegram**: [@unixwzrd](https://t.me/unixwzrd) (Direct message only)
    12	If you are a **legal service provider**, **trial consultant**, or **mental healthcare provider**, please visit our [Support for Professionals](/support/professionals) page for tailored services.
    13	For general inquiries or support outside our scope, please visit our [Resources](/resources) page for additional help.
    14	{% include join_us.html %}

```


## Filename ==>  ./html/faq.md
```markdown
     1	---
     2	layout: page
     3	title: Frequently Asked Questions
     4	menu_item: FAQ
     5	---
     6	- ### What is Distributed Thinking Systems?
     7	    Distributed Thinking Systems is focused on solving complex problems using **AI** and **distributed computing** with a focus on **parental alienation**.
     8	- ### What services do you provide?
     9	    We specialize in AI analysis, parental alienation case support, and high-conflict divorce insights, among other distributed computing services.
    10	- ### How do I get a quote for your services?
    11	    Reach out via our [Contact page](./contact) to discuss your project and get a custom quote.
    12	- ### How is confidentiality maintained?
    13	    We take privacy seriously and handle all data with strict confidentiality protocols. For more details, contact us directly.
    14	- ### How can AI prevent parental alienation?
    15	    We use AI to analyze communication patterns and detect shifts in tone and content that may indicate early signs of parental alienation. This helps families and legal professionals address issues before they escalate.
    16	- ### How can I get involved?
    17	    We’re always looking for **collaborators**, **sponsors**, and **partners** to expand our work. Reach out through our [Contact page](contact.md) to discuss opportunities.
    18	{% include join_us.html %}
    19	{% include getintouch.html %}

```


## Filename ==>  ./html/index.md
```markdown
     1	---
     2	layout: home
     3	title: Welcome to Distributed Thinking Systems
     4	---
     5	## Overview
     6	At **Distributed Thinking Systems**, we specialize in solving complex challenges through **Artificial Intelligence**, **distributed computing**, and **innovative technology**. Our mission is to leverage these tools to combat the harmful effects of **parental alienation** in high-conflict divorce cases, offering solutions to prevent alienation before it starts.
     7	**Parental alienation** is an extremely harmful form of child abuse, where one parent manipulates a child to reject the other parent. This can fracture families, leading to long-term psychological and emotional damage. Despite its impact, parental alienation often goes unrecognized in family courts, leading to harmful custody decisions.
     8	Using **AI** and **data analytics**, we aim to identify early signs of alienation through patterns in communication and family dynamics. These tools offer new insights into custody decisions, ensuring they are made in the child’s best interest.
     9	At **Distributed Thinking Systems**, we are committed to providing solutions that empower families and help children maintain healthy relationships with both parents.
    10	## What We Do
    11	We specialize in:
    12	- **Artificial Intelligence & Machine Learning**: Using AI to uncover patterns that prevent parental alienation.
    13	- **Data Analytics**: Building tools to analyze communications, legal documents, and family dynamics, highlighting signs of alienation.
    14	- **Distributed Computing Systems**: Designing scalable systems using Unix/Linux environments for AI and other solutions.
    15	- **Digital Forensics & Data Recovery**: Offering advanced recovery and analysis, particularly for legal and family-related support.
    16	## About Us
    17	We focus on applying **AI** and **distributed computing** to address real-world challenges. Our primary focus is on analyzing communication patterns from high-conflict divorce cases to prevent long-term emotional damage from parental alienation.
    18	If you are interested in contributing **data from past cases**, partnering in research, or supporting us in any capacity, please [collaborate with us](/collaborate/).
    19	At the intersection of AI and family law, we are committed to protecting parents and children from the long-lasting damage caused by alienation. By leveraging cutting-edge AI, we analyze shifts in communication to prevent problems before they escalate.
    20	{% include join_us.html %}
    21	{% include getintouch.html %}

```


## Filename ==>  ./html/projects.md
```markdown
     1	---
     2	title: "Projects"
     3	layout: page
     4	menu_item: Projects
     5	permalink: /projects/
     6	---
     7	## Open Source Projects
     8	At **Distributed Thinking Systems**, we are constantly pushing boundaries with innovative projects in AI, data science, and distributed computing.
     9	{% include projects_list.html %}
    10	## More to come
    11	<div class=body>
    12	More projects on the way and even some demos and how-to's for things like processing audio, for speech to text and interpersonal communications dynamics and analysis. It will take me a bit of time  to get things organized and some tutorials up, but I will be working non-stop to help provide some good information, both of what I can do and how you may be able to do some of this yourself.
    13	</div>
    14	{% include join_us.html %}
    15	{% include getintouch.html %}

```


## Filename ==>  ./html/projects/TokenSecure.md
```html
     1	---
     2	title: "TokenSecure"
     3	layout: project
     4	project_name: "TokenSecure"
     5	permalink: /projects/TokenSecure/
     6	---
     7	## TokenSecure
     8	A safer way to store access tokens in an encrypted file and access them in your scripts without relying on environment files which could be accidentally be uploaded into a public repository. - unix...
     9	- [View on GitHub](https://github.com/unixwzrd/TokenSecure)
    10	## Project Blog Entries
    11	{% raw %}{% for post in site.categories.TokenSecure %}
    12	  <article class="post">
    13	    <h3><a href="{ '{' } post.url | relative_url { '}' }">{ '{' } post.title { '}' }</a></h3>
    14	    <span class="post-date">{ '{' } post.date | date: "%B %d, %Y" { '}' }</span>
    15	    { '{' }% assign excerpt = post.content | split: '<!--more-->' | first %{ '}' }
    16	    { '{' } excerpt | truncatewords: 50 | markdownify | process_heading { '}' }
    17	    <a href="{ '{' } post.url | relative_url { '}' }" class="btn">Read More</a>
    18	  </article>
    19	{% endfor %}{% endraw %}
    20	{% raw %}{% include join_us.html %}{% endraw %}
    21	{% raw %}{% include getintouch.html %}{% endraw %}

```


## Filename ==>  ./html/projects/TokenSecure/TokenSecure-project-blog-entry.md
```markdown
     1	---
     2	title: "TokenSecure Blog Entry"
     3	layout: post
     4	category: TokenSecure
     5	published: false
     6	---
     7	This is a placeholder for the project blog entry.

```


## Filename ==>  ./html/projects/TorchDevice.md
```html
     1	---
     2	title: "TorchDevice"
     3	layout: project
     4	project_name: "TorchDevice"
     5	permalink: /projects/TorchDevice/
     6	---
     7	## TorchDevice
     8	Module contains class TorchDevice abstracting CUDA/MPS/CPU, intercepting, and redirecting calls to the available device to assist in porting code from CUDA to MPS. - unixwzrd/TorchDevice
     9	- [View on GitHub](https://github.com/unixwzrd/TorchDevice)
    10	## Project Blog Entries
    11	{% raw %}{% for post in site.categories.TorchDevice %}
    12	  <article class="post">
    13	    <h3><a href="{ '{' } post.url | relative_url { '}' }">{ '{' } post.title { '}' }</a></h3>
    14	    <span class="post-date">{ '{' } post.date | date: "%B %d, %Y" { '}' }</span>
    15	    { '{' }% assign excerpt = post.content | split: '<!--more-->' | first %{ '}' }
    16	    { '{' } excerpt | truncatewords: 50 | markdownify | process_heading { '}' }
    17	    <a href="{ '{' } post.url | relative_url { '}' }" class="btn">Read More</a>
    18	  </article>
    19	{% endfor %}{% endraw %}
    20	{% raw %}{% include join_us.html %}{% endraw %}
    21	{% raw %}{% include getintouch.html %}{% endraw %}

```


## Filename ==>  ./html/projects/TorchDevice/TorchDevice-project-blog-entry.md
```markdown
     1	---
     2	title: "TorchDevice Blog Entry"
     3	layout: post
     4	category: TorchDevice
     5	published: false
     6	---
     7	This is a placeholder for the project blog entry.

```


## Filename ==>  ./html/projects/oobabooga-macOS.md
```html
     1	---
     2	title: "oobabooga-macOS"
     3	layout: project
     4	project_name: "oobabooga-macOS"
     5	permalink: /projects/oobabooga-macOS/
     6	---
     7	## oobabooga-macOS
     8	Optimizing performance, building and installing packages required for oobabooga, AI and Data Science on Apple Silicon GPU. The goal is to optimize wherever possible, from the ground up. - unixwzrd/...
     9	- [View on GitHub](https://github.com/unixwzrd/oobabooga-macOS)
    10	## Project Blog Entries
    11	{% raw %}{% for post in site.categories.oobabooga-macOS %}
    12	  <article class="post">
    13	    <h3><a href="{ '{' } post.url | relative_url { '}' }">{ '{' } post.title { '}' }</a></h3>
    14	    <span class="post-date">{ '{' } post.date | date: "%B %d, %Y" { '}' }</span>
    15	    { '{' }% assign excerpt = post.content | split: '<!--more-->' | first %{ '}' }
    16	    { '{' } excerpt | truncatewords: 50 | markdownify | process_heading { '}' }
    17	    <a href="{ '{' } post.url | relative_url { '}' }" class="btn">Read More</a>
    18	  </article>
    19	{% endfor %}{% endraw %}
    20	{% raw %}{% include join_us.html %}{% endraw %}
    21	{% raw %}{% include getintouch.html %}{% endraw %}

```


## Filename ==>  ./html/projects/oobabooga-macOS/oobabooga-macOS-project-blog-entry.md
```markdown
     1	---
     2	title: "oobabooga-macOS Blog Entry"
     3	layout: post
     4	category: oobabooga-macOS
     5	published: false
     6	---
     7	This is a placeholder for the project blog entry.

```


## Filename ==>  ./html/projects/text-generation-webui-macos.md
```html
     1	---
     2	title: "text-generation-webui-macos"
     3	layout: project
     4	project_name: "text-generation-webui-macos"
     5	permalink: /projects/text-generation-webui-macos/
     6	---
     7	## text-generation-webui-macos
     8	A macOS version of the oobabooga gradio web UI for running Large Language Models like LLaMA, llama.cpp, GPT-J, Pythia, OPT, and GALACTICA. - unixwzrd/text-generation-webui-macos
     9	- [View on GitHub](https://github.com/unixwzrd/text-generation-webui-macos)
    10	## Project Blog Entries
    11	{% raw %}{% for post in site.categories.text-generation-webui-macos %}
    12	  <article class="post">
    13	    <h3><a href="{ '{' } post.url | relative_url { '}' }">{ '{' } post.title { '}' }</a></h3>
    14	    <span class="post-date">{ '{' } post.date | date: "%B %d, %Y" { '}' }</span>
    15	    { '{' }% assign excerpt = post.content | split: '<!--more-->' | first %{ '}' }
    16	    { '{' } excerpt | truncatewords: 50 | markdownify | process_heading { '}' }
    17	    <a href="{ '{' } post.url | relative_url { '}' }" class="btn">Read More</a>
    18	  </article>
    19	{% endfor %}{% endraw %}
    20	{% raw %}{% include join_us.html %}{% endraw %}
    21	{% raw %}{% include getintouch.html %}{% endraw %}

```


## Filename ==>  ./html/projects/text-generation-webui-macos/text-generation-webui-macos-project-blog-entry.md
```markdown
     1	---
     2	title: "text-generation-webui-macos Blog Entry"
     3	layout: post
     4	category: text-generation-webui-macos
     5	published: false
     6	---
     7	This is a placeholder for the project blog entry.

```


## Filename ==>  ./html/projects/venvutil.md
```html
     1	---
     2	title: "venvutil"
     3	layout: project
     4	project_name: "venvutil"
     5	permalink: /projects/venvutil/
     6	---
     7	## venvutil
     8	Python virtual environment management functions and script to build and manage performance, compatibility, and regression test venv builds mostly for AI - unixwzrd/venvutil
     9	- [View on GitHub](https://github.com/unixwzrd/venvutil)
    10	## Project Blog Entries
    11	{% raw %}{% for post in site.categories.venvutil %}
    12	  <article class="post">
    13	    <h3><a href="{ '{' } post.url | relative_url { '}' }">{ '{' } post.title { '}' }</a></h3>
    14	    <span class="post-date">{ '{' } post.date | date: "%B %d, %Y" { '}' }</span>
    15	    { '{' }% assign excerpt = post.content | split: '<!--more-->' | first %{ '}' }
    16	    { '{' } excerpt | truncatewords: 50 | markdownify | process_heading { '}' }
    17	    <a href="{ '{' } post.url | relative_url { '}' }" class="btn">Read More</a>
    18	  </article>
    19	{% endfor %}{% endraw %}
    20	{% raw %}{% include join_us.html %}{% endraw %}
    21	{% raw %}{% include getintouch.html %}{% endraw %}

```


## Filename ==>  ./html/projects/venvutil/venvutil-project-blog-entry.md
```markdown
     1	---
     2	title: "venvutil Blog Entry"
     3	layout: post
     4	category: venvutil
     5	published: false
     6	---
     7	This is a placeholder for the project blog entry.

```


## Filename ==>  ./html/resources.md
```markdown
     1	---
     2	layout: page
     3	title: Resources
     4	menu_item: Resources
     5	permalink: /resources/
     6	---
     7	**Information on crisis interventions - See [Emergency Resources](/resources/emergency-resources) page.**
     8	Helpful tools, organizations, and information related to parental alienation, AI, and legal support below. If you have a resource you would like added, [contact us](/contact).
     9	 | National Center for Missing and Exploited Children | 24-Hour Call Center | 1-800-THE-LOST<br> 1-800-843-5678 |
    10	### AI and Technology Tools
    11	- [Anthropic Intelligence](https://www.anthropic.com/) - AI research and development tools.
    12	- [Hugging Face](https://huggingface.co/) - Open-source AI tools.
    13	- [OpenAI](https://openai.com/) - AI research and development tools, and ChatGPT.
    14	- [Wandb](https://wandb.ai/) - AI research and development tools for building and training models.
    15	### Parental Alienation Resources
    16	#### The United States
    17	- [National Center for Missing & Exploited Children](https://www.missingkids.org/) - NCMEC is the nation’s largest and most influential child protection organization.
    18	- [Family Abduction](https://www.missingkids.org/theissues/familyabduction) - A Family Abduction occurs when a child is taken, wrongfully retained, or concealed by a parent or other family member depriving another individual of their custody or visitation rights.
    19	- [Family Abduction: Prevention & Response](https://www.missingkids.org/theissues/familyabduction) - Helpful information on prevention and response involving family abductions.
    20	- [r/ParentalAlienation](https://www.reddit.com/r/ParentalAlienation/) - A community for family members who have experienced parental alienation to seek support and guidance. Whether you're an ex-partner, a child, or an extended family member, this is the place for you.
    21	#### Europe and United Kingdom
    22	- [Parental Alienation Awareness…](https://paawareness.co.uk/) Supporting survivors, raising awareness, reducing isolation
    23	#### Other Support Groups and People
    24	- [KAREN WOODALL –](https://karenwoodall.blog/) Psychotherapist, Writer, Researcher, Trainer
    25	### Mental Health Resources
    26	- [Crisis Text Line](https://www.crisistextline.org/) - Support for those in crisis.
    27	- [National Suicide Prevention Lifeline](https://suicidepreventionlifeline.org/) - Immediate help for those experiencing distress.
    28	- [Find a Therapist](https://www.psychologytoday.com/us/therapists)
    29	- [BetterHelp](https://www.betterhelp.com)
    30	- [Therapy Aid for Financial Assistance](https://therapyaid.com)
    31	### Legal Resources
    32	- [American Bar Association Lawyer Referral](https://www.americanbar.org)
    33	- [National Legal Aid & Defender Association](https://www.nlada.org)
    34	- [Legal Aid Society](https://www.legalaid.org)
    35	{% include join_us.html %}
    36	{% include getintouch.html %}

```


## Filename ==>  ./html/resources/emergency-resources.md
```html
     1	---
     2	title: "Emergency Resources"
     3	layout: page
     4	---
     5	#### If you or someone you know is in immediate danger or experiencing a crisis, in the eUnited States, **CALL 911** or go to the nearest emergency room immediately.
     6	# Emergency Resources by Country
     7	<table>
     8	  <thead>
     9	    <tr>
    10	      <th>Country</th>
    11	      <th>Service</th>
    12	      <th>Contact Number</th>
    13	    </tr>
    14	  </thead>
    15	  <tbody>
    16	    {% assign row_class = "odd" %}
    17	    {% for country in site.data.countries.countries %}
    18	      <!-- First service row for the country -->
    19	      <tr class="{{ row_class }}">
    20	        <td><strong>{{ country.name }}</strong></td>
    21	        <td>{{ country.services[0].service }}</td>
    22	        <td>{{ country.services[0].contact }}</td>
    23	      </tr>
    24	      <!-- Additional services for the country -->
    25	      {% for service in country.services offset:1 %}
    26	        <tr class="{{ row_class }}">
    27	          <td></td>
    28	          <td>{{ service.service }}</td>
    29	          <td>{{ service.contact }}</td>
    30	        </tr>
    31	      {% endfor %}
    32	      <!-- Alternate row classes -->
    33	      {% if row_class == "odd" %}
    34	        {% assign row_class = "even" %}
    35	      {% else %}
    36	        {% assign row_class = "odd" %}
    37	      {% endif %}
    38	    {% endfor %}
    39	  </tbody>
    40	</table>
    41	_Note_: In case of a mental health emergency, please seek immediate professional help.
    42	_Note_: If you notice any information missing or inaccurate on this page, please [contact us](/contact).
    43	{% include getintouch.html %}

```
