---
title: "Simple Site Layout"
description: "Learn the basic structure of a Render Engine site, including file layout, site configuration, and adding pages and collections."
date: August 22, 2024
tags: ["site", "layout", "render-engine"]
---

Render Engine has a very simple site layout. You can see the example site layout below generated via the cli.

```shell
python -m render_engine init
```

```bash
.
├── app.py # Logic/Configuration for building your site
├── content
│  ├── pages # collection of files to build similarly styled pages
│  │  ├── about.md
│  │  └── contact.md
│  └── blogs
├── static # static files (images, css, javascript)
│  ├── img.jpg
│  └── style.css
└── templates # jinja templates
   └── index.html
```

## Building your Site

### Creating your Site

Let's look at the `app.py` file and explore the different components.

```python
# import Render Engine components
# import render engine plugins and themes
from render_engine import (
    Site,
    Page,
    Collection
)
from render_engine_kjaymiller_theme import kjaymiller
from render_engine_youtube_embed import YouTubeEmbed

# create Site() as `app` or `site`
# add your `output_path` (if not default)
# add local `static_paths`
# register plugins and themes

app = Site()
app.output_path = "output"
app.static_paths.add("static")
app.register_plugins(YouTubeEmbed)
app.register_theme(kjaymiller)

# add any custom settings
settings = {
    "SITE_TITLE":"My Cool Website",
    "SITE_URL":"http://example.com",
   "NAVIGATION": [{...}, ...]
   "plugins": "YouTubeEmbed": {...},
   "theme": {...},
}
app.site_vars.update(settings)

# Add Routes. Start with single pages and add Collections
@app.page
class Index(Page):
    template="index.html"

@app.collection
class Pages(Collection):
    content_path="content/pages" # path to files to build similarly styled pages


if __name__ == "__main__":
    app.render()
```

### Importing Render Engine Components

Render Engine uses classes to create most of the objects for the site.

You will need to import the `Site` and `Page`/`Collection` classes you'll need `render_engine`.

```python
# app.py

from render_engine import Site, Page, Collection
```

### Importing parsers needed to generate html

Render Engine uses parsers to convert content into html. There are two built-in parsers: ([BasePageParser](../parsers.md#basepageparser) and [MarkdownPageParser](../parsers.md#markdownpageparser)) or create your own.

Custom parsers can be imported and set in the `Parsers` attribute of the `Page` or `Collection` class.

```python
# app.py
from render_engine_rss import RSSCollection, RSSFeedPageParser
```

!!! IMPORTANT
    Some custom parsers will only work with [custom collections](../custom_collections.md). Please refer to the parser's documentation for more information.****

### Render Engine plugins and themes

Plugins and themes are not required but can be used to quickly get your site's style and functionality up and running quickly.

To use custom plugins and themes, you will need to import the parsers you want to use.

```python
from render_engine_kjaymiller_theme import kjaymiller
from render_engine_youtube_embed import YouTubeEmbed
```

Then you'll need to register the plugins and themes you want to use.

```python
app.register_plugins(YouTubeEmbed)
app.register_theme(kjaymiller)
```

!!! IMPORTANT
    You can register multiple themes but be careful of the order as theme files are looked up in REVERSE order they are added (LIFO - Last in, First out)

```python
from render_engine_kjaymiller_theme import kjaymiller
from render_engine_icon_packs import icon_packs

...

app.register_themes([kjaymiller, icon_packs])
```

### Adding custom site_vars

Render Engine has a few built-in site variables (`site_vars`) that can be used to customize your site. You can also add your own custom settings.

```python
#app.py

app = Site()
app.site_vars.update(
  {
   "SITE_TITLE":"My Cool Website",
  }
)
```

### Adding Pages and Collections

The page that is created there will generate a file called `index.html` in the output directory. That name comes from the class name but can be defined either in the class itself (using the `slug` attribute) or in a markdown file (defined with the `content_path` attribute).

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

### Adding attributes from a file

Render Engine can also add attributes to your page from a markdown file. This is useful if you want to add a lot of content to your page. To do this, Render Engine uses [frontmatter](https://pypi.org/project/python-frontmatter/) to parse the attributes at the top of the markdown file.

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

#### Creating a Collection

Collections are a group of pages that are rendered using the same template and (some) attributes. They are created using the `Collection` class and the `render_collection` decorator.

```python
# app.py

@mysite.render_collection()
class Blog(Collection):
  template="blog.html"
  content_path="content/blog"
```

The `content_path` attribute is the path to the folder that contains the markdown files for the collection. Every markdown page will be converted into a `Page` object. The `template` attribute is the name of the template that will be used to render each page in the collection.

You can also pass custom attributes to the collection. These attributes will be passed onto each page in the collection as well.

#### Custom Collections

We named our collection Blog but there aren't a lot of features that come with a blog included. Render Engine actually has a built-in `Blog` class you can use to create a blog. It will automatically create a collection of posts and a page for each post. It will also create a page for the blog index and an RSS Feed.

It's still rendered using the same `render_collection` decorator.

```python
# app.py

@mysite.render_collection()
class Blog(Blog):
  template="blog.html"
  content_path="content/blog"
```

### Continue to [Creating a Page](creating-a-page.md)
