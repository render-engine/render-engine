---
title: "Parsers"
description: "Overview of content parsers in Render Engine, including BasePageParser, MarkdownPageParser, and custom parsers."
date: August 22, 2024
tags: ["basepageparser", "markdownpageparser", "custom-parsers", "rendering"]
---

Parsers control how content is parsed and rendered.

All [`Page`](page.md?id=page) and [`Collection`](collection.md?id=collection) objects have a `parser`
attribute that is used to parse the content of the object.

Parsers use [staticmethods](https://docs.python.org/3/library/functions.html#staticmethod) to parse content. This allows you to create custom parsers that can be used to parse content in any way you want. Render Engine comes with a [BasePageParser](https://github.com/render-engine/render-engine-parser) and a [MarkdownPageParser](https://github.com/render-engine/render-engine-markdown) that can be used out of the box.

## BasePageParser

The BasePageParser is the default parser for base-Page and collection object. This is a plain text parser that does not do any parsing of the content. It is useful for simple content that does not need to be parsed.

The `BasePageParser` will parse frontmatter and pass attributes of the page. The content will be returned as is.

```python
from render_engine.parsers.base_parsers import BasePageParser
from render_engine.page import Page

base_text = """
---
title: "Hello World"
---

This is base content
"""

class MyPage(Page):
    parser = BasePageParser
    content = base_text

my_page = MyPage()
my_page.title
>>> "Hello World"

my_page.content
>>> "This is base content"

my_page._render_content()
>>> "This is base content"

```

## MarkdownPageParser

In many cases, you will want to create rich content. The `MarkdownPageParser`. You can also pass in attributes to the page via frontmatter at the top of the markdown file.

```python
from render_engine.parsers.base_parsers import BasePageParser
from render_engine.page import Page

base_markdown = """
---
title: "Hello World"
---

This is **dynamic** content
"""

class MyPage(Page):
    parser = BasePageParser
    content = base_text

my_page = MyPage()
my_page.title
>>> "Hello World"

my_page.content
>>> "This is **dynamic** content"

my_page._render_content()
>>> "<p>This is <strong>dynamic</strong> content</p>"

```

## Creating Custom Parsers

You can create custom parsers.

All the staticmethods for parsers should return a tuple where the first entry is a dictionary of attributes and the second entry is the rendered content.

> !!! Warning
    Custom Parsers do not use frontmatter by default. You would need to ensure that your parser handles frontmatter if you want to use it.

For example, to create a parser that renders a dictionary, you could do the following:

```python
from src.render_engine.parsers.base_parsers import BasePageParser

class DictPageParser(BasePageParser):
    @staticmethod
    def parse_content(base_content: dict) -> dict:
        content = base_content.pop("content", "")
        return (base_content, content)

    # `parse_content_path` would be similar in this case.
    # `parse` would be inherited from `BasePageParser`

base_dict = {
    "title": "Hello World"
    "content": This is base content
}

class MyPage(Page):
    parser = DictPageParser
    content = base_dict

my_page = MyPage()
my_page.title
>>> "Hello World"

my_page.content
>>> "This is base content"

my_page._render_content()
>>> "This is base content"
```
