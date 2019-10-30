"""
The Feeds Logic That Makes Up RSS and ATOM FeedTypes.

This is the base files and should only contain the params identified by the
standards defined.

RSS: http://www.rssboard.org/rss-specification
JSON: https://jsonfeed.org/version/1
"""
from more_itertools import first_true
from .page import Page


class RSSFeedItem():
    version = 2.0

    def __init__(self):
        title = getattr(self, 'title', '')
        description = getattr(self, 'description', None)
        content = getattr(self, 'content', None)
        summary = getattr(self, 'summary', None)
        self.description = first_true([description, content, summary], None)

        if not self.title and not self.description:
            error_msg = "Your page must have either a title or a description"
            raise AttributeError(error_msg)

        self.guid = getattr(self, 'guid', None) or self._slug


class RSSFeed(Page):
    pass
