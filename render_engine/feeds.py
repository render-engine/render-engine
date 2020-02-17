"""
The Feeds Logic That Makes Up RSS and ATOM FeedTypes.

This is the base files and should only contain the params identified by the
standards defined.

RSS: http://www.rssboard.org/rss-specification
JSON: https://jsonfeed.org/version/1
"""
import logging

import jinja2
from jinja2 import PackageLoader, select_autoescape
from more_itertools import first_true

from .engine import Engine
from .page import Page


class RSSFeedItem:
    """The Object to be used with an RSS Feed"""

    def __init__(self, cls):
        self.title = getattr(cls, "title", "")
        description = getattr(cls, "description", None)
        content = getattr(cls, "content", None)
        summary = getattr(cls, "summary", None)
        self.description = first_true([description, content, summary], None)

        if not self.title and not self.description:
            error_msg = "Your page must have either a title or a description"
            raise AttributeError(error_msg)

        self.guid = getattr(cls, "guid", None) or cls.slug
        self.pub_date = cls.date_published


class RSSFeed(Page):
    """The RSS Feed Component of an Archive Object"""
    template = 'rss2.0.rss'
    engine = 'rss_engine'
    title = 'RSS Feed'
    link = ''
    slug = ''


class RSSFeedEngine(Engine):
    """The Engine that Processes RSS Feed"""
    extension = ".rss"
    environment = jinja2.Environment(
        loader=PackageLoader("render_engine", "rss"),
        autoescape=select_autoescape(),
        trim_blocks=True,
    )
