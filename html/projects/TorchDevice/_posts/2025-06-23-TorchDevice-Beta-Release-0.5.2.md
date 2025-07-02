---
layout: post
title: "TorchDevice 0.5.2: Still Beta, but Three Months of Refactoring, Testing, and Real-World Breakthroughs"
redirect_from:
  - /projects/TorchDevice/2025/06/23/TorchDevice-Beta-Release-0.5.2/
image: /projects/TorchDevice/images/TorchDevice-HF-Transformers.png
date: 2025-06-22
category: TorchDevice
tags: [PyTorch, Apple Silicon, CUDA, MPS, open source, AI infrastructure]
published: true
excerpt: "TorchDevice is a compatibility layer that makes PyTorch code written for CUDA \"just work\" on Apple's MPS (and vice versa), with minimal friction for devs. It's the kind of glue that shouldn't exist-but absolutely needs to if you live on both sides of the Apple/NVIDIA divide."
---

## Refactoring on Repeat: The Long Road to 0.5.2

If you ever want a masterclass in humility, try refactoring the same codebase for three months straight, then rolling back *again* when you realize the "clean" way isn't always the right way. That, in a nutshell, sums up a big chunk of the TorchDevice story this spring. If you're just tuning in: TorchDevice is a compatibility layer that makes PyTorch code written for CUDA "just work" on Apple's MPS (and vice versa), with minimal friction for devs. It's the kind of glue that shouldn't exist-but absolutely needs to if you live on both sides of the Apple/NVIDIA divide.

### March: Modularization, Rollbacks, and Finding the Right Structure

When I first started hacking away at this project, I thought: _Let's break it up into proper modules, peel off core logic, make it testable._ Classic software engineering optimism, right? I went from a monolithic, slightly terrifying `TorchDevice.py` to a clean directory tree: `core/`, `ops/`, `utils/`, and so on. Each refactor was followed by a wave of test failures, which in turn led to more test improvements. Some nights I'd modularize a component, run the test suite, then revert the next morning because something fundamental broke.

The modular approach *finally* stuck around late spring-mostly because I started moving one feature at a time, keeping all old interfaces backward-compatible until the dust settled. This made for a fair bit of duplicate code and awkward shims at first, but by late May, everything was centralized, and core tests were passing. I also stabilized the "CPU override" feature, letting you explicitly force everything to the CPU (`cpu:-1`), which has saved my bacon in cross-platform workflows more than once.

I will have to admit, it may not be the last time I refactor this codebase, and i'm sure there will be incremental changes going forward, but the goal is still the same - to run PyTorch CUDA code unmodified on Apple Silicon.

### May-June: Real-World Testing and Hugging Face Headaches

By May, the structure was solid enough to take on bigger game: I wanted TorchDevice to survive "real world" PyTorch, not just synthetic tests. So I built a full test automation harness for external projects-especially Hugging Face Transformers, which is both a beast and a benchmark. The test suite runner now lets you target any project, automatically sets up your environment variables, pipes logs everywhere, and spits out clickable, filterable Markdown test reports. The test status for each release is now baked right into the repo, so anyone can see exactly what's working and what's flaky.

Let's be clear: **Transformers is relentless**. It will find every device-handling edge case, from attention mechanisms to random seed management. Getting even 85%+ of the test suite passing on Apple Silicon is an accomplishment, and the remaining failures are (almost always) due to CUDA-only code or weird MPS limitations. Every time a test failed, I'd dive into both TorchDevice and the PyTorch source, patch the signatures, and rebuild until the test turned green (or the red was at least understandable).

### What's New in 0.5.2

- **Fully Modularized Codebase**: Everything lives where it should, and patch orchestration is handled centrally. This makes it a lot easier for others to contribute or just poke around.
- **Automated Test Reporting**: New scripts generate Markdown and JSON test reports, with clickable links to logs and code-finally, debugging with context!
- **Transformers Compatibility**: Hugging Face test automation is baked in, including step-by-step setup for anyone who wants to reproduce or contribute.
- **Cleaner Device Override Semantics**: `cpu:-1` and related overrides now work as advertised, everywhere, every time.
- **Verbose Logging (for now)**: TorchDevice logs nearly everything it does, by design. This is going to get dialed back in future releases, but for now, it's invaluable for tracking device redirection.

