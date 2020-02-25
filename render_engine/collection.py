import logging
import typing
from pathlib import Path

from .page import Page
from .feeds import RSSFeed


class Collection:
<<<<<<< Updated upstream
    engine = ""
=======
    """Collection objects serve as a way to quickly process pages that have a
    LARGE portion of content that is similar or file driven.

    The most common form of collection would be the Blog,
    but can also be static pages that have their content stored in a dedicated file.
    """
    engine = ''
>>>>>>> Stashed changes
    page_content_type = Page
    content_path = "content"
    template = "page.html"
    includes = ["*.md", "*.html"]
    routes = [""]
    has_archive = False
    _archive_template = "archive.html"
    _archive_slug = "all_posts"
    _archive_content_type = Page
    _archive_reverse = False
    # engines that will generate feeds. Engine should output 'rss', or 'JSON' format

    @staticmethod
    def _archive_default_sort(cls):
        return cls.slug

    @property
    def pages(self) -> typing.List[typing.Type[Page]]:
        """Iterate through set of pages and generate a page object for each"""
        pages = []

        for i in self.includes:
            for _file in Path(self.content_path).glob(i):
                page = self.page_content_type(content_path=_file)
                page.routes = self.routes
                page.template = self.template
                pages.append(page)

        return pages

    @property
    def archive(self):
        """Get the collection's pages and create an arcive for those items"""
        archive_page = self._archive_content_type()
        archive_page.template = self._archive_template
        archive_page.slug = self._archive_slug
        archive_page.engine = ""
        archive_page.title = self.__class__.__name__
        archive_page.pages = sorted(
            self.pages,
            key=lambda p: self._archive_default_sort(p),
            reverse=self._archive_reverse,
        )
        return archive_page
