import pluggy

_PROJECT_NAME = "render_engine"
hook_impl = pluggy.HookimplMarker(project_name=_PROJECT_NAME)
hook_spec = pluggy.HookspecMarker(project_name=_PROJECT_NAME)


class SiteSpecs:
    """Plugin hook specifications for the Site class"""

    @hook_spec
    def pre_build_site(self, site: "Site") -> None:
        """Steps Prior to Building the site"""

    @hook_spec
    def post_build_site(self, site: "Site") -> None:
        """Build After Building the site"""

    @hook_spec
    def pre_render_content(page: "Page") -> str:
        """
        Augments the content of the page before it is rendered as output.
        """

    @hook_spec
    def pre_build_collection(self, collection: "Collection") -> None:
        """Steps Prior to Building the collection"""

    @hook_spec
    def post_build_collection(self, site: "Site") -> None:
        """Build After Building the collection"""

    @hook_spec
    def pre_build_collection_pages(self, page: "Page") -> None:
        """Steps Prior to Building the collection pages"""

    @hook_spec
    def post_build_collection_pages(self, site: "Site") -> None:
        """Build After Building the collection pages"""
