import logging
import typing

import maya

from .archive import Archive
from .page import Page


class BlogPost(Page):
    """Page Like Object with slight modifications to work with BlogPosts"""

    template: str = "blog_post.html"
    publish_options: typing.List[str] = [
        "date_published",
        "date",
        "publish_date",
        "date_modified",
        "modified_date",
    ]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.date_published: str = self._get_date_published().rfc2822()

    def _get_date_published(self) -> typing.Type[type(maya.now())]:
        for option in self.publish_options:
            if hasattr(self, option):
                date_object = getattr(self, option)
                maya_date = maya.parse(date_object)
                return maya_date


class Blog(Archive):
    archive_sort: str = "date_published"
    page_content_type: typing.Type[BlogPost] = BlogPost
    reverse: bool = True

    def _generate_archive_page_pages(
        self, collection_pages: typing.List[typing.Type[BlogPost]]
    ) -> typing.List[typing.Type[BlogPost]]:

        page_dot_pages = sorted(
            collection_pages,
            key=lambda page: page._get_date_published(),
            reverse=self.reverse,
        )

        return page_dot_pages
