import itertools
import pathlib
from collections import defaultdict
from typing import Any, Callable, Type

import jinja2
from more_itertools import chunked, flatten

from .feeds import RSSFeed
from .page import Page, _route
from .parsers.markdown import MarkdownPageParser


def format_includes(include: str) -> str:
    """Formats the include to be a list of strings"""
    if not include.startswith("."):
        return f".{include}"
    return include


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
    routes: list[_route],
    collection_vars: dict,
    items_per_page: int | None = None,
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

    feed: Type[RSSFeed]
    feed_title: str
    content_path: pathlib.Path
    content_type: Type[Page] = Page
    archive_template: str | None
    template: str | None
    items_per_page: int | None
    _includes: list[str] = ["*.md", "*.html"]
    sort_by: str = "title"
    subcollections: list[str | list[str]] | None
    routes: list[str] = ["./"]
    PageParser = MarkdownPageParser
    parser_extras: dict[str, Any]
    content_path_filter: Callable[[pathlib.Path], bool] | None
    sort_reverse: bool = False
    has_archive: bool = False

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
    def includes(self):
        for include in self._includes:
            yield include

    @includes.setter
    def includes(self, *extensions: str):
        self._includes = [format_includes(include) for include in extensions]

    @property
    def collection_vars(self):
        """
        Creates Collection Vars to Pass into template.
        """
        return {f"COLLECTION_{key.upper()}": val for key, val in vars(self).items()}

    def gen_page(self, content):
        page = self.content_type(content=content, Parser=self.PageParser)
        page.routes = self.routes
        page.subcollections = getattr(self, "subcollections", [])
        page.subcollection_template = getattr(self, "subcollection_template", [])
        page.template = getattr(self, "template", None)

        for extra, extra_val in getattr(self, "parser_extras", {}).items():
            setattr(page, extra, extra_val)

        for key, val in self.collection_vars.items():
            setattr(page, key, val)

        return page

    @property
    def pages(self) -> list[Type[Page]]:
        """Returns a list of pages for the collection."""
        if getattr(self, "content_path", None):
            pages = flatten(
                [
                    pathlib.Path(self.content_path).glob(extension)
                    for extension in self.includes
                ]
            )

            for page_path in pages:
                yield self.gen_page(content=page_path.read_text())
        return ()

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
                items_per_page=getattr(self, "items_per_page", None),
                routes=self.routes,
                collection_vars=self.collection_vars,
            )
        return ()

    @property
    def _feed(self):
        if hasattr(self, "feed"):
            return self.feed(
                pages=self.pages,
                title=getattr(self, "feed_title", f"{self.title}"),
                slug=f"{self.title}",
                Parser=self.PageParser,
                collection_vars=self.collection_vars,
            )

    def __repr__(self):
        return f"{self}: {__class__.__name__}"

    def __str__(self):
        return f"{self}: {__class__.__name__}"

    def __iter__(self):
        return iter(self.pages)


def render_archives(archive, **kwargs) -> list[Archive]:
    return [archive.render(pages=archive.pages, **kwargs) for archive in archive]
