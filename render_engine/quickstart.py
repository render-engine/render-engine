import logging
import shutil
from pathlib import Path

import click
from jinja2 import Environment, PackageLoader

import render_engine


def create_templates_directory(
    base_dir: str = Path().cwd(),
    templates_dir: str = "templates",
    include_template_files: bool = True,
):
    """Create Base Folders for your
    output_dir, static_dir, content_path, and templates_path
    """

    source_folder = Path(Path(render_engine.__file__).parent, "templates")
    templates_path = Path(base_dir).joinpath(templates_dir)

    if include_template_files:
        return shutil.copytree(source_folder, templates_path, dirs_exist_ok=True)

    else:
        return Path(base_dir).joinpath(content_path).mkdir(parents=True, exist_ok=True)


@click.command()
@click.option(
    "--base-directory", default="./", help="starting directory for your project"
)
@click.option(
    "--static-directory", default="./static", help="static directory for your project"
)
@click.option(
    "--content-directory",
    default="./content/pages",
    help="content directory for your project",
)
@click.option(
    "--static-path/--no-static-path", "-s/-S", default=True, help="create a static path"
)
@click.option(
    "--content-path/--no-content-path",
    "-c/-C",
    default=True,
    help="directory for prerendered files",
)
@click.option(
    "--templates-path/--no-templates-path",
    "-t/-T",
    default=True,
    help="directory for template files",
)
@click.option(
    "--templates-files/--no-templates-files",
    "-f/-F",
    default=True,
    help="files for templates-directory",
)
@click.option(
    "--blog",
    is_flag=True,
    default=True,
    help="Add a Blog Object",
)
@click.option("--microblog", is_flag=True, default=False)
@click.option(
    "--pages-directory",
    is_flag=True,
    help="create a separate pages directory inside of your content path",
)
@click.option(
    "--templates-directory", default="templates", help="directory for template files"
)
def quickstart(
    base_directory,
    static_path,
    content_path,
    templates_path,
    blog,
    microblog,
    templates_files,
    static_directory,
    content_directory,
    pages_directory,
    templates_directory,
):
    """
    CLI that allows folks to quickly build their starting directory
    """

    click.echo("Initiating Quickstart")

    if static_path and not (static_dir := Path(static_directory)).exists():
        static_dir.mkdir(parents=True)

    else:
        logging.warning(f"{static_dir=} already exists. Skipping.")

    if content_path and not (content_dir := Path(content_directory)).exists():
        content_dir.mkdir(
            parents=True,
        )

    else:
        logging.warning(f"{content_dir=} already exists. Skipping.")

    if templates_path:
        create_templates_directory(base_directory, templates_directory, templates_files)

    if not Path("./run.py").exists():
        shutil.copy(
            Path(render_engine.__file__).parent.joinpath("run_template.txt"), "./run.py"
        )

    else:
        logging.warning(f"run.py already exists. Skipping.")
