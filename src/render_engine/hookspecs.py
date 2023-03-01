import pluggy

_PROJECT_NAME = "render_engine"
hook_impl = pluggy.HookimplMarker(project_name=_PROJECT_NAME)
hook_spec = pluggy.HookspecMarker(project_name=_PROJECT_NAME)


def register_plugins(plugins):
    """Register the plugins with the plugin manager"""
    pm = pluggy.PluginManager(project_name=_PROJECT_NAME)
    pm.add_hookspecs(SiteSpecs)

    for plugin in plugins:
        pm.register(plugin)
    return pm


class SiteSpecs:
    """Plugin hook specifications for the Site class"""

    @hook_spec
    def pre_build_site(self, site: "Site") -> None:
        """Steps Prior to Building the site"""

    @hook_spec
    def post_build_site(self, site: "Site") -> None:
        """Build After Building the site"""

    @hook_spec
    def render_content(Page: "page"):
        """
        Augments the content of the page before it is rendered as output.
        """

    @hook_spec
    def pre_build_collection(self, collection: "Collection") -> None:
        """Steps Prior to Building the collection"""

    @hook_spec
    def post_build_collection(self, site: "Site") -> None:
        """Build After Building the collection"""
