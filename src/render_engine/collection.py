import itertools
from collections import defaultdict
from pathlib import Path
from typing import Type

import jinja2
from more_itertools import chunked

from .page import Page, _route
from .parsers.markdown import MarkdownCollectionParser


class Archive(Page):
    """Custom Page object used to make archive pages"""

    def __init__(
        self,
        pages: list[Type[Page]],
        template: str,
        routes: list[_route],
        **kwargs,
    ) -> None:
        """Create a `Page` object for the pages in the collection"""
        super().__init__()
        self.pages = pages
        self.template = template
        self.routes = routes
        for key, val in kwargs.items():
            setattr(self, key, val)


def gen_collection(
    pages: list[Type[Page]] | list[Archive],
    template: str,
    title: str,
    items_per_page: int | None,
    routes: list[_route],
    collection_vars: dict,
) -> list[Archive]:
    """Returns a list of Archive pages containing the pages of data for each archive."""

    if items_per_page:
        page_chunks = chunked(pages, items_per_page)

        pages = [
            Archive(
                pages=pages,
                template=template,
                slug=f"{title}_{i}",
                title=title,
                routes=routes,
                **collection_vars,
            )
            for i, pages in enumerate(page_chunks)
        ]

        return pages

    return [
        Archive(
            pages=pages,
            template=template,
            title=title,
            routes=routes,
            **collection_vars,
        )
    ]


SubCollection = {str, list[Page]}


class Collection:
    """Collection objects serve as a way to quickly process pages that have a
    LARGE portion of content that is similar or file driven.

    The most common form of collection would be a Blog, but can also be
    static pages that have their content stored in a dedicated file.

    Currently, collections must come from a content_path and all be the same
    content type.

    Example::

        from render_engine import Collection

        @site.collection
        class BasicCollection(Collection):
            pass
    """

    content_path: Path
    content_type: Page = Page
    archive_template: str | None
    template: str | None = None
    items_per_page: int | None
    includes: list[str] = ["*.md", "*.html"]
    sort_by: str = "title"
    sort_reverse: bool = False
    has_archive: bool = False
    subcollections: list[str | list[str]] | None
    routes: list[str] = ["./"]

    def __init__(self):
        if not hasattr(self, "title"):
            self.title = self.__class__.__name__

        if hasattr(self, "archive_template"):
            self.has_archive = True
            self.archive_template

            if hasattr(self, "subcollections") and not getattr(
                self, "subcollections_template", None
            ):
                self.subcollection_template = self.archive_template

    @property
    def collection_vars(self):
        """
        Creates Collection Vars to Pass into template.
        """
        return {key.upper(): val for key, val in vars(self).items()}

    @property
    def pages(self) -> list[Type[Page]]:
        return self.Parser(self).parse(self)

    @property
    def sorted_pages(self):
        return sorted(
            self.pages,
            key=lambda page: getattr(page, self.sort_by),
            reverse=self.sort_reverse,
        )

    @property
    def archives(self) -> list[Archive]:
        """Returns a list of Archive pages containing the pages of data for each archive."""
        if self.has_archive:
            return gen_collection(
                pages=self.sorted_pages,
                template=self.archive_template,
                title=self.title,
                items_per_page=self.items_per_page,
                routes=self.routes,
                collection_vars=self.collection_vars,
            )
        return ()

    # def render_feed(self, feed_type: RSSFeed, **kwargs) -> RSSFeed:
    #     return feed_type(pages=self.pages, **kwargs)

    def __repr__(self):
        return f"{self}: {__class__.__name__}"

    def __str__(self):
        return f"{self}: {__class__.__name__}"

    def __iter__(self):
        return iter(self.pages)


def render_archives(archive, **kwargs) -> list[Archive]:
    return [archive.render(pages=archive.pages, **kwargs) for archive in archive]
