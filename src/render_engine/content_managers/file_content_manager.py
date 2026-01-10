import subprocess
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

    def __len__(self):
        return len(list(self.pages))

    def create_entry(
        self,
        filepath: Path = None,
        editor: str = None,
        metadata: dict = None,
        content: str = None,
        update: bool = False,
    ) -> str:
        """
        Create a new entry for the Collection

        :param filepath: Path object for the new entry
        :param editor: Editor to open to edit the entry.
        :param content: The content for the entry
        :param metadata: Metadata for the new entry
        :param update: Allow overwriting the existing file
        """
        if not filepath:
            raise ValueError("filepath needs to be specified.")

        if not update and filepath.exists():
            raise RuntimeError(f"File at {filepath} exists and update is disabled.")

        parsed_content = self.collection.Parser.create_entry(content=content, **metadata)
        filepath.write_text(parsed_content)
        if editor:
            subprocess.run([editor, filepath])
        return f"New entry created at {filepath} ."

    def update_entry(self, page, *, content: str = None, **kwargs) -> str:
        """
        Update an entry

        :param page: Page object to update
        :param content: Content for the updated page
        :param kwargs: Attributes to be included in the updated page
        :return: String indicating that the page was updated.
        """
        self.create_entry(filepath=page.content_path, metadata=kwargs, content=content, update=True)
        if self._pages:
            self._pages = [
                existing_page for existing_page in self._pages if page.content_path != existing_page.content_path
            ]
            self._pages.append(self.collection.get_page(page.content_path))
        return f"Entry at {page.content_path} updated."
