import datetime
import os
import zoneinfo
from typing import Any

from render_engine_markdown import MarkdownPageParser

from .collection import Collection


class Blog(Collection):
    """
    Custom :py:class:`collection.Collection` class with archiving enabled, sort by `date` by default.

    This class represents a blog collection in the render engine. It inherits from the `Collection` class.

    Attributes:
        BasePageParser (class): The base page parser class to use for parsing blog pages.
            Defaults to `MarkdownPageParser`.
        sort_reverse (bool): Flag indicating whether to sort the blog posts in reverse order. Defaults to `True`.
        sort_by (str): The attribute to sort the blog posts by. Defaults to `"date"`.
        has_archive (bool): Flag indicating whether the blog has an archive. Defaults to `True`.
        Feed (class): The feed class to use for generating RSS feeds. Defaults to `RSSFeed`.

    Methods:
        latest(count: int) -> list[Collection]: Returns the latest blog posts from the collection.

    #TODO:
        - Add Support for JSON Feeds
        - Rename the archive items so they are not private
    """

    BasePageParser = MarkdownPageParser
    sort_reverse: bool = True
    sort_by = "date"
    has_archive = True

    @staticmethod
    def _metadata_attrs(**kwargs) -> dict[str, Any]:
        timezone = zoneinfo.ZoneInfo(
            os.environ.get(
                "RENDER_ENGINE_DEFAULT_TIMEZONE",
                "UTC",
            )
        )
        return {
            **Collection._metadata_attrs(),
            **{"date": datetime.datetime.now(tz=timezone)},
        }

    def latest(self, count: int = 1) -> list[Collection]:
        """Get the latest post from the collection."""
        latest_pages = list(
            sorted(
                self.__iter__(),
                key=lambda x: getattr(x, self.sort_by),
                reverse=self.sort_reverse,
            )
        )[0:count]
        return latest_pages
