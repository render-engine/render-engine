import logging
import typing
from pathlib import Path

from .page import Page
from .feeds import RSSFeed


class Collection:
    engine = ""
    """Collection objects serve as a way to quickly process pages that have a
    LARGE portion of content that is similar or file driven.

    The most common form of collection would be a Blog, but can also be
    static pages that have their content stored in a dedicated file.

    Currently, collections must come from a content_path and all be the same
    content type.


    Example
    -------
    from render_engine import Collection

    @site.register_collection()
    class BasicCollection(Collection):
        pass


    Attributes
    ----------
    engine: str, optional
        The engine that the collection will pass to each page. Site's default
        engine
    template: str
        The template that each page will use to render
    routes: List[str]
        all routes that the file should be created at. default []
    content_path: List[PathString], optional
        the filepath to load content from.
    includes: List[str], optional
        the types of files in the content path that will be processed
        default ["*.md", "*.html"]
    has_archive: Bool
        if `True`, create an archive page with all of the processed pages saved
        as `pages`. default `False`
    _archive_template: str, optional
        template filename that will be used if `has_archive==True` default: archive.html"
    _archive_slug: str, optional
        slug for rendered page if `has_archive == True` default: all_posts
    _archive_content_type: Type[Page], optional
        content_type for the rendered archive page
    _archive_reverse: Bool, optional
        should the sorted `pages` be listed in reverse order. default: False

    """
    engine = ''
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
        """attribute pulled from a rendered Page to sort `pages`"""
        return cls.slug

    @property
    def pages(self) -> typing.List[typing.Type[Page]]:
        """Iterate through set of pages and generate a `Page`-like object for each."""
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
        """Create a `Page` object for those items"""
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
