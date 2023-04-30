# Parsers

Parsers control how content is parsed and rendered.

All [`Page`][src.render_engine.page.Page] and [`Collection`][src.render_engine.collection.Collection] objects have a `parser`
attribute that is used to parse the content of the object.

Parsers use [staticmethods](https://docs.python.org/3/library/functions.html#staticmethod) to parse content. This allows you to create custom parsers that can be used to parse content in any way you want. Render Engine comes with a [BasePageParser](#basepageparser) and a [MarkdownPageParser](#markdownpageparser) that can be used out of the box.

## BasePageParser

:::src.render_engine.parsers.base_parsers.BasePageParser

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

In many cases you will want to create rich content. Render Engine comes with a `MarkdownPageParser` that can be used to parse Markdown files. You can also pass in attributes to the page via frontmatter at the top of the markdown file.

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

You can create custom parsers by subclassing [`BasePageParser`][src.render_engine.parsers.base_parsers.BasePageParser].

All the static methods for parsers should return a tuple where the first entry is a dictionary of attributes and the sencond entry is the rendered content.

!!! Warning
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
