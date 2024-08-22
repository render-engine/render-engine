---
title: "Creating a Collection"
description: "Learn how to create and configure collections in Render Engine, including setting up page attributes, templates, and using the `Collection` class."
date: August 22, 2024
tags: ["collections", "page-configuration", "template-variables", "render-engine"]
---

[Collection](../collection.md) objects allow you to build multiple Pages from a single configuration. They are rendered using the site's `collection` decorator.

You can build a collection by defining `Collection` class object. You'll also need to provide a `content_path` that points to the page references for each page. By default, collections work with a directory of files. Each file will be used to build a page.

```bash
pages
├── about.md
├── contact.md
└── ideas.md
```

Each file can have differing information for each page. For example, the `spiderman.md` file could have the following information:

```txt
# content/heroes/spiderman.md

---
title: Spiderman
slug: spiderman
alias: Peter Parker
---

I'm a Photographer for the Daily Bugle. I'm also a superhero.
```

while `hulk.md` could have the following information:

```txt
# content/heroes/hulk.md

---
title: The Incredible Hulk
slug: hulk
alias: Bruce Banner
---

I'm a scientist. I'm also a superhero.
```

> ***NOTE***: For more information on how to build pages, see [Creating a Page][Creating a Page].

The collection would have all the information to parse all its pages the same. These could be attributes like the `template` or the `Parser` that is used to parse each page in the collection. The individual page attributes can be referenced in the template or used for sorting or other functions.

If you want to pass additional objects through the template context (see [Jinja's Template Context](https://jinja.palletsprojects.com/en/3.0.x/api/#the-context)), you can create a dictionary of additional attributes.

For example, if you want to send an attribute called `some_value` with a value of `"42"`, you can assign the dictionary to a `template_vars` attribute within your `Collection` class, and it will be passed to the template through a `collection` attribute that contains the key:value pair (`{"some_value: "42"}`).

```python

# app.py

from render_engine import Site, Collection
from render_engine.parsers.markdown import MarkdownPageParser

app = Site()

@app.collection()
class Heroes(Collection):
  content_path = "content/heroes"
  template = "heroes.html"
  Parser = `MarkdownPageParser`
  template_vars = {
    "some_value": "42"
  }
```

The value of `42` can be accessed in your template using `{{collection.some_value}}`.

## Continue to [Building your Site](building-your-site.md)

[Creating a Page]: creating-a-page.md
