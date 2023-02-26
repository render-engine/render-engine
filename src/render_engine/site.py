import logging
import pathlib
import shutil
from collections import defaultdict
from functools import partial
from typing import Type
from jinja2 import Environment
from rich.progress import Progress

from .collection import Collection
from .engine import engine, url_for
from .hookspecs import register_plugins
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
    partial: bool = False

    site_vars: dict = {
        "SITE_TITLE": "Untitled Site",
        "SITE_URL": "http://localhost:8000/",
    }
    plugins: list

    def __init__(
        self,
        plugins: list[str] = [],
    ) -> None:
        self.route_list = dict()
        self.subcollections = defaultdict(lambda: {"pages": []})
        self.engine.filters["url_for"] = partial(url_for, site=self)
        self.plugins = [*plugins, *getattr(self, "plugins", [])]
        self._pm = register_plugins(plugins=self.plugins)

    @property
    def engine(self) -> Environment:
        env = engine
        env.globals.update(self.site_vars)
        return env

    def add_to_route_list(self, page: Page) -> None:
        """Add a page to the route list"""
        self.route_list[getattr(page, page._reference)] = page

    def collection(self, Collection: Type[Collection]) -> Collection:
        """Create the pages in the collection including the archive"""
        _Collection = Collection(plugins=self.plugins)
        self._pm.hook.pre_build_collection(collection=_Collection) #type: ignore
        self.route_list[_Collection._slug] = _Collection
        return _Collection

    def page(self, Page: type[Page]) -> Page:
        """Create a Page object and add it to self.routes"""
        page = Page(plugins=self.plugins)

        # Expose _title to the user through `title`
        page.title = page._title
        logging.info("Running Post Build Page")
        self.add_to_route_list(page)
        return page

    def render_static(self, directory) -> None:
        """Copies a Static Directory to the output folder"""
        shutil.copytree(
            directory, pathlib.Path(self.output_path) / directory, dirs_exist_ok=True
        )

    def render_output(self, route: str, page: Type[Page]):
        """writes the page object to disk"""
        path = (
            pathlib.Path(self.output_path)
            / pathlib.Path(route)
            / pathlib.Path(page.path_name)
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        return path.write_text(
            page._render_content(engine=self.engine)
        )

    def render_partial_collection(self, collection: Collection) -> None:
        """Iterate through the Changed Pages and Check for Collections and Feeds"""
        for entry in collection._generate_content_from_modified_pages():
            for route in collection.routes:
                self.render_output(route, entry)

        if collection.has_archive:
            for archive in collection.archives:
                logging.debug("Adding Archive: %s", archive.__class__.__name__)

                self.render_output(collection.routes[0], archive)

        if hasattr(collection, "Feed"):
            self.render_output("./", collection._feed)

    def render_full_collection(self, collection: Collection) -> None:
        """Iterate through Pages and Check for Collections and Feeds"""

        for entry in collection:
            for route in collection.routes:
                self.render_output(route, entry)

        if collection.has_archive:
            for archive in collection.archives:
                logging.debug("Adding Archive: %s", archive.__class__.__name__)

                for route in collection.routes:
                    self.render_output(collection.routes[0], archive)

        if hasattr(collection, "Feed"):
            self.render_output("./", collection._feed)

    def render(self) -> None:
        """Render all pages and collections"""

        with Progress() as progress:

            pre_build_task = progress.add_task("Loading Pre-Build Plugins", total=1)
            self._pm.hook.pre_build_site(site=self)

            # Parse Route List
            task_add_route = progress.add_task(
                "[blue]Adding Routes", total=len(self.route_list)
            )
            engine.globals["site"] = self

            for slug, entry in self.route_list.items():
                progress.update(
                    task_add_route, description=f"[blue]Adding[gold]Route: [blue]{slug}"
                )
                if isinstance(entry, Page):
                    for route in entry.routes:
                        progress.update(
                            task_add_route,
                            description=f"[blue]Adding[gold]Route: [blue]{entry._slug}",
                        )
                        self.render_output(route, entry)

                if isinstance(entry, Collection):
                    if self.partial:
                        self.render_partial_collection(entry)
                    else:
                        self.render_full_collection(entry)

            post_build_task = progress.add_task("Loading Post-Build Plugins", total=1)
            self._pm.hook.post_build_site(site=self)

            progress.update(pre_build_task, advance=1)
