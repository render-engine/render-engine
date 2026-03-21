import pathlib
from typing import Any

import frontmatter


def parse_content(content: str) -> tuple[dict, str]:
    """Fetching content and atttributes from a content_path"""
    p = frontmatter.parse(content)
    return p


class BasePageParser:
    """
    The default Parser for Page objects.
    This yields attributes and content using frontmatter.
    The content is not modified.
    """

    @staticmethod
    def parse_content_path(content_path: str | pathlib.Path) -> tuple[dict, str]:
        """
        Fetches content from `Page.content_path` and sets attributes.

        This is a separate method so that it can be overridden by subclasses.

        params:
            content_path:
                The path to the file that will be used to generate the Page's `content`.
                Should be a valid path to a file or a url.
        """
        return parse_content(pathlib.Path(content_path).read_text())

    @staticmethod
    def parse_content(content: str) -> tuple[dict, str]:
        """
        Fetches content from `Page.content` and returns attributes and content.

        This is a separate method so that it can be overridden by subclasses.

        params:
            content:
                The path to the file that will be used to generate the Page's `content`.
                Should be a valid path to a file or a url.
        """

        return parse_content(content)

    @staticmethod
    def parse(
        content: str,
        extras: dict[str, Any] | None = None,
    ) -> str:
        """
        Parses content to be rendered into HTML

        In the base parser, this returns the content as is.

        params:
            content: content to be rendered into HTML
            extras: dictionary with extras to augment attributes
        """
        return content

    @staticmethod
    def create_entry(*, content: str = "Hello World", **kwargs) -> str:
        """
        Writes the content type that would be parsed to the content_path.
        """

        post = frontmatter.Post(content)

        for key, val in kwargs.items():
            post[key] = val

        return frontmatter.dumps(post)