## Bridge Building Between CUDA and MPS

<div style="text-align: center">
<img src="/projects/TorchDevice/images/Making_a_Bridge_For_AI.png" alt="Making a Bridge FOR AI">
</div>
### Not Just for Show: Real TTS and LLM Workflows

TorchDevice isn't just a science project-I've used it to run real TTS models and smaller language models (see the `demos/` directory). It's saved me time on every project where I'd otherwise have to rewrite code for "the other" device backend. Some of my current text-to-speech and audio analysis tools now run out of the box on my M-series Macs, and I've stopped dreading codebases that assume CUDA.

This is actually a longer term plan for me to use this in my main project [Case Analytics](/projects/Case-Analytics/) to make more capabilities, models and open source software more easily available to me. My goal is to spot the signs of Parental Alienation using AI for analysis and detecting patterns in communications and case files. Specialized BERT models and other AI models will be used to analyze communications and case files to detect patterns of Parental Alienation.

This is to the point I believe it is usable, but don't expect it to be bug-free. My plan is to continue working on this and incorporating it into my AI workflows and automation. I has done well with many Open Source projects I've tried it with, and simply importing TorchDevice will handle redirecting torch calls to the default accelerator device.

### Open Issues, Next Steps, and a Call for Help

It's not perfect: about 13% of Transformers tests still fail, and some CUDA-specific features are fundamentally unsupported on Apple hardware. If you see something that can be fixed, please [submit a PR](https://github.com/unixwzrd/TorchDevice). If you hit a bug or run into a compatibility nightmare, open an issue and include the logs-the more cryptic the error, the better.

#### Next up on my roadmap:
- Passing more Transformers tests
- Shoring up missing functionality support for MPS from CUDA
- Reducing the default log verbosity (my scroll finger needs a break)
- Considering putting in a redirect to MLX operations for improved performance
- Improving error diagnostics for easier debugging
- Further modularizing test utilities and improving docs for contributors

#### Give It a Shot!
It's as simple as cloning the repo, installing the dependencies, and running the tests.

```bash
git clone https://github.com/unixwzrd/TorchDevice.git
cd TorchDevice
pip install -e .
pip install -r requirements.txt
python -m unittest discover
```

Then in your code import order does not matter, what could be simpler?

```python
import torch
import TorchDevice
```

There's also a script in bin (dev branch) `numpy-comp` which will recompile a pip install of NumPy optimized for Apple Silicon using the Accelerate Framework. This improves performance about 8x for NumPy operations. This is from my [Python Virtual Environment Utilities Project](/projects/venvutil/) check it out for Python environment tools and scripts geared towards managing virtual environments and ML/AI.

```bash
# (Apple Silicon only - uses the Accelerate Framework)
bin/numpy-comp 1.26.*
```

Will give you the that version of NymPy optimized with the Accelerate Framework.

If you spot something that could be improved, open a PR, contributions of any size are always welcome.

## If You Want to Support TorchDevice

- [⭐ Star on GitHub](https://github.com/unixwzrd/TorchDevice)
- [Patreon](https://www.patreon.com/unixwzrd), [Ko-Fi](https://ko-fi.com/unixwzrd), [Buy Me a Coffee](https://www.buymeacoffee.com/unixwzrd)
- File issues, write docs, or just try it out and let me know what breaks

### Final Thought
If you're stuck porting CUDA code to Apple Silicon, or just want to squeeze more life out of that PyTorch project, give TorchDevice a shot. It's not magic, but after three months of rolling up my sleeves, if anything, the log messages will help identify spots in your code for migration.

**Changelog, docs, demos, and full project details [on GitHub](https://github.com/unixwzrd/TorchDevice).**

*- M S (unixwzrd)*