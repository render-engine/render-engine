import pathlib
import typing

import dtyper
import jinja2
import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from render_engine import Collection, Page, Site
from render_engine.engine import engine


def create_folder(*, folder: pathlib.Path, overwrite: bool) -> pathlib.Path:
    """Create a folder if it doesn't exist or if overwrite is True"""
    folder.mkdir(parents=True, exist_ok=overwrite)
    return folder


CREATE_APP_PY_TEMPLATE = engine.get_template("create_app_py.txt")


def create_templates_folder(
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
        content = path.joinpath(template).write_text(
            engine.get_template(template).render()
        )


def update_site_vars(optional_params: dict) -> dict:
    """Remove any optional params that are None"""
    return {key: value for key, value in optional_params.items() if value}


def create_site_with_vars(
    *,
    site_title: str,
    site_url: str,
    site_description: str | None = None,
    site_author: str | None = None,
    collection_path: str | None = None,
) -> Site:
    """Create a new site from a template"""
    site = Site()
    site_vars = {
        "site_title": site_title,
        "site_url": site_url,
    }
    optional_site_vars_params = {
        "site_author": site_author,
        "site_description": site_description,
        "collections_path": str(collection_path),
    }
    site_vars.update(update_site_vars(optional_site_vars_params))
    site.site_vars = site_vars
    return site


@dtyper.function
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
    output_path: pathlib.Path = typer.Option(
        "output",
        help="custom output folder location.",
        rich_help_panel="Optional Attributes",
    ),
    project_path_name: pathlib.Path = typer.Option(
        "app.py",
        help="name of render_engine app name",
        rich_help_panel="Optional Attributes",
    ),
    project_folder: pathlib.Path = typer.Option(
        pathlib.Path("./"),
        help="path to create the project in",
        rich_help_panel="Optional Attributes",
    ),
    static_path: pathlib.Path = typer.Option(
        pathlib.Path("static"),
        help="custom static folder",
        rich_help_panel="Optional Attributes",
    ),
    collection_path: pathlib.Path = typer.Option(
        pathlib.Path("pages"),
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
    templates_path: pathlib.Path = typer.Option(
        pathlib.Path("templates"),
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

    # creating folders unless skipped
    if not skip_static:
        create_folder(
            folder=static_path,
            overwrite=force,
        )
        site.static_path = static_path

    if not skip_collection:
        create_folder(
            folder=collection_path,
            overwrite=force,
        )

    # creating the app.py file from the template
    pathlib.Path(project_folder).joinpath(project_path_name).write_text(
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

    # Create the templates folder and the index.html file
    templates = ["index.html", "base.html", "content.html"]
    create_templates_folder(
        *templates,
        project_folder=project_folder,
        templates_folder_name=templates_path,
        exists_ok=force,
    )

    # Create the collection
    if not skip_collection:
        with Progress(SpinnerColumn()) as progress:
            task = progress.add_task("Creating collection", total=1)
            _collection_path = pathlib.Path(project_folder).joinpath(collection_path)
            _collection_path.mkdir(exist_ok=force)
            _collection_path.joinpath("sample_pages.md").write_text(
                engine.get_template("base_collection_path.md").render()
            )


def create_app():
    """This is the console script entry point for 'createapp'"""
    typer.run(typer_app)
