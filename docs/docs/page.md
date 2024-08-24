---
title: "Page Objects"
description: "Overview of Page Objects in Render Engine, including BasePage and Page classes, their attributes, and how they fit into the 3-layer architecture"
date: August 22, 2024
tags: ["basepage", "page-objects", "installation"]
---
<!-- markdownlint-disable MD056 -->

At Render Engine's core is the page. A page is a single unit of content. Pages are the building blocks of your site. If you want to display information on your site, you will need to create a page.

## BasePage

All `Page` objects inherit from `BasePage`, allowing for common functionality across all page objects.

The `BasePage` is designed for Render Engine to render common `Page`-like objects. It is not designed to be used directly.

Bases: BaseObject

This is the Base Page object.

It was created to allow for the creation of custom page objects.

This is not intended to be used directly.

**Attributes:**

| Name | Type | Description |
| --- | --- | --- |
| `slug` |  |The slug of the page. Defaults to the `title` slugified. |
| `content` |  |The content to be rendered by the page |
| `parser` |  |The Parser used to parse the page's content. Defaults to `BasePageParser`. |
| `reference` |  |The attribute to use as the reference for the page in the site's route list. Defaults to `slug`. |

### Functions

#### `url_for()`

Returns the URL for the page including the first route.

This gets the relative URL for a page.

> !!! Note
    Pages don't have access to the Site attrs. You cannot get an abolute URL from a Page object.
    Use `{{SITE_URL}}` in your templates to get the absolute URL.

This is the preferred way to reference a page inside of a template.

## Page

When you're creating a `Page`. You may want to provide a [`parser`](parsers.md) or `content`/`content_path`. To do this, you will need to create a `Page` object.

Bases: [`BasePage`](page.md?id=basepage)

The general BasePage object used to make web pages.

Pages can be rendered directly from a template or generated from a file.

> !!! Note
    Not all attributes are defined by default (those that are marked optional) but will be checked for in other areas of the code.

When you create a page, you specify variables passed into rendering template.

**Attributes:**

| Name | Type | Description |
| --- | --- | --- |
| `content_path` | `str | None` |The path to the file that will be used to generate the Page's `content`. |
| `extension` | `str | None` |The suffix to use for the page. Defaults to `.html`. |
| `engine` | `str | None` | If present, the engine to use for rendering the page. **This is normally not set and the `Site` 's engine will be used.** |
| `reference` | `str | None` |Used to determine how to reference the page in the `Site`'s route_list. Defaults to `slug`. |
| `routes` | `str | None` |The routes to use for the page. Defaults to `["./"]`. |
| `template` | `str | None` |The template used to render the page. If not provided, the `Site`'s `content`will be used. |
| `Parser` | `type[BasePageParser]` |The parser to generate the page's `raw_content`. Defaults to `BasePageParser`. |
| `title` | `str` |The title of the page. Defaults to the class name. |

## About Page Attributes

### Users use the public systems use the private

It's important to note that while public attributes are used by users, private attributes are used by the system. For example, the `Page._content` attribute is used by the system to build the `str` value of the page. This means that while the user may change the value of `Page.content`, the system has the ability to return a different value based on the `Page._content` property.

For Example:

```python
class CustomPage(Page):
    @property
    def _content(self):
        return self.content + "!"


class MyPage(CustomPage):
    content = "Hello World"
```

The Content that will be passed to Markup will be "Hello World!".

### Page Content

Page.content and be anything but Page._content must be a `str`.

By default Page._content will return the result of `Page.Parser.parse(Page.content)`.

### Page Templates

`Page.template` should always be a `str`. `Page.template` refers to the template name that will be passed to the engine given to `Page.render()`.
