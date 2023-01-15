## Simple Site Layout
Render Engine has a very simple site layout. You can see the example site layout below.

```bash
.
├── app.py # Logic/Configuration for building your site
├── content
│  ├── pages # collection of files to build similarly styled pages
│  │  └── about.md
│  │  └── contact.md
│  └── index.md # file to build a single page
├── static # static files (images, css, javascript)
│  ├── img.jpg
│  └── style.css
└── templates # jinja templates
   └── index.html
```

## Building your Site

Render Engine uses classes to create most of the object. You will need to import the `Site` and `Page`/`Collection` classes you'll need `render_engine`.

```python
# app.py

from render_engine import Site, Page, Collection
```

### Creating your Site
Let's look at the `app.py` file and explore the different components.

```python
# app.py
from render_engine import Site, Page, Collection
from render_engine.parsers.markdown import MarkdownPageParser


class MySite(Site):
    site_vars = {
      "SITE_TITLE": "My Website",
      "SITE_URL": "https://example.com",
      "SITE_AUTHOR": "Peter Parker",
    }

site = Site()

@site.page
def index(Page):
    Parser = MarkdownPageParser
    title = "Welcome to my Site!"
    template = "index.html"
    content_path = "content/index.md"


@site.collection
def pages(Collection):
    PageParser = MarkdownPageParser
    template = "page.html"
    content_path = "content/pages"

if __name__ == "__main__":
    site.render()
```

The page that is created there will generate a file called `index.html` in the output directory. That name comes from the class name but can be defined either in the class itself (using the `slug` attribute) or in an markdown file (defined with the `content_path` attribute).

The `template` variable is the name of the template file that will be used to render the page. The `title` variable will be passed to the template as `title`.

The default template engine is [jinja2](https://jinja.palletsprojects.com/en/3.0.x/). This means you can use jinja2 syntax in your templates.

```jinja2
# templates/index.html
<h1>{{title}}</h1>
```

would render as:

```html
# output/index.html

<h1>Welcome to my Page!</h1>
```

### Adding attributes from a file:
Render Engine can also add attributes to your page from a markdown file. This is useful if you want to add a lot of content to your page. To do this, Render Engine uses [frontmatter](https://pypi.org/project/python-frontmatter/) to parse the attributes at the topc of the markdown file.

```markdown
# content/index.md
---
title: Welcome to my Page!
template: index.html
---

I'm happy that you are here!
```

In order to use this, you must set the `content_path` attribute to the path of the markdown file.

```python
@mysite.render_page()
class Index(Page):
  content_path="content/index.md"
```

The end result is the same as the previous example. If we want to get the content of the markdown file, we can pass the `content` attribute to the jinja2 template.

```jinja2
# templates/index.html

<h1>{{title}}</h1>
{{content}}
```
The markdown in `content` will converted to html and rendered in the template.

```html
<h1>Welcome to my Page!</h1>
<p>I'm happy that you are here!</p>
```

### Creating a Collection:
Collections are a group of pages that are rendered using the same template and (some) attributes. They are created using the `Collection` class and the `render_collection` decorator.

```python
# app.py

@mysite.render_collection()
class Blog(Collection):
  template="blog.html"
  content_path="content/blog"
```

The `content_path` attribute is the path to the folder that contains the markdown files for the collection. Every markdown page will be converted into a `Page` object. The `template` attribute is the name of the template that will be used to render each page in the collection.

You an also pass custom attributes to the collection. These attributes will be passed into each page in the collection as well.

### Custom Collections

We named our collection Blog but if you noticed there aren't a lot of features that come with a blog included. Render Engine has a built in `Blog` class that you can use to create a blog. It will automatically create a collection of posts and a page for each post. It will also create a page for the blog index and an RSS Feed.

It's still rendered using the same `render_collection` decorator.

```python
# app.py

@mysite.render_collection()
class Blog(Blog):
  template="blog.html"
  content_path="content/blog"
```

### Generating your site

Once you have your site's build file (in our case app.py), you can generate the site by running the `generate` method on your site object.

```bash
python app.py
```

Your site will be generated in the `output` folder. You can change the output folder by passing in the `output_path` attribute to the `Site` class.
