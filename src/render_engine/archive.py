import pathlib

import jinja2

from render_engine.plugins import PluginManager

from .page import BasePage


class Archive(BasePage):
    """
    The Archive is a [Page][src.render_engine.page.Page] object used by the collection
    that focuses on presenting the Collection's pages.

    Parameters:
        pages: The list of pages to include in the archive
        title: The title of the archive
        template: The template to use for the archive
        routes: The routes for where the archive page should be generated
        archive_index: The index of the page in the series of archive pages
        num_of_pages: The total number of pages in the series of archive pages

    !!! Warning "Not Directly Used"
        The Archive object is not meant to be used directly.
        It is used by the [Collection][src.render_engine.Collection] object.
        Attributes can be used to customize.
    """

    def __init__(
        self,
        title: str,
        pages: list[BasePage],
        template: str | jinja2.Template,
        routes: list[str | pathlib.Path],
        archive_index: int = 0,
        num_archive_pages: int = 1,
        plugin_manager: PluginManager | None = None,
    ) -> None:
        super().__init__()
        self.archive_index = archive_index

        if archive_index:
            self.slug = f"{self._slug}{archive_index}"
        self.pages = pages
        self.plugin_manager = plugin_manager
        self.routes = routes
        self.template = template
        self.title = title
