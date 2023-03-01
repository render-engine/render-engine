import datetime
import logging
import typing

import dateutil.parser
import more_itertools
import pluggy

from .collection import Collection
from .feeds import RSSFeed
from .page import Page
from .parsers import BasePageParser
from .parsers.markdown import MarkdownPageParser


class BlogPost(Page):
    """Page Like object with slight modifications to work with BlogPosts."""

    list_attrs = ["tags"]
    invalid_attrs = ["slug", "date_published", "date_modified"]

    @property
    def date_modified(self):
        _date_modified = more_itertools.first_true(
            (
                getattr(self, "_date_modified", None),
                getattr(self, "modified_date", None),
                getattr(self, "date", None),
            ),
            default=None,
        )
        if isinstance(_date_modified, datetime.datetime):
            return _date_modified.replace(tzinfo=None)
        return (
            dateutil.parser.parse(_date_modified).replace(tzinfo=None)
            if _date_modified
            else None
        )

    @property
    def date_published(self):
        _date_published = more_itertools.first_true(
            (
                getattr(self, "_date_published", None),
                getattr(self, "publish_date", None),
                getattr(self, "date", None),
            ),
            default=None,
        )
        if isinstance(_date_published, datetime.datetime):
            return _date_published.replace(tzinfo=None)
        return (
            dateutil.parser.parse(_date_published).replace(tzinfo=None)
            if _date_published
            else None
        )


class Blog(Collection):
    """
    Custom :py:class:`collection.Collection` class with archiving enabled, sort by `date_published` by default.

    Todos:
        - Add Support for JSON Feeds
        - Rename the archive items so they are not private
    """

    BasePageParser = MarkdownPageParser
    content_type: typing.Type[BlogPost] = BlogPost
    sort_reverse: bool = True
    sort_by = "date_published"
    has_archive = True
    Feed = RSSFeed
