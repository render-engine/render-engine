## What is RenderEngine

The idea of Render Engine is that you have the flexibility of dynamic webpages with the performance of static sites.

Render Engine was built out of frustration with existing tools.
Larger frameworks are too vast.
Dynamic Services like _Flask_ required overhead of a server where in many cases were not necessary.
Extensions to Flask that provided a static component added even more unnecessary complexity and updates have been inconsistent.
Other static-site generators like _Pelican_ were built without modern architectures and design practices in mind.

## The _4 layer_ Architecture 

* **[Page](render_engine/page.html)** - A single webpage item built from content, a template, raw data, or a combination of those things.
* **[Collection](render_engine/collection.html)** - A group of webpages built from the same template, organized in a single directory
* **[Engine](render_engine/engine.html)** - The environments that turn your pre-content and templates into rendered HTML
* **[Site](render_engine/site.html)** - The container that holds all Pages and Collections and gives access to global configurations and settings.

You can expand on these areas to customize your engine to your liking.


**Things you can do in with Render Engine:**

- Create **Custom Page Objects** (Like Blogs or MicroBlog Posts)
- Create all types of Page Objects, not just 'html' pages
- Run Multiple Engines for subdomains or multiple template systems or Multiple Sites!
- Dynamically create content at runtime to include into your static sites

## As simple/complex as required

- Render Engine uses [Jinja2] as the defaul engine to bring the power of templates to your page. You can create your own custom engines if you have a specific need.
- Content can be markdown/html/or RAW DATA to give you the content you need.

## Dependencies:
- [Python3.7](https://python.org) or later.
- [Jinja2] - for template things
- [Pendulum] - for datetime things
- [Click] - for some commandline goodness


# Installing Render Engine

### Using pip
`pip install render-engine`

# Get Started Quickly

Render Engine DOESN'T Need the following but the this is a base module that can quickly get you on your way

```
content/ # store content for collections here
run.py # use render_engine run.py to build site
templates/
  - page.html # default template for Page objects. Modify this file to fit your design
  - all_posts.html # default template for Collection objects. Modify this file to fit your design
static/ # will be copied into your generated output. great for storing css/.js/image files
```

[ ] Todo: Build this functionality out into quickstart


[Jinja2]: https://jinja.palletsprojects.com/en/latest
[Pendulum]: https://pendulum.eustace.io
[Click]: https://click.palletsprojects.com/en/latest


