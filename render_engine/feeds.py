"""
The Feeds Logic That Makes Up RSS and ATOM FeedTypes.

This is the base files and should only contain the params identified by the
standards defined.

RSS: http://www.rssboard.org/rss-specification
JSON: https://jsonfeed.org/version/1
"""
import logging

import jinja2
from jinja2 import FileSystemLoader, PackageLoader, select_autoescape
from more_itertools import first_true

from .archive import Archive
from .engine import Engine
from .page import Page
from .site import Site


class RSSFeedItem:
    """The Object to be used with an RSS Feed"""
    def __init__(self, page, **kwargs):
        self.page = page
        self.title = getattr(page, 'title', '')
        description = getattr(page, 'description', None)
        content = getattr(page, 'content', None)
        summary = getattr(page, 'summary', None)
        self.description = first_true([description, content, summary], None)

        if not self.title and not self.description:
            error_msg = "Your page must have either a title or a description"
            raise AttributeError(error_msg)

        self.guid = getattr(page, 'guid', None) or page.slug


class RSSFeed:
    """The RSS Feed Component of an Archive Object"""

    def __init__(self, archive, **kwargs):
        self.archive = archive
        self.archive.archive_content_type = RSSFeedItem

class RSSFeedEngine(Engine):
    """The Engine that Processes RSS Feed"""
    extension = '.rss'
    environment = jinja2.Environment(
                loader=PackageLoader('render_engine', 'rss'),
                autoescape=select_autoescape(),
                trim_blocks=True,
                )

    def __init__(self, feed)
        self.feed = feed


    def render_feed(self,):
        template = self.environment.get_template('rss2.0.rss')
        rendered_page = template.render(items=collection)
        return rendered_page
