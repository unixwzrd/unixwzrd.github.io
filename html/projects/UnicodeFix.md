---
layout: project
title: "UnicodeFix"
category: UnicodeFix
permalink: /projects/UnicodeFix/
---

**UnicodeFix** is a lightweight, open-source tool that normalizes text by converting problematic or invisible Unicode characters into clean, reliable **ASCII**.

If you've ever encountered hidden characters — such as curly quotes, non-breaking spaces, or zero-width joiners — that break code, YAML, Markdown, or configuration files, UnicodeFix is designed to make your text safe, predictable, and portable.

---

## What UnicodeFix Does

- Converts smart quotes, em-dashes, en-dashes, ellipses, and other punctuation into standard ASCII equivalents
- Removes invisible or disruptive Unicode characters, including:
- `U+200B` (Zero-Width Space)  
- `U+200C` (Zero-Width Non-Joiner)  
- `U+200D` (Zero-Width Joiner)  
- `U+2018` (Left Single Quotation Mark ‘ )  
- `U+2019` (Right Single Quotation Mark ’ )  
- `U+201C` (Left Double Quotation Mark “ )  
- `U+201D` (Right Double Quotation Mark ” )  
- `U+2013` (En Dash – )  
- `U+2014` (Em Dash — )  
- `U+2026` (Horizontal Ellipsis … )
- Cleans AI-generated, copied, or web-sourced content to prevent downstream parsing errors
- Reduces risks when working across editors, file formats, and systems

**Bonus Trouble makers**

- `U+FEFF` (Byte Order Mark, BOM) — invisible but can totally screw up parsing in some languages.
- `U+00A0` (Non-Breaking Space) — looks like a regular space but acts differently in many contexts.

---

## Platform Compatibility

UnicodeFix has been developed and tested on **macOS**.  
It is expected to work on **Linux** and **Windows** (via WSL or Python), but has not yet been officially tested across all environments.  
Contributions and testing feedback are welcome.

---

## How to Use

Use it as a command-line tool:

```bash
python cleanup-text.py input.txt -o output.txt
```

Or directly in pipelines:

```bash
cat input.txt | python cleanup-text.py
```

For detailed installation instructions and examples, see:

* [**View the UnicodeFix Project on GitHub**](https://github.com/unixwzrd/UnicodeFix)

---

## Additional Tools

UnicodeFix can be combined with editors like **VS Code**, hex editors like **Hex Fiend**, or clipboard managers to sanitize content at various stages of your workflow.

---

**Built and maintained by [unixwzrd](https://unixwzrd.ai)** — helping ensure clarity, integrity, and trust in your text, one invisible character at a time.