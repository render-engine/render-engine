"""
The Feeds Logic That Makes Up RSS and ATOM FeedTypes.

This is the base files and should only contain the params identified by the
standards defined.

RSS: http://www.rssboard.org/rss-specification
JSON: https://jsonfeed.org/version/1
"""

import logging

import jinja2
import pendulum
from jinja2 import PackageLoader, select_autoescape
from more_itertools import first_true

from .engine import Engine
from .page import Page


class RSSFeedEngine(Engine):
    """The Engine that Processes RSS Feed"""

    extension = ".rss.xml"
    environment = jinja2.Environment(
        loader=PackageLoader("render_engine", "rss"),
        autoescape=select_autoescape(),
        trim_blocks=True,
    )


class RSSFeedItem:
    """
    The Object to be used with an RSS Feed.

    Attributes:
        title (str):
            Title of the post
        description (str):
            Content of the post. Can be the post's (in order) `description`,
            `content` or `summary`.
        guid (str):
            unique identifier of the content
        link (str): link to the post. Due to the design of the system, use the
            reference link and expand to the full link using information from the `site`
        pub_date (str):
            datetime formatted to RFC 822 (or 2822)

    .. _should conform to the RSS 2.0 specification:
       <https://cyber.harvard.edu/rss/rss.html>
    """

    def __init__(self, cls):
        """
        Parse information from the given class object.

        Raises:
            AttributeError:
        """

        self.title = getattr(cls, "title", "")
        # Posts will have one or many of the following
        description = getattr(cls, "description", None)
        content = getattr(cls, "content", None)
        summary = getattr(cls, "summary", None)
        # Set description to the preference
        self.description = first_true([description, content, summary], None)

        # Raise Error if you have neither a title or description
        if not self.title and not self.description:
            error_msg = "Your page must have either a title or a description"
            raise AttributeError(error_msg)

        self.guid = getattr(cls, "guid", cls.slug)
        logging.debug(vars(cls))
        self.link = cls.url
        self.pub_date = cls.date_published.to_rfc2822_string()


class RSSFeed(Page):
    """The RSS Feed Component of an Archive Object"""

    template = "rss2.0.rss"
    engine = RSSFeedEngine()
    link = ""
    slug = ""

    def __init__(self, title, collection):
        super().__init__()
        self.no_index = True
        self.title = title
        self.items = [item.rss_feed_item for item in collection.pages]
