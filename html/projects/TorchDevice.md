---
layout: project
title: "TorchDevice"
category: TorchDevice
permalink: /projects/TorchDevice/
image: /assets/images/projects/TorchDevice/TorchDevice001.png
excerpt: "TorchDevice is a Python library that enables transparent code portability between NVIDIA CUDA and Apple Silicon (MPS) hardware for PyTorch applications. It intercepts PyTorch calls related to GPU hardware, allowing developers to write code that works seamlessly on both hardware types without modification. TorchDevice is designed to assist in porting code from CUDA to MPS and vice versa, making it easier to develop cross-platform PyTorch applications."
---

## Seamless PyTorch Adaptation for Apple Silicon and CUDA

TorchDevice is a Python library that enables transparent code portability between NVIDIA CUDA and Apple Silicon (MPS) hardware for PyTorch applications. It intercepts PyTorch calls related to GPU hardware, allowing developers to write code that works seamlessly on both hardware types without modification. TorchDevice is designed to assist in porting code from CUDA to MPS and vice versa, making it easier to develop cross-platform PyTorch applications.

Many PyTorch-based projects are designed with CUDA-first assumptions, leading to compatibility issues when running on Apple Silicon. TorchDevice is a lightweight wrapper that dynamically adjusts PyTorch calls to ensure smooth execution on both CUDA and Metal-backed Apple hardware.

### Why This Matters

For AI researchers and developers working across different hardware architectures, maintaining **cross-platform compatibility** is often a challenge. This tool provides an **automatic bridge**, so PyTorch operations are routed to the correct backend without manual intervention. Python scripts written for CUDA will be able to work on Apple Silicon without modification and when CUDA calls are made, it will report whether the call was made to CUDA or MPS to assist in porting the code.

THis opens a whole wide range of AI and ML applications to be run on Apple Silicon and other hardware platforms without the need to rewrite the code.

### Key Features

- **Automatic Device Redirection**: Intercepts `torch.device` instantiation and redirects it based on available hardware (CUDA, MPS, or CPU).
- **Seamless integration** - no need to modify existing PyTorch code
- **Optimized for Apple Metal and CUDA**, ensuring performance without extra configuration
- **Works with AI and ML models**, reducing friction when switching between systems
- **Explicit CPU Override**: Provides a special `'cpu:-1'` device specification to force CPU usage regardless of available accelerators.
- **Mocked CUDA Functions**: Provides mocked implementations of CUDA-specific functions, enabling code that uses CUDA functions to run on MPS hardware.
- **Stream and Event Support**: Implements full support for CUDA streams and events on MPS devices, allowing for asynchronous operations and event timing.
- **Unified Memory Handling**: Handles differences in memory management between CUDA and MPS, providing reasonable values for memory-related functions.
- **Logging and Debugging**: Outputs informative log messages indicating how calls are intercepted and handled, assisting in code migration and debugging.
- **Transparent Integration**: Works transparently without requiring changes to existing codebases.
- **PyTorch Compiler Compatibility**: Works seamlessly with PyTorch's dynamo compiler and inductor.

### Development & Availability

This project is **actively developed** and available on **[GitHub](https://github.com/unixwzrd/TorchDevice)**. Future updates may include **enhanced optimizations for mixed-device workflows**.

For installation, usage, and technical details, see the project's **[README](https://github.com/unixwzrd/TorchDevice)**.
