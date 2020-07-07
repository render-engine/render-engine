import logging
import typing

import pendulum

from .blog import Blog, BlogPost
from .feeds import RSSFeedEngine, RSSFeedItem
from .site import Site


class MicroBlogPost(BlogPost):
    """
    Page Like Object with slight modifications to work with BlogPosts

    Attribtues:
        title : str
            default ''. Leave blank.

        slug : str
            the name for the file for that will

        rss_feed_item : RSSFeedItem
            the content in an rss format
    """

    title = ""

    def __init__(self, **kwargs):
        """checks published options and accepts the first that is listed"""
        super().__init__(**kwargs)
        self.slug = pendulum.parse(self.date_published, strict=False).format("YMDHmS")
        self.url = f"{self.routes[0]}/{self.slug}"

    @property
    def rss_feed_item(self):
        feed_item = RSSFeedItem(self)
        return feed_item


class MicroBlog(Blog):
    """
    Custom Blog Class pointing to custom templates
    """

    _archive_template = "microblog_archive.html"
    _archive_slug = "all_microblog_posts"
    page_content_type: typing.Type[MicroBlogPost] = MicroBlogPost
    _archive_reverse: bool = True
    has_archive = True
