import logging
import pathlib
import typing
from collections import defaultdict
from re import template

import pluggy
from jinja2 import Environment, FileSystemLoader
from rich.progress import Progress

from .collection import Collection
from .engine import engine
from .hookspecs import _PROJECT_NAME, SiteSpecs
from .page import Page
from .utils.themes import Theme, ThemeManager


class Site(ThemeManager):
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
        static_paths: 
            list of paths for static folders. This will get copied to the output folder. Folders are recursive.
        site_vars: 
            dictionary that will be passed into page template
        site_settings:
            settings that will be passed into pages and collections but not into templates
    """

    _pm: pluggy.PluginManager
    partial: bool = False
    site_settings: dict = {
        "plugins": {}
    }
    site_vars: dict = {
        "SITE_TITLE": "Untitled Site",
        "SITE_URL": "http://localhost:8000/",
        "DATETIME_FORMAT": "%d %b %Y %H:%M %Z"
    }
    engine: Environment = engine
    template_path: str = "templates"


    def __init__(
        self,
    ) -> None:
        self.route_list = dict()
        self.subcollections = defaultdict(lambda: {"pages": []})
        self.engine.globals.update(self.site_vars)
        
        if self.template_path:
            self.engine.loader.loaders.insert(0, FileSystemLoader(self.template_path))
        
        # Manage Plugins
        self._pm = pluggy.PluginManager(project_name=_PROJECT_NAME)
        self._pm.add_hookspecs(SiteSpecs)

    def update_site_vars(self, **kwargs) -> None:
        self.site_vars.update(**kwargs)
        self.engine.globals.update(self.site_vars)

    def register_plugins(self, *plugins, **settings: dict[str, typing.Any]) -> None:
        """Register plugins with the site
        
        parameters:
            plugins: list of plugins to register
            settings: settings to pass into the plugins
                settings keys are the plugin names as strings.
        """
        
        for plugin in plugins:
            self._pm.register(plugin)        
            self.site_settings['plugins'][plugin.__name__] = getattr(plugin, 'default_settings', {})

        self._pm.hook.add_default_settings(
            site=self,
            custom_settings=settings,
        ) 
        self.site_settings['plugins'].update(**settings)

    @property
    def plugins(self):
        return self._pm.get_plugins()

    def register_theme(self, theme: Theme):
        """Overrides the ThemeManager register_theme method to add plugins to the site"""
        super().register_theme(theme)
        if theme.plugins:
            self.register_plugins(*theme.plugins)


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
        plugins = [*self.plugins, *getattr(_Collection, "plugins", [])]
        
        for plugin in getattr(_Collection, 'ignore_plugins', []):
            plugins.remove(plugin)
        _Collection.register_plugins(plugins)

        self._pm.hook.pre_build_collection(
            collection=_Collection,
            settings=self.site_settings.get('plugins', {}),
        ) #type: ignore
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

        # copy the plugin manager, removing any plugins that the page has ignored
        page._pm = self._pm

        for plugin in getattr(page, 'ignore_plugins', []):
            page._pm.unregister(plugin)

        self.route_list[getattr(page, page._reference)] = page

    def _render_output(self, route: str, page: Page):
        """writes the page object to disk"""
        path = (
            pathlib.Path(self.output_path)
            / pathlib.Path(route)
            / pathlib.Path(page.path_name)
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        settings = {**self.site_settings.get('plugins', {}), **{'route': route}}
        self._pm.hook.render_content(page=page, settings=settings)
        page.rendered_content = page._render_content(engine=self.engine)
        # pass the route to the plugin settings
        self._pm.hook.post_render_content(page=page.__class__, settings=settings, site=self)

        return path.write_text(page.rendered_content)

    def _render_partial_collection(self, collection: Collection) -> None:
        """Iterate through the Changed Pages and Check for Collections and Feeds"""
        for entry in collection._generate_content_from_modified_pages():
            for route in collection.routes:
                self._render_output(route, entry)

        if getattr(collection, 'has_archive', False):
            for archive in collection.archives:
                logging.debug("Adding Archive: %s", archive.__class__.__name__)

                self._render_output(collection.routes[0], archive)

        if hasattr(collection, "Feed"):
            self._render_output("./", collection.feed)

    def _render_full_collection(self, collection: Collection) -> None:
        """Iterate through Pages and Check for Collections and Feeds"""

        for entry in collection:
            for route in collection.routes:
                self._render_output(route, entry)

        if getattr(collection, 'has_archive', False):
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
            self._pm.hook.pre_build_site(
                site=self,
                settings=self.site_settings.get('plugins', {})
                ) #type: ignore


            self.engine.globals.update(self.site_vars)
            # Parse Route List
            task_add_route = progress.add_task(
                "[blue]Adding Routes", total=len(self.route_list)
            )

            self._render_static()

            self.engine.globals["site"] = self
            self.engine.globals["routes"] = self.route_list

            for slug, entry in self.route_list.items():
                progress.update(
                    task_add_route, description=f"[blue]Adding[gold]Route: [blue]{slug}"
                )
                if isinstance(entry, Page):
                    if getattr(entry, "collection", None):
                        self._pm.hook.render_content(Page=entry, settings=self.site_settings.get('plugins', None))
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
            self._pm.hook.post_build_site(
                site=self,
                settings=self.site_settings.get('plugins', {}),
            )
            progress.update(pre_build_task, advance=1)
