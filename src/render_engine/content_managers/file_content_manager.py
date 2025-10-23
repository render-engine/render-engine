from collections.abc import Iterable
from pathlib import Path

from more_itertools import flatten

from render_engine.content_managers import ContentManager


class FileContentManager(ContentManager):
    """Content manager for content stored on the file system as individual files"""

    def __init__(
        self,
        content_path: Path | str,
        collection,
        include_suffixes: Iterable[str] = ("*.md", "*.html"),
        **kwargs,
    ):
        self.content_path = content_path
        self.include_suffixes = include_suffixes
        self.collection = collection
        self._pages = None

    def iter_content_path(self):
        """Iterate through in the collection's content path."""
        return flatten([Path(self.content_path).glob(suffix) for suffix in self.include_suffixes])

    @property
    def pages(self) -> Iterable:
        if self._pages is None:
            self._pages = [self.collection.get_page(page) for page in self.iter_content_path()]
        yield from self._pages

    @pages.setter
    def pages(self, value: Iterable):
        self._pages = value
