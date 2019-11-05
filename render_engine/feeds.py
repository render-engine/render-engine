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

from .collection import Collection
from .engine import Engine
from .page import Page
from .site import Site


class RSSFeedItem():
    def __init__(self):
        self.title = getattr(self, 'title', '')
        description = getattr(self, 'description', None)
        content = getattr(self, 'content', None)
        summary = getattr(self, 'summary', None)
        self.description = first_true([description, content, summary], None)

        if not self.title and not self.description:
            error_msg = "Your page must have either a title or a description"
            raise AttributeError(error_msg)

        self.guid = getattr(self, 'guid', None) or page._slug


class RSSFeedEngine(Engine):
    """The Engine that Processes RSS Feed"""
    extension = '.rss'

    environment = jinja2.Environment(
                loader=PackageLoader('render_engine', 'rss'),
                autoescape=select_autoescape(),
                trim_blocks=True,
                )

    def render_feed(self, collection):
        logging.debug(self.environment.list_templates())
        template = self.get_template('rss2.0.rss')
        logging.debug(f'{template=}')
        rendered_page = template.render(items=collection)
        logging.warning(f'{rendered_page=}')

        return rendered_page
