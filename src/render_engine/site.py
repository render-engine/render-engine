import logging
import shutil
from pathlib import Path
from typing import Callable

from jinja2 import Environment, FileSystemLoader

from .collection import Collection
from .page import Page
from .route import Route


class Site:
    """The site stores your pages and collections to be rendered."""

    path: Path = Path("output")
    """Path to write rendered content."""

    static: str | Path = Path("static")
    """Output Path for the static folder. This will get copied to the output folder"""

    # Vars that will be passed into the render functions
    site_vars: dict = {"SITE_TITLE": "Untitled Site", "SITE_URL": "https://example.com"}

    engine: Environment = Environment(loader=FileSystemLoader("templates"))
    """``Engine`` to generate web pages"""

    plugins: list[Callable] | None = None

    def __init__(
        self, static: str | None = None, plugins: list[Callable] = [], **kwargs
    ) -> None:
        self.site_vars.update(kwargs)
        self.route_list: list[Route] = []

        if plugins and not self.plugin:
            self.plugins = plugins

        elif plugins:

            for plugin in self.plugins:
                setattr(self, plugin.__name__, plugin)

    def collection(self, collection: Collection):
        """Create the pages in the collection including the archive"""
        _collection = collection(engine=self.engine, **self.site_vars)
        logging.warning("Adding Collection: %s", _collection.__class__.__name__)
        for page_obj in _collection:
            for page_routes in page_obj:
                self.route_list.append(page_routes)

        for archive in _collection.archives:
            for page_routes in archive:
                self.route_list.append(page_routes)

    def page(self, page: Page) -> None:
        """Create a Page object and add it to self.routes"""
        _page = page(self.engine, **self.site_vars)
        for page_route in _page.render():
            self.route_list.append(page_route)

    def render_static(self, directory) -> None:
        """Copies a Static Directory to the output folder"""
        return shutil.copytree(
            directory, self.path / Path(directory).name, dirs_exist_ok=True
        )

    def render(self, clean=False) -> None:
        """Render all pages and collections"""
        if clean:
            shutil.rmtree(self.path, ignore_errors=True)

        for route in self.route_list:
            path = self.path / route.filepath
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(route.markup)

        if self.static:
            self.render_static(self.static)
