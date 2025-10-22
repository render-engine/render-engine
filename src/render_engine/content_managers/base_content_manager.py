from abc import ABC, abstractmethod
from collections.abc import Iterable


class ContentManager(ABC):
    """Base ContentManager abstract class"""

    @property
    @abstractmethod
    def pages(self) -> Iterable:
        """The pages managed by the content manager"""
        ...

    def __iter__(self):
        """Iterator for the ContentManager"""
        yield from self.pages
