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

Hands-On 2A reuses the Part 2 banner and preview-path SVG. Its caption explicitly limits the exercise to the content switch; the full production-build, indexing, and process stages in the diagram belong to the real site wrapper and are not reproduced by the lab.

## Part 3 additions

The local Part 3 draft uses `html/assets/images/blog/jekyll-site-tooling/post-03-shared-layouts-hero.png`, `post-03-layout-chain.svg`, and `post-03-metadata-contract.svg`. PNG companions are retained for both diagrams. Their editable sources are `docs/publication/diagrams/src/jekyll-post-03-layout-chain.dot` and `jekyll-post-03-metadata-contract.dot`.

The banner was generated with the built-in imagegen tool using this prompt:

> Create a finished wide 2:1 editorial banner illustration for the third article in a dark engineering-blog series about a customized Jekyll website. Make it visually consistent with tactile publishing-workbench artwork: deep charcoal and navy, restrained amber and cool teal highlights, realistic paper/card material and precise mechanical details. Show one authored project page or simple sheet at the left passing through three visibly nested reusable frames/layers, branching into a coherent site header, project detail card, and blog-list cards on the right. The image should communicate composition and reuse, not a literal flowchart. Clear silhouettes at thumbnail size, sophisticated quiet workbench mood, generous crop-safe edges. No people, no readable text, no letters, no code, no logos, no fake UI labels, no AI brain, no neon cyberpunk.

Render the diagrams from the repository root:

```bash
dot -Tsvg docs/publication/diagrams/src/jekyll-post-03-layout-chain.dot -o html/assets/images/blog/jekyll-site-tooling/post-03-layout-chain.svg
dot -Tpng -Gdpi=150 docs/publication/diagrams/src/jekyll-post-03-layout-chain.dot -o html/assets/images/blog/jekyll-site-tooling/post-03-layout-chain.png
dot -Tsvg docs/publication/diagrams/src/jekyll-post-03-metadata-contract.dot -o html/assets/images/blog/jekyll-site-tooling/post-03-metadata-contract.svg
dot -Tpng -Gdpi=150 docs/publication/diagrams/src/jekyll-post-03-metadata-contract.dot -o html/assets/images/blog/jekyll-site-tooling/post-03-metadata-contract.png
```

The first diagram is limited to the project-page layout path and includes verified in current source; it is not a full runtime graph. The second distinguishes metadata consumed during rendering from the smaller tags/content-type subset enforced by the current taxonomy validator.

Hands-On 3A reuses the Part 3 banner and metadata-contract SVG. Its caption scopes the lab to the checked tags/content-type branch; the other diagram branches remain outside the runnable exercise.

## Part 4 additions

The local Part 4 draft uses `html/assets/images/blog/jekyll-site-tooling/post-04-stable-urls-hero.png` and `post-04-url-contract.svg`; the diagram also has a PNG companion. Its editable source is `docs/publication/diagrams/src/jekyll-post-04-url-contract.dot`. Hands-On 4A reuses both visual assets and explicitly scopes its runnable exercise to the short-link branch.

The banner was generated with the built-in imagegen tool using this prompt:

> Create a finished wide 2:1 editorial banner illustration for Part 4 of a dark engineering-blog series about a customized Jekyll website. Match the established tactile publishing workbench mood: deep charcoal/navy, restrained warm amber and cool teal highlights, realistic paper/card material, precise mechanical details, generous crop-safe negative space. Depict one durable central published page card with a subtle golden anchor or fixed metal pin, while a paper source sheet changes position on the workbench and two older paths feed toward the anchored page through slim physical guide channels. A small separate short-link token also points to the same page. Communicate stable public identity amid moving source material, without making a literal flowchart. Crisp silhouettes readable at thumbnail size. No people, no readable text, no letters, no numbers, no code, no logos, no fake UI labels, no AI brain, no neon cyberpunk.

Render the diagram from the repository root:

```bash
dot -Tsvg docs/publication/diagrams/src/jekyll-post-04-url-contract.dot -o html/assets/images/blog/jekyll-site-tooling/post-04-url-contract.svg
dot -Tpng -Gdpi=150 docs/publication/diagrams/src/jekyll-post-04-url-contract.dot -o html/assets/images/blog/jekyll-site-tooling/post-04-url-contract.png
```

