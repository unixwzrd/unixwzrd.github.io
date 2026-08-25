---
permalink_slug: "unicodefix-v2-0-0-ghostmark-edition"
legacy_project_permalink: "/projects/UnicodeFix/2026/08/20/unicodefix-v2-0-0-the-ghostmark-edition/"
short_link_basis: "/projects/UnicodeFix/_posts/2026-08-20-unicodefix-v2-0-0-ghostmark-edition.md"
short_url: "https://unixwzrd.ai/s/80c3c94c20/"
layout: post
title: "UnicodeFix v2.0.1: The Ghostmark Edition"
date: 2026-08-20
last_modified_at: 2026-08-24 12:00:00 -0500
category: UnicodeFix
tags: [unicode, text-forensics, provenance, c2pa, watermarking, ai-detection, image-metadata, markdown, developer-tools, privacy, python, open-source]
content_type: release
excerpt: "UnicodeFix v2.0.1 extends Ghostmark's evidence-based local auditing and deliberate cleanup to image metadata and recognized C2PA/JUMBF provenance while preserving pixel data and refusing unsupported watermark claims."
image: /assets/images/projects/UnicodeFix-banner.png
published: true
---

Some marks are obvious only after they break a parser, a diff, or a build. Others are meant to carry provenance or survive ordinary editing. Still others are statistical signals that mean nothing unless you know the exact detector, tokenizer, model, key, configuration, and threshold that produced them.

**UnicodeFix v2.0.1 — the Ghostmark Edition** is built around that distinction.

This is an evidence-based local audit and safe-cleanup release. It finds what can hide in plain sight, reports exactly where it lives, separates observable facts from attribution claims, and removes only what it can identify safely.

*Updated August 24, 2026 for v2.0.1 image metadata and provenance support. The original article URL and short link remain unchanged so previously shared links continue to work.*

