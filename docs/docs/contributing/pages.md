# About Page Attributes

## Users use the public systems use the private

It's important to note that while public attributes are used by users, private attributes are used by the system. For example, the `Page._content` attribute is used by the system to build the `str` value of the page. This means that while the user may change the value of `Page.content`, the system has the ability to return a different value based on teh `Page._content` property.

For Example:

```python
class CustomPage(Page):
    @property
    def _content(self):
        return self.content + "!"


class MyPage(CustomPage):
    content = "Hello World"
```

The Content that will be passed to Markup will be "Hello World!".

## Page Content

Page.content and be anything but Page._content must be a `str`.

By default Page._content will return the result of `Page.Parser.parse(Page.content)`.

## Page Templates

`Page.template` should always be a `str`. `Page.template` refers to the template name that will be passed to the engine given to `Page.render()`.
