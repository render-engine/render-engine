import logging
import typing
from collections import defaultdict

import pluggy

_PROJECT_NAME = "render_engine"
hook_impl = pluggy.HookimplMarker(project_name=_PROJECT_NAME)
hook_spec = pluggy.HookspecMarker(project_name=_PROJECT_NAME)


class SiteSpecs:
    """Plugin hook specifications for the Site class"""

    default_settings: dict[str, typing.Any]

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
        settings: dict[str, typing.Any],
    ) -> None:
        """Steps Prior to Building the site"""

    @hook_spec
    def post_build_site(
        self,
        site,
    ) -> None:
        """Build After Building the site"""

    @hook_spec
    def render_content(
        self,
        page,
        settings: dict[str, typing.Any],
    ) -> None:
        """
        Augments the content of the page before it is rendered as output.
        """

    @hook_spec
    def post_render_content(
        self,
        page,
        settings: dict[str : typing.Any],
        site,
    ) -> None:
        """
        Augments the content of the page before it is rendered as output.
        """

    @hook_spec
    def pre_build_collection(
        self,
        collection,
        settings: dict[str, typing.Any],
    ) -> None:
        """Steps Prior to Building the collection"""

    @hook_spec
    def post_build_collection(
        self,
        site,
        settings: dict[str, typing.Any],
    ) -> None:
        """Build After Building the collection"""


class PluginManager:
    plugin_settings = defaultdict(dict)

    def __init__(self):
        self._pm = pluggy.PluginManager(project_name=_PROJECT_NAME)
        self._pm.add_hookspecs(SiteSpecs)

    def register_plugin(self, plugin) -> None:
        """Register a plugin with the site"""
        if self._pm.has_plugin(plugin.__name__):
            logging.info(f"Plugin {plugin} already registered")
            return
        self._pm.register(plugin)

    @property
    def plugins(self) -> set[typing.Any]:
        return self._pm.get_plugins()
