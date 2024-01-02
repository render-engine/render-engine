# ruff: noqa: UP007

import importlib
import json
import pathlib
import shutil
import sys
from typing import Annotated

import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table

from render_engine.cli.event import RegExHandler
from render_engine.site import Site

app = typer.Typer()


def remove_output_folder(output_path: pathlib.Path) -> None:
    """Remove the output folder"""
    if output_path.exists():
        shutil.rmtree(output_path)


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


def get_available_themes(console: Console, app: Site, theme_name: str) -> list[str]:
    """Returns the list of available themes to the Console"""
    try:
        return app.theme_manager.prefix[theme_name].list_templates()
    except KeyError:
        console.print(f"[bold red]{theme_name} not installed[bold red]")
        return []


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
    module_site: Annotated[str, typer.Argument(callback=split_module_site)],
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
    module, site = module_site
    app = get_app(module, site)
    console = Console()

    if theme_name:
        available_themes = get_available_themes(console, app, theme_name)
        if available_themes:
            display_filtered_templates(
                f"[bold green]Available templates for {theme_name} [bold green]",
                available_themes,
                filter_value,
            )
    else:
        console.print("[red]No theme name specified. Listing all installed themes and their templates[red]")
        for theme_prefix, theme_loader in app.theme_manager.prefix.items():
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
    extra_context: Annotated[
        str,
        typer.Option(
            "--extra-context",
            "-e",
            help="Extra context to pass to the cookiecutter template. This must be a JSON string",
        ),
    ] = None,
    no_input: Annotated[bool, typer.Option("--no-input", help="Do not prompt for parameters")] = False,
    output_dir: Annotated[
        pathlib.Path,
        typer.Option(
            help="Directory to output the site to",
            dir_okay=True,
            file_okay=False,
            exists=True,
        ),
    ] = pathlib.Path("./"),
    cookiecutter_args: Annotated[str, typer.Option(callback=lambda x: json.loads(x))] = {},
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
        raise typer.Exit(
            "You need to install cookiecutter to use this command. Run `pip install cookiecutter` to install it.",
        )
    cookiecutter(
        template=template,
        extra_context=extra_context,
        checkout=cookiecutter_args.get("checkout"),
        no_input=cookiecutter_args.get("no_input", no_input),
        replay=cookiecutter_args.get("replay"),
        overwrite_if_exists=cookiecutter_args.get("overwrite_if_exists", False),
        output_dir=output_dir,
        config_file=cookiecutter_args.get("config_file"),
        default_config=cookiecutter_args.get("default_config", False),
        directory=cookiecutter_args.get("directory"),
        skip_if_file_exists=cookiecutter_args.get("skip_if_file_exists", False),
        accept_hooks=cookiecutter_args.get("accept_hooks", True),
        keep_project_on_failure=cookiecutter_args.get("keep_priject_on_failure", False),
    )


@app.command()
def build(
    module_site: Annotated[
        str,
        typer.Argument(
            callback=split_module_site,
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
    module, site = module_site
    app = get_app(module, site)
    if clean:
        remove_output_folder(app.output_path)
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

    module, site = module_site
    app = get_app(module, site)

    if clean:
        remove_output_folder(app.output_path)
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
