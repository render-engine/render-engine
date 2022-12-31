import pathlib
from typing import Any, Type

import frontmatter
from markdown2 import markdown

from ..base_parsers import BaseCollectionParser, BasePageParser


def _attrs_from_content(content):
    """fetches the content"""
    return frontmatter.parse(content)


class MarkdownPageParser(BasePageParser):
    markdown_extras: list[str]

    @property
    def configuration_values(self) -> list[str]:
        """Returns the configuration values that are used by the parser"""
        return ["markdown_extras"]

    @staticmethod
    def attrs_from_content_path(content_path):
        """fetches the content"""
        content = pathlib.Path(content_path).read_text()
        return _attrs_from_content(content)

    @staticmethod
    def attrs_from_content(content):
        """fetches the content"""
        return _attrs_from_content(content)

    def parse(self, content) -> str:
        """Parses the content with the parser"""
        return markdown(content, extras=getattr(self, "markdown_extras", []))


class MarkdownCollectionParser(BaseCollectionParser):
    path_includes: list[str] = ["*.md", "*.html"]
    content_type: Type["Page"]
    PageParser = MarkdownPageParser

    @property
    def configuration_values(self) -> list[str]:
        config = super().configuration_values
        config.extend(
            [
                "path_inclues",
                "markdown_extras",
                "content_type",
                "engine",
                "template",
                "subcollections",
                "subcollection_template",
            ]
        )
        return config

    @staticmethod
    def attrs_from_content(content_path):
        """You cannot fetch attributes from a folder"""
        pass

    @staticmethod
    def attrs_from_iter_path(content_path):
        """You cannot fetch attributes from a folder"""
        pass

    def parse(self, content: str | None = None, content_path: str | None = None) -> Any:
        """Parses the content with the parser"""
        if content_path:
            page_groups = map(
                lambda pattern: pathlib.Path(self.content_path).glob(pattern),
                self.path_includes,
            )
            return [
                self.content_type.from_collection_parser(
                    engine=getattr(self, "engine", None),
                    content_path=page_path,
                    template=self.template,
                    routes=self.routes,
                    subcollections=getattr(self, "subcollections", []),
                    subcollection_template=getattr(self, "subcollection_template", []),
                    **self.collection_vars,
                )
                for page_path in itertools.chain.from_iterable(page_groups)
            ]

        if content:
            raise AttributeError(
                "Cannot parse content from a collection with this parser."
            )
