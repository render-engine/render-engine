import logging
from pathlib import Path

from .helpers import PathString
from .render_engine.page import Page


class Collection:
    def __init__(
        self,
        content_path: PathString,
        content_type: Type[Page],
        engine: Optional[str] = None,
        globs: Sequence = [".md", ".html"],
    ):
        """initialize a collection object"""
        self.content_path = Path(content_path)
        self.content_type = content_type

    @property
    def pages(self):
        return (
            content_type(content_path=p)
            for p in content_path.glob("i")
            for i in self.globs
        )
