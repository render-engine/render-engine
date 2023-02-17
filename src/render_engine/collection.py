import pathlib
from typing import Any, Callable, Generator, Type

import pluggy
from more_itertools import batched, flatten
from slugify import slugify

from .archive import Archive
from .feeds import RSSFeed
from .page import Page, _route
from .parsers import BasePageParser
from .parsers.markdown import MarkdownPageParser


class Collection:
    """Collection objects serve as a way to quickly process pages that have a
    LARGE portion of content that is similar or file driven.

    Currently, collection pages MUST come from a `content_path` and all be the same
    content type.

    Example::

        from render_engine import Collection

        @site.collection
        class BasicCollection(Collection):
            pass
    """

    archive_template: str | None
    content_path: pathlib.Path
    content_type: Type[Page] = Page
    Feed: Type[RSSFeed]
    feed_title: str
    include_suffixes: list[str] = ["*.md", "*.html"]
    items_per_page: int | None
    PageParser: Type[BasePageParser] = MarkdownPageParser
    parser_extras: dict[str, Any]
    routes: list[_route] = ["./"]
    sort_by: str = "title"
    sort_reverse: bool = False
    title: str
    template: str | None

    def __init__(
        self,
        pm: pluggy.PluginManager,
    ) -> None:

        if not hasattr(self, "title"):
            self.title = self.__class__.__name__
        self.has_archive = any(
            [
                hasattr(self, "archive_template"),
                getattr(self, "items_per_page", None),
            ]
        )
        self._pm = pm

    def iter_content_path(self):
        """Iterate through in the collection's content path."""

        return flatten(
            [
                pathlib.Path(self.content_path).glob(suffix)
                for suffix in self.include_suffixes
            ]
        )

    def get_page(self, content_path=None) -> "Page":
        """Returns a list of pages for the collection."""
        _page = self.content_type(
            content_path=content_path, Parser=self.PageParser, pm=self._pm
        )
        _page.parser_extras = getattr(self, "parser_extras", {})
        _page.routes = self.routes
        _page.template = getattr(self, "template", None)
        _page.collection_vars = vars(self)
        return _page

    @property
    def sorted_pages(self):
        return sorted(
            (page for page in self.__iter__()),
            key=lambda page: getattr(page, self.sort_by, self.title),
            reverse=self.sort_reverse,
        )

    @property
    def archives(self) -> Generator[Archive, None, None]:
        """Returns a list of Archive pages containing the pages of data for each archive."""

        if not self.has_archive:
            yield from ()

        sorted_pages = list(self.sorted_pages)
        items_per_page = getattr(self, "items_per_page", len(sorted_pages))
        archives = list(batched(sorted_pages, items_per_page))
        num_of_pages = len(archives)

        for index, pages in enumerate(archives):
            yield Archive(
                pm=self._pm,
                pages=pages,
                template=getattr(self, "archive_template", None),
                title=self.title,
                routes=self.routes,
                archive_index=index,
                num_of_pages=num_of_pages,
            )

    @property
    def _feed(self):
        feed = self.Feed(pm=self._pm)
        feed.pages = [page for page in self]
        feed.title = getattr(self, "feed_title", self.title)
        feed.slug = self.title
        feed.Parser = self.PageParser
        return feed

    @property
    def slug(self):
        return slugify(self.title)

    def __repr__(self):
        return f"{self}: {__class__.__name__}"

    def __str__(self):
        return f"{__class__.__name__}"

    def __iter__(self):
        if not hasattr(self, "pages"):
            for page in self.iter_content_path():
                yield self.get_page(page)
        else:
            for page in self.pages:
                yield page


def render_archives(archive, **kwargs) -> list[Archive]:
    return [archive.render(pages=archive.pages, **kwargs) for archive in archive]
