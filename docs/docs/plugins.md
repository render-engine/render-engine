Plugins are a way to extend the functionality of the render engine site.

Plugins are registered by adding them to the `plugins` list in the site class.

```python

from render_engine import Site, Collection, Page

class MySite(Site):
    plugins = [
        MyPlugin,
    ]

my_site = MySite()
```

Plugins are passed to collections and pages when the `site.collection` and `site.page` methods are called.

```python

@my_site.page # plugins are ran on the page
class MyPage(Page):
    pass

@site.collection # plugins are ran on each page in the collection
class MyCollection(Collection):
    pass

my_site.route_list['mypage']._pm.list_name_plugin()
>>> ['MyPlugin']
```

### Implementing a plugin

Plugins are built with pluggy. See the [pluggy documentation](https://pluggy.readthedocs.io/en/latest/#) for more information.

Plugins use the entrypoints defined in `render_engine.hookspecs`. These allow plugins to be called at different points in the render engine lifecycle.

For example the `CleanOutput` plugin uses the `pre_build_site` entrypoint to remove the output directory before rendering.

### Ingnoring Plugins

Pages and collections can ignore plugins by passing a list of plugin names to the `ignore_plugins` attribute.

```python
class MySite(Site):
    plugins = [
        MyPlugin1,
        MyPlugin2,
    ]

class MyPage(Page):
    ignore_plugins = [MyPlugin1]

my_site.route_list['mypage']._pm.list_name_plugin()
>>> ['MyPlugin2']
```
