import copy
import datetime
import logging
from collections.abc import Callable, Generator
from pathlib import Path
from typing import Any

import dateutil.parser as dateparse
from more_itertools import batched, flatten
from render_engine_parser import BasePageParser
from slugify import slugify

from ._base_object import BaseObject
from .archive import Archive
from .feeds import RSSFeed
from .page import Page
from .plugins import PluginManager


class Collection(BaseObject):
    """
    Collection objects serve as a way to quickly process pages that have a
    portion of content that is similar or file driven.

    Example:

    ```python
    from render_engine import Site, Collection

    site = Site()

    @site.collection
    class BasicCollection(Collection):
        content_path = "content/pages"
    ```

    Collection pages **MUST** come from a `content_path` and all be the same
    content type.  `content_path` can be a string representing a path or URL,
    depending on the [parser][src.render_engine.parsers.base_parsers] used.

    Attributes:

        archive_template: The template to use for the [`Archive`][src.render_engine.archive.Archive] pages.
        content_path: The path to iterate over to generate pages.
        content_type: Type[Page] = Page
        Feed: Type[RSSFeed] = RSSFeed
        feed_title: str
        include_suffixes: list[str] = ["*.md", "*.html"]
        items_per_page: int | None
        Parser: BasePageParser = BasePageParser
        parser_extras: dict[str, Any]
        required_themes: list[callable]
        routes: list[str | Path] = ["./"]
        sort_by: str = "title"
        sort_reverse: bool = False
        title: str
        template: str | None
        archive_template str | None: The template to use for the archive pages.

    Methods:

        iter_content_path(): Iterates through the collection's content path.
        get_page(content_path: str | Path | None = None): Returns the page Object for the specified Content Path.
        sorted_pages: Returns the sorted pages of the collection.
        archives: Returns the Archive objects containing the pages from the content path.
        feed: Returns the Feed object for the collection.
        slug: Returns the slugified title of the collection.

    """

    archive_template: str | Path | None = "archive.html"
    content_path: Path | str
    content_type: type[Page] = Page
    Feed: type[RSSFeed] = RSSFeed
    feed_title: str
    include_suffixes: list[str] = ["*.md", "*.html"]
    items_per_page: int | None
    Parser: BasePageParser = BasePageParser
    parser_extras: dict[str, Any]
    required_themes: list[Callable]
    routes: list[str | Path] = ["./"]
    sort_by: str = "_title"
    sort_reverse: bool = False
    template_vars: dict[str, Any]
    template: str | None
    plugin_manager: PluginManager | None

    def __init__(
        self,
    ) -> None:
        if parser := getattr(self, "PageParser", None):
            logging.warning(
                DeprecationWarning(
                    f"The deprecated`PageParser` attribute is used in `{self.__class__.__name__}`. \
                        Use the `Parser` attribute instead."
                )
            )
            self.Parser = parser

        if getattr(self, "items_per_page", False):
            self.has_archive = True
        self.title = self._title
        self.template_vars = getattr(self, "template_vars", {})

    def iter_content_path(self):
        """Iterate through in the collection's content path."""
        return flatten([Path(self.content_path).glob(suffix) for suffix in self.include_suffixes])

    def get_page(
        self,
        content_path: str | Path | None = None,
    ) -> Page:
        """Returns the page Object for the specified Content Path"""
        _page = self.content_type(
            content_path=content_path,
            Parser=self.Parser,
        )

        if getattr(self, "_pm", None):
            _page.register_plugins(self.plugins, **self.plugin_settings)
        _page.parser_extras = getattr(self, "parser_extras", {})
        _page.routes = self.routes
        _page.template = getattr(self, "template", None)
        _page.collection = self.to_dict()

        return _page

    @staticmethod
    def _date_key(page: Page) -> datetime.datetime:
        """
        Key for ensuring proper handling of dates for sorting
        There are 2 issues here:
        1. We need to convert a string to a datetime for proper sorting
        2. We need to strip the timezone so that we are consistently dealing with timezone naive objects

        :param page: The Page object to handle the date for
        :return: Timezone naive datetime object
        """
        date = getattr(page, "date")
        _date = dateparse.parse(date) if isinstance(date, str) else copy.copy(date)
        return _date.replace(tzinfo=None) if isinstance(_date, datetime.datetime) else _date

    @property
    def sorted_pages(self):
        """
        Returns pages in the collection sorted by the `self.sort_by` attribute.

        Exceptions:
            AttributeError: This is raised when the attribute is missing from one or more pages
            TypeError: This happens when the values being compared are of two different types

        """
        # Dates need special handling so figure out if that's needed and set it here
        sort_key = self._date_key if self.sort_by == "date" else lambda page: getattr(page, self.sort_by)
        try:
            return sorted(
                (page for page in self.__iter__()),
                key=sort_key,
                reverse=self.sort_reverse,
            )
        except AttributeError as e:
            raise AttributeError(
                f"Cannot sort pages: '{self.sort_by}' attribute is missing from one or more pages."
                f"Make sure all pages in collection '{self._title}' have the '{self.sort_by}' attribute defined."
            ) from e

    @property
    def archives(self) -> Generator[Archive, None, None]:
        """
        Returns a [Archive][src.render_engine.archive.Archive] objects containing the pages from the `content_path` .

        Archives are an iterable and the individual pages are built shortly after the collection pages are built.
        This happens when [Site.render][render_engine.Site.render] is called.
        """
        if not getattr(self, "has_archive", False):
            logging.warning(
                "`has_archive` is set to `False` for %s. While an archive will be generated. \
                The file will not be saved.",
                self._title,
            )
            yield from ()

        sorted_pages = list(self.sorted_pages)
        items_per_page = getattr(self, "items_per_page", len(sorted_pages))
        archives = [sorted_pages]

        if items_per_page != len(sorted_pages):
            archives.extend(list(batched(sorted_pages, items_per_page)))
            self.template_vars["num_of_pages"] = len(archives) - 1 / items_per_page
        else:
            self.template_vars["num_of_pages"] = 1

        for index, pages in enumerate(archives):
            yield Archive(
                pages=pages,
                template=getattr(self, "archive_template", None),
                template_vars=self.template_vars,
                title=self._title,
                routes=self.routes,
                archive_index=index,
                plugin_manager=getattr(self, "plugin_manager", None),
                is_index=not index,
            )

    @property
    def feed(self):
        feed = self.Feed()
        feed.pages = self.sorted_pages
        feed.title = getattr(self, "feed_title", self._title)
        feed.slug = self._slug
        feed.Parser = self.Parser
        return feed

    @property
    def slug(self):
        return slugify(self.title)

    def __repr__(self):
        return f"{self}: {__name__}"

    def __str__(self):
        return f"{__name__}"

    def __iter__(self):
        if not hasattr(self, "pages"):
            self.pages = [self.get_page(page) for page in self.iter_content_path()]
        for page in self.pages:  # noqa: UP028
            yield page

    def _run_collection_plugins(self, site, hook_type: str):
        """
        Run plugins for a collection

        :param site: The site object triggering the call
        :param hook_type: The hook to run
        """
        if not getattr(self.plugin_manager, "_pm", None) or not self.plugin_manager.plugins:
            return
        try:
            method = getattr(self.plugin_manager.hook, hook_type)
        except AttributeError:
            logging.error(f"Unknown {hook_type=}")
            return
        method(collection=self, site=site, settings=self.plugin_manager.plugin_settings)


def render_archives(archive, **kwargs) -> list[Archive]:
    return [archive.render(pages=archive.pages, **kwargs) for archive in archive]
