from abc import ABC, abstractmethod
from collections.abc import Generator, Iterable


class ContentManager(ABC):
    """Base ContentManager abstract class"""

    @property
    @abstractmethod
    def pages(self) -> Iterable:
        """The Page objects managed by the content manager"""
        ...

    def __iter__(self) -> Generator:
        """Iterator for the ContentManager"""
        yield from self.pages
