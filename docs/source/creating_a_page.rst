Page Objects
============

At their foundation evey webpage that you create in *Render Engine* is a :class:`Page <render_engine.page.Page>` object.

Basic Page from Template
===================================================

The simplest page (possibly your index) will only require some basic information.

Example:: 

    @site.register_route('basic_page.html')
    class BasicPage(Page):
        template = 'template_file.html' # user provided template

The :meth:`@site.register_route <render_engine.site.Site.register_route>` decorator adds an initialized version of the class to the specified site's :attr:`routes <render_engine.site.Site.routes>` array.

The :attr:`template <render_engine.page.Page.template>` attribute is passed to the page's engine (either manually defined or assigned by the engine). This template will be used when creating your Markup.

If no template is defined, the content will be converted to Markup and generated.

Adding Metadata to your Page
============================

Page objects have attributes that your html page will use. Different types of pages may require certain attributes but pages should check for those required attributes and supply placeholders/ and necessary warning messages.

Here are some attributes that can modify how your Page generates content.

    - :attr:`slug <render_engine.page.Page.slug>`
    - :attr:`title <render_engine.page.Page.title>`
    - :attr:`always_refresh <render_engine.page.Page.always_refresh>`
    - markdown_extras
    - routes
    - engine
    - content_path  

Adding Variables to your Page
=============================

The default engine to generate your Page is `Jinja2 <https://palletsprojects.com/p/jinja/>`. Jinja allows for you to supply variables to your templates. These variables are the attributes you supply your Page object with.:: 

    # Basic Page with Variables
    @site.register_route('page_with_vars')
    class PageWithVars(Page):
        title = 'Site Title'
        template = template_file.html


    # templates/template_file.html
    <html>
        <title>{{title}}</title>
    </html>

    # output/pagewithvars.html
    <html>
        <title>Site Title</title>
    </html>



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
