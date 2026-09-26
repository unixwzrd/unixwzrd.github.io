# Project catalog lab

This exercise runs a frozen copy of the site's `utils/bin/fetch_og.py` with invented repositories in a temporary directory. The runner replaces GitHub fetching and image rendering with local stubs. It does not read or write the real site's catalog or pages, and it makes no network request.

The copy is here to show the current generator's data merge, visibility, ordering, and first-page scaffolding. It is a teaching snapshot, not an installable project-publishing package.

Run with Python 3 and the generator's existing Python dependencies (`requests`, `PyYAML`, and `beautifulsoup4`):

```bash
python3 run_lab.py
python3 run_lab.py --reorder
python3 run_lab.py --show-hidden
```

Each run prints the generated project entries in catalog order, whether each one has a repository link, the final ExampleTool description, and the starter files. `--reorder` moves QuietTool to the first generated position. `--show-hidden` changes HiddenTool from `none` to `public`, adding a generated repository URL. These are changes to the invented inputs; they do not render Jekyll's menus. Each run ends with `PASS: ordered projects, visibility, overrides, and new-project scaffolding`. All generated files are discarded when the temporary directory closes.
