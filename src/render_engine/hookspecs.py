# ruff: noqa: F821

import warnings
from typing import Any

import pluggy

from render_engine.collection import Collection
from render_engine.page import Page
from render_engine.site import Site

_PROJECT_NAME = "render_engine"
hook_impl = pluggy.HookimplMarker(project_name=_PROJECT_NAME)
warnings.warn(
    "`render_engine.hookspecs` will be deprecated in version 2024.3.1,  Please use `render_engine.plugins` instead.",
    DeprecationWarning,
)
hook_spec = pluggy.HookspecMarker(project_name=_PROJECT_NAME)


class SiteSpecs:
    """
    `hookspecs.SiteSpecs` will be deprecated in version 2024.3.1,  Please use `plugins.SiteSpecs` instead.

    Plugin hook specifications for the Site class.

    This class defines the hook specifications for various operations related to the Site class.
    These hooks can be implemented by plugins to customize the behavior of the site building process.
    """

    default_settings: dict[str, Any]

    @hook_spec
    def add_default_settings(
        self,
        site: Site,
    ) -> None:
        """Add default settings to the site"""

    @hook_spec
    def pre_build_site(
        self,
        site: Site,
        settings: dict[str, Any],
    ) -> None:
        """Steps Prior to Building the site"""

    @hook_spec
    def post_build_site(
        self,
        site: Site,
    ) -> None:
        """Build After Building the site"""

    @hook_spec
    def render_content(
        self,
        page: Page,
        settings: dict[str, Any],
    ) -> None:
        """
        Augments the content of the page before it is rendered as output.
        """

    @hook_spec
    def post_render_content(
        self,
        page: Page,
        settings: dict[str, Any],
        site: "Site",
    ) -> None:
        """
        Augments the content of the page before it is rendered as output.
        """

    @hook_spec
    def pre_build_collection(
        self,
        collection: Collection,
        settings: dict[str, Any],
    ) -> None:
        """Steps Prior to Building the collection"""

    @hook_spec
    def post_build_collection(
        self,
        site: "Site",
        settings: dict[str, Any],
    ) -> None:
        """Build After Building the collection"""
