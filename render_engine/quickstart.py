import render_engine
import click
from jinja2 import Environment, PackageLoader

import shutil
from pathlib import Path


def create_templates_directory(
    base_dir: str = Path().cwd(),
    templates_dir: str = "templates",
    include_template_files: bool = True,
):
    """
    Create Base Folders for your
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
    "--base-directory", default=".", help="starting directory for your project"
)
@click.option(
    "--static-directory", default="static", help="static directory for your project"
)
@click.option(
    "--content-directory", default="content", help="content directory for your project"
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
    prompt="Would you like to create a blog object",
    help="Add a Blog Object",
)
@click.option("--microblog", is_flag=True, default=False)
@click.option(
    "--pages-directory",
    is_flag=True,
    help="create a separate pages directory inside of your content path",
)
@click.option("--templates-directory", default='templates',
        help="directory for template files")
def _main(
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

    if static_path:
        Path(base_directory).joinpath(static_directory).mkdir(
            parents=True, exist_ok=True
        )

    if content_path:
        Path(base_directory).joinpath(content_directory).mkdir(
            parents=True, exist_ok=True
        )

    if templates_path:
        create_templates_directory(
            base_directory, templates_directory, templates_files
        )


if __name__ == "__main__":
    _main()
