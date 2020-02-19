import logging
import typing

import pendulum
from more_itertools import flatten

from .collection import Collection
from .page import Page
from .feeds import RSSFeedItem, RSSFeed, RSSFeedEngine
from .site import Site


class BlogPost(Page):
    """Page Like Object with slight modifications to work with BlogPosts"""

    template: str = "blog_post.html"
    publish_options: typing.List[str] = [
        "date_published",
        "date",
        "publish_date",
        "date_modified",
        "modified_date",
    ]

    def __init__(self, **kwargs):
        """checks published options and accepts the first that is listed"""
        super().__init__(**kwargs)
        for option in self.publish_options:
            if hasattr(self, option):
                date_object = getattr(self, option)
                self.sortable_date = pendulum.parse(date_object, strict=False)
                self.sortable_date = self.sortable_date.set(
                        tz=pendulum.local_timezone())
                self.date_published = self.sortable_date.to_rfc2822_string()
                break

            self.slug = str(self)

    @property
    def rss_feed_item(self):
        feed_item = RSSFeedItem(self)
        return feed_item

class Blog(Collection):
    page_content_type: typing.Type[BlogPost] = BlogPost
    _archive_reverse: bool = True
    has_archive: bool = True
    feeds = [RSSFeed]

    @staticmethod
    def _archive_default_sort(cls):
        return cls.sortable_date
