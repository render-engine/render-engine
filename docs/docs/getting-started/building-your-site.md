---
title: "Building your Site"
description: "Instructions on how to build your site using Render Engine, including using the `render()` method and the CLI `build` command."
date: August 22, 2024
tags: ["building", "site-generation", "render-engine"]
---

Once you've created the [layout](layout.md) of your site, you can start building it.

## Calling `render()`

Once you have your site's build file (in our case app.py), you can generate the site by calling the site's `render()` method.

```app.py
from render_engine.site import Site

app = Site()

@app.Page
class Page(Page):
    pass

if __name__ == '__main__':
    app.render()
```

## Calling `render-engine build`

You can also use the [CLI](../cli.md#building-your-site-with-render-engine-build) `build` command to build your site. It requires you to pass in the module and site object `module:object` format.

```bash
render-engine build app:app
```

Your site will be generated in the `output` folder.
