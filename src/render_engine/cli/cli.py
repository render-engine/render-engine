# ruff: noqa: UP007

import importlib
import pathlib
import sys
import typing
from typing import Annotated

import typer
from rich.console import Console
from rich.progress import Progress

from render_engine.cli.event import RegExHandler
from render_engine.engine import engine
from render_engine.site import Site

app = typer.Typer()


def split_module_site(module_site: str) -> tuple[str, str]:
    """splits the module_site into a module and a class name"""
    try:
        import_path, app_name = module_site.split(":", 1)
    except ValueError:
        raise typer.BadParameter(
            "module_site must be of the form `module:site`",
        )
    return import_path, app_name


def get_app(import_path, app_name) -> Site:
    """Split the site module into a module and a class name"""
    sys.path.insert(0, ".")
    importlib.import_module(import_path)
    return getattr(sys.modules[import_path], app_name)


def _create_folder(*, folder: pathlib.Path, overwrite: bool) -> pathlib.Path:
    """Create a folder if it doesn't exist or if overwrite is True"""
    folder.mkdir(parents=True, exist_ok=overwrite)
    return folder


CREATE_APP_PY_TEMPLATE = engine.get_template("create_app_py.txt")


def _create_templates_folder(
    *templates,
    project_folder: pathlib.Path,
    templates_folder_name: pathlib.Path,
    exists_ok: bool,
) -> None:
    """Create a folder for templates and optionally create an index.html file"""
    path = project_folder.joinpath(templates_folder_name)
    path.mkdir(
        exist_ok=exists_ok,
    )

    for template in templates:
        path.joinpath(template).write_text(engine.get_template(template).render())


def _create_site_with_vars(
    *,
    site_title: typing.Optional[str] = None,  # noqa: UP007
    site_url: typing.Optional[str] = None,
    site_description: typing.Optional[str] = None,
    site_author: typing.Optional[str] = None,
    collection_path: typing.Optional[str] = None,
) -> Site:
    """Create a new site from a template"""
    site = Site()
    potential_site_vars = {
        "site_title": site_title,
        "site_url": site_url,
        "site_author": site_author,
        "site_description": site_description,
        "collections_path": str(collection_path),
    }
    site_vars = {key: value for key, value in potential_site_vars.items() if value}
    site.site_vars.update(site_vars)
    return site


