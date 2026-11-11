from markdown2 import markdown
from typing import Any

from .base_parsers import BasePageParser


class MarkdownPageParser(BasePageParser):
    """
    Uses the BasePageParser to frontmatter parser the attrs
    Markdown2 then parses the content
    """

    @staticmethod
    def parse(content: str, extras: dict[str, Any] | None = None) -> str:
        """Parses the content with the parser"""
        return markdown(
            content,
            extras=extrasMPP.get("markdown_extras", []) if extras else [],
        )
