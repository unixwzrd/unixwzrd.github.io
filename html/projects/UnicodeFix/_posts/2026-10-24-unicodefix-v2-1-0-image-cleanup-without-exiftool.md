---
permalink_slug: "unicodefix-v2-1-0-image-cleanup-without-exiftool"
short_link_basis: "/projects/UnicodeFix/_posts/2026-10-24-unicodefix-v2-1-0-image-cleanup-without-exiftool.md"
short_url: "https://unixwzrd.ai/s/276c1fd905/"
layout: post
title: "UnicodeFix v2.1.0: Image Cleanup Without ExifTool"
date: 2026-10-24
category: UnicodeFix
content_type: update
tags: [unicode, image-metadata, provenance, developer-tools, python, open-source]
excerpt: "UnicodeFix v2.1.0 brings PNG, JPEG, and WebP metadata cleanup into the Python package, removes the ExifTool dependency, and makes the supported formats and safety boundaries explicit."
image: /assets/images/projects/UnicodeFix-banner.png
published: true
---

UnicodeFix's image cleanup no longer needs ExifTool. In **v2.1.0**, I replaced the external backend with built-in image-container handling, so a normal Python installation includes the image cleanup runtime. There is no separate executable to install, no version check to satisfy, and no subprocess waiting for something to turn up on your `PATH`.

That does not mean I replaced it with a routine that opens an image and saves a fresh copy. Removing metadata should not require recompressing your photograph or quietly changing how it displays. The new backend works on the container around the image data, with explicit checks before it publishes the cleaned file.

<!--more-->

## Built In, Without Re-encoding

The writable formats are **PNG, JPEG, and WebP**, including APNG, progressive JPEG, and animated WebP. UnicodeFix preserves the original image coding data, ICC profiles, orientation, supported color-space fields, and animation frames and timing. Pillow handles EXIF parsing and serialization, but it does not re-save the image pixels during cleanup.

Before the separate output file is published, UnicodeFix re-audits it and compares protected block hashes and rendering metadata against the original. Unknown blocks are retained; malformed framing and unsupported metadata variants stop the write rather than inviting a best guess. This is selected metadata cleanup, not a promise that every possible private payload has been found and removed.

## The Commands Stay Familiar

The automatic routing introduced in v2.0.2 is still there. `cleanup-text` recognizes image signatures and sends them to the image backend, while ordinary text keeps its own pipeline:

~~~sh
# Audit without writing.
cleanup-text --report --metrics photo.jpg

# Preview the requested image cleanup without writing.
cleanup-text --dry-run photo.jpg

# Write photo.clean.jpg; leave photo.jpg alone.
cleanup-text photo.jpg
~~~

The dedicated `cleanup-image` command remains available and still defaults to audit-only. Image output must be a different file, and an existing output requires an explicit `--force` to replace it. None of that changed just because the backend moved into the package.

Recognized C2PA provenance also remains an explicit decision. Metadata cleanup can invalidate a retained credential, so UnicodeFix refuses that operation unless you request `--strip-provenance`. It recognizes supported C2PA/JUMBF carriers structurally, including fragmented JPEG carriers, but it does not validate their signatures or trust chains. Removing a provenance record is not the same thing as detecting or removing a watermark embedded in pixels.

## A More Specific Support Boundary

There is an important compatibility change: **TIFF, HEIF, AVIF, GIF, and BMP are audit-only in this release**, even where the previous ExifTool-backed path supported writing. I would rather state that plainly than carry over an old support claim that the new writer cannot meet. HEIF and AVIF inventory depends on an available Pillow decoder; if only the header can be recognized, the report says the inventory is incomplete.

Inputs are limited to 256 MiB per file. Images with unsupported rendering-sensitive metadata can also be restricted to audit, even when the container format is normally writable. The [image guide](https://github.com/unixwzrd/UnicodeFix/blob/main/docs/cleanup-image.md) documents those limits and the preservation rules.

## Upgrading

The current baseline is **Python 3.11 or newer with Pillow 13.x**, following the patched-Pillow update in v2.0.3. ExifTool and Perl are not required by UnicodeFix's image pipeline anymore. If your scripts parse image reports, note that image schema **2.1** replaces the old ExifTool installation/version object with a backend-neutral status object; the old `--exiftool` option and `exiftool=` API parameter have been removed rather than retained as compatibility aliases.

The [UnicodeFix repository](https://github.com/unixwzrd/UnicodeFix) has the installation instructions, and the [changelog](https://github.com/unixwzrd/UnicodeFix/blob/main/CHANGELOG.md) covers both releases. The practical result is a simpler installation with the same local-processing approach, a writer that checks what it preserves, and fewer things to go hunting for when you just wanted to clean a file.
