"""
The Archive is the Page object used by the collection that focuses on presenting Page objects.
"""
import pathlib
import typing

import jinja2
import pluggy

from .page import Page


class Archive(Page):
    """
    ???+ Warning "Not Directly Used"
        The Archive object is not meant to be used directly. It is used by the [Collection][src.render_engine.Collection] object. Attributes can be used to customize the [archive_template][src.render_engine.collection.Collection].

    Custom [`Page`][src.render_engine.page.Page] object used to show all the pages in a [Collection][src.render_engine.Collection].

    Parameters:
        pm: The [Plugin Manager](https://pluggy.readthedocs.io/en/stable/api_reference.html#pluggy.PluginManager) object to include
        pages: The list of pages to include in the archive
        title: The title of the archive
        template: The template to use for the archive
        routes: The routes for where the archive page should be generated
        archive_index: The index of the page in the series of archive pages
        num_of_pages: The total number of pages in the series of archive pages
    """

    def __init__(
        self,
        pm: pluggy.PluginManager,
        pages: list[Page],
        title: str,
        template: str | jinja2.Template,
        routes: list[str | pathlib.Path],
        archive_index: int = 0,
        num_of_pages: int = 1,
        **kwargs,
    ) -> None:
        super().__init__(pm=pm)
        self.pages = pages
        self.template = template
        self.routes = routes
        self.title = title

        if num_of_pages > 1:
            self.slug = f"{self.slug}{archive_index}"

        for key, val in kwargs.items():
            setattr(self, key, val)
