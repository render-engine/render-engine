import pathlib
from typing import Any, Type

import frontmatter

def parse_content(content: str):
    """Fething content and atttributes from a content_path"""
    p = frontmatter.parse(content)
    return p

class BasePageParser:
    @staticmethod
    def parse_content_path(content_path):
        """
        Fething content from a content_path and set attributes.
        """
        return parse_content(pathlib.Path(content_path).read_text())

    @staticmethod
    def parse_content(content: str):
        """Parses"""
        return parse_content(content)

    @staticmethod
    def parse(content: str, page: "Page"=None):
        """parses the content"""
        return content