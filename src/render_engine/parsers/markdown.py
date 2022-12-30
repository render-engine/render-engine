import pathlib
from typing import Any

import frontmatter
from markdown2 import markdown

from .base_parsers import BasePageParser


def _attrs_from_content(content) -> tuple[dict[str, Any], str | None]:
    """fetches the content"""
    return frontmatter.parse(content)


class MarkdownParser(BasePageParser):
    markdown_extras: list[str] | None

    @property
    def configuration_values(self) -> list[str]:
        return ["markdown_extras"]

    def markup_from_content_path(self, content_path):
        """Parses the content from the content path"""
        content = pathlib.Path(content_path).read_text()
        self.parse(content)

    @staticmethod
    def attrs_from_content_path(content_path) -> tuple[dict[str, Any], str | None]:
        """fetches the content"""
        content = pathlib.Path(content_path).read_text()
        return _attrs_from_content(content)

    @staticmethod
    def attrs_from_content(content) -> tuple[dict[str, Any], str | None]:
        """fetches the content"""
        return _attrs_from_content(content)

    def parse(self, content):
        """Parses the content with the parser"""
        return markdown(content, extras=self.markdown_extras or [])
