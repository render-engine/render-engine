# Render Engine

The idea of Render Engine is that you have the flexibility of dynamic webpages with the performance of static sites.

Render Engine was built out of frustration with existing tools.
Larger frameworks are too vast.
Dynamic Services like _Flask_ required overhead of a server where in many cases were not necessary.
Extensions to Flask that provided a static component added even more unnecessary complexity and updates have been inconsistent.
Other static-site generators like _Pelican_ were built without modern architectures and design practices in mind.

## The _4 layer_ Architecture 

* **[Page](./docs/page.md)** - A single webpage item built from content, a template, raw data, or a combination of those things.
* **[Collection](./docs/collection.md)** - A group of webpages built from the same template, organized in a single directory
* **[Engine](./docs/engine.md)** - The environments that turn your pre-content and templates into rendered HTML
* **[Site](./docs/site.md)** - The container that holds all Pages and Collections and gives access to global configurations and settings.

You can expand on these areas to customize your engine to your liking.


**Things you can do in with Render Engine:**

- Create **Custom Page Objects** (Like Blogs or MicroBlog Posts)
- Create all types of Page Objects, not just 'html' pages
- Run Multiple Engines for subdomains or multiple template systems or Multiple Sites!
- Dynamically create content at runtime to include into your static sites

## Getting Started (Quickly)

### Requirements
Render Engine requires Python 3.7 or later to run.

* While this "should" run on any operating system, it has been tested on _Unix-based systems_.

### Install via `pip`

```
pip install render-engine
```

### Setup Directory
The default engine used is [Jinja2](). You don't _have_ to supply a template but if you don't the engine will only supply the content directly.

```
- run.py
- templates/
|
---- page.html
```

in `run.py`

```
from render-engine import Site, Engine, Page

app = Site()
app.SITE_TITLE = 'YOUR WEBSITE'
app.SITE_LINK = 'http://example.com'



@app.register_route
class Index(Page):
    content = '<h1>Hello World</h1>'

@app.render()
```
