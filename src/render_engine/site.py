import copy
import logging
from collections import defaultdict
from pathlib import Path

from jinja2 import FileSystemLoader, PrefixLoader
from rich.progress import Progress

from .collection import Collection
from .engine import engine
from .page import Page
from .plugins import PluginManager, handle_plugin_registration
from .themes import Theme, ThemeManager


class Site:
    """
    Central coordinator for the static site generation process.

    The Site class manages the entire site structure, coordinating Pages, Collections,
    themes, plugins, and the rendering pipeline. It serves as the main entry point
    for building a static site.

    Architecture Overview:
    - Pages: Individual content pieces rendered to specific routes
    - Collections: Groups of related pages with shared properties and archive generation
    - Themes: Template and styling packages that can be applied site-wide
    - Plugins: Extensions that hook into various stages of the build process


    Attributes:
        site_vars (dict): Global variables available in all templates (e.g., SITE_TITLE, SITE_URL)
        plugin_settings (dict): Configuration for registered plugins
        route_list (dict): Mapping of route slugs to Page/Collection objects
        theme_manager (ThemeManager): Handles template loading and static file management
        plugin_manager (PluginManager): Manages plugin registration and execution

    Methods:
        collection(): Register a Collection class with the site
        page(): Register a Page class with the site
        render(): Execute the complete site build process
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
        Register a Collection with the site and establish the site-collection relationship.

        This method creates a bidirectional relationship between the Site and Collection:
        - The Collection gets a reference to the Site's PluginManager
        - The Site stores the Collection in its route_list for rendering
        - Collection-specific plugins and themes are registered
        - The Collection becomes accessible via site.route_list[collection_slug]

        The relationship enables:
        - Site-wide plugin inheritance with collection-specific overrides
        - Theme requirements specified by the collection
        - Access to site variables and settings during rendering

        Args:
            Collection: The Collection class to register (not instantiated)

        Returns:
            Collection: The instantiated and configured Collection object
        """
        # Instantiate the collection and establish plugin inheritance
        _Collection = Collection()
        _Collection.plugin_manager = copy.deepcopy(self.plugin_manager)

        # Register any themes required by this collection
        self.register_themes(*getattr(_Collection, "required_themes", []))

        # Handle collection-specific plugin registration
        if plugins := getattr(_Collection, "plugins", []):
            handle_plugin_registration(
                _Collection.plugin_manager,
                plugins,
                getattr(_Collection, "plugin_settings", dict()),
            )

        # Remove any plugins the collection wants to ignore
        for plugin in getattr(_Collection, "ignore_plugins", []):
            _Collection.plugin_manager.unregister_plugin(plugin)

        # Register collection in site's route_list for URL resolution
        # This enables cross-referencing: {{ "collection_slug" | url_for }}
        # And collection.page references: {{ "collection_slug.page_slug" | url_for }}
        self.route_list[_Collection._slug] = _Collection
        return _Collection

    def page(self, _page: Page) -> Page:
        """
        Register a Page with the site and establish the site-page relationship.

        This method creates a bidirectional relationship between the Site and Page:
        - The Page gets a reference to the Site's PluginManager
        - The Site stores the Page in its route_list for rendering
        - Page-specific plugins are registered and site plugins are inherited
        - The Page becomes accessible via site.route_list[page_slug]

        The relationship enables:
        - Site-wide plugin inheritance with page-specific overrides
        - Access to site variables and settings during rendering
        - Consistent plugin management across all site content

        Args:
            _page: The Page class to register (not instantiated)

        Returns:
            Page: The instantiated and configured Page object
        """
        # Instantiate the page and expose title attribute for templates
        page = _page()
        page.title = page._title  # Expose _title to the user through `title`

        # Establish plugin inheritance from site to page
        page.plugin_manager = copy.deepcopy(self.plugin_manager)

        # Handle page-specific plugin registration
        if plugins := getattr(page, "plugins", []):
            handle_plugin_registration(page.plugin_manager, plugins, getattr(page, "plugin_settings", dict()))

        # Remove any plugins the page wants to ignore
        for plugin in getattr(page, "ignore_plugins", []):
            page.plugin_manager.unregister_plugin(plugin)

        # Register page in site's route_list for URL resolution
        # This enables direct page references: {{ "page_slug" | url_for }}
        # The _reference attribute (default: "_slug") determines the route key
        self.route_list[getattr(page, page._reference)] = page
        return page

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
        Execute the complete site build process, orchestrating Pages and Collections.

        This method coordinates the rendering of all registered Pages and Collections,
        establishing the final site-page/collection relationships and executing the
        complete build pipeline with plugin hooks.

        Build Process:
        1. Pre-build site plugins execute
        2. Themes are loaded and site variables injected into templates
        3. Static files are copied to output directory
        4. Each Page/Collection gets a reference to the Site (entry.site = self)
        5. Pages and Collections are rendered with their respective plugin hooks
        6. Post-build site plugins execute

        The site.route_list contains all registered content, and during rendering:
        - Pages get rendered to their specified routes
        - Collections get rendered along with their archives and feeds
        - All content has access to site variables and the complete route list

        This establishes the runtime relationship where Pages and Collections
        can reference the Site and other routes during template rendering.
        """
        with Progress() as progress:
            # Phase 1: Pre-build setup
            pre_build_task = progress.add_task("Loading Pre-Build Plugins and Themes", total=1)
            self.plugin_manager.hook.pre_build_site(
                site=self,
                settings=self.plugin_manager.plugin_settings,
            )  # type: ignore

            self.load_themes()
            self.theme_manager.engine.globals.update(self.site_vars)
            progress.update(pre_build_task, advance=1)

            # Phase 2: Route processing setup
            task_add_route = progress.add_task("[blue]Adding Routes", total=len(self.route_list))
            self.theme_manager._render_static()

            # Inject site context into template globals for cross-referencing
            # This enables templates to access site info and cross-reference other content
            self.theme_manager.engine.globals["site"] = self
            self.theme_manager.engine.globals["routes"] = self.route_list

            # Phase 3: Render each registered Page/Collection
            # route_list maps slugs to Page/Collection objects for URL resolution
            for slug, entry in self.route_list.items():
                # Establish bidirectional relationship: entry gets site reference
                # This allows Pages/Collections to access site config and other routes
                entry.site = self
                progress.update(task_add_route, description=f"[blue]Adding[gold]Route: [blue]{slug}")
                args = []

                match entry:
                    case Page():
                        # Render page to each of its routes
                        for route in entry.routes:
                            progress.update(
                                task_add_route,
                                description=f"[blue]Adding[gold]Route: [blue]{entry._slug}",
                            )
                            args = [route, self.theme_manager]
                    case Collection():
                        # Execute pre-build collection plugins
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

                # Render the entry (Page or Collection)
                entry.render(*args)

                # Execute post-build collection plugins if this is a Collection
                if isinstance(entry, Collection):
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

            # Phase 4: Post-build cleanup
            post_build_task = progress.add_task("Loading Post-Build Plugins", total=1)
            self.plugin_manager.hook.post_build_site(
                site=self,
                settings=self.plugin_manager.plugin_settings,
            )
            progress.update(post_build_task, advance=1)
