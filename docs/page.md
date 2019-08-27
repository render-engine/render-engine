# Page Objects

The Page Object is the basic building block for all objects. Essentially your site is built from one or many Page objects.

## Page.slug
The stem of the URL that relates to this Page's file.

## Page.content
This is the raw content of the file. Currently _HTML_ and _Markdown_ are to supported.

## Page.content_path
Alternatively, you can specify a filepath that uses an [RST-Like Metadata system](#) to identify attributes for the page object. 

This is great for building dynamic pages without cluttering up your [engine runner](#).

## Page.extension
The output extension that the rendered page will have.

## Page.template
If your page uses a template file (render_engine supports [Jinja2](https://palletsprojects.com/p/jinja/) out of the box) then you can specify your template file and render engine will use that to build out your page. It will use any standard or additional attrs as template markup variables by default. No more manually telling it what to use.

## template_vars
**Common template_vars Include:**

* `date_published`
* `date_modified`
* `author`
* `link`
* `media`
* `tags`
* `category`

Additional Attrs can be of _any_ type.

## Page.html
This is content that is converted to html from markdown.

TODO: Add support for RST
