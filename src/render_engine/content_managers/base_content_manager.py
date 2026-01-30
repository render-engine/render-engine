from abc import ABC, abstractmethod
from collections.abc import Generator, Iterable
from pathlib import Path


class ContentManager(ABC):
    """Base ContentManager abstract class"""

    @property
    @abstractmethod
    def pages(self) -> Iterable:
        """The Page objects managed by the content manager"""
        ...

    @pages.setter
    @abstractmethod
    def pages(self, value: Iterable):
        pass

    def __len__(self):
        return len(list(self.pages))

    def __iter__(self) -> Generator:
        """Iterator for the ContentManager"""
        yield from self.pages

    @abstractmethod
    def create_entry(
        self,
        filepath: Path | None = None,
        editor: str | None = None,
        metadata: dict | None = None,
        content: str | None = None,
    ):
        """Create a new entry"""
        pass

    def find_entry(self, **kwargs):
        """
        Find an entry

        :param kwargs: List of attributes to search by
        :return: Page if it was found otherwise None
        """
        for page in self:
            if all(getattr(page, attr, None) == value for attr, value in kwargs.items()):
                return page
        return None

    @abstractmethod
    def update_entry(self, *, page, **kwargs):
        """Update an entry"""
        pass
