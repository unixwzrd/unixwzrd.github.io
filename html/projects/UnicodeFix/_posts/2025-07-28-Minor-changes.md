---
layout: post
title: "UnicodeFix: 2025-07-28: Extended ASCII, Global Ready"
image: /assets/images/projects/UnicodeFix/8-bit-extended-ASCII.png
date: 2025-07-28
category: UnicodeFix
tags: [unicode, python, ai, text-cleaning, detection, open-source, shortcuts, devtools, ai-watermarks, anti-cheat]
excerpt: "Quick update: **UnicodeFix now handles extended 8-bit ASCII.** If you're dealing with files from Europe or anywhere special characters roam - like \"M\u00FCnchen,\" \"fa\u00E7ade,\" \"Ni\u00F1o,\" or \"stra\u00DFe\" - they'll now get cleaned up right along with the Unicode ghosts.."
published: true
---

## Extended Character sets

Quick update: **UnicodeFix now handles extended 8-bit ASCII.** If you're dealing with files from Europe or anywhere special characters roam - like "München," "façade," "Niño," or "straße" - they'll now get cleaned up right along with the Unicode ghosts.

We also patched a VS Code quirk: UnicodeFix now ensures your files end with a clean, honest newline, no matter how your editor behaves.

Tested on text from around the world - no more missed accents, broken umlauts, or mystery bytes.

```sh
cat résumé.txt | cleanup-text > resume.txt
```

Stay human. Stay global. UnicodeFix it.

* *Mia & the Unixwzrd*
