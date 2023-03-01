"""
The Archive is the Page object used by the collection that focuses on presenting Page objects.
"""
import pathlib
import jinja2

from .page import BasePage 


class Archive(BasePage):
    """
    ???+ Warning "Not Directly Used"
        The Archive object is not meant to be used directly. 
        It is used by the [Collection][src.render_engine.Collection] object. 
        Attributes can be used to customize the 
        [archive_template][src.render_engine.collection.Collection].

    Custom [`Page`][src.render_engine.page.Page] object used to show all the pages in a [Collection][src.render_engine.Collection].

    Parameters:
        pages: The list of pages to include in the archive
        title: The title of the archive
        template: The template to use for the archive
        routes: The routes for where the archive page should be generated
        archive_index: The index of the page in the series of archive pages
        num_of_pages: The total number of pages in the series of archive pages
    """

    def __init__(
        self,
        title: str,
        pages: list[BasePage],
        template: str | jinja2.Template,
        routes: list[str | pathlib.Path],
        archive_index: int = 0,
        num_archive_pages: int = 1,
    ) -> None:
        super().__init__()
        self.pages = pages
        self.template = template
        self.routes = routes
        self.title = title

        if num_archive_pages > 1:
            self.slug = f"{self._slug}{archive_index}"
