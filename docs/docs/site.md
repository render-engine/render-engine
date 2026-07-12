---
title: "Site"
description: "Overview of the Site class in Render Engine, including attributes, functions for managing pages and collections, and rendering content."
date: August 22, 2024
tags: ["site", "pages", "collections", "rendering"]
---

The site stores your pages and collections to be rendered.

**Attributes:**

| Name                   | Type     | Description                                                    |
|------------------------|----------|----------------------------------------------------------------|
| `output_path`          | `str`    | path to write rendered content                                 |
| `static_paths`         | `set`    | paths for static folders copied to output (recursive)          |
| `site_vars`            | `dict`   | dictionary that will be passed into page template              |
| `render_html_site_map` | `bool`   | When True render the site map as an HTML file. Default: False. |
| `render_xml_site_map`  | `bool`   | When True render the site map as an XML file. Default: False.  |
| `slug_only_urls`       | `bool`   | default value for pages for [`slug_only_url`]                  |

> !!! Note
    These attributes can be set as class level attributes when subclassing `Site`, as parameters during instantiation,
    or updated as attributes later on. If they are set as class level attributes those values will be used during
    instantiation regardless of what is sent to the constructor.

## Functions

### `Site()`

```python
from render_engine import Site

Site(
    *,
    output_path: str | Path = "output",
    template_path: str | Path = "templates",
    static_paths: set[str | Path] = {"static"},
    plugin_settings: object | dict = SENTINEL,
    render_html_site_map: bool = False,
    render_xml_site_map: bool = False,
    slug_only_urls: bool = False,
    site_vars: object | dict = SENTINEL,
    static_include_patterns: set[str] | None = None,
    static_exclude_patterns: set[str] | None = None,
    static_exclude_dirs: set[str] | None = None,
    static_include_dirs: set[str] | None = None,
    include_static_in_site_map: bool = False,
) -> None:
    pass
```

The `Site` constructor takes the following keyword arguments:

<!-- markdownlint-disable MD056 -->
<!-- markdownlint-disable MD060 -->
| Name                   | Type         | Description                                                                              |
|------------------------|--------------|------------------------------------------------------------------------------------------|
| `output_path`          | `str | Path` | Path to write rendered content.                                                          |
| `template_path`        | `str | Path` | Path to location of template files.                                                      |
| `static_paths`         | `str | Path` | Paths for static folders copied to output (recursive).                                   |
| `plugin_settings`      | `dict`       | Dictionary caontaining plugin settings.                                                  |
| `render_html_site_map` | `bool`       | When True render the site map as an HTML file. Default: False.                           |
| `render_xml_site_map`  | `bool`       | When True render the site map as an XML file. Default: False.                            |
| `slug_only_urls`       | `bool`       | Default value for Page objects rendering slub only URLS. Default: False                  |
| `site_vars`            | `dict`       | The site_vars dictionary containing data to be passed to all templates during rendering. |
| `static_include_patterns` | `set[str] \| None` | Glob patterns a static file must match to be included. Default: `None` (no filtering). |
| `static_exclude_patterns` | `set[str] \| None` | Glob patterns that exclude a static file even if it matched an include pattern. Default: `None`. |
| `static_exclude_dirs`  | `set[str] \| None` | Directory names to skip entirely under any static path. Default: `None`. |
| `static_include_dirs`  | `set[str] \| None` | Subdirectory paths that override `static_exclude_dirs` for matching subdirectories. Default: `None`. |
| `include_static_in_site_map` | `bool` | When True, static files are added to the site map. Default: `False`. |
<!-- markdownlint-enable MD056 -->
<!-- markdownlint-enable MD060 -->

### `collection(Collection)`

Add the collection to the route list to be rendered later.

This is the primary way to add a collection to the site and
can either be called on an uninstantiated class or on the class definition as a decorator.

In most cases. You should use the decorator method.

```Python
from render_engine import Site, Collection

site = Site()

@site.collection # works
class Pages(Collection):
    pass


class Posts(Collection):
    pass

site.collection(Posts) # also works
```

### `load_themes`

function for registering the themes with the theme_manager.
Used prior to rendering and cli-tasks

### `page(Page)`

Add the page to the route list to be rendered later.
Also remaps `title` in case the user wants to use it in the template rendering.

This is the primary way to add a page to the site and can either be called
on an uninstantiated class or on the class definition as a decorator.

In most cases. You should use the decorator method.

```Python
from render_engine import Site, Page

site = Site()

@site.page # works
class Home(Page):
    pass

class About(Page):
    pass

site.page(About) # also works
```

### `register_theme(theme)`

Overrides the ThemeManager register_theme method to add plugins to the site

### `register_themes(*themes)`

Register multiple themes.

**Parameters:**

| Name      | Type    | Description               | Default |
| --------- | ------- | ------------------------- | ------- |
| `*themes` | `Theme` | Theme objects to register | `()`    |

### `render()`

Render all pages and collections.

These are pages and collections that have been added to the site using
the [`Site.page`]
and [`Site.collection`] methods.

Render should be called after all pages and collections have been added to the site.

You can choose to call it manually in your file or
use the CLI command [`render-engine build`]

[`render-engine build`]: cli.md?id=build
[`site.collection`]: site.md?id=collection
[`site.page`]: site.md?id=page
[`slug_only_url`]: page.md#slug-only-urls
