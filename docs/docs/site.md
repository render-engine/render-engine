---
title: "Site"
description: "Overview of the Site class in Render Engine, including attributes, functions for managing pages and collections, and rendering content."
date: August 22, 2024
tags: ["site", "pages", "collections", "rendering"]
---

The site stores your pages and collections to be rendered.

**Attributes:**

| Name | Type | Description |
| --- | --- | --- |
| `output_path` | `str` |path to write rendered content |
| `partial` | `bool` |if True, only render pages that have been modified. Uses gitPython to check for changes. |
| `static_paths` | `set` |set of paths for static folders. This will get copied to the output folder. Folders are recursive. |
| `site_vars` | `dict` |dictionary that will be passed into page template |
| `site_settings` |  |settings that will be passed into pages and collections but not into templates |

## Functions

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

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `*themes` | `Theme` |Theme objects to register | `()` |

### `render()`

Render all pages and collections.

These are pages and collections that have been added to the site using
the [`Site.page`](site.md?id=page)
and [`Site.collection`](site.md?id=collection) methods.

Render should be called after all pages and collections have been added to the site.

You can choose to call it manually in your file or
use the CLI command [`render-engine build`](cli.md?id=build)
