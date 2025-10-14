---
title: "SiteMap Objects"
description: "Overview of the SiteMap"
date: September 27, 2025
tags: ["site-map"]
---
Prior to rendering the `Site` Render Engine will create a `SiteMap` containing searchable information
about all of the `Collection` and `Page` objects it has.

## Searching the `SiteMap`

To search the `SiteMap` use the `find` method.

```python
    def find(
        self,
        value: str,
        attr: str = "slug",
        collection: str = None,
        full_search: bool = False,
    ) -> SiteMapEntry | None:
```

### Parameters

- `value`: The value to search for
- `attr`: Optional attribute to search by. Options are `slug`, `title`, `path_name`. Defaults to `slug`.
- `collection`: Limit the search to a single `Collection`. Defaults to `None`.
- `full_search`: Search all `Page` and `Collection` objects. Defaults to `False`.

Notes:

1. If `collection` is set the search will be limited to that `Collection` object regardless of whether
`full_search` is set.
2. If `full_search` is set it will return the first match found. If you have 3 pages with the same `slug`,
1 not in a `Collection` and 2 others in different `Collection` objects, the first one defined will be the
one found.

## Generating an HTML site map

The `SiteMap` object has an `html` property that will return an HTML sitemap with _absolute_ URLs with the
`Site`'s `SITE_URL`.

As a convenience, Render Engine will generate a site map page if the `Site` property of `render_html_site_map`
is `True` (it defaults to `False`.) Please note that this will not be templated. Should you wish the generated
site map to be on a template you can add the following to your app:

```python
@app.page
class SiteMapPage(Page):
    template = "site_map_template.html"
    content = "{{ site_map.html }}"
    skip_site_map = True
```

Please note the `skip_site_map = True` to avoid having a self-referential link to the site map.

## Generating an XML site map

To have your site generate an XML site map set the `render_xml_site_map` property of your `Site` object
to `True` (defaults to `False`.) This will create the `site_map.xml` file in the root output directory
of your site.

## The `SiteMapEntry` object

The `SiteMap` is a collection of `SiteMapEntry` objects. Each `SiteMapEntry` has the following attributes
and properties:

### Attributes and Properties

- `slug` - The `slug` for the referenced `Page` or `Collection`.
- `title` - The `title` for the referenced `Page` or `Collection`.
- `path_name` - The `path_name` for the referenced `Page` or `Collection`.
- `entries` - A list of `SiteMapEntry` objects representing the `Page` objects in a given `Collection`.
for a `Page` this will be an empty `list`.
- `url_for` - This property will provide the _relative_ URL for the given entry.
