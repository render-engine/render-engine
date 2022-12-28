::: render_engine.page


## list-attrs
`list-attrs` are attributes that can be defined by the page object.

```markdown
# my-page.md

---
name: my-page
tags: tag1, tag2
---

This is a test page
```

`list-attrs` will convert `tags` into an array of strings.


```
class page(Page):
    content_path: my-page.md


print(page().tags) 
# >>> ['tag1', 'tag2']
```