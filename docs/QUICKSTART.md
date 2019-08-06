## Import Render Engine into your run file

`render_engine import Engine`

## Define your Engine
`engine = Engine()`
You can have more than one engine. This is great if you are building multiple sites or subdomains.

## Adding Pages to the Engine (The Hard Way)
### Build a basic page with no Template
You can all the basic componenents of Render Engine rather easily. This isn't the preferred method of created pages but will "technically work"

```
from render_engine.page import Page

engine.routes.appeng(Page(
        slug='/index', # Use the slug, not the filename
        content="""<html>
        <body><h1>This is a Sample Page</h1></body>
        </html>"""
        ))
```

You can also build a page from a template using (Jinja2 no need to import it) 
This is still a  harder way of doing adding a page to the engine. 

```
engine.routes.append(Page(
        slug='/index_template_hard',
        template='index.html', # resolves to <DEFAULT TEMPLATE PATH>/index.html',
        TEMPLATE_VARIABLE='This is <strike>Render Engine</strike>', #Template Var
        ))
```

## Adding Pages (The Easy Way)
What if your Template Variables are more complicated than just a static value? What if you have multiple variables to add.

There is an easy and consistent way to add content to the engine.

You can use the `@route` decorator.

```
@engine.route('/index_template_easy', template='index.html')
def get_template_var():
    addition = 2 + 2
    another_thing = 'Hello!'
    return {
            'TEMPATE_VARIABLE': addition,
            'ANOTHER_VARIABLE': another_thing,
            }
```

One thing the _Easy Way_ allows for is multiple routes.

If you've got nothing to pass just pass or return an empty dictionary

```
@engine.route(
        '/multiple_routes/',
        '/pages/multiple_routes',
        template='index.html',
        )
def multiple_routes():
    pass # or return {}
```

## Collections
What about creating a blog or series of pages based on content?

We call those **collections**.

I'm not showing you the hard way.. Nope won't do it. Here is how you can build a collection and add the pages to the engine.

```
engine.build_collection(
        '/blog',
        name='Blog',
        template='blog_post',
        feeds=True,
        Archive=True,
        # There are other options but the only required things are at least one route
        )
    VARIABLE_AUTHOR_INPUT = page.author if page.author else collection.author
    return {
            'VARIABLE_AUTHOR_INPUT': VARIABLE_AUTHOR_INPUT,
            }
```

Where is it pulling content from? It's whatever the 'content_path' is set in your engine. By default it's `./content`. This will create a collection of all of the markdown or html (by default) files and create a page for each one.

If you have variables that you want to set for each one do just like you did with the `@engine.route` decorator for collection level vars, use the local `collection` and for page-based objects, use the the `page` variable.
    
## Custom Collections
Collections can also have mulitple routes.
if you have a collection of Pages, you can define a custom collection of
different type objects with the pages kwargs.

## Generating the files
This is what makes the magic happen!

To generate the file, call `engine.run()` at the end!
