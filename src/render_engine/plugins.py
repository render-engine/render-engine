import logging
from collections import defaultdict
from collections.abc import Iterable
from typing import Any

import pluggy

_PROJECT_NAME = "render_engine"
hook_impl = pluggy.HookimplMarker(project_name=_PROJECT_NAME)
hook_spec = pluggy.HookspecMarker(project_name=_PROJECT_NAME)


class SiteSpecs:
    """
    Hook specifications defining plugin integration points throughout the site build process.

    This class defines the complete plugin API for Render Engine, providing hooks at every
    major stage of the site generation pipeline. Plugins implement these hook methods
    to customize behavior, add features, or modify content during the build process.

    Hook Execution Order:
    1. pre_build_site: Before any site processing begins
    2. pre_build_collection: Before each collection is processed
    3. render_content: Prior to page content rendering
    4. post_render_content: After page content is rendered
    5. post_build_collection: After each collection is processed
    6. post_build_site: After entire site build is complete


    Attributes:
        default_settings (dict[str, Any]): Default configuration for the plugin
    """

    default_settings: dict[str, Any]

    @hook_spec
    def add_default_settings(
        self,
        site,
    ) -> None:
        """Add default settings to the site"""

    @hook_spec
    def pre_build_site(
        self,
        site,
        settings: dict[str, Any],
    ) -> None:
        """Steps Prior to Building the site"""

    @hook_spec
    def post_build_site(
        self,
        site,
        settings: dict[str, Any],
    ) -> None:
        """Build After Building the site"""

    @hook_spec
    def render_content(
        self,
        page,
        settings: dict[str, Any],
        site,
    ) -> None:
        """
        Augments the content of the page before it is rendered as output.
        """

    @hook_spec
    def post_render_content(
        self,
        page,
        settings: dict[str, Any],
        site,
    ) -> None:
        """
        Augments the content of the page before it is rendered as output.
        """

    @hook_spec
    def pre_build_collection(
        self,
        collection,
        site,
        settings: dict[str, Any],
    ) -> None:
        """Steps Prior to Building the collection"""

    @hook_spec
    def post_build_collection(
        self,
        collection,
        site,
        settings: dict[str, Any],
    ) -> None:
        """Build After Building the collection"""


class PluginManager:
    """
    Central coordinator for plugin registration, configuration, and execution.

    The PluginManager handles the complete lifecycle of plugins within Render Engine,
    from registration to execution. It maintains plugin settings, manages the hook
    system, and coordinates plugin execution across the site build pipeline.

    Plugin Hierarchy:
    - Site plugins: Applied to all content (pages and collections)
    - Collection plugins: Override site plugins for specific collections
    - Page plugins: Override collection and site plugins for individual pages
    - Theme plugins: Automatically registered when themes are loaded

    Registration Process:
    1. Plugin classes are registered with the manager
    2. Default settings are merged with user-provided settings
    3. Plugin instances are created and configured
    4. Hook implementations are discovered and registered

    Execution:
    - Hooks are called in order during site build process
    - Plugin settings are passed to each hook execution
    - Exceptions in one plugin don't stop execution of others

    Attributes:
        plugin_settings (dict): Stores configuration for each registered plugin
        _pm: Internal pluggy PluginManager instance
    """

    plugin_settings: dict = defaultdict(dict)

    def __init__(self):
        self._pm = pluggy.PluginManager(project_name=_PROJECT_NAME)
        self._pm.add_hookspecs(SiteSpecs)

    def register_plugin(self, plugin) -> None:
        """Register a plugin with the plugin manager"""
        if self._pm.has_plugin(plugin.__name__):
            logging.info(f"Plugin {plugin} already registered")
            return
        self._pm.register(plugin)

    def unregister_plugin(self, plugin):
        """Unregister a plugin with the plugin manager"""
        if self._pm.has_plugin(plugin.__name__):
            self._pm.unregister(plugin)

    @property
    def plugins(self) -> set[Any]:
        """
        Get the set of registered plugins.

        Returns:
            set: A set containing the registered plugins.
        """
        return self._pm.get_plugins()

    @property
    def hook(self):
        """
        Give access to the hook to run plugins.

        Returns:
            HookRelay: The hook to actually trigger the plugins.
        """
        return self._pm.hook


def handle_plugin_registration(
    plugin_manager: PluginManager,
    plugins: Iterable[tuple[type, dict]] | type,
    current_settings: dict,
):
    """
    Process and register a collection of plugins with their settings.

    This function handles the complex process of plugin registration, supporting
    multiple input formats and properly merging settings hierarchies. It's used
    internally by Site, Collection, and Page classes to manage their plugin ecosystems.

    Input Formats:
    - Single plugin class: MyPlugin
    - Plugin with settings tuple: (MyPlugin, {'setting': 'value'})
    - List of plugins: [MyPlugin1, (MyPlugin2, {'setting': 'value'})]

    Settings Hierarchy (in order of precedence):
    1. User-provided settings (highest priority)
    2. Current settings from parent (site/collection)
    3. Plugin's default_settings (lowest priority)

    Registration Process:
    1. Normalize plugin input to (plugin_class, settings_dict) format
    2. Check for duplicate registration (prevents double-loading)
    3. Register plugin with the internal plugin manager
    4. Merge settings according to hierarchy rules
    5. Store final settings for runtime access

    Args:
        plugin_manager: The PluginManager instance to register plugins with
        plugins: Plugin(s) to register - can be single plugin or iterable
        current_settings: Existing settings from parent context (site/collection)

    Example:
        # Register single plugin
        handle_plugin_registration(pm, MyPlugin, {})

        # Register plugin with settings
        handle_plugin_registration(pm, (MyPlugin, {'enabled': True}), {})

        # Register multiple plugins
        plugins = [MyPlugin1, (MyPlugin2, {'setting': 'value'})]
        handle_plugin_registration(pm, plugins, site_settings)
    """
    for plugin_definition in plugins:
        if isinstance(plugin_definition, tuple):
            if len(plugin_definition) == 2:
                plugin, settings = plugin_definition
            else:
                plugin, settings = plugin_definition[0], dict()
        else:
            plugin, settings = plugin_definition, dict()

        plugin_name = plugin.__name__
        logging.debug(f"Registering Plugin {plugin_name}")
        plugin_manager.register_plugin(plugin)
        default_settings = getattr(plugin, "default_settings", dict())
        logging.debug(
            f"Registering settings: default: {default_settings} "
            f"current: {current_settings.get(plugin_name, dict())} "
            f"overrides: {settings}"
        )
        plugin_manager.plugin_settings[plugin_name] = {
            **default_settings,
            **current_settings.get(plugin_name, dict()),
            **settings,
        }
