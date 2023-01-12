# \<CONTENTPARSER>

Explain the type of content this parser works with.

Add some information about the type of content

Let people know what is doing the underlying parsing.
The underlying parser i

## Parser Options:
These are the options that can be pulled from the Page object:

| Option | Description |
| --- | --- |
| `<arg1>` | You can add notes about the args here|


## Content Path Type

Provide a suggestion for the type of content that your parser expects.

\<CONTENTPARSER> expects a `path|url` in the content_path field of the Page object.

```python
class MyPage(Page):
    content_path = "~/.my_page.md"
    # or content_path = "https://example.com/my_page.md"
```
