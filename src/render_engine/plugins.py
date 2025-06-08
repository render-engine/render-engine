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
    Plugin hook specifications for the Site class.

    This class defines the hook specifications for various stages of site building and rendering.
    Each hook method represents a specific stage and can be implemented by plugins to customize the behavior.

    Attributes:
        default_settings (dict[str, Any]): The default settings for the site.

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
    Manages the plugins for the site.

    Attributes:
        plugin_settings (dict): A dictionary that stores the settings for each plugin.
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
    Register plugins to a plugin_manager

    :param plugin_manager: The plugin manager to register the plugins
    :param plugins: List of tuples containing the plugin and settings:
        [(Plugin1, {}), (Plugin2, {'setting': 'updated'})]
    :param current_settings: Dictionary of current settings
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
