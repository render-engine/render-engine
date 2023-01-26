import importlib
import pathlib
import sys
import typing
from http.server import HTTPServer, SimpleHTTPRequestHandler

import dtyper
import typer
from rich.console import Console
from rich.progress import Progress

from render_engine.engine import engine
from render_engine.site import Site

app = typer.Typer()


def get_app(module_site: str) -> Site:
    """Split the site module into a module and a class name"""
    sys.path.insert(0, ".")
    import_path, app_name = module_site.split(":", 1)
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
    site_title: str | None = None,
    site_url: str | None = None,
    site_description: str | None = None,
    site_author: str | None = None,
    collection_path: str | None = None,
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


@dtyper.function
@app.command()
def init(
    collection_path: pathlib.Path = typer.Option(
        pathlib.Path("pages"),
        help="create your content folder in a custom location",
        rich_help_panel="Path Options",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force overwrite of existing files",
        rich_help_panel="Flags",
    ),
    output_path: pathlib.Path = typer.Option(
        "output",
        help="custom output folder location.",
        rich_help_panel="Path Attributes",
    ),
    project_path_name: pathlib.Path = typer.Option(
        "app.py",
        help="name of render_engine app name",
        rich_help_panel="Path Attributes",
    ),
    project_folder: pathlib.Path = typer.Option(
        pathlib.Path("./"),
        help="path to create the project in",
        rich_help_panel="Path Attributes",
    ),
    site_author: typing.Optional[str] = typer.Option(
        None,
        help="(Optional): Author of the site",
        rich_help_panel="Site Vars",
    ),
    site_description: typing.Optional[str] = typer.Option(
        None,
        help="(Optional): Site Description",
        rich_help_panel="Site Vars",
    ),
    site_title: typing.Optional[str] = typer.Option(
        None,
        "--title",
        "-t",
        help="title of the site",
        rich_help_panel="Site Vars",
        show_default=False,
    ),
    site_url: typing.Optional[str] = typer.Option(
        None,
        "--url",
        "-u",
        help="URL for the site",
        rich_help_panel="Site Vars",
        show_default=False,
    ),
    skip_collection: bool = typer.Option(
        False,
        "--skip-collection",
        "-C",
        help="Skip creating the content folder and a collection",
        rich_help_panel="Flags",
    ),
    skip_static: bool = typer.Option(
        False,
        "--skip-static",
        "-S",
        help="Skip copying static files",
        rich_help_panel="Flags",
    ),
    static_path: pathlib.Path = typer.Option(
        pathlib.Path("static"),
        help="custom static folder",
        rich_help_panel="Path Attributes",
    ),
    templates_path: pathlib.Path = typer.Option(
        pathlib.Path("templates"),
        "--templates-path",
        help="custom templates folder",
    ),
):
    """CLI for creating a new site"""

    # creating the site object and site_vars

    project_folder_path = pathlib.Path(project_folder)
    with Progress() as progress:
        progress.console.rule("[green][bold]Creating Project")
        task_project = progress.add_task("Creating Site", total=5)
        site = _create_site_with_vars(
            site_title=site_title,
            site_url=site_url,
            site_description=site_description,
            site_author=site_author,
            collection_path=collection_path,
        )
        progress.update(task_project, advance=1)

        # add output path
        if output_path:
            site.output_path = str(output_path)

        # creating folders unless skipped
        if not skip_static:
            task_static_folder = progress.add_task(
                f"Creating Static Folder: [blue]{static_path}",
                total=1,
            )
            static = project_folder_path.joinpath(static_path)
            static.mkdir(exist_ok=force)
            site.static_path = str(static_path)
            progress.update(task_static_folder, advance=1)

        progress.update(task_project, advance=1)

        # creating the app.py file from the template
        project_config_path = (
            pathlib.Path(project_folder).joinpath(project_path_name).with_suffix(".py")
        )
        task_generate_project_path = progress.add_task(
            f"Generating App File: [blue]{project_config_path}", total=1
        )

        project_config_path.write_text(
            CREATE_APP_PY_TEMPLATE.render(
                site_title=site_title,
                site_url=site_url,
                site_description=site_description,
                site_author=site_author,
                output_path=output_path,
                static_path=static_path,
                collection_path=collection_path,
            )
        )
        progress.update(task_generate_project_path, advance=1)
        progress.update(task_project, advance=1)

        # Create the templates folder and the index.html file
        task_templates = progress.add_task(
            f"Creating Templates Folder: [blue]{templates_path}", total=1
        )
        templates = ["index.html", "base.html", "content.html"]
        _create_templates_folder(
            *templates,
            project_folder=project_folder,
            templates_folder_name=templates_path,
            exists_ok=force,
        )

        progress.update(task_templates, advance=1)
        progress.update(task_project, advance=1)

        # Create the collection
        if not skip_collection:
            task_create_collection = progress.add_task(
                f"Creating Collection: [blue]{collection_path}", total=1
            )
            _collection_path = pathlib.Path(project_folder).joinpath(collection_path)
            _collection_path.mkdir(exist_ok=force)
            _collection_path.joinpath("sample_pages.md").write_text(
                engine.get_template("base_collection_path.md").render()
            )

            progress.update(task_create_collection, advance=1)
        progress.update(task_project, advance=1)


@app.command()
def build(site_module: str):
    """CLI for creating a new site"""
    app = get_app(site_module)
    app.render()


@app.command()
def serve(
    module_site: str,
    build: bool = False,
    directory: typing.Optional[str] = typer.Option(
        None,
        "--directory",
        "-d",
        help="Directory to serve",
        show_default=False,
    ),
    port: int = typer.Option(
        8000,
        "--port",
        "-p",
        help="Port to serve on",
        show_default=False,
    ),
):
    """CLI for creating a new site"""
    app = get_app(module_site)

    if build:
        app.render()

    if not directory:
        directory = app.output_path

    class server(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)

    server_address = ("localhost", port)
    httpd = HTTPServer(server_address, server)
    console = Console()
    console.print(f"Serving [blue]{directory} on http://localhost:{port}")
    console.print(f"Press [bold red]CTRL+C[/bold red] to stop serving")
    return httpd.serve_forever()


def cli():
    app()
