from pathlib import Path

import logging

from .page import Page

class Collection:
    template = None
    engine = None
    content_type = Page
    content_path = 'content'
    includes = ["*.md", "*.html"]
    routes = ['']

    @property
    def pages(self):
        pages = []

        for i in self.includes:
            for p in Path(self.content_path).glob(i):
                pages.append(self.content_type(content_path=p))

        return pages
