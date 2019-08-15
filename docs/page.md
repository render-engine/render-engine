Title: Page Object

The Page Object is the basic building block for all objects. Essentially your site is built from one or many Page objects.

### Page.slug
The stem of the URL that relates to this Page's file.

### Page.content
This is the raw content of the file. Currently _HTML_ and _Markdown_ are to supported.

### Page.markup
This is content that is converted to html and [marked up](#) for a template engine to parse.

TODO: Add support for RST

### Page.content_from_file
Alternatively, you can specify a filepath that uses an [RST-Like Metadata system](#) to identify attributes for the page object. 

This is great for building dynamic pages without cluttering up your [engine runner](#).

## Additional Page Attrs
Other attributes that extend the functionality of Page objects. This is great when you have non-standardized data that you want to present. 

This can be also be used with creating pages that support the display of [Collections][collections].

Common Additional Attrs Include:

* `date_published`
* `date_modified'
* `author`
* `link`
* `media`
* `tags`
* `category`

Additional Attrs can be of _any_ type.

### Page.template
If your page uses a template file (render_engine supports [Jinja2](https://palletsprojects.com/p/jinja/) out of the box) then you can specify your template file and render engine will use that to build out your page. It will use any standard or additional attrs as template markup variables by default. No more manually telling it what to use.

