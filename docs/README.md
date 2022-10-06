## What is RenderEngine

The idea of Render Engine is that you have the flexibility of dynamic webpages with the performance of static sites.

Render Engine was built out of frustration with existing tools.

## This is in Beta!

That Means:
- Things can (and will change)
- Things may break


## The _3 layer_ Architecture 

* **[Page](render_engine/page.html)** - A single webpage item built from content, a template, raw data, or a combination of those things.
* **[Collection](render_engine/collection.html)** - A group of webpages built from the same template, organized in a single directory
* **[Site](render_engine/site.html)** - The container that helps to render all Pages and Collections in with uniform settigns and variables

### The 4th Layer
Your site will have an _Engine_ as well. This is your templating engine and is Jinja2 by default. You can of course supply your own engine if you like.

You can expand any of these areas to customize your engine to your liking.

## As simple/complex as required

- Create your own templates to design the site your way (or don't and still get HTML)
- Content can be markdown/html to give you the content you need. You can also specify markdown extensions to expand how your content renders.

# Getting Started
## Installing Render Engine
Use pip - `pip install render-engine`

### Dependencies:
- Developed on [Python 3.10](https://python.org).

#### Other Dependencies that install with render-engine
- [Jinja2] - for template things
- [Pendulum] - for datetime things
- [more-itertools] - for iteration things
- [markdown2] - for markdown things


## Steps to Working Site
### Import Site and Page
`from render_engine import Site, Page`

### Create Site Class

```python
class MySite(Site):
    site_vars = {
      SITE_TITLE: "My Website",
      SITE_URL: "https://example.com",
      "some_template_variable": "Pass this to every page",
    }

mysite = MySite(static="static") # copies static files to your output
```

### Create a Page and let the site render it
```python
@mysite.render()
class Index(Page):
  title="Welcome to my Page!"

```


### Create some Collections
You don't have to render all the pages individually. You can create a collection of pages using **frontmatter** and markdown.

With frontmatter you can set your own variables to add to your jinja template.

```markdown
---
title: Spiderman Quotes
hero: spiderman
---

> With great power comes great responsibility -- Uncle Ben

```

Then store all of your markdown files in a folder and render them as a collection. You can set parameters around your collection like if you want an archive and how you want that archive sorted.

```python
@mysite.render_collection
class Heroes(Collection):
    has_archive: True
    sort_by: hero
    sort_reverse: true
    archive_template: "heroes.html"
    content_path: './content'
```

There is also a custom blog collection that has many of the features needed to get your blog off the ground.

```python
from render_engine import Blog

@mysite.render_collection
class Blog(Blog):
    content_path: './blog' # archive and sorting setup by default
```

Finally execute your python file.


---

### Featuers still in development:
- RSS Feeds
- SubCollections (Tags, Categories, Etc)
- Sitemap generation
- Visual Reporting

---

# Sponsors
This and much of the work that I do is made possible by those that sponsor me
on github.

### Sponsors at the $20/month and higher Level
- [Brian Douglas](https://github.com/bdougie)
- [Carol Willing](https://github.com/willingc)

Thank you to them and all of those that continue to support this project!

[Jinja2]: https://jinja.palletsprojects.com/en/latest
[Pendulum]: https://pendulum.eustace.io
[Click]: https://click.palletsprojects.com/en/latest
[more-itertools]: https://more-itertools.readthedocs.io/en/stable/
[markdown2]: https://pypi.org/project/markdown2/
