import logging
import typing

import maya
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
                maya_date = maya.parse(date_object)
                self.date_published = maya_date.rfc2822()
                break

    @property
    def rss_feed_item(self):
        feed_item = RSSFeedItem(self)
        return feed_item

class Blog(Collection):
    page_content_type: typing.Type[BlogPost] = BlogPost
    reverse: bool = True
    has_archive = True

    @staticmethod
    def _archive_default_sort(cls):
        return cls.date_published
