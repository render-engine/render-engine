from render_engine import Engine

engine = Engine(
        template_path='tests/functional_tests/templates',
        base_content_path='tests/functional_tests/content',
        )

# Build a basic page with no Template
from render_engine.page import Page
engine.routes.append(Page(
        slug='/index', # Use the slug, not the filename
        content="""<html>
        <body><h1>This is a Sample Page</h1></body>
        </html>"""
        ))

# Build a page from a Template (The hard way)
engine.routes.append(Page(
        slug='/index_template_hard',
        template='index.html', # resolves to <DEFAULT TEMPLATE PATH>/index.html',
        TEMPLATE_VARIABLE='This is Render Engine', #Template Var
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
        template='post.html',
        # There are other options but the only required things are at least one route
        )

# This is what makes the magic happen!
# Call `engine.run()` at the end!
engine.run() 
