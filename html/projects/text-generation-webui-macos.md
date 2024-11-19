---
title: "text-generation-webui-macos"
layout: project
project_name: "text-generation-webui-macos"
permalink: /projects/text-generation-webui-macos/
---
## text-generation-webui-macos

A macOS version of the oobabooga gradio web UI for running Large Language Models like LLaMA, llama.cpp, GPT-J, Pythia, OPT, and GALACTICA. - unixwzrd/text-generation-webui-macos

- [View on GitHub](https://github.com/unixwzrd/text-generation-webui-macos)

## Project Blog Entries

{% raw %}{% for post in site.categories.text-generation-webui-macos %}
  <article class="post">
    <h3><a href="{ '{' } post.url | relative_url { '}' }">{ '{' } post.title { '}' }</a></h3>
    <span class="post-date">{ '{' } post.date | date: "%B %d, %Y" { '}' }</span>
    { '{' }% assign excerpt = post.content | split: '<!--more-->' | first %{ '}' }
    { '{' } excerpt | truncatewords: 50 | markdownify | process_heading { '}' }
    <a href="{ '{' } post.url | relative_url { '}' }" class="btn">Read More</a>
  </article>
{% endfor %}{% endraw %}

{% raw %}{% include join_us.html %}{% endraw %}

{% raw %}{% include getintouch.html %}{% endraw %}
