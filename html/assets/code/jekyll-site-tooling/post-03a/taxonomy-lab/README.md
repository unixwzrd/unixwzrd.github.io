# What the metadata check actually catches

This is an invented Jekyll site that carries a frozen copy of this website's `03_tag_taxonomy_validator.rb` plugin. The sample taxonomy is small, but the validation code is the same as the site version inspected for Part 3. The lab demonstrates what that code rejects and what it does not check. It does not run this website's pre-commit hooks, project generator, or publishing workflow.

Requirements: Ruby, Bundler, and Jekyll 4.3-compatible gems. From this directory:

```bash
bundle install
./run_lab.sh
```

Expected result:

```text
PASS valid: accepted
PASS unknown-tag: rejected
PASS alias-tag: rejected
PASS duplicate-tag: rejected
PASS unknown-content-type: rejected
PASS missing-series-order: accepted
PASS draft-with-old-tag: accepted
```

`run_lab.sh` copies the fixture into separate case directories under `out/`, adds one invented post per case, and builds each case with its own generated destination. It checks the exit status and the expected error text. Logs and rendered output stay under `out/` for inspection. All names, posts, and taxonomy values are invented.

The deliberately missing `series_order` passes because the current taxonomy plugin checks tags and `content_type`, not every series field. The draft with an old tag passes with `--drafts` because the plugin skips actual `_drafts` paths. Neither pass means that post is ready for publication. Move a draft into `_posts` and it becomes subject to the tag check. The real site's templates, project lookup, URL rules, images, and editorial review are outside this small fixture.

The frozen plugin is `site/_plugins/03_tag_taxonomy_validator.rb`, copied unchanged from this site's source with SHA-256 `f8734a26c65ece8d1c206ffa0a1d4756d6fdadaeb73af56c96f356d8369e39d7`. Compare it with the current website source before reusing the exercise after the site code changes; the article's results were verified against the snapshot packaged with it.
