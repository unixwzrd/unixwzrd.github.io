---
short_url: "https://unixwzrd.ai/s/2d11ffe75d/"
short_link_basis: "/_posts/series/beyond-static-building-a-publication-system-around-jekyll/2026-10-22-from-a-yaml-project-catalog-to-a-project-publishing-system.md"
layout: post
title: "From a YAML Project Catalog to a Project Publishing System"
date: 2026-10-22 08:00:00 -0500
categories: [technology]
tags: [jekyll, website-development, developer-workflow, automation]
excerpt: "A project is more than one page here. I wanted one catalog entry to lead to a card, a place in navigation, a landing page, and a blog for its updates."
series: "Beyond Static: Building a Publication System Around Jekyll"
series_part: 5
series_order: 50
series_total: 10
series_url: /blog/series/beyond-static-building-a-publication-system-around-jekyll/
series_previous_title: "Stable URLs in a Repository That Keeps Moving"
series_previous_url: /technology/2026/10/15/stable-urls-in-a-repository-that-keeps-moving/
series_next_title: "Diagrams and Source Code That Behave Like Editorial Content"
series_companion_title: "Hands-On: Follow a Project Through the Catalog"
series_companion_url: /hands-on/2026/10/22/hands-on-follow-a-project-through-the-catalog/
series_companion_date: 2026-10-22 10:00:00 -0500
image: /assets/images/blog/jekyll-site-tooling/post-05-project-catalog-hero.png
---

Jekyll started out looking like a way to publish a blog. I still have blog posts, but there is no longer one stream that makes sense for everything on this site. A technical article, a tutorial, a series installment, and an update about one of my projects have different jobs. I wanted readers to find each one where it belongs without maintaining a second website every time the material grew.

Projects were where that problem got particularly irritating. Adding one meant more than writing a page. It needed a card on the Projects page, a sensible place in the menu, its own landing page, and somewhere for later updates to go. If I had to hand-edit all those places each time, I knew they would drift apart. So I built a catalog and let the site assemble the repeated parts from it.

<!--more-->

## One Project, Several Places to Find It

Suppose I add an invented project called Example Tool. Its entry goes in the ordered `repositories` list in `repos.yml`. That is the authored input. The entry identifies the repository and can carry overrides for things I want to control myself, such as its title, description, visibility, or image. I can move the entry in that list when I want it to appear earlier or later among projects.

The `fetch_og.py` generator reads that list. It tries to fetch repository metadata, combines the result with my overrides, prepares an image, and writes the processed entries to `github_projects.yml`. It keeps the order of successfully processed entries; it does not alphabetize them on the way out. This is a separate refresh step, not something that runs merely because a reader opens a page or because Jekyll sees a YAML edit.

I originally used GitHub's OG thumbnail information for this kind of presentation. Rate limiting made that a poor thing to depend on for every card, so I started generating the project card images locally. The current generator still asks GitHub for repository data when it can. An explicit image override, an existing local image, and fallback paths are still part of the implementation. “Local card” describes the presentation path, not a promise that the whole refresh is offline.

On a new project, the generator also creates a project landing page and directories for that project's `_posts` and `_drafts`. It leaves a draft template and a starter introduction. That introduction is a starting point for me to edit; it is not an article I would consider finished just because a script wrote it. The main generator calls this scaffolding when the landing page is absent. If a landing page already exists, a later run does not act as a general repair tool for every missing child file.

{% include blog_diagram.html
   src="/assets/images/blog/jekyll-site-tooling/post-05-publishing-paths.svg"
   alt="The ordered repos YAML file feeds the project generator, which writes project data consumed by the Projects menu, grouped Projects page, and project pages. A separate ordered blog sections YAML file feeds Blog navigation and hub views. Post front matter drives series and discovery lists."
   caption="Three inputs solve different placement problems; no single YAML file controls the whole site."
   variant="series" %}

## The Menu Is a View of the Data

The header includes a shared navigation template. In the Projects dropdown, “All Projects” is fixed at the top; then Liquid walks the generated project list and shows entries whose visibility is not `none`. The Projects page reads that same generated list, but it presents private projects and public projects in separate groups. Moving Example Tool in the authored catalog changes its relative position in the menu after a successful refresh and build. On the page, its relative order changes *within its visibility group*. The grouping is another presentation decision.

