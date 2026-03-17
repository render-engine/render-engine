---
title: "Installing Render Engine"
description: "Instructions for installing Render Engine, including dependencies and additional modules."
date: August 22, 2024
tags: ["installation", "render-engine"]
---

To use the render engine, you must have Python 3.10 or greater installed. You can download Python from [python.org].

- Linux/MacOS: [python.org]
- Windows: Install Python using [pymanager on Microsoft Store][ms-store], which manages Python installations.

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

## Continue to [Creating Your App]

[render-engine-rss]: https://pypi.org/project/render-engine-rss/

[creating your app]: creating-your-app.md
[ms-store]: https://apps.microsoft.com/detail/9NQ7512CXL7T
[python.org]: https://python.org
