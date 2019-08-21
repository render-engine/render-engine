# QUICKSTART #
## Installing Render Engine ##

> **Note:** This Product is Not Officially Released. These are the instructions for installing from the test repository

Render Engine is currently hosted in the [_Test Python Package Index_](https://test.pypi.org/project/render-engine/)

### Using pip
`pip install -i https://test.pypi.org/simple/ render-engine`

### Using [pipenv](https://pipenv.readthedocs.io/en/latest/) ###
In your `Pipfile` add the following.
```
[[[[source]]]]
name = "pypi - test"
url = "https://test.pypi.org/simple"

[pipenv]
allow_prereleases = true
```

The [[[[source]]]] adds the _Test PyPI_ to the lists of repositories to check for packages. Then you can install the package using  `pipenv install`.  


## 1. Create a new python file. 
`touch run.py`

## 2. Import the Engine object into your file

`from render_engine import Engine`

\* notice that calling Render Engine is done using _underscores_
## 3. Create  your Engine Object
`engine = Engine()`
You can have more than one engine. This is great if you are building multiple sites or subdomains.


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
