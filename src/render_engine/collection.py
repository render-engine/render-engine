import pathlib
from typing import Any, Callable, Type

import pluggy
from more_itertools import batched, chunked, flatten

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

    def __init__(
        self,
        pm: pluggy.PluginManager | None = None,
    ) -> None:

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
        """Creates Collection Vars to Pass into template."""
        return {f"COLLECTION_{key.upper()}": val for key, val in vars(self).items()}

    def _iter_content_path(self):
        """Iterate through all files in the collection's content path."""
        return flatten(
            [
                pathlib.Path(self.content_path).glob(extension)
                for extension in self.includes
            ]
        )

    def get_page(self, content_path=None) -> list[Type[Page]]:
        """Returns a list of pages for the collection."""

        class Page(self.content_type):
            routes = self.routes
            subcollections = getattr(self, "subcollections", [])
            subocollection_template = getattr(self, "subcollection_template", [])
            template = getattr(self, "template", None)
            Parser = self.PageParser

            def __init__(self, collection, content_path):
                self.content_path = content_path
                for extra, extra_val in getattr(
                    collection, "parser_extras", {}
                ).items():
                    setattr(self, extra, extra_val)

                for key, val in getattr(collection, "collection_vars", {}).items():
                    setattr(self, key, val)

                super().__init__(pm=getattr(collection, "pm", None))

        return Page(self, content_path)

    @property
    def sorted_pages(self):
        return sorted(
            (page for page in self.__iter__()),
            key=lambda page: getattr(page, self.sort_by, self.title),
            reverse=self.sort_reverse,
        )

    @property
    def archives(self) -> list[Archive]:
        """Returns a list of Archive pages containing the pages of data for each archive."""
        for pages in batched(
            self.sorted_pages,
            getattr(self.items_per_page, len(list(self._iter_content_path()))),
        ):
            yield Archive(
                pages=pages,
                template=self.archive_template,
                title=self.title,
                routes=self.routes,
                collection_vars=self.collection_vars,
            )

    @property
    def _feed(self):
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
        for page in self._iter_content_path():
            yield self.get_page(page)


def render_archives(archive, **kwargs) -> list[Archive]:
    return [archive.render(pages=archive.pages, **kwargs) for archive in archive]
