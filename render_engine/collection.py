import logging
from pathlib import Path

from .page import Page


class Collection:
    content_type = Page
    content_path = "content"
    engine = None
    template = "page.html"
    includes = ["*.md", "*.html"]
    routes = [""]

    @property
    def pages(self):
        pages = []

        for i in self.includes:
            for p in Path(self.content_path).glob(i):
                page = self.content_type(content_path=p)

                if self.template:
                    page.template = self.template

                pages.append(page)

        return pages
