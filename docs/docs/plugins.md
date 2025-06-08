---
title: "Enhancing Functionality with Plugins"
description: "Guide to using and managing plugins in Render Engine. Learn how to register plugins, apply them to pages and collections, and exclude specific plugins."
date: August 22, 2024
tags: ["plugins", "render-engine", "customization"]
---

Plugins are a way to extend the functionality of the render engine site.

## Registering Plugins

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

When the `site.collection` and `site.page` methods are called the collection/page is populated with all currently
registered plugins. Additional calls to `site.register_plugins` after the call to `site.collection` or
`site.page` will **not** register the new plugin with the collection/page.

```python
from render_engine import Site, Collection, Page
from my_plugins import Plugin1, Plugin2

app = Site()
app.register_plugins(Plugin1)


@my_site.page # Plugin1 is registered here.
class MyPage(Page):
    pass

@site.collection # Plugin1 is registered here.
class MyCollection(Collection):
    pass

app.register_plugins(Plugin2) # Plugin2 is only registered for the site and not for MyPage or MyCollection
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

### Overriding and Augmenting Plugin Settings

Plugins are implemented with a dictionary of default settings. These settings can be overridden and/or augmented
when we register the plugin.

```python
# Add a keyword parameter where the key is the plugin class name and the value is the new settings
app.register_plugins(MyPlugin1, MyPlugin2, MyPlugin1={'settings': 'overide'})
```

Alternatively when adding a plugin to a collection or page:

```python

@app.page
class MyPage(Page):
    plugins = [(MyPlugin, {'settings': 'override'})]
```

**Note**: Registering a plugin with settings will merge the default settings with the overridden settings. If you
register a plugin that has default settings of `{'setting1': 'a'}` with settings `{'setting2': 'b'}` the
settings sent to the plugin will be `{'setting1': 'a', 'setting2': 'b'}`.

### Implementing a plugin

Plugins are built with pluggy. See the [pluggy documentation](https://pluggy.readthedocs.io/en/latest/#) for more information.

Plugins use the entrypoints defined in `render_engine.plugins`. These allow plugins to be called at different
points in the render engine lifecycle.

Currently supported hooks are:

| Hook | Parameters |
| ---- | ---- |
| pre_build_site | `site: Site, settings: dict` |
| post_build_site | `site: Site, settings: dict` |
| pre_build_collection | `collection: Collection, site: Site, settings: dict` |
| post_build_collection | `collection: Collection, site: Site, settings: dict` |
| render_content | `page: Page, settings: dict, site: Site` |
| post_render_content | `page: Page, settings: dict, site: Site` |

All plugin classes must include a dictionary of `default_settings`. All of the hooks take a `site: Site`
and a `settings: dict` parameter. The `pre_build_collection` and `post_build_collection` also take a
`collection: Collection` parameter. The `render_content` and `post_render_content` take a
`page: Page` parameter in addition to the

**Plugin hooks must be `staticmethod` and do not take `self` as a parameter.**

To access the settings in your plugin you need to use `settings[<PluginClassName>]`:

```python
class MyPlugin:
    default_settings = {}

    @staticmethod
    @hook_impl
    def pre_build_site(site; Site, settings: dict):
        my_settings = settings['MyPlugin']
        ...
```
