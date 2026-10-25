---
layout: project
title: "UnicodeFix"
category: UnicodeFix
permalink: /projects/UnicodeFix/
image: /assets/images/projects/UnicodeFix-banner.png
excerpt: "UnicodeFix v2.1.0 audits and safely cleans text and supported image metadata locally, with built-in PNG, JPEG, and WebP cleanup and no ExifTool dependency."
---

## Find What Your Editor Does Not Show

**UnicodeFix v2.1.0 — the Ghostmark Edition** is a local, evidence-based text and image audit and cleanup tool. It finds invisible characters, provenance wrappers, image metadata, configured statistical-watermark signals, hard-wrapped Markdown, and hidden payloads in source comments, then shows where the evidence lives and removes only what it can identify safely.

Everything runs locally after installation. Your text is not uploaded to a detector, vendor, or model service.

`cleanup-text` recognizes image inputs and routes them to the built-in image backend. PNG, JPEG, and WebP cleanup is included in the normal Python installation, without a separate ExifTool executable. The default writes a separate `.clean` image, removes supported non-rendering metadata, and verifies preservation of image coding data and rendering metadata before publication. Recognized C2PA provenance still requires an explicit `--strip-provenance` choice.

TIFF, HEIF, AVIF, GIF, and BMP are audit-only in this release. HEIF/AVIF inventory depends on an available decoder and is explicitly marked incomplete when only the header is recognized. Image inputs are limited to 256 MiB per file; unsupported metadata variants can also prevent writing. See the [image guide](https://github.com/unixwzrd/UnicodeFix/blob/main/docs/cleanup-image.md) for the full format and preservation rules.

## Evidence Before Attribution

Ghostmark keeps different kinds of evidence in their proper categories:

- **Provenance:** recognized local C2PA carriers and structured manifest elements. Provenance does not, by itself, prove AI authorship.
- **Unicode security:** bidi controls, default-ignorables, variation selectors, tag and private-use characters, noncharacters, normalization differences, mixed scripts, and confusable signals.
- **Known watermarks:** results from explicitly configured local detector profiles for supported schemes. A result applies only to that named detector and configuration.
- **Authorship signals:** optional, locally calibrated model-distribution measurements reported as probabilistic evidence, never as an automatic cleanup trigger.
- **Typography:** smart quotes, dashes, unusual whitespace, and other observable normalization candidates.
- **Formatting:** Markdown soft breaks, wrapped list continuations, and probable fixed-column wrapping.

UnicodeFix does not claim that typography identifies an author, that C2PA proves a document was AI-generated, or that one named detector can find every possible watermark.

## Audit, Preview, or Clean

Use report mode to inventory a file without changing it:

```bash
cleanup-text --report --metrics --json document.md
```

Preview the exact requested transformation in memory and inspect a unified diff:

```bash
cleanup-text --dry-run --diff --unwrap-markdown document.md
```

Clean supported text and invisible-character problems, opt into safe Markdown unwrapping, or explicitly remove complete recognized local provenance carriers:

```bash
cleanup-text document.txt
cleanup-text --unwrap-markdown README.md
cleanup-text --strip-provenance document.md
cleanup-text --source app.py
cleanup-text photo.jpg
cleanup-text --dry-run photo.jpg
```

Category-aware thresholds can turn selected findings into useful CI gates without treating informational typography or wrapping as a security failure.

## Safety Boundaries

- Recognized C2PA provenance is preserved unless `--strip-provenance` is explicit, and external manifest URLs are never retrieved during normal operation.
- Markdown unwrapping is opt-in and preserves code, tables, front matter, HTML, hard breaks, list structure, and other meaningful boundaries.
- Source mode classifies comments, strings, identifiers, and syntax. It cleans only supported comment payloads and checks parsing before and after transformation.
- Statistical watermark detection requires a named local profile and matching local artifacts. UnicodeFix does not guess at proprietary or unknown schemes.
- Authorship probabilities require explicit calibration against a matched held-out corpus and remain report-only.
- Text in-place writes use a synced same-directory atomic replacement, retain permissions, and never overwrite an existing preserved backup. Images always require a separate output file, and existing output requires an explicit `--force` to replace it.

## Installation

UnicodeFix requires **Python 3.11 or newer** and **Pillow 13.x**, and is tested on macOS and Ubuntu through CI. The normal Python installation includes image audit and supported image cleanup; ExifTool and Perl are not required.

```bash
git clone https://github.com/unixwzrd/UnicodeFix.git
cd UnicodeFix
./setup.sh
```

The optional local watermark and authorship lab can be installed separately when you already have the required detector or model artifacts:

```bash
./setup.sh --watermark-lab
```

For the complete command reference, research ledger, test documentation, and release history, visit the [UnicodeFix repository on GitHub](https://github.com/unixwzrd/UnicodeFix).

## Local, Inspectable, and Open

UnicodeFix remains open source under the MIT License. Its local research harness and detector profiles are designed to make the scheme, configuration, artifacts, and limitations inspectable instead of presenting a mystery score as fact.

**Built and maintained by [unixwzrd](https://unixwzrd.ai)** — helping ensure clarity, integrity, and trust in your text, one invisible character at a time.
