Collection
----

A Collection is great when you have many pages with similar attributes or pages
that should be grouped together.

Collection attributes will be applied to each page in the collection.

### content_items

`content_items: typing.List[Page] = []`

If you have a group of [Page]-like items that you would like to be bundled into a
collection.

This is good for building a collection of objects of a DIFFERENT [content_type].

### content_path

`content_path: str = ""`

Builds items of the same [content_type].

Used for content files in a folder that you would like to have the same
content_type, template, routes.

`content_path`


### Combining `content_items` and `content_path`

It is possible to define both `content_items` and a `content_path` in a
collection. This could lead to unexpected consequences when rendering your
site. You could potentially overwrite files. Make sure all objects are
unique.


### content_type

content_type: typing.Type[Page] = Page

Sets the `content_type` for each item in the `[content_path]`.


### template

template: str = "page.html"

Sets the template the for each item in the `[content_path]`.


### includes

`includes: typing.List[str] = [".md", "*.html"]`

The type of files that will be looked at in the `[content_path]`.

Any files in [content_path] with extensions not listed in `includes` will be
skipped.


### routes

`routes: typing.List[str] = [""]`



### subcollections

`subcollections: typing.List[str] = []`




Not So Safe Attributes
====

### engine

`engine: Optional[str]=None # _inherits from Site_`

The engine needs to be added to the site dictionary of engines.

```
import Mako

class mako(Engine):
  ... # code for mako to be compatible with Render Engine

site = Site()
site.engines['Mako'] = mako

class MyCollection():
  engine = 'Mako'
```

The page's Engine of the is responsible for generating content for your
webpage. In most cases this will be provided by the site and should not be
changed.

[content_type]: #content-type
[Page]: page.html
