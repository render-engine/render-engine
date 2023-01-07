# Creating a Page:

`Page` objects represent a single webpage on your site. They are rendered using the site's `page` decorator. You can pass any attributes into the `Page` class that you want to be available in your template. There are also some special variables that are used by Render Engine.

The most important attributes are `template`, `content` or `content_path` and the Page's `Parser`

```python
# app.py

@mysite.page()
class Index(Page):
  title="Welcome to my Page!"
  template="index.html"
```

The page that is created there will generate a file called `index.html` in the output directory. That name comes from the class name but can be defined either in the class itself (using the `slug` attribute) or in an markdown file (defined with the `content_path` attribute).

The `template` variable is the name of the template file that will be used to render the page. The `title` variable will be passed to the template as `title`.

The default template engine is [jinja2](https://jinja.palletsprojects.com/en/3.0.x/). This means you can use jinja2 syntax in your templates.

```jinja2
# templates/index.html
<h1>{{title}}</h1>
```
