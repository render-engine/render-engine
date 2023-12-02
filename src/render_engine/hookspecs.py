# ruff: noqa: F821

import typing

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
        site: "Site",
    ) -> None:
        """Add default settings to the site"""

    @hook_spec
    def pre_build_site(
        self,
        site: "Site",
        settings: dict[str, typing.Any],
    ) -> None:
        """Steps Prior to Building the site"""

    @hook_spec
    def post_build_site(
        self,
        site: "Site",
        settings: dict[str, typing.Any],
    ) -> None:
        """Build After Building the site"""

    @hook_spec
    def render_content(
        self,
        page: "page",
        settings: dict[str, typing.Any],
    ) -> None:
        """
        Augments the content of the page before it is rendered as output.
        """

    @hook_spec
    def post_render_content(
        self,
        page: "page",
        settings: dict[str : typing.Any],
        site: "Site",
    ) -> None:
        """
        Augments the content of the page before it is rendered as output.
        """

    @hook_spec
    def pre_build_collection(
        self,
        collection: "Collection",
        settings: dict[str, typing.Any],
    ) -> None:
        """Steps Prior to Building the collection"""

    @hook_spec
    def post_build_collection(
        self,
        site: "Site",
        settings: dict[str, typing.Any],
    ) -> None:
        """Build After Building the collection"""
