---
title: "Theme Management"
description: "Guide to managing themes in Render Engine, including adding custom templates, handling static files, and integrating third-party themes."
date: August 22, 2024
tags: ["themes", "static-files", "custom-templates", "theme-management"]
---

Themes are managed by your Site.

In Render Engine, themes are a collection of Jinja templates and static files used to render your site.

Themes can be added by registering a theme or providing your templates in the `templates` folder of your project.

## Adding your templates

You can provide your own theme by adding a `templates` folder to your project_path.

### Setting a custom templates path

You can set a custom templates path by setting the `template_path` attribute of your site.

```python
from render_engine import Site

class  MySite(Site):
    template_path = 'my_templates'

# You can also set this after you've initialized the class
# app = MySite()
# app.template_path = "my_templates"
```

## Handling Static Files

Static files can be added to the site as well either by you or a theme. This allows you to import custom css files, images, javascript and more.

Unlike templates you can have more than one static_path you wish to include. You can add mores static paths using `site.static_path.add("<path/to/static>")`.

```python
from render_engine import Site

class MySite(Site):
    static_path = "my_static"

# You can also set this after you've initialized the class
# app = MySite()
# app.static_path = "my_static"

```

Static files can be added at any level under the `static_path` directory.

All files and directories under the `static_path` will be copied to the `output_path` .

## Adding third-party themes

`Themes` can be added to your site by registering them.

```python
from sometheme import SomeTheme
from anothertheme import AnotherTheme

app = Site()
app.register_themes(SomeTheme)
```

## Falling back to default theme

Render Engine has a default theme collection that can be used as a fallback. These themes are used if a theme is not found in the registered themes.

Default Themes Templates pages:

- page.html

> **Note:**
> The default theme is extremely bare-bones and is only there in case you don't have a theme registered. It is recommended to register a theme or provide your own templates.
