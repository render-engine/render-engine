::: src.render_engine.page.Page

## Invalid Attrs

Some attributes need to be not modified. For example, the `Page.slug` attribute needs to be slugified. If the user tries to set the `Page.slug` attribute to a non-slugified string, the path will be invalid.

To protect your Page from _unexpected_ behavior, the `invalid_attrs` attribute is a list of attributes that cannot be set. If the user tries to set an attribute in the `invalid_attrs` list, a debug message will be logged and the value will be stored in an attribute with prefixed with `_`.

Example:
```md

# test-page.md

---
title: Test Page
slug: test-page
---

This is a test page.
```

```python
# app.py

@site.page
class Page:
    content_path = 'test-page.md'
```

Rendering the page with result in the following debug message:

```shell
>>> 'slug' is not a valid attribute. Setting to '_slug'
```
