# ruff: noqa: UP007
import importlib
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table

from render_engine import Collection, Site
from render_engine.cli.event import ServerEventHandler

app = typer.Typer()


def get_site_content_paths(site: Site) -> list[Path | None]:
    """Get the content paths from the route_list in the Site"""

    base_paths = map(lambda x: getattr(x, "content_path", None), site.route_list.values())
    return list(filter(lambda x: x is not None, base_paths))


def get_site(import_path: str, site: str) -> Site:
    """Split the site module into a module and a class name"""
    sys.path.insert(0, ".")
    importlib.import_module(import_path)
    return getattr(sys.modules[import_path], site)


def remove_output_folder(output_path: Path) -> None:
    """Remove the output folder"""

    # TODO: #778 Should we check for Operating System
    if output_path.exists():
        shutil.rmtree(output_path)


def split_module_site(module_site: str) -> tuple[str, str]:
    """splits the module_site into a module and a class name"""
    try:
        import_path, site = module_site.split(":", 1)
    except ValueError:
        raise typer.BadParameter(
            "module_site must be of the form `module:site`",
        )
    return import_path, site


def get_available_themes(console: Console, site: Site, theme_name: str) -> list[str]:
    """Returns the list of available themes to the Console"""
    try:
        return site.theme_manager.prefix[theme_name].list_templates()
    except KeyError:
        console.print(f"[bold red]{theme_name} not installed[bold red]")
        return []


def create_collection_entry(content: str | None, collection: Collection, **context):
    """Creates a new entry for a collection"""
    return collection.Parser.create_entry(content=content, **collection._metadata_attrs(), **context)


def split_args(args: list[str] | None) -> dict[str, str]:
    return {value.split("=")[0]: value.split("=")[1] for value in args if args}


def display_filtered_templates(title: str, templates_list: list[str], filter_value: str) -> None:
    """Display filtered templates based on a given filter value."""
    table = Table(title=title)
    table.add_column("[bold blue]Templates[bold blue]")
    for template in templates_list:
        if filter_value in template:
            table.add_row(f"[cyan]{template}[cyan]")
    rprint(table)


@app.command()
def templates(
    module_site: Annotated[tuple[str, str], typer.Argument(callback=split_module_site)],
    theme_name: Annotated[str, typer.Option("--theme-name", help="Theme to search templates in")] = "",
    filter_value: Annotated[str, typer.Option("--filter-value", help="Filter templates based on names")] = "",
):
    """
    CLI for listing available theme templates.

    Params:
        module_site: Python module and initialize Site class
        theme_name: Optional. Specifies the theme to list templates from.
        filter_value: Optional. Filters templates based on provided names.
    """
    module, site_name = module_site
    site = get_site(module, site_name)
    console = Console()

    if theme_name:
        available_themes = get_available_themes(console, site, theme_name)
        if available_themes:
            display_filtered_templates(
                f"[bold green]Available templates for {theme_name} [bold green]",
                available_themes,
                filter_value,
            )
    else:
        console.print("[red]No theme name specified. Listing all installed themes and their templates[red]")
        for theme_prefix, theme_loader in site.theme_manager.prefix.items():
            templates_list = theme_loader.list_templates()
            display_filtered_templates(
                f"[bold green]Showing templates for {theme_prefix}[bold green]",
                templates_list,
                filter_value,
            )


