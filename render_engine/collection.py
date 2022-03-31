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


class Archive(Page):
    """Custom Page object used to make archive pages"""

    template: str = "archive.html"
    no_index: bool = True
    sort_by: typing.Tuple[str] = "title"


    def __init__(
            self, /, title:str, pages: list, reverse: bool = False
        ) -> None:
        """Create a `Page` object for the pages in the collection"""
        super.__init__()

        sorted_pages = sorted(
            pages,
            key=lambda p: getattr(p, self.sort_by),
            reverse=reverse,
        )

        self.pages = [sorted_pages]

        archive_pages = []


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
    content_items: list[Page] = list
    content_path: str = "./content"
    content_type: Page = Page
    template: str = "page.html"
    includes: list[str] = ["*.md", "*.html"]
    routes: list[str] = list
    subcollections: list[str] = list
    has_archive: bool = False
    feeds: list[typing.Optional[RSSFeed]] = list
    markdown_extras = ["fenced-code-blocks", "footnotes"]
    paginated: bool = False
    items_per_page: int = 10

    def __init__(self):
        if not hasattr(self, 'title'):
            self.title = self.__class__.__name__

        for index, page in enumerate(pages):

            archive_page = Archive()
            archive_page.collection = self
            archive_page.routes = [self.routes[0]]
            archive_page.pages = pages[index]
            archive_page.title = self.title
            archive_page.page_index = (index, len(pages))

        if self.paginated:
            pages = list(more_itertools.chunked(sorted_pages, self.items_per_page))

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

#            if self.paginated:
#                archive_page.slug = f"{archive_page.slug}-{index}"
#
#            archive_pages.append(archive_page)
#
#        return archive_pages

    
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
