---
layout: post
title: "Building This Site With AI"
date: 2024-09-27 17:30:00 -0500
categories: [coding, ai, blog]
---

## I managed to get this site up and running finally in spite of AI.

Initially I wanted to use a web builder which would produce my HTML, CSS, and SCSS files, in a nice WISIWIG format and even tried out a couple of the web builder products. I mostly wanted something I could move to any hosting service available and did not want to get locked into a proprietary platform. I tried **Mobirise**, but didn't like their pricing model, you could buy lots of nice modules, but had to pay a recurring fee to use them, then I tried **Sparkle**, but there was a high learning curve for someone who is a s non-creative as me. I liked Sparkle, and might give it another ho sometime, but learning it was going to take a lot of effort.

Eventually I settled on a fairly simple web framework, Jekyll. It used familiar markdown fro its pages and could generate some content using Liquid, a sort of embedded programming language which would allow a bit of dynamic content creation for my site. It also had a fairly steep learning curve and Gaslight GPT would sometimes take me down a serpentine path, only to discover after a week, the solution I was looking for a very simple and if it kew about it, why couldn't it have told me the solution a week ago, I found this rather frustrating. For anyone who thinks they can build a system who is not a programmer, I'm not sure we are there yet. It's coming, but there was still a plot o times where I had to call GPT-4o out over things I knew were wrong, and have it go look on the web for a solution.

<!--more-->

The upside of the whole process is I now know, for the most part how everything is set up, know enough to know when GPT-4o is not giving me a straight answer, and I have learned a lot in the process, more than I wanted to, but I have the beginnings of a site I can build on. One nice thing was that support for different screen sizes was pretty much built-in to the CSS and SCSS, along with light and dark mode handling. Another thing was that having the source code allowed me to make easy customizations once I figured out the Jekyll layout and filesystem structure.

I used AI to assists me with things lie SCSS, CSS, HTML, Liquid for Jekyll, and it was not all slow going.  Many times the AI would send me down a rabbit hole for a week or so. This wasted a lot of time because on more than one occasion, GPT-4o would forgot what we were working on to begin with and give me a completely different page instead. Sometimes offering me solutions to issues which would not work , and then offer the same solutions again an hour or so later.  Sometimes the solution was 95% complete, but I needed that 5% in order to have a complete solution. Going in endless circles until I could fins a different approach to the same problem. This process was excruciating, and I have had to hack some Jekyll code myself, which was not my desire.

One instance was the menu bar items at the top of the page. It kept insisting to put a "navigation.yml" file in the _data directory and it would magically create the navigation menus.  It didn't and I'm sure there were some other steps to getting it to work. I'm sure others have come up with solutions for this, but mine ultimately required an additional tag to the front-matter of the markdown Jekyll Pages like this:

```markdown
{% raw %}
---
title: "Distributed Thinking Systems Blog"
layout: page
menu_item: Blog
permalink: /blog/
---
{% endraw %}
```

I had to create my own variable in the front-matter for "menu-item" which would be how the menu item would appear.

```markdown
{% raw %}
      <nav class="site-nav">
        <input type="checkbox" id="nav-trigger" class="nav-trigger" />
        <label for="nav-trigger">
          <span class="menu-icon">
            <svg viewBox="0 0 18 15" width="18px" height="15px">
              <path d="M18,1.484c0,0.82-0.665,1.484-1.484,1.484H1.484C0.665,2.969,0,2.304,0,1.484l0,0C0,0.665,0.665,0,1.484,0 h15.032C17.335,0,18,0.665,18,1.484L18,1.484z M18,7.516C18,8.335,17.335,9,16.516,9H1.484C0.665,9,0,8.335,0,7.516l0,0 c0-0.82,0.665-1.484,1.484-1.484h15.032C17.335,6.031,18,6.696,18,7.516L18,7.516z M18,13.516C18,14.335,17.335,15,16.516,15H1.484 C0.665,15,0,14.335,0,13.516l0,0c0-0.82,0.665-1.483,1.484-1.483h15.032C17.335,12.031,18,12.695,18,13.516L18,13.516z"/>
            </svg>
          </span>
        </label>

        <div class="trigger">
          {%- for path in page_paths -%}
            {%- assign my_page = site.pages | where: "path", path | first -%}
            {%- if my_page.title -%}
            <a class="page-link" href="{{ my_page.url | relative_url }}">{{ my_page.`menu_item` | escape }}</a>
            {%- endif -%}
          {%- endfor -%}
        </div>
      </nav>
{% endraw %}
```

This fixed the issue, but created more items I need to put in my Font Matter for my Jekyll markdown. There were a number of places I had to come up with custom solutions, such as the [Emergency Services](/resources/emergency-resources/) page.  I ended up using a data file, but getting the grouping to work out was a nightmare and several days of working with GPT-4o, and then the new o1 models came out and I decided to use it. The o1-preview had the issue solved in about 2 hours with a nice, fully functional solution..

I ended up using a data file structured like this:

```yaml
countries:
  - name: "USA"
    services:
      - { service: "Emergency Services", contact: "911" }
      - { service: "National Suicide Hotline", contact: "1-800-273-8255" }
      - { service: "Crisis Text Line", contact: "Text HOME to 741741" }
  - name: "UK"
    services:
      - { service: "NHS Helpline", contact: "111" }
      - { service: "Samaritans", contact: "116 123" }
  - name: "Australia"
    services:
      - { service: "Lifeline Australia", contact: "13 11 14" }
      - { service: "Beyond Blue", contact: "1300 22 4636" }
 ```

 To allow additional entries to be added with minimal effort, I ended up using a YAML file. The corresponding page for emergency-services.md had to have som custom liquid code adde to make the table display correctly along with SCSS code. The JEqually Liquid code I used looks like this:

```markdown
{% raw %}
{% assign row_class = "odd" %}
<table>
  <thead>
    <tr>
      <th>Country</th>
      <th>Service</th>
      <th>Contact Number</th>
    </tr>
  </thead>
  <tbody>
    {% for country in site.data.countries.countries %}
      <!-- First service row for the country -->
      <tr class="{{ row_class }}">
        <td><strong>{{ country.name }}</strong></td>
        <td>{{ country.services[0].service }}</td>
        <td>{{ country.services[0].contact }}</td>
      </tr>

      <!-- Additional services for the country -->
      {% for service in country.services offset:1 %}
        <tr class="{{ row_class }}">
          <td></td>
          <td>{{ service.service }}</td>
          <td>{{ service.contact }}</td>
        </tr>
      {% endfor %}

      <!-- Alternate row classes -->
      {% if row_class == "odd" %}
        {% assign row_class = "even" %}
      {% else %}
        {% assign row_class = "odd" %}
      {% endif %}
    {% endfor %}
    </tbody>
  </table>
{% endraw %}
```

But it allowed me to make the grouping appear as it should.  All services in the country under a single color and no country name in the first column other than the first one.  This was no small feat on my part to get GPT-4o to do it, and in fact=, it took the o1-preview to do it. I will say that I am extremely impressed with the new o1 models and how they work.  They have saved me a lot of time and effort, and I would probably still be making small changes, unable to be where I am now.


Ultimately, I want to get back to coding and producing functional code for projects rather than a web site.

{% include join_us.html %}

{% include getintouch.html %}