Visibility needs careful wording here. A public project can have its repository link shown. A private one can still have a project page and appear in the inspected list and menu, but those views omit its repository link. An entry marked `none` is filtered from those views. These are display choices, not access controls, and hiding a menu item does not prove that a previously generated page or file disappeared from the site. I still have to decide what content is safe to publish.

The Blog dropdown is a different path. It starts with fixed “Blog Home” and “All Posts” links, then reads the visible sections from `blog_sections.yml` in file order, and ends with fixed “Topics.” The Blog hub uses those same visible section entries for its cards and recent lists. So I can reorder the middle of that menu by editing YAML, but the fixed links stay where the template puts them. The General section is configured today with `visible: false`; that keeps it out of these views without deleting its page or posts.

This is the part I like about the result. The finished site is static, but I do not have to hard-code every card and dropdown item. Liquid and the generated data assemble them during the build. A YAML edit becomes a different set of HTML pages on the next build; nothing is querying a live database in the reader's browser.

## A Project Gets Its Own Blog

The project landing page uses the `project` layout. Its `category` front-matter value lets the shared project lookup find the generated metadata, and the layout passes that category to the shared blog list. When I write an update under Example Tool's project posts, it can appear on that project's page without me building another blog application. The same post can also be found through broader discovery routes where it belongs.

That is one reason I do not think of the site as “the blog” anymore. There is a Technology section for standalone technical writing, a Hands-On section for exercises, series landing pages that gather related installments, the Parental Alienation section, project update blogs, and an all-posts archive that crosses those routes. Hands-On posts can sit beside a Technology installment in its series without filling the ordinary Technology index with lab instructions. The configured Blog hub's Series recent list currently selects the Local First AI series, while the `/blog/series/` directory discovers all series landing pages. Those two views answer different questions.

Order has several meanings as well. Catalog order controls projects before the Projects page splits them into groups. Section order controls the Blog menu and hub. `series_order` gives a reader a deliberate path through a series, including its lettered Hands-On companions. The archive and shared post lists use their own discovery ordering, which can account for an update notice and later modification time. I do not want an article revised today to be mistaken for a brand-new installment in the series; nor do I want its useful update buried simply because the original publication date was older.

## Front Matter Is Part of the Wiring

Part 3 showed how the layouts and includes avoid repeating page markup. Front matter is how I tell those shared pieces what a particular page *is*. The `category` on a project landing page connects it to its data and update list. A series post can declare its series, `series_order`, neighboring installments, and a Hands-On companion. An image gives the card and page a banner. An update notice with `last_modified_at` can affect discovery presentation. Optional audio has its own publishing path. The short-link basis from Part 4 gives a shared URL an identity that can survive a source move.

I can add another front-matter key whenever the site needs one. But a key by itself does nothing. Some Liquid include, layout, plugin, or checker has to read it, and I need to know which view it changes. `tags` are a separate topical vocabulary; adding a custom key does not automatically make it a tag or mean the current taxonomy check validates it. That distinction keeps the flexibility useful instead of turning the top of every Markdown file into a bag of unexplained switches.

## What I Still Have to Do

The catalog saves me from repeating the structure. It does not write a good project introduction, review a private description for disclosure, or guarantee that a failed metadata fetch produced a card. It also does not refresh itself on every normal Jekyll build. I run the generator when project data needs updating, inspect what it wrote, edit the starter content, and check the resulting site.

The [Hands-On 5A companion]({{ page.series_companion_url | relative_url }}) runs the generator on invented repositories without touching this catalog or calling GitHub. It makes the order, overrides, visibility fields, and starter files visible in one small run.

## Current State

The payoff is that Example Tool can have a coherent home. Its catalog entry can become generated metadata and a card; shared Liquid can place it in the Projects menu and page; its landing page can collect its own updates. Then the wider Blog sections, series pages, and archive offer other routes for readers who did not start at the Projects menu. It took Python, YAML, Liquid, layouts, and front matter to get there, but each piece has a job I can point to.

## Next Work

Once the right content lands in the right place, it still has to be readable. Part 6 turns to diagrams and source code: how I stopped treating them as awkward attachments and made them part of the article itself.
