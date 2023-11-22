# ruff: noqa: F821

from markdown2 import markdown

from ..base_parsers import BasePageParser

__all__ = ["BasePageParser"]


class MarkdownPageParser(BasePageParser):
    """
    Uses the Base Parse to frontmatter parser the attrs
    Markdown2 then parses the content
    """

    @staticmethod
    def parse(content: str, page: "Page") -> str:
        """Parses the content with the parser"""
        extras = getattr(page, "parser_extras", {})
        markup = markdown(content, extras=extras.get("markdown_extras", []))
        return markup
