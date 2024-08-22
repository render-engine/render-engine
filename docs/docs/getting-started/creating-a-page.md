---
title: "Creating a Page"
description: "Guide to creating and configuring `Page` objects in Render Engine, including setting attributes, handling content, and using `Parser` for content files."
date: August 22, 2024
tags: ["pages", "jinja2", "content-management", "render-engine"]
---

`Page` objects represent a single webpage on your site. They are rendered using the site's `page` decorator. You can pass any attributes into the `Page` class that you want to be available in your template. There are also some special variables that are used by Render Engine.

The most important attributes are `template`, `content` or `content_path` and the Page's `Parser`. These attributes tell the `Page` object how to render the output. That said, they are optional and render_engine will try to build the page without them.

```python
# app.py
from render_engine import Site, Page

app = Site()

@app.page
class Index(Page):
  title="Welcome to my Page!"
  template="index.html"
```

## Page Attributes

Because the template is rendered with [Jinja2], you can use any Jinja2 syntax in the template file. For example, you can use the `title` variable in the template like this:

```html
# templates/index.html

<h1>{{title}}</h1>

```

There are plenty of variables that are also inherited from the site as well

## Pages with Content

If you have some content that you want to use on your page, you can define it in the `content` attribute. This is useful for small pages that don't need a lot of content.

```python

@app.page
class About(Page):
  title="About Me"
  template="about.html"
  content="""
  I am a person who likes to write about things.
  """

```

### Pages with Content Files

If you have a lot of content, you can define the content in a file and use the `content_path` attribute to point to that file. You'll need to make sure the file type is supported by a [`Parser`][Parser] and that the `Parser` is defined in the `Page` class.

```txt
# content/about.md

---
title: About Me
slug: about
name: Peter Parker
alias: Spiderman
---

I'm {{name}}. I'm a web developer and I like to write about things.

When there's trouble, I'm there to save the day! As your friendly neighborhood {{alias}}!
```

The top section of the file is the metadata for the `Page`. Most Parsers will use this to set the `Page`'s attributes. The rest of the file is the content of the page. You can add attributes in the content file or in the Page itself.

```python
# app.py

import render_engine.parsers.markdown import MarkdownPageParser

@app.page
class About(Page):
  template="about.html"
  Parser=MarkdownPageParser
  content_path="content/about.md"

```

### Continue to [Creating a Collection](creating-a-collection.md)

[Jinja2]: https://palletsprojects.com/p/jinja/
[Parser]: ../parsers.md
