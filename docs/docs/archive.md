---
title: "Archive"
description: "Guide to Archive objects used to display and manage a list of pages in a collection."
date: August 22, 2024
tags: ["archive", "parameters", "collection"]
---

Archives are a [`BasePage`](page.md?id=basepage) object used to display a list of [`Page`](page.md?id=page) objects in a [`Collection`](collection.md?id=collection).

Archive objects create a customizable page that can be controlled via its parent Collection.

Bases: [`BasePage`](page.md?id=basepage)

The Archive is a [Page](page.md?id=page) object used by the collection
that focuses on presenting the Collection's pages.

**Parameters:**

<!-- markdownlint-disable -->

| Name | Type | Description | Default |
| ---- | ---- | ---- | ---- |
| `pages` | `list[`[`BasePage`](page.md?id=basepage)`]` | The list of pages to include in the archive | _required_                                                |
| `title`         | `str`                                       | The title of the archive                                 | _required_                                                |
| `template`      | `str                                        | Template`                                                | The template to use for the archive                       | "archive.html" |
| `routes`        | `list[str                                   | Path]`                                                   | The routes for where the archive page should be generated | _required_     |
| `archive_index` | `int`                                       | The index of the page in the series of archive pages     | `0`                                                       |
| `num_of_pages`  |                                             | The total number of pages in the series of archive pages | _required_                                                |

> !!! Warning Not Directly Used
    The Archive object is not meant to be used directly.
    It is used by the [Collection](collection.md?id=collection) object.
    Attributes can be used to customize.

Collection.archives yields a generator of Archive objects. Each Archive object will have a `pages` attribute that is a list of Page objects referenced in that Archive Page. The number of pages is determined by the `Collection.items_per_page` attribute.

## Enabling Archive Pages

By default render engine will only create the archive page if either of the following conditions are met:

- The `Collection.items_per_page` attribute is set to a value greater than 0.
- The `Collection.has_archive` attribute is set to True.

## Archive Page Numbers

Archive pages are numbered starting at `0`. **The first page is always a list containing all the items.**

If `items_per_page` is greater than `0`, the remaining will contain the items in the collection, split into groups of `items_per_page`.

You can get the total number of `Archive` pages by grabbing the `Archive.num_archive_pages` attribute.
