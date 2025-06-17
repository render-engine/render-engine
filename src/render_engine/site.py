import copy
import logging
from collections import defaultdict
from pathlib import Path

from jinja2 import FileSystemLoader, PrefixLoader
from rich.progress import Progress

from .archive import Archive
from .collection import Collection
from .engine import engine
from .page import Page
from .plugins import PluginManager, handle_plugin_registration
from .themes import Theme, ThemeManager


class Site:
    """
    The site stores your pages and collections to be rendered.

    Attributes:
        site_vars (dict): A dictionary containing site-wide variables and their values.
        plugin_settings (dict): A dictionary containing plugin settings.

    Methods:
        update_site_vars(**kwargs): Updates the site-wide variables with the given key-value pairs.
        register_plugins(*plugins, **plugin_settings): Registers the specified plugins with the site.
        register_theme(theme): Registers a theme with the site.
        register_themes(*themes): Registers multiple themes with the site.
        update_theme_settings(**settings): Updates the theme settings with the given key-value pairs.
        collection(Collection): Adds a collection to the site's route list.
        page(Page): Adds a page to the site's route list.
        load_themes(): Loads the themes registered with the site.
        render(): Renders all pages and collections added to the site.

    Properties:
        output_path: The output path where the rendered files will be saved.
        static_paths: The paths to static files used in the site.
        template_path: The path to the template files used for rendering.
    """

    site_vars: dict = {
        "SITE_TITLE": "Untitled Site",
        "SITE_URL": "http://localhost:8000/",
        "DATETIME_FORMAT": "%d %b %Y %H:%M %Z",
        "head": set(),
        "theme": {},
    }
    _output_path: str | Path = "output"
    _template_path: str | Path = "templates"
    _static_paths: set = {"static"}
    plugin_settings: dict = {"plugins": defaultdict(dict)}

    def __init__(
        self,
    ) -> None:
        self.plugin_manager = PluginManager()
        self.theme_manager = ThemeManager(
            engine=engine,
            output_path=self._output_path,
            static_paths=self._static_paths,
        )
        self.route_list: dict = {}
        self.site_settings: dict = {}
        self.subcollections: dict[str, list] = {"pages": []}
        self.theme_manager.engine.globals.update(self.site_vars)
        if self.theme_manager.engine.loader is not None:
            self.theme_manager.engine.loader.loaders.insert(0, FileSystemLoader(self._template_path))

    @property
    def output_path(self) -> Path | str:
        return self.theme_manager.output_path

    @output_path.setter
    def output_path(self, output_path: Path | str) -> None:
        self.theme_manager.output_path = output_path

    @property
    def static_paths(self) -> set:
        return self.theme_manager.static_paths

    @static_paths.setter
    def static_paths(self, static_paths: set) -> None:
        self.theme_manager.static_paths = static_paths

    def update_site_vars(self, **kwargs) -> None:
        self.site_vars.update(**kwargs)
        self.theme_manager.engine.globals.update(self.site_vars)

    def register_plugins(self, *plugins, **plugin_settings) -> None:
        """
        Register plugins for the site

        :param plugins: List of plugins to register
        :param plugin_settings: KW arguments where the key is the plugin name and the value is a dictionary of settings.
        """
        handle_plugin_registration(
            self.plugin_manager,
            [(plugin, plugin_settings.get(plugin.__name__, dict())) for plugin in plugins],
            self.plugin_settings,
        )

    def register_theme(self, theme: Theme) -> None:
        """Overrides the ThemeManager register_theme method to add plugins to the site"""
        self.theme_manager.register_theme(theme)

        if theme.plugins:
            self.register_plugins(*theme.plugins)

    def register_themes(self, *themes: Theme) -> None:
        """
        Register multiple themes.

        Args:
            *themes: Theme objects to register
        """
        for theme in themes:
            self.register_theme(theme)

    def update_theme_settings(self, **settings) -> None:
        for key, value in settings.items():
            self.site_vars["theme"].update({key: value})

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
        _Collection.plugin_manager = copy.deepcopy(self.plugin_manager)
        self.register_themes(*getattr(_Collection, "required_themes", []))

        if plugins := getattr(_Collection, "plugins", []):
            handle_plugin_registration(
                _Collection.plugin_manager,
                plugins,
                getattr(_Collection, "plugin_settings", dict()),
            )

        for plugin in getattr(_Collection, "ignore_plugins", []):
            _Collection.plugin_manager.unregister_plugin(plugin)

        self.route_list[_Collection._slug] = _Collection
        return _Collection

    def page(self, _page: Page) -> Page:
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
        page = _page()
        page.title = page._title  # Expose _title to the user through `title`

        # copy the plugin manager, removing any plugins that the page has ignored
        page.plugin_manager = copy.deepcopy(self.plugin_manager)

        if plugins := getattr(page, "plugins", []):
            handle_plugin_registration(page.plugin_manager, plugins, getattr(page, "plugin_settings", dict()))

        for plugin in getattr(page, "ignore_plugins", []):
            page.plugin_manager.unregister_plugin(plugin)

        self.route_list[getattr(page, page._reference)] = page
        return page

    def _render_output(self, route: str | Path, page: Page | Archive) -> int:
        """writes the page object to disk"""
        path = Path(self.output_path) / Path(route) / Path(page.path_name)
        path.parent.mkdir(parents=True, exist_ok=True)
        settings = dict()

        if hasattr(page, "plugin_manager") and page.plugin_manager is not None:
            settings = {**self.plugin_manager.plugin_settings, "route": route}
            page.plugin_manager.hook.render_content(page=page, settings=settings, site=self)
        page.rendered_content = page._render_content(engine=self.theme_manager.engine)
        # pass the route to the plugin settings

        if hasattr(page, "plugin_manager") and page.plugin_manager is not None:
            page.plugin_manager.hook.post_render_content(page=page.__class__, settings=settings, site=self)

        return path.write_text(page.rendered_content)

    def _render_full_collection(self, collection: Collection) -> None:
        """Iterate through Pages and Check for Collections and Feeds"""

        for entry in collection:
            entry.plugin_manager = copy.deepcopy(self.plugin_manager)

            for route in entry.routes:
                self._render_output(route, entry)

        if getattr(collection, "has_archive", False):
            for archive in collection.archives:
                logging.debug("Adding Archive: %s", archive.__class__.__name__)

                for route in collection.routes:
                    self._render_output(collection.routes[0], archive)

                if archive.is_index:
                    archive.slug = "index"
                    self._render_output(collection.routes[0], archive)

        if hasattr(collection, "Feed"):
            self._render_output("./", collection.feed)

    def load_themes(self) -> None:
        """
        function for registering the themes with the theme_manager.
        Used prior to rendering and cli-tasks
        """
        # load themes in the ChoiceLoader/FileLoader
        for theme_prefix, theme_loader in self.theme_manager.prefix.items():
            logging.info(f"loading theme: {theme_prefix}")
            if self.theme_manager.engine.loader is not None:
                self.theme_manager.engine.loader.loaders.insert(-1, theme_loader)
        # load themes in the PrefixLoader
        if self.theme_manager.engine.loader is not None:
            self.theme_manager.engine.loader.loaders.insert(-1, PrefixLoader(self.theme_manager.prefix))

    @property
    def template_path(self) -> str:
        if self.theme_manager.engine.loader is not None:
            return self.theme_manager.engine.loader.loaders[0].searchpath[0]
        return ""

    @template_path.setter
    def template_path(self, template_path: str) -> None:
        if self.theme_manager.engine.loader is not None:
            self.theme_manager.engine.loader.loaders.insert(0, FileSystemLoader(template_path))

    def render(self) -> None:
        """
        Render all pages and collections.

        These are pages and collections that have been added to the site using
        the [`Site.page`][src.render_engine.Site.page]
        and [`Site.collection`][src.render_engine.Site.collection] methods.

        Render should be called after all pages and collections have been added to the site.

        You can choose to call it manually in your file or
        use the CLI command [`render-engine build`][src.render_engine.cli.build]
        """

        with Progress() as progress:
            pre_build_task = progress.add_task("Loading Pre-Build Plugins and Themes", total=1)
            self.plugin_manager.hook.pre_build_site(
                site=self,
                settings=self.plugin_manager.plugin_settings,
            )  # type: ignore

            self.load_themes()
            self.theme_manager.engine.globals.update(self.site_vars)
            progress.update(pre_build_task, advance=1)
            # Parse Route List
            task_add_route = progress.add_task("[blue]Adding Routes", total=len(self.route_list))

            self.theme_manager._render_static()

            self.theme_manager.engine.globals["site"] = self
            self.theme_manager.engine.globals["routes"] = self.route_list

            for slug, entry in self.route_list.items():
                progress.update(task_add_route, description=f"[blue]Adding[gold]Route: [blue]{slug}")
                if isinstance(entry, Page):
                    for route in entry.routes:
                        progress.update(
                            task_add_route,
                            description=f"[blue]Adding[gold]Route: [blue]{entry._slug}",
                        )
                        self._render_output(route, entry)

                if isinstance(entry, Collection):
                    progress.update(
                        task_add_route,
                        description=f"[blue]Adding[gold]Route: [blue]Collection {entry._slug}",
                    )
                    pre_build_collection_task = progress.add_task(
                        "Loading Pre-Build-Collection Plugins",
                        total=1,
                    )
                    entry._run_collection_plugins(
                        hook_type="pre_build_collection",
                        site=self,
                    )
                    progress.update(pre_build_collection_task, advance=1)

                    self._render_full_collection(entry)

                    post_build_collection_task = progress.add_task(
                        "Loading Post-Build-Collection Plugins",
                        total=1,
                    )
                    entry._run_collection_plugins(
                        hook_type="post_build_collection",
                        site=self,
                    )
                    progress.update(post_build_collection_task, advance=1)
                progress.update(task_add_route, advance=1)

            post_build_task = progress.add_task("Loading Post-Build Plugins", total=1)
            self.plugin_manager.hook.post_build_site(
                site=self,
                settings=self.plugin_manager.plugin_settings,
            )
            progress.update(post_build_task, advance=1)
