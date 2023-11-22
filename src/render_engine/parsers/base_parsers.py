# ruff: noqa: F821

import pathlib

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
    def parse_content_path(content_path: str) -> tuple[dict, str]:
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
    def parse(content: str, page: "Page" = None):
        """
        Parses content to be rendered into HTML

        In the base parser, this returns the content as is.

        params:
            content: content to be rendered into HTML
            page: Page object to gain access to attributes
        """
        return content
