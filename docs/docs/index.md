---
title: "What is RenderEngine"
description: "Overview of Render Engine, its 3-layer architecture, installation instructions, and initial setup."
date: August 22, 2024
tags:
  ["render-engine", "3-layer-architecture", "installation", "getting-started"]
---

## What is RenderEngine

### The _3 layer_ Architecture

- **[Page](page.md)** - A single webpage item built from content, a template, raw data, or a combination of those things.
- **[Collection](collection.md)** - A group of webpages built from the same template, organized in a single directory
- **[Site](site.md)** - The container that helps to render all Pages and Collections in with uniform settings and variables

### Installing Render Engine

In order to use render engine, you must have python 3.10 installed. You can download python from [python.org](https://python.org).

- Linux/MacOS: [python.org](https://python.org)
- Windows: [Microsoft Store](https://apps.microsoft.com/store/detail/python-311/9NRWMJP3717K)

Render Engine is available in PyPI and can be installed using pip:

```bash
pip install render-engine
```

To use the cli, install the cli extras

```bash
pip install render-engine[cli]
```

## Getting Started

Check out the [Getting Started](./getting-started/getting-started.md).
