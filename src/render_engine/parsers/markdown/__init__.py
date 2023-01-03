import itertools
import pathlib
from typing import Any, Type

import frontmatter
from markdown2 import markdown

from ..base_parsers import BasePageParser


def _attrs_from_content(content):
    """fetches the content"""
    return frontmatter.parse(content)


class MarkdownPageParser(BasePageParser):
    configuration_values = ["markdown_extras"]

    @staticmethod
    def markup(page, content) -> str:
        """Parses the content with the parser"""
        markup = markdown(content, extras=getattr(page, "markdown_extras", None))
        return markup
