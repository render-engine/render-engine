import logging
import typing

import maya
from more_itertools import flatten

from .archive import Archive
from .page import Page
from .feeds import RSSFeedItem, RSSFeedEngine
from .site import Site


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

    def __init__(self, **kwargs):
        """checks published options and accepts the first that is listed"""
        super().__init__(**kwargs)
        for option in self.publish_options:
            if hasattr(self, option):
                date_object = getattr(self, option)
                maya_date = maya.parse(date_object)
                self.date_published = maya_date.rfc2822()


class Blog(Archive):
    default_sort: str = "date_published"
    page_content_type: typing.Type[BlogPost] = BlogPost
    reverse: bool = True

    def __init__(self):
        super().__init__()

    def _generate_archive_page_pages(
        self, collection_pages: typing.List[typing.Type[BlogPost]]
    ) -> typing.List[typing.Type[BlogPost]]:

        page_dot_pages = sorted(
            collection_pages,
            key=lambda page: self.default_sort,
            reverse=self.reverse,
        )

        return page_dot_pages


class BlogSite(Site):
    tags = []
    categories = []
    name = 'blog.rss'

    def __init__(self, *, title, description, link):
        self.title = title
        self.description = description
        self.link = link
        self.feed_engine = RSSFeedEngine()
        self.feed_engine.environment.globals.update({
                'title': self.title,
                'description': self.description,
                'link': self.link,
                })

    def register_collection(self, collection_cls):
        """Create a site dedicated to the blog posts"""
        collection = collection_cls().pages

        for page in collection:
            rssItem = RSSFeedItem(page)

            if hasattr(page, "tags"):
                self.tags.add(page.tags)

            if hasattr(page, "category"):
                self.tags.add(page.tags)

            self.route(cls=page)


    def render(self):
        super().render()
        content = self.feed_engine.render_feed(self.routes)
        route = self.output_path.joinpath(self.blog_name)
        route.write_text(content)
