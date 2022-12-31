from abc import ABC, abstractmethod
from typing import Type


class BasePageParser(ABC):
    def __init__(self, page: "Page", **kwargs):
        for value in self.configuration_values:
            setattr(self, value, kwargs.get(value, None))

    @property
    @abstractmethod
    def configuration_values(self) -> list[str]:
        """The configuration values that the parser needs"""
        pass

    @staticmethod
    @abstractmethod
    def attrs_from_content_path(self, content_path):
        """
        Fething content from a content_path and set attributes.
        """
        pass

    @staticmethod
    @abstractmethod
    def attrs_from_content(self, content_path):
        """
        Fething content from a content_path and set attributes.
        """
        pass

    @abstractmethod
    def parse(self, content):
        """Convert the raw_content into HTML or the finalized format"""
        pass


class BaseCollectionParser(ABC):
    PageParser: Type[BasePageParser]

    def __init__(self, collection: "Collection"):
        content_type = kwargs.get("content_type", None)
        for value in self.configuration_values:
            if attr := getattr(collection, value, None):
                setattr(self, attr, collection.value)

        for item, value in collection.collection_vars.items():
            setattr(self, item, value)

    @property
    @abstractmethod
    def configuration_values(self) -> list[str]:
        """The configuration values that the parser needs"""
        return ["routes", "collection_vars"]

    @staticmethod
    @abstractmethod
    def attrs_from_iter_path(content_path):
        """
        Fething content from a content_path and set attributes.
        """
        pass

    @staticmethod
    @abstractmethod
    def attrs_from_content(content_path):
        """
        Fething content from a content_path and set attributes.
        """
        pass

    @abstractmethod
    def parse(self, content: str, content_path: str):
        """Generate Pages from the iter_path or content"""
        pass
