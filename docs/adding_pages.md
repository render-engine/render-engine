# Adding Pages (the **Easy**🧙‍♀️ way and the **Hard**😈 way)
Render Engine is all about making things easy for the developer to quickly get pages created. That said some ways are easier than others.

### Build a basic page with no Template
You can call the basic componenents of Render Engine rather easily. This isn't the preferred method of created pages but will _technically_ work.

```
from render_engine.page import Page

engine.routes.append(Page(
        slug='/index', # Use the slug, not the filename
        content="""<html>
        <body><h1>This is a Sample Page</h1></body>
        </html>"""
        ))
```

You can also build a page from a template using (Jinja2 no need to import it) 
This is still a  harder way to add a page to the engine. 

```
page = Page(
        slug='/index_template_hard',
        template='index.html', # resolves to <DEFAULT TEMPLATE PATH>/index.html',
        TEMPLATE_VARIABLE='This is <strike>Render Engine</strike>', #Template Var
        )

Engine.routes.append(page)
```

#### Adding Pages (The Easy Way)
What if your Template Variables are more complicated than just a static value? What if you have multiple variables to add.

There is an easy and consistent way to add content to the engine.

You can use the `@engine.route` decorator.

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

The _Easy Way_ allows for is multiple routes.

If you've got nothing to pass just `pass` or return an empty dictionary

```
@engine.route(
        '/multiple_routes/',
        '/pages/multiple_routes',
        template='index.html',
        )
def multiple_routes():
    pass # or return {}
```
