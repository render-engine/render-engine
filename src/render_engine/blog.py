import datetime
import typing

import more_itertools
import pendulum

from .collection import Collection
from .feeds import RSSFeed
from .page import Page


class BlogPost(Page):
    """Page Like object with slight modifications to work with BlogPosts."""

    list_attrs = ["tags"]
    feed = RSSFeed

    def __init__(self, **kwargs):
        """
        checks published options and accepts the first that is listed

        Attributes:
            date : pendulum.datetime
                date parsed in datetime format. usesul for sorting and things
            date_published : str
                date formated for `RSSFeed`
            date_friendly : str
                an easy to read string version of the date
        """

        super().__init__(**kwargs)
        date_published = more_itertools.first_true(
            (
                getattr(self, "date_published", None),
                getattr(self, "publish_date", None),
                getattr(self, "date", None),
            )
        )

        if isinstance(date_published, datetime.datetime):
            self.date_published = pendulum.instance(date_published).set(
                tz=pendulum.local_timezone()
            )  # TODO: fixes issue with datetimes parsed by frontmatter being converted to datetimes instead of str
        else:
            self.date_published = pendulum.parse(date_published, strict=False).set(
                tz=pendulum.local_timezone()
            )

        date_modified = more_itertools.first_true(
            (
                getattr(self, "date_modified", None),
                getattr(self, "modified_date", None),
            ),
            default=None,
        )

        if not date_modified:
            self.date_modified = self.date_published

        else:
            self.date_modified = pendulum.parse(date_modified, strict=False).set(
                tz=pendulum.local_timezone()
            )

        self.date_friendly = self.date_modified.format("MMM DD, YYYY HH:mm A")


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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._feed = getattr(self, "feed", RSSFeed)(
            title=f"{self.SITE_TITLE} {self.title}", pages=self.pages
        )
