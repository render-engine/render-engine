---
title: "Installing Render Engine"
description: "Instructions for installing Render Engine, including dependencies and additional modules."
date: August 22, 2024
tags: ["installation", "render-engine"]
---

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

Render Engine also supports multiple parsers and modules. You will need to install them separately.

For example, to use the rss parser, you will need to install the [render-engine-rss] module:

```bash
pip install render-engine render-engine-rss
```

## Continue to [Creating Your App](creating-your-app.md)

[render-engine-rss]: https://pypi.org/project/render-engine-rss/
