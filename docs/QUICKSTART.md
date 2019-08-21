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

## 4. Create an Index Page ##

Use `@engine.build()` and create a function to hold any variables you want to pass into the page. Pass the template `index.html` to the page.

```
@engine.build(template='index.html')
``` 

That will look for `index.html` in the engines `template_path` directory (_./templates_ by default)



## Create Collections
You can build a collection and add the pages to the engine using the `engine.build_collection` method.

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

Where is it pulling content _from_? 

It's whatever you have 'content_path' set in your engine. By default it's `./content`. This will create a [[Collection]] for each markdown or html file (by default) files and create a page for each one.

## Generating the files
This is what makes the magic happen!

To generate the file, call `engine.run()` at the end!
