import collections
import itertools
import logging
import operator
import typing
from pathlib import Path

import more_itertools
from slugify import slugify

from .feeds import RSSFeed
from .page import Page


class Collection:
    """Collection objects serve as a way to quickly process pages that have a
    LARGE portion of content that is similar or file driven.

    The most common form of collection would be a Blog, but can also be
    static pages that have their content stored in a dedicated file.

    Currently, collections must come from a content_path and all be the same
    content type.


    Example::

        from render_engine import Collection

        @site.register_collection()
        class BasicCollection(Collection):
            pass
    """

    engine: typing.Optional[str] = None
    content_items: typing.List[Page] = []
    content_path: str = ""
    content_type: typing.Type[Page] = Page
    template: str = "page.html"
    includes: typing.List[str] = ["*.md", "*.html"]
    routes: typing.List[str] = [""]
    subcollections: typing.List[str] = []
    has_archive: bool = False
    archive_template: str = "archive.html"
    archive_reverse: bool = False
    archive_sort: typing.Tuple[str] = "title"
    paginated: bool = False
    items_per_page: int = 10
    title: typing.Optional[str] = ""
    feeds: typing.List[typing.Optional[RSSFeed]] = []
    markdown_extras = ["fenced-code-blocks", "footnotes"]

    def __init__(self):
        if not self.title:
            self.title = self.__class__.__name__

    @property
    def slug(self):
        return slugify(self.title)

    @property
    def pages(self) -> typing.List[Page]:
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
                    page = self.content_type.from_content_path(
                        filepath,
                        markdown_extras=self.markdown_extras,
                    )
                    page.routes = self.routes
                    page.template = self.template
                    _pages.append(page)

        return _pages

    @property
    def archive(self):
        """Create a `Page` object for the pages in the collection"""

        sorted_pages = sorted(
            self.pages,
            key=lambda p: getattr(p, self.archive_sort),
            reverse=self.archive_reverse,
        )

        if self.paginated:
            pages = list(more_itertools.chunked(sorted_pages, self.items_per_page))

        else:
            pages = [sorted_pages]

        class Archive(Page):
            no_index = True
            template = self.archive_template
            routes = [self.routes[0]]
            title = self.title
            always_refresh = True

        archive_pages = []

        for index, page in enumerate(pages):
            archive_page = Archive()
            archive_page.collection = self
            archive_page.routes = [self.routes[0]]
            archive_page.pages = pages[index]
            archive_page.title = self.title
            archive_page.page_index = (index, len(pages))

            if self.paginated:
                archive_page.slug = f"{archive_page.slug}-{index}"

            archive_pages.append(archive_page)

        return archive_pages

    def get_subcollections(self):
        subcollections = {}

        # get all the values for each of the subcollections
        for _subcollection in self.subcollections:
            subcollection_lists = collections.defaultdict(list)
            subcollections[_subcollection] = []

            for page in self.pages:

                if attr := getattr(page, _subcollection, None):

                    if isinstance(attr, list):

                        for attribute_item in attr:
                            subcollection_lists[attribute_item].append(page)

                    else:
                        subcollection_lists[attr].append(page)

            for attr, subcollection in subcollection_lists.items():

                class SubCollection(self.__class__):
                    content_path = None
                    content_items = subcollection
                    title = attr
                    slug = slugify(attr)

                subcollections[_subcollection].append(SubCollection())

        return subcollections
