"""
The Feeds Logic That Makes Up RSS and ATOM FeedTypes.

This is the base files and should only contain the params identified by the
standards defined.

RSS: http://www.rssboard.org/rss-specification
JSON: https://jsonfeed.org/version/1
"""

from .page import Page


class RSSFeedItem():
    version = 2.0

    def __init__(self, Page):
        if not hasattr(Page, 'title'):
            Page.title = ''

        if hasattr(Page, 'description'):
            pass

        elif hasattr(Page, 'content'):
            Page.description = Page.content

        elif hasattr(Page, 'summary'):
            Page.description = Page.summary

        else:
            Page.description = ''

        if not any([Page.title, Page.description]):
            error_msg = "Your page must have either a title or a description"
            raise AttributeError(error_msg)

        self.page = Page

    @property
    def content(self):
        template = '''<item>{% if page.title %}{{page.title}}{% endif %}</item>'''

class RSSFeed(Page):
    pass
