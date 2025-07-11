---
title: "Collection"
description: "Guide to creating and managing collections in Render Engine, including attributes, functions, and archives."
date: August 22, 2024
tags: ["collection", "render-engine", "archive"]
---

Bases: `BaseObject`

Collection objects serve as a way to quickly process pages that have a portion of content that is similar or file driven.

Example:

```Python
from render_engine import Site, Collection

site = Site()

@site.collection
class BasicCollection(Collection):
    content_path = "content/pages"
```

Collection pages **MUST** come from a `content_path` and all be the same content type.

`content_path` can be a string representing a path or URL, depending on the [parser](parsers.md?id=basepageparser) used.

`sort_by` can be either a single `attribute` as a `str` or a `list` of attributes to be used as a sort key.

Attributes:

```Python
archive_template: The template to use for the Archive pages.
content_path: The path to iterate over to generate pages.
content_type: Type[Page] = Page
Feed: Type[RSSFeed]
feed_title: str
include_suffixes: list[str] = ["*.md", "*.html"]
items_per_page: int | None
Parser: BasePageParser = BasePageParser
parser_extras: dict[str, Any]
required_themes: list[callable]
routes: list[str] = ["./"]
sort_by: str | list = "title"
sort_reverse: bool = False
title: str
template: str | None
archive_template str | None: The template to use for the archive pages.
```

## Attributes

`archives: typing.Generator[Archive, None, None]` `property`

Returns a [Archive](archive.md) objects containing the pages from the `content_path`.

Archives are an iterable and the individual pages are built shortly after the collection pages are built. This happens when [Site.render](site.md?id=render) is called.

## Functions

`get_page(content_path=None)`

Returns the [page](page.md) Object for the specified Content Path

`iter_content_path()`

Iterate through in the collection's content path.

## Passing Collection Variables to a Rendered Page

You can access attributes from the `Collection` class inside all of its rendered pages.

To do so, you must create an attribute called `template_vars` and populate it with a dictionary of key:value pairs.

In turn, each `Page` in the collection will have a `collection` attribute, similar to `Page.template_vars`. The dictionary includes any additional attributes you have defined within the `Collection` class.

```python
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

<!-- markdownlint-disable-next-line -->
```
{{collection.some_value}}
```

## Collection Archives

Collection archives are a special type of page that is automatically generated for each collection.

You can have archives generated by setting the `has_archive` to True.

If you call `archives` from your collection and neither `has_archive` nor `items_per_page` is set, an error will be raised and an archive containing all pages will be generated.

For more information, see [Collection Archives](archive.md).
