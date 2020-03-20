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
    Page Like object with slight modifications to work with BlogPosts.

    Attributes:
        template : str
            the default template that the site will look for
        rss_feed_item : RSSFeedItem
            the content in an rss format
        date : pendulum.datetime
            date parsed in datetime format. usesul for sorting and things
        date_published : str
            date formated for `RSSFeed`
        date_friendly : str
            an easy to read string version of the date

    """

    template = "blog_post.html"

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
        # Add some flexibility to date detection
        date = first_true([
                getattr(self, 'date_modified', None),
                getattr(self, 'modified_date', None),
                getattr(self, 'date_published', None),
                getattr(self, 'publish_date', None),
                getattr(self, 'date'),
                ])
        logging.debug(f'{date=} detected!')
        parsed_date = pendulum.parse(date, strict=False)
        self.date = parsed_date.set(tz=pendulum.local_timezone())
        self.date_published = self.date.to_rfc2822_string()
        self.date_friendly = self.date.format('MMM DD, YYYY HH:mm A')

    @property
    def rss_feed_item(self):
        return RSSFeedItem(self)


class Blog(Collection):
    """
    Custom Collection Class with Archiving Enabled and the RSS Feed

    Todos:
        - Add Support for JSON Feeds
        - Rename the archive items so they are not private
    """

    page_content_type: typing.Type[BlogPost] = BlogPost
    _archive_reverse: bool = True
    has_archive: bool = True
    feeds = [RSSFeed]

    @staticmethod
    def _archive_default_sort(cls):
        """
        How to sort pages

        Attributes:
            _archive_default_sort : Any
                default BlogPost.date

        Todos:
            - Rename the archive items so they are not private
        """
        return cls.date
