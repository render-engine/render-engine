from pathlib import Path

from .page import Page

class Collection:
    template = None
    engine = None
    routes = ['']

    def __init__(self):
        """initialize a collection object"""
        self.content_type = Page
        self.content_path = Path('content')
        self.includes = ["*.md", "*.html"]

    @property
    def pages(self):
        pages = []

        for i in self.includes:

            for p in self.content_path.glob(i):
                pages.append(self.content_type(content_path=p))

        return pages
