# Markdown Parser

This is a parser for the Markdown markup language. This is the default parser for render_engine pages.

[Markdown](https://www.markdownguide.org) is a lightweight markup language with plain text formatting syntax. It is designed so that it can be converted to HTML and many other formats using a tool by the same name.

The underlying parser is [python-markdown2](https://pypi.org/project/markdown2/).

## Parser Options:
These are the options that can be pulled from the page:

| Option | Description |
| --- | --- |
| `markdown_extras` | A list of extensions to use. See [python-markdown2](https://pypi.org/project/markdown2/) for a list of extensions. |

## Content Path Type

Provide a suggestion for the type of content that your parser expects.

\<CONTENTPARSER> expects a `path|url` in the content_path field of the Page object.

```python
class MyPage(Page):
    content_path = "~/.my_page.md"
    # or content_path = "https://example.com/my_page.md"
```
