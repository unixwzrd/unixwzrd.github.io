---
title: "Announcing TorchDevice 0.0.5 Beta – Transparent Hardware Redirection for PyTorch"
date: "2025-03-05"
category: TorchDevice
tags: [introduction, overview]
published: true
---

We’re pleased to announce the release of **TorchDevice 0.0.5 Beta**, a significant milestone in simplifying hardware compatibility for PyTorch applications. This release introduces robust enhancements, thorough testing, and a powerful new **CPU override feature** to ensure seamless integration across CUDA and Apple Silicon (Metal) hardware.

## Why TorchDevice?

PyTorch is extensively optimized for CUDA hardware. However, developers using Apple Silicon devices face compatibility challenges due to PyTorch's CUDA-centric assumptions. **TorchDevice** bridges this gap by transparently redirecting PyTorch device calls to the correct backend (CUDA, Metal, or CPU) without needing any manual intervention or code modifications.

## What's New in 0.0.5?

Apart from improving testing, more functionality is now working in this version. Compatibility with Streams, Events, and Context management.

### CPU Override Feature
The highlight of this release is the new **CPU override functionality**, enabling developers to explicitly force CPU usage, invaluable for:

- **Debugging and testing** GPU-dependent code on a CPU.
- **Ensuring consistent behavior** across various testing environments.
- **Resource management** by reserving GPU resources for specific tasks.

Activation is straightforward:
```python
import torch
import TorchDevice

# Forces CPU usage universally
device = torch.device('cpu:-1')

# Operations below explicitly use CPU despite CUDA or MPS availability
tensor = torch.randn(5, 5)  # CPU-based tensor
model = torch.nn.Linear(10, 5).to('cuda')  # Redirected to CPU automatically
```

Expanded and Improved Testing

TorchDevice 0.0.5 is extensively tested using HuggingFace Transformers, successfully passing most test scenarios and ensuring robust compatibility with widely-used models. Further testing and refinements continue, enhancing stability and coverage.

Comprehensive Documentation & Examples

We’ve expanded the documentation to clearly guide developers through installation, configuration, and troubleshooting, making adoption effortless.
  - Detailed README
  - Practical usage examples and tutorials
  - Open community support and contributions via GitHub issues and pull requests

What’s Next?

Our future plans include:
  - Enhanced runtime flexibility for CPU overrides
  - Granular control over device selection per operation
  - Performance optimizations for mixed-device workflows

Community and Support

TorchDevice is actively developed and maintained, and your support helps us accelerate improvements and features. If you or your organization finds value in TorchDevice, consider supporting development through sponsorship or donations.

## Help Support Our Projects

If you find this useful help support my work;
  - [Patreon](https://patreon.com/unixwzrd)
  - [Ko-Fi](https://ko-fi.com/unixwzrd)

Your feedback drives our roadmap. Let’s make PyTorch more accessible and efficient for everyone.