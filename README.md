# unixwzrd.github.io

Personal Jekyll workspace for **[unixwzrd.ai](https://unixwzrd.ai)**. This README focuses on **tooling** in the repo; it is not a catalog of site topics or pages.

- [unixwzrd.github.io](#unixwzrdgithubio)
  - [Tooling](#tooling)
  - [Site source](#site-source)
  - [Contributing](#contributing)
  - [License and use](#license-and-use)


## Tooling

Most reusable value for others is under **`utils/`** (validation, OpenGraph / project cards, monitoring, fixes) and **`scripts/`** (Jekyll helpers).

| Doc or directory | What it is |
|------------------|------------|
| [utils/README.md](utils/README.md) | **Index of utilities** - checks, `fetch_og`, monitors, fix-ups, with clickable paths. |
| [docs/guides/reference-utilities.md](docs/guides/reference-utilities.md) | Operator quick reference (env, commands, file locations). |
| [docs/tools/pre-commit-checks.md](docs/tools/pre-commit-checks.md) | `check_site.sh` and `utils/bin/checks/` pipeline. |
| [docs/README.md](docs/README.md) | Documentation index (deploy, publishing, templates, monitoring). |
| [scripts/](scripts/) | e.g. short-link front matter backfill - see [docs/templates/blog-templates.md](docs/templates/blog-templates.md). |

**Typical checks:** from repo root, `./utils/bin/check_site.sh` (after `bundle install` and your usual Ruby/Python env).

## Site source

Jekyll source lives in [`html/`](html/). It powers the public site and is **not** offered as a template or for wholesale reuse.

## Contributing

**Tooling only:** suggestions, issues, or PRs that improve `utils/`, `scripts/`, or shared automation/docs are welcome.

**Not soliciting:** drive-by edits to public site copy, layout, or branding in `html/` (unless we've agreed otherwise).

## License and use

- **`html/`** (pages, posts, assets, site-specific copy): **all rights reserved** - not licensed for copying or republishing the site as yours.
- **`utils/`** and **`scripts/`**: MIT License - see [LICENSE](LICENSE).

---

**Updated:** 2026-05-02


