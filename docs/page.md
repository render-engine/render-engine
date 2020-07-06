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

class Index(Page):
  pass

site.route(Index())

```

Built-in Attributes of `Page`
======

Built-in attributes are not exposed to the template and can be used to give the
site instructions for building.

### engine
`engine: Optional[str]=None # _inherits from Site_`

:Caution: The engine is your translating tool, do no overwrite for a single
page unless you are doing something very specific.

```
import Mako

class mako(Engine):
  ... # code for mako to be compatible with Render Engine

site = Site()
site.engines['Mako'] = mako

class Index(Page):
  engine = 'Mako'
```

The page's Engine of the is responsible for generating content for your
webpage. In most cases this will be provided by the site and should not be
changed.

### template

`template: Optional[str]=None # _inherits from Site_`

Templates are given to the engine to create dynamic content to your site. 

The default template used for pages is `page.html`. Templates are commonly
changed.

```
class About(page): # the default template `templates/page.html` will be used.
    pass


class Index(Page): # the overriden template `templates/index.html` will be used.
    template = 'index.html'
```

### routes

`route: Optional[Union['str']]=['']`

Routes are the path to where the rendered content will be generated.

```
class About(Page):
    routes = ['/pages'] # will create page at '/pages/about.html'

```

### slug

`slug: Optional[str]=''`

The slug is the filename for the generated content.


It is referred to as the slug as the slug is often the pathname for a webpage. In static sites, the slug and the filename are identical.

The slug can be passed in as a string into the class object. It will always be
[slugified](https://pypi.org/project/python-slugify/) when the page is generated.
```
class somePage(Page):
    slug = 'about' # sets the filename to about.html
```

If no slug is provided, the title of the page will be used as the slug. 

```
# With Slug Present

class somePage(Page):
    slug = 'about' # sets the filename to about.html
    title = 'The About Page' # will not be used

# With No Slug Present

class somePage(Page):
    title = 'The About Page' # sets the filename to 'the-about-page.html'
```

If there is no slug or title, the class name will be used from `self.class.__name__`.

```
class Index(Page):
    pass # the filename will be 'index.html'

```

### content_path

`content_path: Optional[str]=''`

If a content_path is included, the page object will read the text at the given path and will process the path for attributes and content.

```
class About(page):
  content_path = 'content/pages/about.md'
```

### list_attrs

`list_attrs: Optional[Union['str']]=None`
