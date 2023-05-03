At Render Engine's core is the page. A page is a single unit of content. Pages are the building blocks of your site. If you want to display information on your site, you will need to create a page.

## BasePage

All `Page` objects inherit from `BasePage`, allowing for common functionality across all page objects.

The `BasePage` is designed for Render Engine to render common `Page`-like objects. It is not designed to be used directly.

::: src.render_engine.page.BasePage

## Page

When you're creating a `Page`. You may want to provide a [`parser`](/parsers) or `content`/`content_path`. To do this, you will need to create a `Page` object.

::: src.render_engine.page.Page