@app.command()
def init(
    template: Annotated[
        str,
        typer.Argument(help="Template to use for creating a new site"),
    ] = "https://github.com/render-engine/cookiecutter-render-engine-site",
    extra_context: (
        Annotated[
            Optional[str],
            typer.Option(
                "--extra-context",
                "-e",
                help="Extra context to pass to the cookiecutter template. This must be a JSON string",
            ),
        ]
        | None
    ) = None,
    no_input: Annotated[bool, typer.Option("--no-input", help="Do not prompt for parameters")] = False,
    output_dir: Annotated[
        Path,
        typer.Option(
            help="Directory to output the site to",
            dir_okay=True,
            file_okay=False,
            exists=True,
        ),
    ] = Path("./"),
    config_file: Annotated[Optional[Path], typer.Option("--config-file", "-c")] = None,
) -> None:
    """
    Create a new site configuration. You can provide extra_context to the cookiecutter template.

    Also any argument that cookiecutter accepts can be passed to this command.

    The template can be a local path or a git repository.
    """

    # Check if cookiecutter is installed
    try:
        from cookiecutter.main import cookiecutter
    except ImportError:
        typer.echo(
            "You need to install cookiecutter to use this command. Run `pip install cookiecutter` to install it.",
            err=True,
        )
        raise typer.Exit(0)
    cookiecutter(
        template=template,
        extra_context=extra_context,
        output_dir=output_dir,
        config_file=config_file,
        no_input=no_input,
    )


@app.command()
def build(
    module_site: Annotated[
        str,
        typer.Argument(
            help="module:site for Build the site prior to serving",
        ),
    ],
    clean: Annotated[
        bool,
        typer.Option(
            "--clean",
            "-c",
            help="Clean the output folder prior to building",
        ),
    ] = False,
) -> None:
    """
    CLI for creating a new site

    Params:
        module_site: Python module and initialize Site class

    """
    module, site_name = split_module_site(module_site)
    site = get_site(module, site_name)
    if clean:
        remove_output_folder(Path(site.output_path))
    site.render()


@app.command()
def serve(
    module_site: Annotated[
        str,
        typer.Argument(
            help="module:site for Build the site prior to serving",
        ),
    ],
    clean: Annotated[
        bool,
        typer.Option(
            "--clean",
            "-c",
            help="Clean the output folder prior to building",
        ),
    ] = False,
    reload: Annotated[
        bool,
        typer.Option(
            "--reload",
            "-r",
            help="Reload the server when files change",
        ),
    ] = False,
    directory: Annotated[
        str,
        typer.Option(
            "--directory",
            "-d",
            help="Directory to serve",
            show_default=False,
        ),
    ] = "output",
    port: Annotated[
        int,
        typer.Option(
            "--port",
            "-p",
            help="Port to serve on",
            show_default=False,
        ),
    ] = 8000,
) -> None:
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

    module, site_name = split_module_site(module_site)
    site = get_site(module, site_name)

    if clean:
        remove_output_folder(Path(site.output_path))
    site.render()

    server_address = ("127.0.0.1", port)

    handler = ServerEventHandler(
        import_path=module,
        server_address=server_address,
        dirs_to_watch=get_site_content_paths(site) if reload else None,
        site=site,
        patterns=None,
        ignore_patterns=[r".*output\\*.+$", r"\.\\\..+$", r".*__.*$"],
    )

    with handler:
        pass


@app.command()
def new_entry(
    module_site: Annotated[
        str,
        typer.Argument(
            help="module:site for Build the site prior to serving",
        ),
    ],
    collection: Annotated[
        str,
        typer.Argument(help="The Collection from which youre metadata is defined"),
    ],
    filename: Annotated[
        str,
        typer.Option(help="The filename in which to save the path. Will be saved in the collection's `content_path`"),
    ],
    content: Annotated[
        Optional[str],
        typer.Option(),
    ] = None,
    args: Annotated[
        Optional[list[str]],
        typer.Option(
            help="key value attrs to include in your entry use the format `--args key=value`",
        ),
    ] = None,
):
    """Creates a new collection entry based on the parser. Entries are added to the Collections content_path"""
    module, site_name = split_module_site(module_site)
    parsed_args = split_args(args) if args else {}
    site = get_site(module, site_name)
    _collection = next(coll for coll in site.route_list.values() if type(coll).__name__.lower() == collection.lower())
    entry = create_collection_entry(content=content, collection=_collection, **parsed_args)
    filepath = Path(_collection.content_path).joinpath(filename)
    filepath.write_text(entry)
    Console().print(f'New {collection} entry created at "{filepath}"')

    if editor := os.getenv("EDITOR", None):
        subprocess.run([editor, filepath])


def cli():
    app()
