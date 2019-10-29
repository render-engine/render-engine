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

    def __init__(self):
        if getattr(self, 'title', None) == True:
            self.title = ''

        if getattr(self, 'description', None) == True:
            pass

        elif getattr(self, 'content', None) == True :
            self.description = self.content

        elif getattr(self, 'summary', None) == True:
            self.description = self.summary

        else:
            Page.description = ''

        if not any([self.title, self.description]):
            error_msg = "Your page must have either a title or a description"
            raise AttributeError(error_msg)

        if getattr(self, 'guid', None) == True:
            pass

        else:
            self.guid = self._slug


    @property
    def content(self):
        pass


class RSSFeed(Page):
    pass
