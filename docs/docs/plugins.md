---
title: "Enhancing Functionality with Plugins"
description: "Guide to using and managing plugins in Render Engine. Learn how to register plugins, apply them to pages and collections, and exclude specific plugins."
date: August 22, 2024
tags: ["plugins", "render-engine", "customization"]
---

Plugins are a way to extend the functionality of the render engine site.

Plugins are registered by using `register_plugins`

```python
from render_engine import Site
from my_plugin import MyPlugin

app = Site()
app.register_plugins(MyPlugin, my_plugin={"foo":"bar"})
```

Alternatively, you can pass a list of plugins to the `plugins` attribute of the `Site` class.

Plugins are passed to collections and pages when the `site.collection` and `site.page` methods are called.

```python
from render_engine import Site, Collection, Page

@my_site.page # plugins are ran on the page
class MyPage(Page):
    pass

@site.collection # plugins are ran on each page in the collection
class MyCollection(Collection):
    pass

my_site.route_list['mypage']._pm.list_name_plugin()
>>> ['MyPlugin']
```

## Single Page/Collection plugins

Plugins can be implemented on a case by case basis by adding them to the objects `plugins` attribute.

```python
app.register_plugins(MyPlugin1)

@app.page
class MyPage(Page):
    plugins = [MyPlugin2]

my_.route_list['mypage']._pm.list_name_plugin()
>>> ['MyPlugin1', 'MyPlugin2']

```

### Ignoring Plugins

Pages and collections can ignore plugins by passing a list of plugin names to the `ignore_plugins` attribute.

```python
app.register_plugins(MyPlugin1, MyPlugin2)

@app.page
class MyPage(Page):
    ignore_plugins = [MyPlugin1]

my_site.route_list['mypage']._pm.list_name_plugin()
>>> ['MyPlugin2']
```

### Implementing a plugin

Plugins are built with pluggy. See the [pluggy documentation](https://pluggy.readthedocs.io/en/latest/#) for more information.

Plugins use the entrypoints defined in `render_engine.hookspecs`. These allow plugins to be called at different points in the render engine lifecycle.
