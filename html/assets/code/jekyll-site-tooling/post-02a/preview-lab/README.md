# A tiny Jekyll preview switch

This lab builds an invented four-post site in two modes. It does not run a server, touch your Jekyll site, fetch project metadata, or use the repository's `jekyll-site` wrapper. Output goes only under this lab's `out/` directory.

Requirements: Ruby, Bundler, and Jekyll 4.3-compatible gems. From this directory:

```bash
bundle install
./preview.sh current
./preview.sh review
./verify.sh
```

`current` omits the inclusion flags. Its index should show only `CURRENT-POST-MARKER`. `review` passes `--future --drafts --unpublished`; its index should show all four markers. `verify.sh` checks those claims and exits nonzero if either view is wrong. The fixture's future date is deliberately far ahead so the contrast remains visible for years.

The wrapper uses `jekyll build`, not `jekyll serve`, so the two outputs are easy to compare without a port or a background process. The corresponding serve flags are the same three inclusion switches. A local current-content view is still not a production deployment test; the exercise only proves the fixture's content selection under the Jekyll version you ran.

This is the slice of the actual `utils/bin/jekyll-site` command that the lab models: default `start` serves with `--future --drafts --unpublished`, while `start --current` serves without them. The real command first runs a production build and Pagefind indexing, may refresh project OpenGraph data, then starts a development server and records its PID. `start -n` skips only that metadata refresh; it still builds, indexes, and serves. None of those lifecycle and indexing steps are reproduced here. The lab deliberately leaves `JEKYLL_ENV` unset because it is testing the inclusion flags, not simulating the two environments used by the site wrapper.

The script accepts only `current` and `review`, resolves the package's own directory, and writes to fixed destinations beneath it. If you adapt it for a real site, inspect your build hooks, generated-data steps, destination, and process handling before running it against your own tree.
