# Reusable Packages from the Jekyll Site Tooling Series

Status: packaging proposal for Publisher review, September 25, 2026. No reusable software release or license change is authorized by this document.

## What already exists

Hands-On 2A, 3A, and 4A have downloadable ZIPs, checksums, source viewers, and runnable invented cases. They are teaching fixtures scoped to one mechanism each. They do not install into somebody else's Jekyll site or promise that the site's full pipeline runs there. The series should label them **labs**, not finished plugins or a site starter kit.

The repository's [README](../../README.md) and [LICENSE](../../LICENSE) draw a consequential boundary: `utils/` and `scripts/` are MIT-licensed, while `html/`, including `_plugins`, `_includes`, site assets, and the current lab ZIPs, is all rights reserved. Download access does not itself grant reuse rights. Before inviting readers to copy one of those plugin files, the Publisher would need to grant a package-specific license and ensure the ZIP, repository documentation, and any separate package agree. Do not silently relicense the whole website or assume the existing MIT notice covers `html/`.

## Candidate order

| Candidate | Reader value | Work needed before calling it reusable |
| --- | --- | --- |
| Short-link plugin and redirect checks | Keep compact links on the reader's own domain and retain them through source moves | Extract the hash and redirect behavior from this site's origin and project-post generator ordering; document `jekyll-redirect-from`, basis migration, collisions, and canonical URL changes; test against a clean Jekyll fixture; grant an explicit license for the selected code. Hands-On 4A currently proves only the module's decision logic. |
| Tag taxonomy validator | Enforce a reader-owned canonical tag and content-type vocabulary | Ship an example taxonomy schema, installation instructions, draft policy, and failing/pass cases; test an actual Jekyll build. Hands-On 3A already supplies a narrow plugin exercise, but its taxonomy is invented. Grant an explicit license for the selected plugin. |
| Project publishing starter | Turn a YAML catalog entry into data, a card, a landing page, and a project blog | Separate catalog schema, metadata fetching, image generation, scaffolding, Liquid views, and privacy/visibility policy; replace site paths and branding with configuration; prove reruns preserve authored content. This is a later package, not a copy of `fetch_og.py` plus the entire `html/` tree. |
| Source-code and diagram presentation | Let technical authors show downloadable source and readable diagrams | Extract the filter, include, styles, and viewer behavior together; test path containment and responsive/keyboard behavior in a clean theme. The current pieces depend on this site's layouts and assets. |
| Local service/check runner | Give operators build, preview, and validation commands | Replace site-specific environment sourcing, Ruby/Python paths, project refresh, Pagefind, fixed port, PID handling, and output deletion with explicit options and safe defaults. Split read-only checks from mutating repairs before reuse. Do not package the current wrapper as a drop-in script. |

## First pilot

Start with a **self-contained short-link kit** after the Publisher chooses its license. It is the smallest feature with a clear external use case and an existing lab. Put a clean sample Jekyll site, installable plugin files, a README with the exact front matter and redirect dependency, and a verification command in one versioned archive. Use `site.example` and invented posts. The sample should prove that the same `/s/` route survives a source move when `short_link_basis` stays fixed, that a wrong declared `short_url` fails, and that Jekyll actually writes the redirect to the current canonical page. Check that the archive contains no real project catalog, site credentials, private paths, branding assets, or unpublished posts.

For an initial release, a documented `_plugins` installation and versioned ZIP are simpler to review than a Ruby gem. If multiple independent sites adopt it and the API stabilizes, a plugin gem becomes reasonable. [Jekyll documents both `_plugins` files and gem-based plugins](https://jekyllrb.com/docs/plugins/installation/); this site's [Actions build](../../.github/workflows/jekyll.yml) already runs its custom plugins. A whole-site theme is a separate, much broader choice because Jekyll themes package layouts, includes, and assets too; the current site presentation and copy are not offered as a reusable theme. See [Jekyll's theme packaging guide](https://jekyllrb.com/docs/themes/).

## Acceptance boundary

Call a package reusable only after clean extraction, installation into an unrelated minimal Jekyll site, passing positive and negative behavior checks, generated-output verification, documentation of dependencies and configuration, an explicit license for every included source file, and a privacy review. The series can continue offering smaller teaching labs while those conditions remain open. Publishing an archive, a gem, or a separate repository is a distinct Publisher decision.
