## What is RenderEngine

The idea of Render Engine is that you have the flexibility of dynamic webpages with the performance of static sites.

Render Engine was built out of frustration with existing tools.
Larger frameworks are too vast.
Dynamic Services like _Flask_ required overhead of a server where in many cases were not necessary.
Extensions to Flask that provided a static component added even more unnecessary complexity and updates have been inconsistent.
Other static-site generators like _Pelican_ were built without modern architectures and design practices in mind.

## The _3 layer_ Architecture 

* **[Page](render_engine/page.html)** - A single webpage item built from content, a template, raw data, or a combination of those things.
* **[Collection](render_engine/collection.html)** - A group of webpages built from the same template, organized in a single directory
* **[Site](render_engine/site.html)** - The container that holds all Pages and Collections and gives access to global configurations and settings.

Your site will have an [Engine](render_engine/engine.html) that can _render_ your html (and other things), hence the name.

You can expand any of these areas to customize your engine to your liking.

**Things you can do in with Render Engine:**

- Create **Custom Page Objects** (Like Blog or MicroBlog Posts)
- Create all types of Page Objects, not just 'html' pages
- Run Multiple Engines for subdomains or multiple template systems or Multiple Sites!
- Dynamically create content at runtime to include into your static sites

## As simple/complex as required

- Render Engine uses [Jinja2] as the defaul engine to bring the power of templates to your page. You can create your own custom engines if you have a specific need.
- Content can be markdown/html/or RAW DATA to give you the content you need.

# Installing Render Engine

## Dependencies:
- [Python3.8](https://python.org) or later.

### Other Dependencies that install with render-engine
- [Jinja2] - for template things
- [Pendulum] - for datetime things
- [Click] - for some commandline goodness
- [more-itertools] - for iteration things
- [markdown] - for markdown things

### Using pip
`pip install render-engine`

# Get Started Quickly

### The Quick Way

`render-engine-quickstart`

![render-engine-quickstart](https://s3-us-west-2.amazonaws.com/kjaymiller/images/Render%20Engine%20Quickstart.gif)

This will create your essential files and a `run.py` that you can use to build
your output file using `python run.py`

Render Engine DOESN'T Need the following but this model can quickly get you on your way.

```
content/ # store content for collections here
run.py # use `python run.py` to build your site.
templates/
  - page.html # default template for Page objects. Modify this file to fit your design
  - all_posts.html # default template for Collection objects. Modify this file to fit your design
static/ # will be copied into your generated output. great for storing css/.js/image files
```

## Sponsors
This and much of the work that I do is made possible by those that sponsor me
on github. 

### Sponsors at the $20/month and higher Level
- [Brian Douglas](https://github.com/bdougie)
- [Anthony Shaw](https://github.com/tonybaloney)
- [Carol Willing](https://github.com/willingc)

Thank you to them and all of those that continue to support this project!

[Jinja2]: https://jinja.palletsprojects.com/en/latest
[Pendulum]: https://pendulum.eustace.io
[Click]: https://click.palletsprojects.com/en/latest
[more-itertools]: https://more-itertools.readthedocs.io/en/stable/
[markdown]: https://python-markdown.github.io