@app.command()
def init(
    collection_path: Annotated[
        pathlib.Path,
        typer.Option(
            help="create your content folder in a custom location",
            rich_help_panel="Path Options",
        ),
    ] = pathlib.Path("pages"),
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            "-f",
            help="Force overwrite of existing files",
            rich_help_panel="Flags",
        ),
    ] = False,
    output_path: Annotated[
        pathlib.Path,
        typer.Option(
            help="custom output folder location.",
            rich_help_panel="Path Attributes",
        ),
    ] = "output",
    project_path_name: Annotated[
        pathlib.Path,
        typer.Option(
            help="name of render_engine app name",
            rich_help_panel="Path Attributes",
        ),
    ] = "app.py",
    project_folder: Annotated[
        pathlib.Path,
        typer.Option(
            exists=True,
            dir_okay=True,
            writable=True,
            help="path to create the project in",
            rich_help_panel="Path Attributes",
        ),
    ] = pathlib.Path("./"),
    owner_name: Annotated[
        typing.Optional[str],
        typer.Option(
            prompt="Owner Name",
            help="Site Owners's Name",
            rich_help_panel="Site Vars",
        ),
    ] = ...,
    owner_email: Annotated[
        typing.Optional[str],
        typer.Option(
            prompt="Owner Email",
            help="Email of Site's Owner",
            rich_help_panel="Site Vars",
        ),
    ] = ...,
    site_description: Annotated[
        typing.Optional[str],
        typer.Option(
            help="(Optional): Site Description",
            rich_help_panel="Site Vars",
        ),
    ] = None,
    site_title: Annotated[
        typing.Optional[str],
        typer.Option(
            "--title",
            "-t",
            help="title of the site",
            rich_help_panel="Site Vars",
            show_default=False,
        ),
    ] = None,
    site_url: Annotated[
        typing.Optional[str],
        typer.Option(
            "--url",
            "-u",
            help="URL for the site",
            rich_help_panel="Site Vars",
            show_default=False,
        ),
    ] = None,
    skip_collection: Annotated[
        bool,
        typer.Option(
            "--skip-collection",
            "-C",
            help="Skip creating the content folder and a collection",
            rich_help_panel="Flags",
        ),
    ] = False,
    skip_static: Annotated[
        bool,
        typer.Option(
            "--skip-static",
            "-S",
            help="Skip copying static files",
            rich_help_panel="Flags",
        ),
    ] = False,
    static_path: Annotated[
        pathlib.Path,
        typer.Option(
            help="custom static folder",
            rich_help_panel="Path Attributes",
        ),
    ] = pathlib.Path("static"),
    templates_path: Annotated[
        pathlib.Path,
        typer.Option(
            "--templates-path",
            help="custom templates folder",
        ),
    ] = pathlib.Path("templates"),
):
    """
    CLI for creating a new site configuration.

    Params:
        collection_path: create your content folder in a custom location
        force: Force overwrite of existing files
        output_path: custom output folder location
        project_path_name: name of render_engine app name
        project_folder: path to create the project
        owner:  owner of the site
        site_description: Site Description
        site_title: title of the site
        site_url: URL for the site
        skip_collection: Skip creating the content folder and a collection
        skip_static: Skip copying static files
        static_path: custom static folder
        templates_path: custom templates folder
    """
    # creating the site object and site_vars

    pathlib.Path(project_folder)
    with Progress() as progress:
        progress.console.rule("[green][bold]Creating Project")
        # creating the app.py file from the template
        project_config_path = pathlib.Path(project_folder).joinpath(project_path_name).with_suffix(".py")
        task_generate_project_path = progress.add_task(f"Generating App File: [blue]{project_config_path}", total=1)

        project_config_path.write_text(
            CREATE_APP_PY_TEMPLATE.render(
                site_title=site_title,
                site_url=site_url,
                site_description=site_description,
                owner={"name": owner_name, "email": owner_email},
                output_path=output_path,
                skip_static=skip_static,
                static_path=static_path,
                collection_path=collection_path,
                skip_collection=skip_collection,
            )
        )
        progress.update(task_generate_project_path, advance=1)

        # Create the templates folder and the index.html file
        task_templates = progress.add_task(f"Creating Templates Folder: [blue]{templates_path}", total=1)
        templates = ["index.html"]
        _create_templates_folder(
            *templates,
            project_folder=project_folder,
            templates_folder_name=templates_path,
            exists_ok=force,
        )

        progress.update(task_templates, advance=1)

        # Create the collection
        if not skip_collection:
            task_create_collection = progress.add_task(f"Creating Collection: [blue]{collection_path}", total=1)
            _collection_path = pathlib.Path(project_folder).joinpath(collection_path)
            _collection_path.mkdir(exist_ok=force)
            _collection_path.joinpath("sample_page.md").write_text(
                engine.get_template("base_collection_path.md").render()
            )

            progress.update(task_create_collection, advance=1)


@app.command()
def build(module_site: Annotated[str, typer.Argument(callback=split_module_site)]):
    """
    CLI for creating a new site

    Params:
        site_module: module and class name of the site

    """
    module, site = module_site
    app = get_app(module, site)
    app.render()


@app.command()
def serve(
    module_site: Annotated[
        str,
        typer.Argument(
            callback=split_module_site,
            help="module:site for Build the site prior to serving",
        ),
    ],
    reload: Annotated[
        bool,
        typer.Option(
            "--reload",
            "-r",
            help="Reload the server when files change",
        ),
    ] = None,
    directory: Annotated[
        str,
        typer.Option(
            "--directory",
            "-d",
            help="Directory to serve",
            show_default=False,
        ),
    ] = None,
    port: Annotated[
        int,
        typer.Option(
            "--port",
            "-p",
            help="Port to serve on",
            show_default=False,
        ),
    ] = 8000,
):
    """
    Create an HTTP server to serve the site at `localhost`.

    !!! warning
        this is only for development purposes and should not be used in production.

    Params:
        module_site: Python module and initialize Site class
        reload: Use to reload server on file change
        build: flag to build the site prior to serving the app
        directory: Directory to serve. If `module_site` is provided, this will be the `output_path` of the site.
        port: Port to serve on
    """

    if module_site:
        module, site = module_site
        app = get_app(module, site)
        app.render()

    if not directory:
        if module_site:
            directory = app.output_path
        else:
            directory = "output"

    server_address = ("127.0.0.1", port)

    handler = RegExHandler(
        server_address=server_address,
        dir_to_serve=directory,
        app=app,
        module_site=module_site,
        patterns=None,
        ignore_patterns=[r".*output\\*.+$", r"\.\\\..+$", r".*__.*+$"],
    )

    console = Console()

    if not reload:
        console.print(f"[bold green]Starting server on http://{server_address[0]}:{server_address[1]}[/bold green]")
        handler._server(server_address=server_address, directory=directory).serve_forever()
    else:
        console.print("Watching for changes...")
        handler.watch()


def cli():
    app()
