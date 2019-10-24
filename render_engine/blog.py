import maya

from ._helpers import PathString
from .archive import Archive
from .page import Page


class BlogPost(Page):
    """Page Like Object with slight modifications to work with BlogPosts"""

    template = "blog_post.html"
    publish_options = [
            "date_published",
            "date",
            "publish_date",
            "date_modified",
            "modified_date",
        ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.date_published = self._get_date_published().rfc2822()

    def _get_date_published(self):
        for option in self.publish_options:
            if hasattr(self, option):
                date_object = getattr(self, option)
                maya_date = maya.parse(date_object)
                return maya_date


class Blog(Archive):
    archive_sort = "date_published"
    page_content_type = BlogPost
    reverse = True

    def _generate_archive_page_pages(self, collection_pages):
        page_dot_pages = sorted(
            collection_pages,
            key=lambda page: page._get_date_published(),
            reverse=self.reverse,
        )
        return page_dot_pages
