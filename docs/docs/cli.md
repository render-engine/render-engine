---
title: "Render Engine CLI"
description: "Guide to using Render Engine CLI for creating, building, and serving your site."
date: August 22, 2024
tags: ["render-engine", "cli", "site-setup", "build", "serve"]
---

Render Engine comes with a CLI that can be used to create, build, and serve your site.

## creating your app with `render-engine init`

The `init` command is a hook to call [cookiecutter](https://github.com/cookiecutter/cookiecutter).

This allows you to quickly create or augment your render-engine site using a pre-existing cookiecutter template.

The default is the [cookiecutter-render-engine-site](https://github.com/render-engine/cookiecutter-render-engine-site).

Create a new site configuration. You can provide extra_context to the cookiecutter template.

Also any argument that cookiecutter accepts can be passed to this command.

The template can be a local path or a git repository.

### `collection-path` (`Path`: default=`"pages"`)

The path to the folder that will contain your [collections](collection.md). This is where you will put your data files to be processed.

### `force` (`bool`: default=`False` as `no-force`)

Overwrite existing files and folders. If `no-force`, an error will be raised if **ANY** of the files already exist.

### `output-path` (`Path`: default=`"output"`)

The path to the [`output`](site.md?id=output_path) directory. This is where your rendered site will be served.

### `project-path-name` (`Path`: default=`"app.py"`)

The name of the python file that will contain the Render Engine setup. This is where you will define your [site](site.md), [pages](page.md) and [collections](collection.md).

### `project-folder` (`Path`: default=`"."`)

The name of the folder that will contain your project. This is where your [`project-path-name`](#project-path-name-path-defaultapppy), [`output-path`](#output-path-path-defaultoutput), [`templates-path`](#templates-path-path-defaulttemplates), and [`collection-path`](#collection-path-path-defaultpages) will be created.

#### `site-description` (`str|None`: default=`None`)

A short description of your site.  This will be passed into the [`Site`](site.md) object and available in [`site_vars`](site.md?id=site_vars).

#### `skip-collection` (`bool`: default=`False` as `no-skip-collection`)

If `True`, a [`collection-path`](collection.md?id=content_path) folder will not be created.

#### `skip-static` - (`bool`: default: `False` as `no-skip-static`)

If `True`, will not create the [`static`](site.md?id=static_path) folder. This is where you will put your static files (images, css, js, etc).

#### `templates-path` (`Path`: default=`"templates"`)

The path to the folder that will contain your [`templates`](templates.md). This is where you will put your Jinja2 templates.

## Building your site with `render-engine build`

CLI for creating a new site

**Parameters:**

| Name | Type | Description | Default |
| --- | --- | --- | --- |
|`module_site`|`Annotated[str, Argument(callback=split_module_site, help='module:site for Build the site prior to serving')]`|Python module and initialize Site class|_required_|

`build` requires a `module_site` parameter in the format of `module:site`. `module` is the name of the python file that contains the `site` variable you've initialized. If the site `site` variable is in the `app.py` file, then the `module_site` parameter would be `app:site`.

## Serving your site (locally) with `render-engine serve`

The `serve` command creates a simple webserver that you can use to view your files.

`serve` requires a `module_site` argument in the format of `module:site`. `module` is the name of the python file that contains the `site` variable you've initialized. If the site `site` variable is in the `app.py` file, then the `module_site` parameter would be `app:site`.

You can also use the `--reload` flag to have the site rebuild when changes are made.

Create an HTTP server to serve the site at `localhost`.

> !!! Warning
    This is only for development purposes and should not be used in production.

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `module_site` | `Annotated[str, Argument(callback=split_module_site, help='module:site for Build the site prior to serving')]` |Python module and initialize Site class | _required_ |
| `reload` | `Annotated[bool, Option(--reload, -r, help='Reload the server when files change')]` |Use to reload server on file change | `None` |
| `build` |  |flag to build the site prior to serving the app | _required_ |
| `directory` | `Annotated[str, Option(--directory, -d, help='Directory to serve', show_default=False)]` |Directory to serve. If `module_site`is provided, this will be the `output_path`of the site. | `None` |
| `port` | `Annotated[int, Option(--port, -p, help='Port to serve on', show_default=False)]` |Port to serve on | `8000` |

> !!! Note
    `--reload` triggers a rebuild after re-importing the site object. Certain changes will not be picked up in the rebuild and reload.
