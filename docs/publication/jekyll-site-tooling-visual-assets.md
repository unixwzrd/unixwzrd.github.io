# Jekyll Series Part 1 Visual Assets

Created September 22, 2026 for local browser review of Part 1 and its landing page. The current article consumes the SVG figures; PNG renders are kept as inspectable companions. The banner is a generated raster asset and has no deterministic regeneration guarantee.

| Role | Workspace asset | Source |
| --- | --- | --- |
| Shared Part 1 and landing banner | `html/assets/images/blog/jekyll-site-tooling/post-01-publishing-workbench-hero.png` | Built-in imagegen, prompt below |
| Project publishing path | `html/assets/images/blog/jekyll-site-tooling/post-01-project-flow.svg` and `.png` | `docs/publication/diagrams/src/jekyll-post-01-project-flow.dot` |
| Project-post URL identity | `html/assets/images/blog/jekyll-site-tooling/post-01-url-identity.svg` and `.png` | `docs/publication/diagrams/src/jekyll-post-01-url-identity.dot` |

The banner was generated with the built-in imagegen tool, then copied into the website assets. Final prompt:

> Create a finished wide editorial banner illustration for a dark-themed engineering blog article about extending a Jekyll website, titled in the webpage (not in the image) 'Jekyll, One Problem at a Time'. Use-case: stylized-concept. Landscape 2:1 composition, intended crop around 1600x800. Depict a thoughtful, tactile publication workbench: a central stack of clean modular page templates and Markdown sheets feeding through a precise small mechanical publishing apparatus, branching into distinct finished web-page cards, a project tile, a navigation strip, and a diagram frame. One subtle golden thread connects each stage, expressing repeated small fixes becoming a coherent publishing workflow. Background deep charcoal/navy, restrained warm amber and cool teal highlights to match a sophisticated dark engineering site; realistic material texture, crisp silhouettes, gentle depth, uncluttered composition. Make the central forms readable even at article-card thumbnail size. No people, no code text, no letters, no words, no logos, no fake UI labels, no AI brain imagery, no neon cyberpunk, no stock-photo look. Leave some calm negative space around the edges so the site can crop responsively.

Render the DOT sources from the repository root:

```bash
dot -Tsvg docs/publication/diagrams/src/jekyll-post-01-project-flow.dot -o html/assets/images/blog/jekyll-site-tooling/post-01-project-flow.svg
dot -Tpng -Gdpi=150 docs/publication/diagrams/src/jekyll-post-01-project-flow.dot -o html/assets/images/blog/jekyll-site-tooling/post-01-project-flow.png
dot -Tsvg docs/publication/diagrams/src/jekyll-post-01-url-identity.dot -o html/assets/images/blog/jekyll-site-tooling/post-01-url-identity.svg
dot -Tpng -Gdpi=150 docs/publication/diagrams/src/jekyll-post-01-url-identity.dot -o html/assets/images/blog/jekyll-site-tooling/post-01-url-identity.png
```

The project diagram distinguishes authored catalog input, generated data and cards, conditional scaffolding, and the Liquid views. The URL diagram is scoped to project posts, for which publication date and `permalink_slug` define the canonical route. Both diagrams use a dark canvas, have alternative text in the article, and open through the site's full-size viewer.

Browser review on the running local Jekyll server found the banner and both SVGs loaded. At a 1280-pixel viewport the labels were visible in context. At a 390-pixel viewport the figures scaled within the page and their labels became small; the full-size viewer link remains the readable route on narrow screens. This is a known presentation limit of wide diagrams, not evidence that the viewer itself was tested on a phone.

## Part 2 additions

The local Part 2 draft uses `html/assets/images/blog/jekyll-site-tooling/post-02-local-preview-hero.png` and `post-02-preview-path.svg`. A PNG companion is retained at `post-02-preview-path.png`; the Graphviz source is `docs/publication/diagrams/src/jekyll-post-02-preview-path.dot`.

The banner was generated with the built-in imagegen tool using this prompt:

> Create a finished wide editorial banner illustration for a dark-themed engineering blog post about operating a local Jekyll preview server. Landscape 2:1 composition, intended crop around 1600x800. Make it visually related to a refined tactile publishing-workbench series: two distinct clean page views on one desktop workbench, one view suggesting upcoming editorial material through a subtle translucent amber layer, the other showing a crisp current-publication view in cool teal; a small restrained mechanical switch or lever links them, with a quiet stack of markdown pages feeding the preview apparatus. The workbench should feel hands-on and practical, not magical. Deep charcoal/navy background, warm amber and cool teal accents, realistic material texture, crisp readable silhouettes at thumbnail size, moderate negative space at the edges. No people, no code text, no letters, no words, no logos, no fake UI labels, no AI brain imagery, no neon cyberpunk, no stock-photo look.

Render the diagram from the repository root:

```bash
dot -Tsvg docs/publication/diagrams/src/jekyll-post-02-preview-path.dot -o html/assets/images/blog/jekyll-site-tooling/post-02-preview-path.svg
dot -Tpng -Gdpi=150 docs/publication/diagrams/src/jekyll-post-02-preview-path.dot -o html/assets/images/blog/jekyll-site-tooling/post-02-preview-path.png
```

The diagram separates optional metadata refresh, the production build and Pagefind indexing, and the development server's two content modes. It does not imply that Pagefind is regenerated after every watched edit.
