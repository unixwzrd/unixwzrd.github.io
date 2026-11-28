# Utilities reference

The canonical tool inventory is maintained in [utils/README.md](../../utils/README.md). It lists each implementation by its current path relative to utils/, explains intended invocation and effects, separates automated tests from manual diagnostics, and documents artifact-retention boundaries.

## Common entry points

    utils/bin/check-site help
    utils/bin/check-site checks --list
    utils/bin/check-site test
    utils/bin/check-site artifacts

- Use check-site checks for the ordered local site workflow.
- Use check-site test for deterministic source regressions.
- Use check-site test --site PATH to validate an already-rendered site.
- Use check-browser only for a local browser review and only with an existing Playwright CLI.
- Use check-site artifacts for report-only artifact inventory. Deletion requires explicit manifest review and --apply.

## Important distinctions

All maintained tools use their canonical utils/ paths directly. The former root scripts directory and compatibility aliases have been removed; current commands are listed in the catalog.

The diagnostics directory contains manual probes that may use networks, send email, or interact with running services. They are not equivalent to the offline automated test suite.

Some ordered checks validate or normalize source files. Read the listed purpose before selecting a mutating check, and review the working-tree diff afterward.

See [testing](testing.md), [pre-commit checks](../tools/pre-commit-checks.md), and [maintenance](maintenance.md) for operating procedures.

## Article listening and retained narration

The shared CLI commands have distinct purposes. article-tts extracts rendered prose for inspection, local playback, or editorial listening. article-audio manages approved public MP3 narration and its identity manifest.

### Inspect and listen with article-tts

By default, the extractor reads the rendered post-content region. It retains the title, headings, paragraphs, list items, blockquotes, visible link text, and inline-code words. It omits URLs, navigation, diagrams, captions, tables, code blocks, source disclosures, support material, forms, audio, video, and comments.

Inspect exact extracted prose and chunk sizing without calling TTS:

    utils/bin/article-tts http://127.0.0.1:4000/technology/2026/09/08/voice-cloning-across-hosts-making-tts-operational/ --dry-run

Generate and play a retained local copy:

    TTS_BRIDGE_URL=http://127.0.0.1:11440/v1 TTS_BRIDGE_VOICE=narrator utils/bin/article-tts http://127.0.0.1:4000/technology/2026/09/08/voice-cloning-across-hosts-making-tts-operational/ --play

Without --output-dir, article-tts creates a new system temporary directory and prints its location. An explicit directory retains the extracted article, chunk text, chunk WAVs, joined WAV, MP3, and manifest; reusing it can resume completed chunks.

For local browser listening, start the development helper in a separate terminal:

    TTS_BRIDGE_URL=http://127.0.0.1:11440/v1 TTS_BRIDGE_VOICE=narrator utils/bin/article-tts --browser-server

The player appears only on exact loopback hostnames and is present on regular pages, product pages, posts, and review layouts according to site defaults. It never loads on a public hostname. The player omits navigation, forms, embedded frames, update listings, comments, and support/footer material. Blog extraction remains limited to the post reading area; other pages use the shared local-reader content marker.

Select text and press Play to hear that selection. With no selection, click within content to establish a cursor and Play continues from there; without a cursor, Play starts at the beginning. Restart begins at the page title. Pause, Resume, and Stop control the local playback queue; leaving the page stops playback.

Browser playback uses sentence-aware chunks through the local relay at 127.0.0.1:11441. The relay allows configured local Jekyll origins and the local WebReader for Safari extension, keeps endpoint and voice settings out of page JavaScript, and rejects ordinary external webpage origins. Audio is decoded in browser memory and is not written to disk. The bridge returns each WAV chunk before it is played, so this is buffered chunk playback rather than byte-stream audio.

If using a different port, configure the relay's allowed origin and the browser's articleTtsRelayUrl setting only for the loopback relay. Do not expose the helper to a public network.

### Check or generate public MP3 narration

article-audio uses the same prose extractor but publishes only a joined MP3 and privacy-safe identity manifest. It compares the cleaned rendered article text hash, public narration profile name, chunk size, and MP3 hash; timestamps alone do not trigger regeneration.

Check one source post without contacting TTS:

    utils/bin/article-audio --check html/_posts/technology/2025-04-08-Remote-Debugging-With-VSCode.md

Check all publishable posts the local site can render:

    utils/bin/article-audio --check --all

Generate or refresh one narration file while the local site and TTS engine are available:

    TTS_BRIDGE_URL=http://127.0.0.1:11440/v1 TTS_BRIDGE_VOICE=narrator utils/bin/article-audio --generate html/_posts/technology/2025-04-08-Remote-Debugging-With-VSCode.md

Use --generate --all only for an intentional batch. Existing current MP3s are reused; only missing or stale files call TTS. --force regenerates selected narration even when its manifest is current. A failed synthesis uses temporary output and preserves the last complete public MP3.

The tracked public defaults are in utils/etc/article-audio.defaults.json. It contains no private bridge endpoint, model, or voice alias. Supply those through TTS_BRIDGE_URL, TTS_BRIDGE_VOICE, and optional TTS_BRIDGE_MODEL. Change the public profile value when the intended voice, model, or synthesis policy changes.

Generated files use html/assets/audio/blog/<category>/YYYY-MM-DD-<slug>.mp3 and the adjacent .audio.json manifest. Generation does not edit post front matter. Listen to and approve an MP3 before adding its printed audio path to a post; the production player appears only after this opt-in.

