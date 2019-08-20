## What is RenderEngine

The idea of Render Engine is that you have the flexibility of dynamic webpages with the performance of static sites.

Render Engine was built out of frustration with existing tools. Larger frameworks like _Django_ were too vast. Dynamic Services like _Flask_ required overhead of a server where in many cases were not necessary. Extensions to Flask that provided a static component added  even more unnecessary complexity. Other static-site generators like _Pelican_ were built without modern architectures and design practices in mind.  


## The _3 layer_ architecture. 

* **[Page](./docs/page.md)** - A single webpage item built from content, a template, raw data, or a combination of those things.
* **[Collection](./docs/collection.md)** - A group of webpages with some connection
* **[Engine](./docs/engine.md)** - A manager that provides top layer configuration and consistency

You can expand on these areas to customize your engine to your liking.


**Things you can do in with Render Engine:**

- Create **Custom Page Objects** for _Blog Posts_ or _Podcast Episodes_
- Create all types of Page Objects, not just 'html' pages
- Create _Sub-Collections_ from pages with a common attributes
- Run Multiple Engines for subdomains or multiple template systems or Multiple Sites!
- Dynamically create content at runtime to include into your static sites

Check out our [Quickstart](docs/QUICKSTART.md) to get started...

## As simple/complex as required

- Render Engine uses [Jinja2] to bring the power of templates to your page.
- Content can be markdown/html/or RAW DATA to give you the content you need.
- Static Content because some things (will) never change.

[Jinja2]: https://jinja.palletsprojects.com/en/latest
