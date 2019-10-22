from pathlib import Path

from .render_engine import Page


class Collection:
    def __init__(self):
        """initialize a collection object"""
        self.content_type = Page
        self.content_path = Path('content')
        self.pages = {}
        self.includes = ["*.md", "*.html"]

    @property
    def pages(self):
        return (
                self.content_type(content_path=p)
                for i in self.includes
                for p in self.content_path.glob(i)
            )
