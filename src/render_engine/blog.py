import datetime
import logging
import typing

import more_itertools
import pendulum

from .collection import Collection
from .feeds import RSSFeed
from .page import Page
from .parsers import BasePageParser
from .parsers.markdown import MarkdownPageParser


class BlogPost(Page):
    """Page Like object with slight modifications to work with BlogPosts."""

    list_attrs = ["tags"]

    def __init__(
        self,
        content: str | None = None,
        content_path: str | None = None,
        Parser: typing.Type["BasePageParer"] = MarkdownPageParser,
    ):
        """
        checks published options and accepts the first that is listed

        Attributes:
            date : pendulum.datetime
            date_published : str
            date_friendly : str
        """

        super().__init__(content=content, content_path=content_path, Parser=Parser)

        # protect date_published, modified_date, or date_friendly in the frontmatter

        protected_date_attrs = ["modified_date", "date_published", "date_friendly"]
        self.date_friendly = self.date_modified.format("MMM DD, YYYY HH:mm A")

    @property
    def date_modified(self):
        date_modified = more_itertools.first_true(
            (
                getattr(self, "_date_modified", None),
                getattr(self, "modified_date", None),
            ),
            default=None,
        )

        if not date_modified:
            self._date_modified = self.date_published

        else:
            self._date_modified = pendulum.parse(date_modified, strict=False).set(
                tz=pendulum.local_timezone()
            )

        return self._date_modified

    @property
    def date_published(self):
        date_published = more_itertools.first_true(
            (
                getattr(self, "_date_published", None),
                getattr(self, "publish_date", None),
                getattr(self, "date", None),
            )
        )

        if isinstance(date_published, datetime.datetime):
            return pendulum.instance(date_published).set(tz=pendulum.local_timezone())

        elif date_published:
            return pendulum.parse(date_published, strict=False).set(
                tz=pendulum.local_timezone()
            )

        else:
            raise ValueError("No Date Published Found")

        return self._date_published


class Blog(Collection):
    """
    Custom :py:class:`collection.Collection` class with archiving enabled, sort by `date_published` by default.

    Todos:
        - Add Support for JSON Feeds
        - Rename the archive items so they are not private
    """

    content_type: typing.Type[BlogPost] = BlogPost
    sort_reverse: bool = True
    sort_by = "date_published"
    has_archive = True
    feed = RSSFeed
