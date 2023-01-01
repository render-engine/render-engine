import pathlib
import typing

import jinja2
import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from render_engine import Collection, Page, Site
from render_engine.engine import render_engine_templates_loader

environment = jinja2.Environment(
    loader=render_engine_templates_loader,
    trim_blocks=True,
    lstrip_blocks=True,
)


def create_folder(*, folder, overwrite: bool) -> pathlib.Path:
    """Create a folder if it doesn't exist or if overwrite is True"""
    new_folder = pathlib.Path(folder)
    new_folder.mkdir(parents=True, exist_ok=overwrite)
    return new_folder


path = str | None


def create_app_from_template(
    site_title: str,
    site_url: str,
    site_description: path,
    site_author: path,
    static_path: path,
    output_path: path,
    collection_path: path,
) -> str:
    return environment.get_template("create_app_py.txt").render(
        site_title=site_title,
        site_url=site_url,
        site_description=site_description,
        site_author=site_author,
        output_path=output_path,
        static_path=static_path,
        collection_path=collection_path,
    )


def create_templates_folder(
    *templates,
    templates_folder_name: str,
    exists_ok: bool,
    environment: jinja2.Environment,
) -> None:
    """Create a folder for templates and optionally create an index.html file"""
    path = pathlib.Path(templates_folder_name)
    path.mkdir(
        exist_ok=exists_ok,
    )

    for template in templates:
        content = path.joinpath(template).write_text(
            environment.get_template(template).render()
        )


def update_site_vars(optional_params: dict) -> dict:
    """Remove any optional params that are None"""
    return {key: value for key, value in optional_params.items() if value}


def create_site_with_vars(
    site_title: str,
    site_url: str,
    site_description: path,
    site_author: path,
    collection_path: path,
) -> Site:
    """Create a new site from a template"""
    site = Site()
    site_vars = {
        "site_title": site_title,
        "site_url": site_url,
    }
    optional_site_vars_params = {
        "site_title": site_author,
        "site_description": site_description,
        "collections_path": collection_path,
    }
    site_vars.update(update_site_vars(optional_site_vars_params))
    site.site_vars = site_vars
    return site


def typer_app(
    site_title: str = typer.Option(
        ...,
        "--title",
        "-t",
        help="title of the site",
        prompt=True,
        rich_help_panel="Required Attributes",
        show_default=False,
    ),
    site_url: str = typer.Option(
        ...,
        "--url",
        "-u",
        help="URL for the site",
        prompt=True,
        rich_help_panel="Required Attributes",
        show_default=False,
    ),
    site_description: typing.Optional[str] = typer.Option(
        None,
        help="(Optional): Site Description",
        rich_help_panel="Optional Attributes",
    ),
    site_author: typing.Optional[str] = typer.Option(
        None,
        help="(Optional): Author of the site",
        rich_help_panel="Optional Attributes",
    ),
    output_path: typing.Optional[str] = typer.Option(
        None,
        help="custom output folder location.",
        rich_help_panel="Optional Attributes",
    ),
    static_path: typing.Optional[str] = typer.Option(
        None,
        help="custom static folder",
        rich_help_panel="Optional Attributes",
    ),
    collection_path: typing.Optional[str] = typer.Option(
        None,
        help="create your content folder in a custom location",
        rich_help_panel="Optional Attributes",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force overwrite of existing files",
        rich_help_panel="Flags",
    ),
    run_on_complete: bool = typer.Option(
        False,
        "--run-after",
        "-x",
        help="Run the site after creating the quickstart",
        rich_help_panel="Flags",
    ),
    skip_static: bool = typer.Option(
        False,
        "--skip-static",
        "-S",
        help="Skip copying static files",
        rich_help_panel="Flags",
    ),
    skip_collection: bool = typer.Option(
        False,
        "--skip-collection",
        "-C",
        help="Skip creating the content folder and a collection",
        rich_help_panel="Flags",
    ),
    templates_path: typing.Optional[str] = typer.Option(
        "templates",
        "--templates-path",
        help="custom templates folder",
    ),
):
    """CLI for creating a new site"""
    # creating the site object and site_vars

    site = create_site_with_vars(
        site_title=site_title,
        site_url=site_url,
        site_description=site_description,
        site_author=site_author,
        collection_path=collection_path,
    )

    # add output path
    if output_path:
        site.output_path = output_path

    collection = {
        "skip": skip_collection,
        "path": collection_path or "pages",
    }

    # creating folders unless skipped
    static = {
        "skip": skip_static,
        "path": static_path or "static",
    }

    if not static["skip"]:
        static_path = create_folder(folder=static["path"], overwrite=force)

        if not static["path"] == "static":
            site.static = static_path

    if not collection["skip"]:
        collection_path = create_folder(folder=collection["path"], overwrite=force)

    # creating the app.py file from the template
    pathlib.Path("app.py").write_text(
        create_app_from_template(
            site_title=site_title,
            site_url=site_url,
            site_description=site_description,
            site_author=site_author,
            output_path=output_path,
            static_path=static_path,
            collection_path=collection_path,
        )
    )

    # Create the templates folder and the index.html file
    templates = ["index.html", "base.html", "content.html"]
    create_templates_folder(
        *templates,
        templates_folder_name="templates",
        exists_ok=force,
        environment=environment,
    )

    # Create the collection
    if not skip_collection and collection_path:
        with Progress(SpinnerColumn()) as progress:
            task = progress.add_task("Creating collection", total=1)
            pathlib.Path(collection_path).joinpath("sample_pages.md").write_text(
                environment.get_template("base_collection_path.md").render()
            )

    if run_on_complete:
        typer.echo("Running the site")
        create_app()


def create_app():
    """This is the console script entry point for 'createapp'"""
    typer.run(typer_app)
