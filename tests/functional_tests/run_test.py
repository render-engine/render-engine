from render_engine import Engine

engine = Engine()

# Build a basic page with no Template
from render_engine.page import Page
engine.routes.appeng(Page(
        slug='/index', # Use the slug, not the filename
        content="""<html>
        <body><h1>This is a Sample Page</h1></body>
        </html>"""
        ))

# Build a page from a Template (The hard way)
engine.routes.append(Page(
        slug='/index_template_hard',
        template='index.html', # resolves to <DEFAULT TEMPLATE PATH>/index.html',
        TEMPLATE_VARIABLE='This is <strike>Render Engine</strike>', #Template Var
        ))

# But What if your Template Variables are more complicated than that
# What if there is a bunch of Variables
# Here is the Easier Way
@engine.route('/index_template_easy', template='index.html')
def get_template_var():
    addition = 2 + 2
    another_thing = 'Hello!'
    return {
            'TEMPATE_VARIABLE': addition,
            'ANOTHER_VARIABLE': another_thing,
            }

# One thing the _Easy Way_ allows for is multiple routes.
@engine.route(
        '/multiple_routes/',
        '/pages/multiple_routes',
        template='index.html',
        )
def multiple_routes():
    pass # got nothing to pass as a variabl just pass or return an empty dict


# What about creating a blog or series of pages based on content?
# We call those collections
# I'm not showing you the hard way.. Nope won't do it.
engine.build_collection(
        '/blog',
        name='Blog',
        template='blog_post',
        feeds=True, 
        Archive=True,
        # There are other options but the only required things are at least one route
        )
    """Where is it pulling content from? It's whatever the 'content_path' is set
    in your engine. By default it's `./content`.
    This will create a collection of all of the markdown or html (by default)
    files and create a page for each one.
    
    If you have variables that you want to set for each one do just like
    you did with the `@engine.route` decorator for collection level vars, use
    the local `collection` and for page-based objects, use the the `page`
    variable
    
    Collections can also have mulitple routes.
    if you have a collection of Pages, you can define a custom collection of
    different type objects with the pages kwargs.
    """
    VARIABLE_AUTHOR_INPUT = page.author if page.author else collection.author
    # In our default template there is no need for this as the {{Author}}
    # template is smart enough to know this but if you want to make your own
    # custom templates this is something you can do.
    return {
            'VARIABLE_AUTHOR_INPUT': VARIABLE_AUTHOR_INPUT,
            }

# This is what makes the magic happen!
# Call `engine.run()` at the end!
engine.run() 
