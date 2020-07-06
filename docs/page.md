Page
----

Everything that that is visible to the web is just a page.

```
class Index(Page):
  pass
```

Page objects contain all the metadata.

You can register the page object in your site with the `@register_route`
decorator or you can pass the page object into the site with `site.route`.

```
@site.register_route
class Index(Page):
  pass
```

Using `@site.register_route` vs `route`
======

`@site.register_route` is an easy way to create a webpage for a given `Page`
object.

`@site.register_route` calls `site.route`, so there is no benefit to using one
over the other except for line count.


```
@site.register_route
class Index(Page):
  pass

# This is the same as

class Index(Page)
  pass

site.route(Index())

```

Built-in Attributes of `Page`
======

* engine
* template
* routes
* list_attrs
