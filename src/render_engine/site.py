import logging
import pathlib
import shutil
from collections import defaultdict

from jinja2 import Environment
from rich.progress import Progress

from .collection import Collection
from .engine import engine
from .hookspecs import register_plugins
from .page import Page


class Site:
    """
    The site stores your pages and collections to be rendered.

    Attributes:
        engine: Jinja2 Environment used to render pages
        output_path: 
            path to write rendered content
        partial: 
            if True, only render pages that have been modified. Uses gitPython to check for changes.
        plugins: 
            list of plugins that will be loaded and passed into each object
        static: 
            path for the static folder. This will get copied to the output folder.
        site_vars: 
            dictionary that will be passed into page template
        site_settings:
            settings that will be passed into pages and collections but not into templates
    """

    output_path: str = "output"
    static_path: str = "static"
    partial: bool = False
    site_settings: dict = {
        "plugins": {}
    }
    site_vars: dict = {
        "SITE_TITLE": "Untitled Site",
        "SITE_URL": "http://localhost:8000/",
        "DATETIME_FORMAT": "%d %b %Y %H:%M %Z"
    }
    plugins: list
    engine: Environment = engine


    def __init__(
        self,
        plugins: list[str] = [],
    ) -> None:
        self.route_list = dict()
        self.subcollections = defaultdict(lambda: {"pages": []})
        self.engine.globals.update(self.site_vars)
        self.plugins = [*plugins, *getattr(self, "plugins", [])]
        self._pm = register_plugins(plugins=self.plugins)

    def collection(self, Collection: type[Collection]) -> Collection:
        """
        Add the collection to the route list to be rendered later.

        This is the primary way to add a collection to the site and 
        can either be called on an uninstantiated class or on the class definition as a decorator.

        In most cases. You should use the decorator method.

        ```python
        from render_engine import Site, Collection

        site = Site()

        @site.collection # works
        class Pages(Collection):
            pass


        class Posts(Collection):
            pass

        site.collection(Posts) # also works
        ```
        """
        _Collection = Collection()
        _Collection.register_plugins(self.plugins)
        self._pm.hook.pre_build_collection(collection=_Collection) #type: ignore
        self.route_list[_Collection._slug] = _Collection
        return _Collection

    def page(self, Page: Page) -> Page:
        """
        Add the page to the route list to be rendered later.
        Also remaps `title` in case the user wants to use it in the template rendering.

        This is the primary way to add a page to the site and can either be called
        on an uninstantiated class or on the class definition as a decorator.

        In most cases. You should use the decorator method.

        ```python

        from render_engine import Site, Page

        site = Site()

        @site.page # works
        class Home(Page):
            pass

        class About(Page):
            pass

        site.page(About) # also works
        ```
        """
        page = Page()
        page.title = page._title # Expose _title to the user through `title`
        page.register_plugins(self.plugins)
        self.route_list[getattr(page, page._reference)] = page

    def _render_static(self) -> None:
        """Copies a Static Directory to the output folder"""
        shutil.copytree(
            self.static_path,
            pathlib.Path(self.output_path) / pathlib.Path(self.static_path).name,
            dirs_exist_ok=True
        )

    def _render_output(self, route: str, page: type[Page]):
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

    def _render_partial_collection(self, collection: Collection) -> None:
        """Iterate through the Changed Pages and Check for Collections and Feeds"""
        for entry in collection._generate_content_from_modified_pages():
            entry._pm.hook.render_content(Page=entry)
            for route in collection.routes:
                self._render_output(route, entry)

        if collection.has_archive:
            for archive in collection.archives:
                logging.debug("Adding Archive: %s", archive.__class__.__name__)

                self._render_output(collection.routes[0], archive)

        if hasattr(collection, "Feed"):
            self._render_output("./", collection.feed)

    def _render_full_collection(self, collection: Collection) -> None:
        """Iterate through Pages and Check for Collections and Feeds"""

        for entry in collection:
            entry._pm.hook.render_content(Page=entry)
            for route in collection.routes:
                self._render_output(route, entry)

        if collection.has_archive:
            for archive in collection.archives:
                logging.debug("Adding Archive: %s", archive.__class__.__name__)

                for route in collection.routes:
                    self._render_output(collection.routes[0], archive)

        if hasattr(collection, "Feed"):
            self._render_output("./", collection.feed)

    def render(self) -> None:
        """
        Render all pages and collections.

        These are pages and collections that have been added to the site using 
        the [`Site.page`][src.render_engine.Site.page] 
        and [`Site.collection`][src.render_engine.Site.collection] methods.

        Render should be called after all pages and collections have been added to the site.

        You can choose to call it manually in your file or use the CLI command [`render-engine build`][src.render_engine.cli.build]
        """

        with Progress() as progress:

            pre_build_task = progress.add_task("Loading Pre-Build Plugins", total=1)
            self._pm.hook.pre_build_site(site=self)

            # Parse Route List
            task_add_route = progress.add_task(
                "[blue]Adding Routes", total=len(self.route_list)
            )

            if pathlib.Path(self.static_path).exists():
                self._render_static()
            self.engine.globals["site"] = self
            self.engine.globals["routes"] = self.route_list

            for slug, entry in self.route_list.items():
                progress.update(
                    task_add_route, description=f"[blue]Adding[gold]Route: [blue]{slug}"
                )
                if isinstance(entry, Page):
                    if getattr(entry, "collection", None):
                        entry._pm.hook.render_content(Page=entry)
                    for route in entry.routes:
                        progress.update(
                            task_add_route,
                            description=f"[blue]Adding[gold]Route: [blue]{entry._slug}",
                        )
                        self._render_output(route, entry)

                if isinstance(entry, Collection):
                    if self.partial:
                        self._render_partial_collection(entry)
                    else:
                        self._render_full_collection(entry)
            progress.add_task("Loading Post-Build Plugins", total=1)
            self._pm.hook.post_build_site(site=self)
            progress.update(pre_build_task, advance=1)
