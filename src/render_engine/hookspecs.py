import pluggy

from render_engine.page import Page

_PROJECT_NAME = "render_engine"
hook_impl = pluggy.HookimplMarker(project_name=_PROJECT_NAME)
hook_spec = pluggy.HookspecMarker(project_name=_PROJECT_NAME)


class SiteSpecs:
    """Plugin hook specifications for the Site class"""

    @hook_spec
    def pre_build_site(self, site: "Site") -> None:
        """Steps Prior to Building the site"""
        pass

    @hook_spec
    def post_build_site(self, site: "Site") -> None:
        """Build After Building the site"""
        pass
