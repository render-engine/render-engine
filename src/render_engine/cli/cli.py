# ruff: noqa: UP007
import datetime
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Annotated, Optional

import toml
import typer
from dateutil import parser as dateparser
from dateutil.parser import ParserError
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from toml import TomlDecodeError

from render_engine import Collection, Site
from render_engine.cli.event import ServerEventHandler
from render_engine.cli.utils import get_site

# Load the config file. The config the pyproject.toml. CLI config is in `render-engine.cli`

CONFIG_FILE_NAME = "pyproject.toml"

# Initialize the arguments and default values
module_site_arg, collection_arg = None, None
default_module_site, default_collection = None, None


def load_config(config_file: str = CONFIG_FILE_NAME):
    """Load the config from the file"""
    global module_site_arg, collection_arg, default_module_site, default_collection
    stored_config = {}
    try:
        with open(config_file) as stored_config_file:
            try:
                stored_config = toml.load(stored_config_file).get("render-engine", {}).get("cli", {})
            except TomlDecodeError as exc:
                typer.echo(f"Encountered an error while parsing {config_file} - {exc}.")
            else:
                typer.echo(f"Config loaded from {config_file}")
    except FileNotFoundError:
        typer.echo(f"No config file found at {config_file}")

    if stored_config:
        # Populate the argument variables and default values from the config
        if (module := stored_config.get("module")) and (site := stored_config.get("site")):
            module_site_arg = typer.Option(
                help="module:site for Build the site prior to serving",
            )
            default_module_site = f"{module}:{site}"
        if default_collection := stored_config.get("collection"):
            collection_arg = typer.Option(
                help="The Collection from which your metadata is defined",
            )

    # If there is no config, use the positional arguments.
    if not module_site_arg:
        module_site_arg = typer.Argument(help="module:site for Build the site prior to serving [REQUIRED]")
    if not collection_arg:
        collection_arg = typer.Argument(help="The Collection from which your metadata is defined [REQUIRED]")


load_config()

app = typer.Typer()


def get_site_content_paths(site: Site) -> list[Path | str | None]:
    """Get the content paths from the route_list in the Site"""

    base_paths = map(lambda x: getattr(x, "content_path", None), site.route_list.values())
    base_paths = list(filter(None, base_paths))
    base_paths.extend(site.static_paths)
    if site.template_path:
        base_paths.append(site.template_path)
    return list(filter(None, base_paths))


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
    if not args:
        return {}
    split_arguments = {}
    for arg in args:
        # Accept arguments that are split with either `:` or `=`. Raise a ValueError if neither is found
        split_arg = re.split(r"[:=]", arg, maxsplit=1)
        if len(split_arg) != 2:
            raise ValueError(
                f"Invalid argument: {repr(arg)}. Arguments must have the "
                f"key, value pair separated by either an = or a :"
            )
        k, v = map(str.strip, split_arg)
        if k in split_arguments:
            # Do not allow redefinition of arguments
            raise ValueError(f"Key {repr(k)} is already defined.")
        split_arguments[k] = v
    return split_arguments


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
    module_site: Annotated[
        str,
        module_site_arg,
    ] = default_module_site,
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
    if not module_site:
        raise typer.BadParameter("You need to specify module:site")
    module, site_name = split_module_site(module_site)
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
        module_site_arg,
    ] = default_module_site,
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
    if not module_site:
        raise typer.BadParameter("You need to specify module:site")
    module, site_name = split_module_site(module_site)
    site = get_site(module, site_name)
    if clean:
        remove_output_folder(Path(site.output_path))
    site.render()


@app.command()
def serve(
    module_site: Annotated[
        str,
        module_site_arg,
    ] = default_module_site,
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
    if not module_site:
        raise typer.BadParameter("You need to specify module:site")
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
        site=site_name,
        output_path=site.output_path,
        patterns=None,
        ignore_patterns=[r".*output\\*.+$", r"\.\\\..+$", r".*__.*$"],
    )

    with handler:
        pass


@app.command()
def new_entry(
    # In order to preserve the position if the defaults are not set from a config file we need to give them all a
    # default value. This means that Typer does not see them as required.
    module_site: Annotated[
        Optional[str] if default_module_site else str,
        module_site_arg,
    ] = default_module_site,
    collection: Annotated[
        Optional[str] if default_collection else str,
        collection_arg,
    ] = default_collection,
    filename: Annotated[
        str,
        typer.Argument(
            help="The filename in which to save the path. Will be saved in the collection's `content_path` [REQUIRED]"
        ),
    ] = None,
    content: Annotated[
        Optional[str],
        typer.Option(
            help="The content to include in the page. Either this or `--content-file` may be provided but not both"
        ),
    ] = None,
    content_file: Annotated[
        Optional[str],
        typer.Option(
            help="Path to a file containing the desired content. "
            "Either this or `--content` may be provided but not both",
        ),
    ] = None,
    title: Annotated[
        Optional[str],
        typer.Option(
            help="Title for the new page. If this is also provided via `--args` this will be preferred.",
        ),
    ] = None,
    slug: Annotated[
        Optional[str],
        typer.Option(
            help="Slug for the new page. If this is also provided via `--args` this will be preferred.",
        ),
    ] = None,
    args: Annotated[
        Optional[list[str]],
        typer.Option(
            help="key value attrs to include in your entry use the format `--args key=value` or `--args key:value`",
        ),
    ] = None,
    include_date: Annotated[
        Optional[bool],
        typer.Option(
            help="Include today's date in your entry.",
            is_flag=True,
        ),
    ] = False,
):
    """Creates a new collection entry based on the parser. Entries are added to the Collections content_path"""
    if not module_site or not collection or not filename:
        # Since some of the variables may come from the config and they all now have a default value we must check to
        # make sure all are set and error out correctly.
        raise typer.BadParameter("All required argements (module-site, collection, and filename) are required")
    module, site_name = split_module_site(module_site)
    parsed_args = split_args(args) if args else {}
    # There is an issue with including `title` in the context to the parser that causes an exception. We can fix
    # this by popping it out of the arguments here and using regex to push it back in later.
    _title = parsed_args.pop("title", None)
    # Prefer the title keyword from the one provided in `--args` in case someone does both.
    title = title or _title
    if slug:
        # If `slug` is provided as a keyword add it to the `parsed_args` to be included in the rendering.
        # Prefer the keyword to what is passed via `--args`
        parsed_args["slug"] = slug
    # Verify that we have a valid date should it be supplied or requested
    if date := parsed_args.pop("date", None):
        try:
            date = dateparser.parse(date)
        except ParserError:
            raise ValueError(f"Invalid date: {repr(date)}.") from None
    elif include_date:
        date = datetime.datetime.today()
    if date:
        parsed_args["date"] = date

    site = get_site(module, site_name)
    _collection = next(coll for coll in site.route_list.values() if type(coll).__name__.lower() == collection.lower())
    if content and content_file:
        raise TypeError("Both content and content_file provided. At most one may be provided.")
    if content_file:
        try:
            with open(content_file) as f:
                content = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Content file {repr(content_file)} not found.")
    entry = create_collection_entry(content=content or "", collection=_collection, **parsed_args)
    if title:
        # If we had a title earlier this is where we replace the default that is added by the template handler with
        # the one supplied by the user.
        entry = re.sub(r"title: Untitled Entry", f"title: {title}", entry)
    filepath = Path(_collection.content_path).joinpath(filename)
    filepath.write_text(entry)
    Console().print(f'New {collection} entry created at "{filepath}"')

    if editor := os.getenv("EDITOR", None):
        subprocess.run([editor, filepath])


def cli():
    app()
