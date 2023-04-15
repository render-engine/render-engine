from .collection import Collection
from .feeds import RSSFeed
from .page import Page
from .parsers.markdown import MarkdownPageParser


class BlogPost(Page):
    """Page Like object with slight modifications to work with BlogPosts."""
    list_attrs = ["tags"]
    invalid_attrs = ["slug"]


class Blog(Collection):
    """
    Custom :py:class:`collection.Collection` class with archiving enabled, sort by `date` by default.

    Todos:
        - Add Support for JSON Feeds
        - Rename the archive items so they are not private
    """

    BasePageParser = MarkdownPageParser
    content_type: BlogPost = BlogPost
    sort_reverse: bool = True
    sort_by = "date"
    has_archive = True
    Feed = RSSFeed