[Get UnicodeFix v2.0.1 on GitHub](https://github.com/unixwzrd/UnicodeFix)

## New in v2.0.1: Image Metadata and Provenance

Ghostmark now applies the same audit-first approach to supported raster images. The new `cleanup-image` command inventories image structure and removable metadata locally, identifies recognized C2PA/JUMBF tags when the installed backend can read them, and reports location, identity or device, editing, and other metadata as separate categories.

Audit an image without writing anything:

```bash
cleanup-image --report photo.jpg
cleanup-image --report --json graphic.png
```

Image audit is included in the normal Python installation. Lossless cleanup requires ExifTool 12.70 or newer. UnicodeFix checks the installed version and remains audit-only when ExifTool is missing or too old.

```bash
cleanup-image --dry-run --strip-metadata photo.jpg
cleanup-image --strip-metadata photo.jpg
cleanup-image --strip-provenance graphic.png
cleanup-image --strip-metadata --strip-provenance -o share.png graphic.png
```

Metadata removal does not decode or re-encode the pixels. It preserves pixel data, ICC profiles, orientation, and color-space tags, writes a separate `<name>.clean<extension>` file by default, refuses in-place image editing, and will not overwrite an existing output unless `--force` is explicit.

Provenance receives an additional safety boundary. Changing ordinary metadata can invalidate a signed Content Credential even if its JUMBF bytes remain, so UnicodeFix refuses metadata cleanup on a recognized C2PA image unless `--strip-provenance` is also explicit. If an XMP C2PA reference is present, provenance removal also requires `--strip-metadata` so the reference is not left behind. After removal, UnicodeFix verifies that recognized C2PA/JUMBF tags are absent.

The write path supports JPEG, PNG, WebP, TIFF, HEIF, and AVIF when both Pillow and ExifTool recognize the container. Proprietary raw formats and SVG remain audit-only.

### What Image Cleanup Does Not Claim

Metadata and provenance are not the same as a pixel-domain watermark. UnicodeFix does not claim that removing EXIF, XMP, or C2PA makes an image free of AI-related signals.

SynthID, visible logos, and unknown pixel-domain schemes remain `unsupported` without a compatible public local detector and its required configuration. UnicodeFix does not present cropping, recompression, filtering, or inpainting as verified removal. Version 2.0.1 can identify and remove the metadata and recognized provenance it documents; it does not manufacture certainty about signals it cannot observe.

`cleanup-text` also recognizes common image signatures now and directs binary input to `cleanup-image` instead of failing with an unhelpful UTF-8 decoding error.

## No Generic “AI Detector” Theater

Ghostmark does not claim that a curly quote came from a chatbot. It does not treat column-80 wrapping as proof of authorship. It does not call every provenance record an AI watermark, and it does not present an unsupported probability as truth.

Instead, Ghostmark introduces a shared findings model used by human-readable, JSON, and CSV reports. Text findings are separated into six categories:

- `provenance` for recognized local C2PA carriers and structured manifest elements
- `unicode_security` for bidi controls, default-ignorables, variation selectors, tags, private-use characters, noncharacters, normalization differences, mixed scripts, and confusable signals
- `known_watermark` for the result of a named, explicitly configured local detector profile
- `authorship_signal` for optional locally calibrated model-distribution measurements
- `typography` for observable normalization candidates such as smart quotes, dashes, and unusual whitespace
- `formatting` for Markdown soft breaks, wrapped list continuations, and probable fixed-column wrapping

Detailed reports retain the category, signal, count, confidence, removability, planned action, and exact source location when it is available. Compact aggregate output remains available for people and CI systems that need a concise result.

## Audit First, Preview Next, Clean Deliberately

The three primary workflows are now explicit.

Audit a document without changing it:

```bash
cleanup-text --report --metrics document.md
cleanup-text --report --metrics --json document.md
```

Preview the complete requested transformation in memory and inspect the proposed change:

```bash
cleanup-text --dry-run --diff --unwrap-markdown document.md
```

Clean supported text problems, opt into Markdown reformatting, or explicitly remove recognized local provenance:

```bash
cleanup-text document.txt
cleanup-text --unwrap-markdown README.md
cleanup-text --strip-provenance document.md
cleanup-text --source app.py
```

The `--metrics` report is now deterministic: bytes, characters, lines, words, newline style, ASCII and non-ASCII counts, and an exact code-point inventory. The older NLTK extras and generic “AI-likeness” measurements have been removed rather than carried forward as evidence they could not support.

Category-aware thresholds make the reporting useful in CI. A policy can fail on Unicode security or provenance findings without treating informational typography or line wrapping as a security incident.

## Provenance Is Protected

UnicodeFix recognizes C2PA before generic invisible-character cleanup so a valid credential is not silently destroyed.

C2PA records provenance. It does not automatically identify the author, model, or truth of a document. Complete recognized local carriers remain in place unless `--strip-provenance` is explicitly requested, malformed lookalikes are retained and reported, and UnicodeFix never retrieves an external manifest URL during normal operation.

The tool also refuses to reformat signed C2PA content unless stripping was explicitly requested, because even harmless-looking Markdown serialization can invalidate a credential.

## Markdown and Source Cleanup Have Guardrails

The new `--unwrap-markdown` mode joins CommonMark soft line breaks within the same paragraph, including paragraphs inside lists and block quotes. It preserves real list items, nested structures, hard breaks, tables, front matter, HTML, link definitions, and fenced, indented, and inline code. The transformation is opt-in and idempotent.

Source mode takes a similarly conservative approach. `--source` distinguishes comments from strings, identifiers, and syntax. It can remove recognized provenance and supported hidden payloads from comments, but it leaves strings and identifiers byte-for-byte unchanged and checks parsing before and after cleanup.

The Markdown and source profiles remain separate because they solve different problems and should not quietly rewrite one another's inputs.

## Local Watermark Profiles, With Their Limits Attached

The optional local watermark lab supports explicit detector profiles for configured KGW and SynthID Text schemes, along with deterministic research fixtures. A profile must name the required algorithm, parameters, tokenizer, model or detector artifacts, key or seed where required, and calibrated threshold.

The result is deliberately narrow: `detected`, `not_detected`, `insufficient_text`, `unsupported`, or `configuration_error` for that named profile. “Not detected” never means that the text contains no possible watermark.

UnicodeFix cannot generically identify or remove an unknown proprietary, lexical, semantic, or source-code watermark. It does not download detector artifacts at runtime or contact a vendor service or model hub.

## Authorship Signals Are Not Proof

An optional authorship profile can measure paragraph-level likelihood, perplexity, selected-token rank, and top-10 rate using pinned local causal-model artifacts. A probability is shown only when the profile includes calibration coefficients fitted on a matched held-out corpus.

Those measurements are reported separately from watermark evidence and never trigger cleanup. The reference model, tokenizer, quantization, corpus, text length, domain, language, and calibration all affect the result. A smaller local model may make an experiment convenient; it does not make the conclusion certain.

## Safer Files and a Harder Release Gate

In-place cleanup now writes and syncs a unique temporary file in the same directory, retains the original permissions, and atomically replaces the input. When preservation is requested, UnicodeFix never overwrites an existing backup.

The release gate runs Black, Ruff, pytest, both installed console scripts, the shell integration suite, and ShellCheck across maintained shell scripts. The 2.0 line also aligns source parsing with tree-sitter 0.25 and 0.26 so supported source languages do not silently fall back to a generic lexer.

Python 3.10 or newer is now required. UnicodeFix is tested on macOS and Ubuntu and remains distributed through GitHub releases rather than PyPI.

## Privacy and Control Stay Local

Everything runs locally after installation. UnicodeFix does not upload text or images to a detector, vendor, or model service, and it does not dereference external provenance manifests during ordinary operation.

That boundary matters. The privacy questions around hidden carriers, external manifest references, statistical marks, and vendor-controlled detectors are legitimate, but concern is not evidence. Ghostmark is designed to expose what can be observed, preserve exact locations and limitations, and say `unsupported` when the necessary public algorithm, key, model, tokenizer, or calibration is unavailable.

The [UnicodeFix repository](https://github.com/unixwzrd/UnicodeFix) includes the full CLI documentation, vendor watermark matrix, feasibility ledger, local research harness, example profiles, tests, and release history.
