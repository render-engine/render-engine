# Creating a Collection

[Collection] objects allow you to build multiple Pages from a single configuration. They are rendered using the site's `collection` decorator.

You can build a collection by defining `Collection` class object. You'll also need to provide a `content_path` that points to the page references for each page. By default, collections work with a directory of files. Each file will be used to build a page.

```bash
pages
├── about.md
├── contact.md
└── ideas.md
```

Each file can have the differing information for each page. For example, the `about.md` file could have the following information:

```txt
# content/pages/about.md

---
title: About Me
slug: about
name: Peter Parker
alias: Spiderman
---

I'm {{name}} and I like to write about things.

When I'm not writing, I'm usually fighting crime as your friendly neighborhood {{alias}}.
```

For more information on how to build pages, see [Creating a Page][Creating a Page].


The collection would have all the information to parse the page the same. These could be attributes like the `template` or the `PageParser` that is used to parse each page in the collection.

```python

# app.py

from render_engine import Site, Collection
from render_engine.parsers.markdown import MarkdownPageParser

app = Site()

@app.collection()
class Pages(Collection):
  content_path = "content/pages"
  PageParser =

```

[Collection]: ../collection
[Creating a Page]: /getting-started/creating-a-page
