import logging
import typing
from pathlib import Path

from .page import Page


class Collection:
    engine = ''
    page_content_type = Page
    content_path = "content"
    template = "page.html"
    includes = ["*.md", "*.html"]
    routes = ['']

    @property
    def pages(self) -> typing.List[typing.Type[Page]]:
        pages = []

        for i in self.includes:
            for _file in Path(self.content_path).glob(i):
                page = self.page_content_type(content_path=_file)
                page.routes = self.routes
                page.template = self.template
                pages.append(page)

        return pages
