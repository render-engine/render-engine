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

## Including Static Files in the Site Map

By default, the `SiteMap` also includes an entry for every static file found in
the `Site`'s `static_paths` (e.g. images, CSS, JS, and any other files copied
from your static directories). This means static assets show up in both the
generated HTML site map and the XML site map alongside your `Page` and
`Collection` entries.

Static file entries use the URL they are ultimately served at, based on where
`static_paths` are copied to in the output directory. For example, a file at
`static/images/logo.png` will appear in the site map with the URL
`/static/images/logo.png`.

If you want to add static files to a `SiteMap` manually — for example, when
working with the `SiteMap` object directly rather than through `Site.render()`
— use the `add_static_files` method:

```python
def add_static_files(
    self,
    static_paths: Iterable[str | Path],
    include_patterns: Iterable[str] | None = None,
    exclude_patterns: Iterable[str] | None = None,
    exclude_dirs: Iterable[str] | None = None,
    include_dirs: Iterable[str] | None = None,
) -> None:
```

<!--  markdownlint-disable-next-line MD024 -->
### Parameters

- `static_paths`: An iterable of directories (as `str` or `Path`) to walk for
  static files. This is normally `Site.static_paths`, the same set of
  directories copied to the output folder.
- `include_patterns`: An iterable of glob patterns a file must match to be
  included in the site map. Defaults to `None`, meaning no filtering — every
  file is included.
- `exclude_patterns`: An iterable of glob patterns that exclude a file even
  if it matched an `include_patterns` entry. Defaults to `None`, excluding
  nothing.
- `exclude_dirs`: An iterable of directory names to skip entirely, matched
  against any path segment relative to the static directory. Defaults to
  `None`, excluding nothing.
- `include_dirs`: An iterable of subdirectory paths that override
  `exclude_dirs`, forcing inclusion for matching subdirectories even if a
  parent directory was excluded. Defaults to `None`, meaning no override.

Note: `SiteMap.update()` will automatically call `add_static_files` for you
if the `SiteMap` has `static_paths` set and `include_static_in_site_map` is
`True`, using `Site.static_include_patterns`, `Site.static_exclude_patterns`,
`Site.static_exclude_dirs`, and `Site.static_include_dirs` — so in most cases
you won't need to call this directly, or configure filtering anywhere except
on your `Site` object. Setting `include_static_in_site_map=False` on `Site`
excludes static files from the site map entirely, without affecting whether
they are copied to the output directory. For example:

```python
site = Site(
    static_paths={"static"},
    static_include_patterns=("*.css", "*.js", "*.png"),
    static_exclude_dirs=("drafts",),
    static_include_dirs=("drafts/public",),
    include_static_in_site_map=True,
)
```

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

## The `StaticSiteMapEntry` object

`StaticSiteMapEntry` is a subclass of `SiteMapEntry` used to represent static
files (images, CSS, JS, etc.) in the site map, rather than `Page` or
`Collection` objects. It shares the same `url_for` property and `__str__`
behavior as `SiteMapEntry`, so it can be used interchangeably anywhere a
`SiteMapEntry` is expected — for example, when iterating over a `SiteMap` or
using `SiteMap.find()`.
