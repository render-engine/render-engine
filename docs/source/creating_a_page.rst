Page Objects
============

At their foundation evey webpage that you create in *Render Engine* is a :class:`**Page** <render_engine.page.Page>` object.

A page is a class is initialized added to the `routes` array.


Basic Page from Template
===================================================

The simplest page (possibly your index) will only require some basic information.

Example:: 

    @site.register_route('basic_page.html')
    class BasicPage(Page):
        template = 'template_file.html' # user provided template

The `@site.register_route` decorator adds an initialized version of the class to the specified site's `routes` array.

The `template` attribute is passed to the page's engine (either manually defined or assigned by the engine). This template will be used when creating your Markup.

Example:: 

    # Basic Page with Variables
    @site.register_route('page_with_vars')
    class PageWithVars(Page):
        title = 'Site Title'


    # Page Loading from File
    @site.register_route('page_from_file')
    class PageFromFile(Page):
        content_path = 'index.md' # loaded from content path can be '.md' or '.html'


    # Page Inherited from Other Page
    @site.register_route('basic_page.html')
    class BasicPage(Page):
        template = 'template_file.html' # user provided template
        title = 'Base Page'


    @site.register_route('other_page.html')
    class InheritingPage(BasicPage):
        # template will be inherited from the BasicPage
        title = 'Inherited Page'
