::: src.render_engine.collection.Collection

# Passing Collection Variables to a Rendered Page

You can access attributes from the `Collection` class inside all of its rendered pages.

To do so, you must create an attribute called `template_vars` and populate it with a dictionary of key:value pairs.

In turn, each `Page` in the collection will have a `collection` attribute, similar to `Page.template_vars`. The dictionary includes any additional attributes you have defined within the `Collection` class.

```
from render_engine import Site, Collection

site = Site()

@site.collection
class BasicCollection(Collection):
    content_path = "content/pages"
    template_vars = {
        "some_value": "42"
    }

```

You can access `some_value` in your template like this:

```
{{collection.some_value}}
```