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

    Feed: Type[RSSFeed]
    feed_title: str
    content_path: pathlib.Path
    content_type: Type[Page] = Page
    archive_template: str | None
    template: str | None
    items_per_page: int | None
    include_extensions: list[str] = ["*.md", "*.html"]
    sort_by: str = "title"
    subcollections: list[str | list[str]] | None
    routes: list[_route] = ["./"]
    PageParser: Type[BasePageParser] = MarkdownPageParser
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

        if any(
            [
                hasattr(self, "archive_template"),
                getattr(self, "items_per_page", None),
                getattr(self, "subcollections", None),
            ]
        ):

            self.has_archive = True

            if hasattr(self, "subcollections") and not getattr(
                self, "subcollections_template", None
            ):
                self.subcollection_template = self.archive_template

        else:
            self.has_archive = False

    def _iter_content_path(self):
        """Iterate through all files in the collection's content path."""

        return flatten(
            [
                pathlib.Path(self.content_path).glob(extension)
                for extension in self.include_extensions
            ]
        )

    def get_page(self, content_path=None) -> list[Type["Page"]]:
        """Returns a list of pages for the collection."""

        _page = self.content_type(content_path=content_path, Parser=self.PageParser)
        _page.routes = self.routes
        _page.subcollections = getattr(self, "subcollections", [])
        _page.subcollection_template = getattr(self, "subcollection_template", [])
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

        if hasattr(self, "items_per_page"):
            for index, pages in enumerate(
                list(
                    batched(
                        self.sorted_pages,
                        getattr(self, "items_per_page", len(list(self.__iter__()))),
                    )
                )
            ):
                yield Archive(
                    pages=pages,
                    template=getattr(self, "archive_template", None),
                    title=f"{self.title}-{index}",
                    routes=self.routes,
                )
        else:
            yield Archive(
                pages=self.sorted_pages,
                template=getattr(self, "archive_template", None),
                title=self.title,
                routes=self.routes,
            )

    @property
    def _feed(self):
        feed = self.Feed()
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
            for page in self._iter_content_path():
                yield self.get_page(page)
        else:
            for page in self.pages():
                yield page


def render_archives(archive, **kwargs) -> list[Archive]:
    return [archive.render(pages=archive.pages, **kwargs) for archive in archive]
