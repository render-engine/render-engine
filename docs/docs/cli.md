# Render Engine CLI

Render Engine comes with a CLI that can be used to create, build, and serve your site.

## creating your app with `render-engine init`

::: src.render_engine.cli.cli.init

### `collection-path` (`Path`: default=`"pages"`)

The path to the folder that will contain your [collections](../collection). This is where you will put your data files to be processed.

### `force` (`bool`: default=`False` as `no-force`)

Overwrite existing files and folders. If `no-force`, an error will be raised if **ANY** of the files already exist.

### `output-path` (`Path`: default=`"output"`)

The path to the [`output`](../../site#output_path) directory. This is where your rendered site will be served.

### `project-path-name` (`Path`: default=`"app.py"`)

The name of the python file that will contain the Render Engine setup. This is where you will define your [site](../../site), [pages](../../page) and [collections](../../collection).

### `project-folder` (`Path`: default=`"."`)

The name of the folder that will contain your project. This is where your [`project-path-name`](#project-path-name-path-defaultapppy), [`output-path`](#output-path-path-defaultoutput), [`templates-path`](#templates-path-path-defaulttemplates), and [`collection-path`](#collection-path-path-defaultpages) will be created.

#### `site-description` (`str|None`: default=`None`)

A short description of your site.  This will be passed into the [`Site`](../site.md) object and available in [`site_vars`](../site.md#site_vars).

#### `site-author` - (`str|None` default: `None`)

The author of the site.  This will be passed into the [`Site`](../site.md) object and available in [`site_vars`](../site.md#site_vars).

#### `skip-collection` (`bool`: default=`False` as `no-skip-collection`)

If `True`, a [`collection-path`](../collection#content_path) folder will not be created.

#### `skip-static` - (`bool`: default: `False` as `no-skip-static`)

If `True`, will not create the [`static`](../../site#static_path) folder. This is where you will put your static files (images, css, js, etc).

#### `templates-path` (`Path`: default=`"templates"`)

The path to the folder that will contain your [`templates`](../templates). This is where you will put your Jinja2 templates.

## Building your site with `render-engine build`

::: src.render_engine.cli.cli.build

`build` requires a `module_site` parameter in the format of `module:site`. `module` is the name of the python file that contains the `site` variable you've initialized. If the site `site` variable is in the `app.py` file, then the `module_site` parameter would be `app:site`.

## Serving your site (locally) with `render-engine serve`

The `serve` command creates a simple webserver that you can use to view your files.

`serve` requires a `module_site` argument in the format of `module:site`. `module` is the name of the python file that contains the `site` variable you've initialized. If the site `site` variable is in the `app.py` file, then the `module_site` parameter would be `app:site`.

You can also use the `--reload` flag to have the site rebuild when changes are made.

:::src.render_engine.cli.cli.serve

!!! Note
    `--reload` triggers a rebuild after re-importing the site object. Certain changes will not be picked up in the rebuild and reload.
