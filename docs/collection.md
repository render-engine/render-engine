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

Subcollections are a filtered group of items in the collections. Subcollections 
are created by specifying the attribute to check against.

```
class TestPage1(Page):
		foo = 'bar'

class TestPage2(Page):
		foo = 'biz'


class MyCollection(Collection):
		subcollections = ['foo']


# This would yield two subcollections
bar(Collection):
		content_items = [TestPage1]

biz(Collection):
		content_items = [TestPage2]

```

Subcollections have [archives][Archive]. Each subcollection inherits from its
parent and therefore gives you the ability to pull attributes that it's parent
also has (by default). This is great for mirroring functionality between the
collection and subcollection.

Subcollections are not added to a site until the site is rendered. Note that
due to this, You may see extended processing times based on the number of
subcollections your site has.

## archive

`has_archive: bool = False`

An archive is a list of pages with references to the page items.

If [paginated](#paginated) is False, the list will only contain a single
Archive [Page] object.

If [paginated](#paginated) is True, the list will be segmented by the
[items_per_page](#items_per_page) value.

Instruct the [Site] to generate archives with the [has_archive] flag.

You can generate archives by calling the `Archive` attribute. EVEN IF
`has_archive` is set to `False`

## Archive Values

Even though Archive objects are [Page]

## archive_template

`archive_template: str = "archive.html"`

Template that will be used with `[Collection.archive](#archive)`



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
[Page]: /page.html
[Archive]: #archive
[Site]: /site.html
