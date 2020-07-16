import itertools
import logging
import operator
import typing
from pathlib import Path

import more_itertools

from .feeds import RSSFeed
from .page import Page


class Collection:
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

    engine: typing.Optional[str] = ""
    content_items: typing.List[Page] = []
    content_path: str = ""
    page_content_type: typing.Type[Page] = Page
    template: str = "page.html"
    includes: typing.List[str] = ["*.md", "*.html"]
    routes: typing.List[str] = [""]
    subcollections: typing.List[str] = []
    has_archive: bool = False
    archive_template: str = "archive.html"
    archive_slug: str = "all_posts"
    archive_content_type: Page = Page
    archive_reverse: bool = False
    paginated: bool = False
    items_per_page: int = 10
    title: typing.Optional[str] = ''
    feeds: typing.List[typing.Optional[RSSFeed]] = []

    def __init__(self):
        if not self.title:
            self.title = self.__class__.__name__

    @staticmethod
    def archive_default_sort(cls):
        """attribute pulled from a rendered Page to sort `pages`"""
        return cls.slug

    @property
    def _pages(self) -> typing.List[Page]:
        _pages = []

        if self.content_items:
            _pages = self.content_items

        if self.content_path:

            if Path(self.content_path).samefile("/"):
                logging.warning(
                    f"{self.content_path=}! Accessing Root Directory is Dangerous..."
                )

            for pattern in self.includes:

                for filepath in Path(self.content_path).glob(pattern):
                    page = self.page_content_type.from_content_path(filepath)
                    page.routes = self.routes
                    page.template = self.template
                    _pages.append(page)

        return _pages


    @property
    def pages(self) -> typing.List[typing.Union[Page, typing.List]]:
        """Iterate through set of pages and generate a `Page`-like object for each."""

        sorted_pages = sorted(
            self._pages,
            key=lambda p: self.archive_default_sort(p),
            reverse=self.archive_reverse,
        )

        if self.paginated:
            return list(more_itertools.chunked(sorted_pages, self.items_per_page))

        else:
            return sorted_pages


    @property
    def archive(self):
        """Create a `Page` object for the pages in the collection"""
        archive_page = self.archive_content_type()
        archive_page.no_index = True
        archive_page.template = self.archive_template
        archive_page.slug = self.archive_slug
        archive_page.engine = ""
        archive_page.routes = [self.routes[0]]
        archive_page.pages = self.pages
        archive_page.title = self.title

        if self.paginated:
            archive_pages = []

            for index, page in enumerate(self.pages):
                archive_page = self.archive_content_type()
                archive_page.no_index = True
                archive_page.template = self.archive_template
                archive_page.slug = f"{self.archive_slug}_{index}"
                archive_page.engine = ""
                archive_page.routes = [self.routes[0]]
                archive_page.pages = self.pages[index]
                archive_page.title = self.title
                archive_page.page_index = index
                archive_pages.append(archive_page)


            return archive_pages

        else:
            archive_page = self.archive_content_type()
            archive_page.no_index = True
            archive_page.template = self.archive_template
            archive_page.slug = f"{self.archive_slug}"
            archive_page.engine = ""
            archive_page.routes = [self.routes[0]]
            archive_page.pages = self.pages
            archive_page.title = self.title
            archive_page.page_index = 0
            return [archive_page]


    @classmethod
    def from_subcollection(cls, collection, attr, attrval):
        sub_content_items = []

        for page in collection._pages:

            if attrval in getattr(page, attr, []):
                sub_content_items.append(page)

        class SubCollection(Collection):
            archive_template = collection.archive_template
            archive_slug = collection.archive_slug
            archive_content_type = collection.archive_content_type
            archive_reverse = collection.archive_reverse
            content_items = sub_content_items
            has_archive = True
            routes = [attrval]
            title = attrval

        return SubCollection()


    def subcollection(self, attr):
        """Returns a list of all of the values in a subcollection"""
        attrvals = []

        for page in self._pages:
            if hasattr(page, attr):
                attrvals.append(getattr(page, attr))

        return attrvals
