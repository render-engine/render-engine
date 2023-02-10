from typing import Any, Type

import frontmatter
from markdown2 import markdown

from ..base_parsers import BasePageParser


class MarkdownPageParser(BasePageParser):
    configuration_values = ["markdown_extras"]

    @staticmethod
    def markup(content: str, page: "Page") -> str:
        """Parses the content with the parser"""
        markup = markdown(content, extras=getattr(page, "markdown_extras", None))
        return markup
