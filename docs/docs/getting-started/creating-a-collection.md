# Creating a Collection

[Collection] objects allow you to build multiple Pages from a single configuration. They are rendered using the site's `collection` decorator.

You can build a collection by defining `Collection` class object. You'll also need to provide a `content_path` that points to the page references for each page. By default, collections work with a directory of files. Each file will be used to build a page.

```bash
pages
├── about.md
├── contact.md
└── ideas.md
```

Each file can have the differing information for each page. For example, the `spiderman.md` file could have the following information:

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

The collection would have all the information to parse all its pages the same. These could be attributes like the `template` or the `PageParser` that is used to parse each page in the collection. The individual pages attributes can  be referenced in the template or used for sorting or other functions.

```python

# app.py

from render_engine import Site, Collection
from render_engine.parsers.markdown import MarkdownPageParser

app = Site()

@app.collection()
class Heroes(Collection):
  content_path = "content/heroes"
  template = "heroes.html"
  PageParser = `MarkdownPageParser`
```

[Collection]: ../collection
[Creating a Page]: /getting-started/creating-a-page
