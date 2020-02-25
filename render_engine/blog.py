import logging
import typing
from typing import List

import pendulum
from more_itertools import first_true

from .collection import Collection
from .page import Page
from .feeds import RSSFeedItem, RSSFeed, RSSFeedEngine
from .site import Site


class BlogPost(Page):
    """
    `Page` Like object with slight modifications to work with BlogPosts.
    """

    template: str = "blog_post.html"
    def __init__(self, **kwargs):
        """checks published options and accepts the first that is listed"""
        super().__init__(**kwargs)
        date = first_true([
                getattr(self, 'date_modified', None),
                getattr(self, 'modified_date', None),
                getattr(self, 'date_published', None),
                getattr(self, 'publish_date', None),
                getattr(self, 'date'),
                ])
        parsed_date = pendulum.parse(date, strict=False)
        self.date = parsed_date.set(tz=pendulum.local_timezone())
        self.date_published = self.date.to_rfc2822_string()

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
        return cls.date
