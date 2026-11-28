# unixwzrd.github.io

Personal Jekyll workspace for **[unixwzrd.ai](https://unixwzrd.ai)**. This README focuses on **tooling** in the repo; it is not a catalog of site topics or pages.

- [unixwzrd.github.io](#unixwzrdgithubio)
  - [Tooling](#tooling)
  - [Site source](#site-source)
  - [Contributing](#contributing)
  - [License and use](#license-and-use)


## Tooling

Maintained tooling lives under **`utils/`**: operator commands, Jekyll authoring helpers, validation, monitoring, and automated tests. Commands and tutorials use these canonical paths directly; there is no root scripts directory or compatibility-symlink layer.

| Doc or directory | What it is |
|------------------|------------|
| [utils/README.md](utils/README.md) | **Index of utilities** - checks, `fetch_og`, monitors, fix-ups, with clickable paths. |
| [docs/guides/reference-utilities.md](docs/guides/reference-utilities.md) | Operator quick reference (env, commands, file locations). |
| [docs/tools/pre-commit-checks.md](docs/tools/pre-commit-checks.md) | `check_site.sh` and `utils/bin/checks/` pipeline. |
| [docs/README.md](docs/README.md) | Documentation index (deploy, publishing, templates, monitoring). |
| [utils/tests/](utils/tests/) | Canonical Ruby, Python, and browser regressions; manual side-effect diagnostics are separate. |

**Typical checks:** from repo root, `utils/bin/check-site test` runs deterministic regressions. `utils/bin/check-site test --site /absolute/path/to/production-build` also verifies rendered output. `utils/bin/check-site checks` runs the existing numbered local pipeline, including checks that can build or normalize files. Both commands select the existing local project environments when available and never install missing packages.

**Artifact housekeeping:** `utils/bin/check-site artifacts` reports old browser diagnostics without deleting anything. See the [maintenance guide](docs/guides/maintenance.md) for review manifests and the explicit removal mechanism.

## Site source

Jekyll source lives in [`html/`](html/). It powers the public site and is **not** offered as a template or for wholesale reuse.

## Contributing

**Tooling only:** suggestions, issues, or PRs that improve `utils/` or shared automation/docs are welcome.

**Not soliciting:** drive-by edits to public site copy, layout, or branding in `html/` (unless we've agreed otherwise).

## License and use

- **`html/`** (pages, posts, assets, site-specific copy): **all rights reserved** - not licensed for copying or republishing the site as yours.
- **`utils/`**: MIT License - see [LICENSE](LICENSE). Tools moved from the former scripts directory retain their existing MIT license.

---

**Updated:** 2026-11-27



