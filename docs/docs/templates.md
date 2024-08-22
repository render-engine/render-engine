---
title: "Templates"
description: "Guide to using templates in Render Engine with Jinja2, including global variables, filters, and formatting options."
date: August 22, 2024
tags: ["jinja2", "templates", "filters", "site-variables","route-list"]
---

Like most Python web frameworks, Render Engine also supports templating.

Render Engine uses the [Jinja2](https://palletsprojects.com/p/jinja/) templating engine. Jinja2 is a very powerful templating engine that is used by many Python web frameworks.

## Template Globals

Render Engine provides a few global variables that you can use in your templates.

### route_list

The route_list global is a list of all the routes that are registered with Render Engine. This is useful if you want to create a navigation bar or a sitemap.

### Attributes from site_vars

The site_vars global is a dictionary of all the variables that are defined in the `Site.site_vars`file. This is useful if you want to reference a variable site_wide in your templates.

```python

from render_engine import Site, Page

site = Site()
site.site_vars["SITE_NAME"] = "My Site"
site.site_vars["SITE_URL"] = "https://example.com"

```

### SITE_TITLE

The title of the site. This is useful if you want to reference the site title in your templates.

### SITE_URL

The url of the site. This is useful if you want to reference the site url in your templates. It can also be used to create absolute urls for your pages.

### DATETIME_FORMAT

This is the default format that the `format_datetime` filter will use. You can override this by setting the `DATETIME_FORMAT` variable in your `Site.site_vars` file.

By default this is set to `"%d %b %Y %H:%M %Z"`.

## Filters

Render Engine comes with a few [filters](https://jinja.palletsprojects.com/en/3.1.x/templates/#filters) that you can use in your templates.

### url_for(page)

The url_for filter is a wrapper around the `url_for` method for Pages. It allows you to reference a page by its slug or by its collection and slug.

```jinja2

{# The about page is a standalone `Page` #}
{{about | url_for}}

{# The about page is in the `Pages` collection. #}
{{'pages.about'| url_for }}

If you want to reference the archive for the page you can just use the Collection.slug attribute. You can also reference the paginated values with the page parameter on the `url_for` filter.

{# The about page is in the `Pages` collection. #}
{{'pages.about'| url_for }}

{# The `pages.archive[0]` url #}
{{'pages'| url_for }}

{# The first index of a paginated archive #}
{{'pages'|url_for(page=1)}}

```

### to_pub_date

This filter converts a datetime object to a [RFC 822](https://tools.ietf.org/html/rfc822) formatted date. This is useful for RSS feeds.

```jinja2

{{ page.date | to_pub_date }} --> Mon, 01 Jan 2000 00:00:00 -0000

```

### format_datetime

This filter converts a datetime object to a string. This is useful for formatting dates in your templates.

By default this will format to the site's `DATETIME_FORMAT` (default: `"%d %b %Y %H:%M %Z"`).

```jinja2

{{ page.date | format_datetime("%B %d, %Y") }} --> January 01, 2000

```
