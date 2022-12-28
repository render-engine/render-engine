import logging
import pathlib
import shutil
from collections import defaultdict
from typing import Callable

from jinja2 import Environment, FileSystemLoader

from .collection import Collection
from .page import Page


class Site:
    """
    The site stores your pages and collections to be rendered.

    Attributes:
        output_path: str to write rendered content. **Default**: `output`
        static: Output str Path for the static folder. This will get copied to the output folder. **Default**: `static`
        site_vars: Vars that will be passed into the render functions

            Default `site_vars`:

            - SITE_TITLE: "Untitled Site"
            - SITE_URL: "http://example.com"
    """

    output_path: str = "output"
    static_path: str = "static"
    # TODO: #74 Should this be called from a config file for easier testing?
    site_vars: dict = {
        "SITE_TITLE": "Untitled Site",
        "SITE_URL": "https://example.com",  # TODO: #73 Make this http://localhost:8000
    }
    plugins: dict[str, Page] | None = None

    def __init__(
        self,
    ) -> None:
        self.route_list: defaultdict = defaultdict(list)
        self.subcollections: defaultdict = defaultdict(lambda: {"pages": []})

    @property
    def engine(self) -> Environment:
        env = Environment(loader=FileSystemLoader("templates"))
        env.globals = self.site_vars
        return env

    def add_to_route_list(self, page: Page) -> None:
        """Add a page to the route list"""
        self.route_list[page.url_for] = page

    def collection(self, collection: Collection):
        """Create the pages in the collection including the archive"""
        _collection = collection(engine=self.engine, **self.site_vars)
        logging.info("Adding Collection: %s", _collection.__class__.__name__)

        for page in _collection.pages:
            logging.debug("Adding Page: %s", page.__class__.__name__)
            self.add_to_route_list(page)

        for archive in _collection.archives:
            logging.debug("Adding Archive: %s", archive.__class__.__name__)
            self.add_to_route_list(archive)

        if feed := (getattr(_collection, "_feed", None)):
            self.add_to_route_list(feed)

    def page(self, page: Page) -> None:
        """Create a Page object and add it to self.routes"""
        logging.info("Adding Page: %s", page.__class__.__name__)
        _page = page(self.engine, **self.site_vars)
        self.add_to_route_list(_page)

    def render_static(self, directory) -> None:
        """Copies a Static Directory to the output folder"""

    def render_output(self, route, page):
        """writes the page object to disk"""
        if page._extension == ".xml":
            logging.debug("%s, %s", page.content, page.pages)
        path = (
            pathlib.Path(self.output_path)
            / pathlib.Path(route)
            / pathlib.Path(page.url)
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        return path.write_text(page._render_content())

    def build_subcollections(self, page) -> None:
        if subcollections := getattr(page, "subcollections", []):
            logging.debug("Adding subcollections: %s", subcollections)

            for attr in subcollections:
                logging.debug("Adding attr: %s", attr)

                for page_attr in getattr(page, attr, []):
                    logging.debug("Adding page_attr: %s", page_attr)
                    self.subcollections[page_attr]
                    self.subcollections[page_attr]["pages"].append(page)
                    self.subcollections[page_attr]["route"] = attr

                    if "template" not in self.subcollections[page_attr]:
                        self.subcollections[page_attr][
                            "template"
                        ] = page.subcollection_template

    def render(self, clean=False) -> None:
        """Render all pages and collections"""

        if clean:
            shutil.rmtree(self.path, ignore_errors=True)

        # Parse Route List
        for page in self.route_list.values():
            self.build_subcollections(page)

            for route in page.routes:
                self.render_output(route, page)

        # Parse SubCollection
        for tag, subcollection in self.subcollections.items():
            page = Page(
                self.engine,
                title=tag,
                template=subcollection["template"],
                pages=subcollection["pages"],
            )
            self.render_output(
                Path(page.routes[0]).joinpath(subcollection["route"]), page
            )

        if path := (pathlib.Path(self.static_path)).exists():
            self.render_static(path)