The figure depicts only the project-post canonical route, a declared legacy redirect, and a basis-derived short redirect. It does not imply that an ordinary series post gets a `permalink_slug` or that the isolated lab writes redirect HTML.

## Part 5 additions

Part 5 and Hands-On 5A use `html/assets/images/blog/jekyll-site-tooling/post-05-project-catalog-hero.png`. The editable data-flow figure is `docs/publication/diagrams/src/jekyll-post-05-publishing-paths.dot`, rendered as `post-05-publishing-paths.svg` and `.png`. The figure keeps the project generator, Blog section YAML, and front-matter/discovery paths separate.

The banner was generated with the built-in imagegen tool using this prompt:

> Create a finished wide 2:1 editorial banner illustration for Part 5 of a dark engineering blog series about a customized Jekyll website. Match the established tactile publishing workbench aesthetic: deep charcoal/navy background, restrained warm amber and cool teal highlights, realistic paper/card material, precise mechanical details, generous crop-safe negative space. Show a single tidy catalog sheet on a workbench feeding a small mechanical publishing apparatus; from it emerge a polished project card, a project landing page with several update cards, and an orderly navigation strip. Alongside it, a second smaller stack of section cards feeds a separate navigation strip. Convey controlled organization and build-time assembly, not a literal flowchart. Crisp silhouettes readable at thumbnail size. No people, no readable text, no letters, no numbers, no code, no logos, no fake UI labels, no AI brain, no neon cyberpunk.

Render the diagram from the repository root:

```bash
dot -Tsvg docs/publication/diagrams/src/jekyll-post-05-publishing-paths.dot -o html/assets/images/blog/jekyll-site-tooling/post-05-publishing-paths.svg
dot -Tpng -Gdpi=150 docs/publication/diagrams/src/jekyll-post-05-publishing-paths.dot -o html/assets/images/blog/jekyll-site-tooling/post-05-publishing-paths.png
```

## Part 6 additions

Part 6 uses `html/assets/images/blog/jekyll-site-tooling/post-06-diagrams-and-source-hero.png`. Its two figures separate the editable-diagram/render/viewer route from the source-file/highlight/download route. Their editable sources are `html/assets/code/jekyll-site-tooling/post-06/jekyll-post-06-diagram-path.dot` (Graphviz) and `jekyll-post-06-source-path.mmd` (Mermaid). The article exposes these same source files through its collapsed source viewer, with explicit downloads. Each has SVG and PNG renders in the blog image asset directory. The Mermaid SVG's percentage width is replaced with numeric width and height from its `viewBox`, matching the publication convention documented in `docs/templates/blog-templates.md`.

The banner was generated with the built-in imagegen tool using this prompt:

> Create a finished wide 2:1 editorial banner illustration for Part 6 of an established dark engineering-blog series about extending a Jekyll website. Match a tactile publishing workbench mood: deep charcoal/navy background, restrained warm amber and cool teal highlights, realistic paper/card material, precision tools, gentle depth, generous crop-safe negative space. On the workbench show one editable technical diagram sheet and one code manuscript becoming two finished article elements: a crisp dark-canvas diagram panel with distinct connected shapes, and a neatly folded source-code panel with an explicit small download-tab shape. A magnifying frame or desk loupe suggests that the diagram can be opened larger. The transformation should feel mechanical and editorial rather than magical or a literal flowchart. Crisp silhouettes at thumbnail size. No people, no readable text, no letters, no numbers, no code glyphs, no logos, no fake UI labels, no AI brain, no neon cyberpunk.

Render both figures from the repository root with the authoring helper, which writes SVG and PNG and normalizes Mermaid SVG dimensions:

```bash
python3 utils/bin/render-blog-diagram.py html/assets/code/jekyll-site-tooling/post-06/jekyll-post-06-diagram-path.dot html/assets/images/blog/jekyll-site-tooling/post-06-diagram-path
python3 utils/bin/render-blog-diagram.py html/assets/code/jekyll-site-tooling/post-06/jekyll-post-06-source-path.mmd html/assets/images/blog/jekyll-site-tooling/post-06-source-path
```
