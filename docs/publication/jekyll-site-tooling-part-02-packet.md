# Part 2: A Local Jekyll Server I Can Actually Operate

Status: Part 2 local browser draft prepared September 23, 2026. On September 25 the Publisher asked to finish it and add a Hands-On companion if useful. Hands-On 2A is now in the local post tree and linked from Part 2. Both October 1 dates are provisional and supply a future-dated series preview. The Publisher has published Part 1; this packet does not record remote publication of Part 2 or 2A.

## Source inventory and claim boundaries

| Source | What it establishes | Limit |
| --- | --- | --- |
| `utils/bin/jekyll-site` | `start`, `restart`, `build`, `stop`; refresh flags; PID and port checks; production build followed by development serve; default inclusion flags and `--current` | Source behavior only. This turn did not invoke the wrapper or test stop/restart/process handling |
| `_config.yml` | Jekyll configuration is not reloaded by `serve`; source is `html`; pretty permalink routing | Do not generalize that every watched file behaves like configuration |
| `html/_includes/series_index.html` | Excludes drafts, unpublished posts, and `_drafts` paths from series listing; sorts main posts by `series_order` | A served draft need not be listed as a series installment |
| `html/_includes/series_navigation.html` | Supports previous and next links, and a scheduled-next label when the next post is absent from `site.posts` | Future-post presence differs between preview and normal production output |
| `docs/guides/service-management.md`, `CHANGELOG.md` | Historical motivation and documented operations | The guide includes old watcher and `status` claims; the Publisher confirms FileWatcher is not in use |
| Running local Jekyll preview | Part 2 and the series landing return HTTP 200 and the article and art are rendered | Local browser availability is not a production or deployed-site test |

## Fact table

| Article claim | Disposition |
| --- | --- |
| Default `start` includes future, draft, unpublished material; `--current` omits those flags | Confirmed in current wrapper |
| Both preview modes use `JEKYLL_ENV=development` | Confirmed in current wrapper |
| Wrapper builds with `JEKYLL_ENV=production` and runs Pagefind before serving | Confirmed in current wrapper; subsequent watched rebuilds were not proven to reindex search |
| `start` refreshes project OG data by default; `restart` skips refresh by default; `-r` forces and `-n` wins conflicts | Confirmed in current wrapper |
| Wrapper checks PID and port, may terminate a port occupant, and replaces generated build output | Confirmed in current wrapper; not tested at runtime in this turn |
| Ordinary content edits are watched by the active Jekyll server; `_config.yml` needs restart | Observed local post appears without wrapper restart; configuration restart instruction in `_config.yml` |
| FileWatcher is part of the active loop | Rejected by Publisher correction; omitted from active workflow |
| `jekyll-site status` exists | Rejected by command parser; not offered in article |

## Privacy and drift review

The article contains no environment values, private paths, project catalog rows, credentials, recipients, service identifiers, or logs. It uses repository-relative command names and generic feature descriptions. It does not claim a scheduled service, successful public search, measured reliability, or deployment. The port's exact number is unnecessary and omitted. The older service guide's watcher and `status` sections are treated as drift, not current operating instructions. `--current` is described as a content view, not an exact production build.

## Narrative outline and handoff

Open with the concrete irritation of an invisible future post. Explain the two editorial questions and how the wrapper's inclusion flags answer them. Trace the build-and-serve stages with one diagram, then distinguish ordinary watched edits from restart and refresh decisions. Close by treating preview as one review step and leading into the layout hierarchy in Part 3.

The local post is `html/_posts/series/beyond-static-building-a-publication-system-around-jekyll/2026-10-01-a-local-jekyll-server-i-can-actually-operate.md`. The rendered route is `/technology/2026/10/01/a-local-jekyll-server-i-can-actually-operate/`. The date and title remain editorial choices until the Publisher accepts them. Part 1's next-link metadata now points to the provisional Part 2 route so preview navigation works and a production build can show its scheduled date before release. No commit, push, or deployment occurred in this drafting turn.

## Hands-On 2A companion

The local companion is `html/_posts/series/beyond-static-building-a-publication-system-around-jekyll/2026-10-01-hands-on-build-a-jekyll-preview-switch.md`, rendered at `/hands-on/2026/10/01/hands-on-build-a-jekyll-preview-switch/`. Its ten-file package lives under `html/assets/code/jekyll-site-tooling/post-02a/preview-lab/`; a reproducibly ordered ZIP and SHA-256 file are next to it. The parent post links the companion, and the series landing lists it under Hands-On Companions.

The lab uses an invented site with one ordinary, one future, one draft, and one unpublished post. `preview.sh current` omits inclusion flags and `preview.sh review` passes `--future --drafts --unpublished`. `verify.sh` checks the generated index, not merely Jekyll's exit status. The extracted archive passed the checksum and verification run under the checkout's Ruby/Jekyll environment. A changed-date negative case failed with `current view unexpectedly contains FUTURE-POST-MARKER`, as intended. The exercise uses `jekyll build`, with fixed destinations inside the package and no server/process management. It does not prove the full website wrapper or deployed site behavior.

The Publisher asked whether 2A reflects current operation. The article and packaged README now map the lab's two inclusion modes directly to `jekyll-site start` and `start --current`, and identify the production build, Pagefind index, optional metadata refresh, development server, and PID handling that the lab intentionally leaves out. They also explain why a preview-visible future post is not automatically present in the Pagefind index. This is a source-backed relationship to the active wrapper, not a claim that the toy lab duplicates it.
