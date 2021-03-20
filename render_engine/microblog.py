import typing

from .blog import Blog, BlogPost


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

    def __init__(self, **kwargs):
        """checks published options and accepts the first that is listed"""
        super().__init__(**kwargs)

        self.slug = self.date_published.format("YMMDDHHmmss")
        self.title = ""


class MicroBlog(Blog):
    """
    Custom Blog Class pointing to custom templates
    """

    _archive_template = "microblog_archive.html"
    _archive_slug = "all_microblog_posts"
    content_type: typing.Type[MicroBlogPost] = MicroBlogPost
    _archive_reverse: bool = True
    has_archive = True
