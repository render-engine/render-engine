"""
The Archive is the Page object used by the collection that focuses on presenting Page objects.
"""
import typing

from .page import Page, _route


class Archive(Page):
    """Custom Page object used to make archive pages"""

    def __init__(
        self,
        pages: list[Page],
        title: str,
        template: str | None,
        routes: list[_route],
        archive_index: int = 0,
        num_of_pages: int = 1,
        **kwargs,
    ) -> None:
        """Create a `Page` object for the pages in the collection"""
        super().__init__()
        self.pages = pages
        self.template = template
        self.routes = routes
        self.title = title

        if num_of_pages > 1:
            self.slug = f"{self.slug}{archive_index}"

        for key, val in kwargs.items():
            setattr(self, key, val)
