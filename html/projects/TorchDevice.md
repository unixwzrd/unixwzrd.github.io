---
layout: project
title: "TorchDevice"
category: TorchDevice
permalink: /projects/TorchDevice/
image: /assets/images/projects/TorchDevice/TorchDevice001.png
excerpt: "TorchDevice is compatibility tooling for running CUDA-oriented PyTorch code on Apple Silicon by redirecting common CUDA device calls to MPS where practical."
---

## CUDA-to-MPS Compatibility for PyTorch

TorchDevice is compatibility tooling for Python projects that were written with CUDA-first PyTorch assumptions but need to run on Apple Silicon using MPS.

It intercepts common PyTorch device calls and redirects them based on the available backend: CUDA, MPS, or CPU. The goal is not to hide every hardware difference. The goal is to reduce the first round of breakage when trying to run existing CUDA-oriented code on local Apple hardware.

### Why This Matters

Many AI and ML examples assume NVIDIA hardware. That creates friction for developers working locally on Apple Silicon, especially when testing older code, research projects, or tools that hard-code CUDA device behavior.

TorchDevice acts as a bridge for that situation. It can help local experiments get running faster, make porting work more explicit, and show where CUDA-specific assumptions still need attention.

### Key Features

- **Automatic Device Redirection**: Intercepts `torch.device` instantiation and redirects it based on available hardware (CUDA, MPS, or CPU).
- **Drop-in compatibility layer**: Reduces code changes needed for common CUDA-to-MPS test runs.
- **Apple Silicon focused**: Helps CUDA-oriented PyTorch code run against Apple's Metal-backed MPS backend where practical.
- **AI and ML workflow support**: Reduces friction when moving experiments between CUDA systems and local Apple hardware.
- **Explicit CPU Override**: Provides a special `'cpu:-1'` device specification to force CPU usage regardless of available accelerators.
- **Mocked CUDA Functions**: Provides mocked implementations of CUDA-specific functions, enabling code that uses CUDA functions to run on MPS hardware.
- **Stream and Event Support**: Implements full support for CUDA streams and events on MPS devices, allowing for asynchronous operations and event timing.
- **Unified Memory Handling**: Handles differences in memory management between CUDA and MPS, providing reasonable values for memory-related functions.
- **Logging and Debugging**: Outputs informative log messages indicating how calls are intercepted and handled, assisting in code migration and debugging.
- **Transparent Integration**: Works transparently without requiring changes to existing codebases.
- **PyTorch Compiler Compatibility**: Works with PyTorch's dynamo compiler and inductor.

### Development & Availability

This is older compatibility tooling, but it remains useful for local Apple Silicon experiments and CUDA-to-MPS porting work. It is available on [GitHub](https://github.com/unixwzrd/TorchDevice).

For installation, usage, and technical details, see the project's **[README](https://github.com/unixwzrd/TorchDevice)**.
