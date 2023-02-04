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
        template: str,
        routes: list[_route],
        **kwargs,
    ) -> None:
        """Create a `Page` object for the pages in the collection"""
        super().__init__()
        self.pages = pages
        self.template = template
        self.routes = routes
        for key, val in kwargs.items():
            setattr(self, key, val)
