> ***Warning***
> Render Engine 2022.12.3 introduced a change to the schema where now the following commands were changed. I apologize for any inconvenience.
> - `render_page` is just `page`
> - `render_collection` is just `collection`
> - You will need to now add `site.render()` where `site` is your `Site` instance

## What is RenderEngine
## The _3 layer_ Architecture 

* **[Page](.github/render_engine/page.html)** - A single webpage item built from content, a template, raw data, or a combination of those things.
* **[Collection](.github/render_engine/collection.html)** - A group of webpages built from the same template, organized in a single directory
* **[Site](.github/render_engine/site.html)** - The container that helps to render all Pages and Collections in with uniform settigns and variables

## Installing Render Engine

In order to use render engine, you must have python 3.9+ installed. You can download python from [python.org](https://python.org).

- Linux/MacOS: [python.org](https://python.org)
- Windows: [Microsoft Store](https://apps.microsoft.com/store/detail/python-311/9NRWMJP3717K)

Render Engine is available in PyPI and can be installed using pip:

```bash
pip install render-engine
```

## Getting Started
Check out the [Getting Started](https://render-engine.readthedocs.io/en/latest/page.md) Section in the [Documentation](https://render-engine.readthedocs.io)

## Sponsors
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
