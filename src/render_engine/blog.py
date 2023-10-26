from .collection import Collection
from .feeds import RSSFeed
from .parsers.markdown import MarkdownPageParser


class Blog(Collection):
    """
    Custom :py:class:`collection.Collection` class with archiving enabled, sort by `date` by default.

    TODOS:
        - Add Support for JSON Feeds
        - Rename the archive items so they are not private
    """

    BasePageParser = MarkdownPageParser
    sort_reverse: bool = True
    sort_by = "date"
    has_archive = True
    Feed = RSSFeed

    def latest(self, count: int = 1):
        """Get the latest post from the collection."""
        latest_pages = list(sorted(self.__iter__(), key=lambda x: getattr(x, self.sort_by), reverse=self.sort_reverse))[
            0:count
        ]
        return latest_pages
