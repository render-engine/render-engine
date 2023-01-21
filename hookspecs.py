import pluggy

from render_engine import _PROJECT_NAME
from render_engine.page import Page
from render_engine.site import Site

hook_spec = pluggy.HookspecMarker(project_name=_PROJECT_NAME)


class SiteSpecs:
    """Plugin hook specifications for the Site class"""

    @hook_spec
    def pre_build_site(self, site: Site) -> None:
        """Steps Prior to Building the site"""
        pass

    @hook_spec
    def post_build_site(self, site: Site) -> None:
        """Build After Building the site"""
        pass
