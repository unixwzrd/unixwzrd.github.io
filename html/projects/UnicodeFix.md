---
layout: project
title: "UnicodeFix"
category: UnicodeFix
permalink: /projects/UnicodeFix/
---

**UnicodeFix** is a lightweight, open-source utility that cleans up messy text by converting strange or invisible Unicode characters into clean, readable **ASCII**. If you've ever pasted content into your code editor and had it break because of curly quotes, non-breaking spaces, or hidden characters — this tool can save your sanity.

Whether you're a developer, writer, or just someone who copies and pastes from the internet, UnicodeFix helps normalize your text so it behaves.

---

## 🔧 What Does It Do?

- Replaces smart quotes, em/en dashes, ellipses, and other Unicode punctuation with standard ASCII
- Removes invisible Unicode characters like:
  - `U+200B` (Zero-width space)  
  - `U+200C` (Non-joiner)  
  - `U+200D` (Joiner)
- Makes AI-generated or copied web content safer to paste into your terminal, editor, or scripts
- Avoids hidden errors in YAML, JSON, Markdown, and other plain text formats

---

## ✅ Platform Compatibility

UnicodeFix has been developed and tested on **macOS**.  
It should work on **Linux** and **Windows (via WSL or Python)**, but is **not yet officially tested** on those platforms. Contributions or testing feedback welcome!

---

## 🚀 Get Started

Run it as a CLI tool with a simple one-liner:

```bash
python cleanup-text.py input.txt -o output.txt
```

Or pipe directly from stdin and back to stdout:

```bash
cat input.txt | python cleanup-text.py
```

More details and usage examples on GitHub:

👉 [**View the GitHub Project**](https://github.com/unixwzrd/UnicodeFix)

---

## 💬 Tip

Combine with tools like **VS Code**, **Hex Fiend**, or **Clipboard managers** to debug and sanitize tricky copy-pasted text.

---

Built by [unixwzrd](https://unixwzrd.ai) — bringing clarity back to your clipboard, one invisible character at a time.