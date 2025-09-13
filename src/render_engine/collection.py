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
    Container for groups of related pages with shared properties and automatic features.

    Collections provide a powerful way to manage multiple pages that share common
    characteristics, such as blog posts, documentation pages, or product listings.
    They automatically generate archives, feeds, and provide sorting/pagination.

    Architecture Role:
    - Groups Page objects with similar structure and purpose
    - Generates Archive pages for pagination when items_per_page is set
    - Creates RSS/Atom feeds automatically
    - Applies consistent templates and parsing to all contained pages
    - Supports complex sorting and filtering of content

    Site Integration:
    - Registered with Site via @site.collection decorator or site.collection() method
    - Inherits site's plugin manager with collection-specific overrides
    - Gets site reference during rendering for cross-site linking
    - Accessible in templates via site.routes[collection_slug]
    - Can reference other collections and pages during rendering

    Content Discovery:
    - Scans content_path directory for files matching include_suffixes
    - Parses each file using the specified Parser
    - Creates Page objects for each discovered content file
    - Applies collection-level settings to all pages

    Example:
        @site.collection
        class Blog(Collection):
            content_path = "content/posts"
            template = "post.html"
            archive_template = "archive.html"
            items_per_page = 10
            sort_by = "date"
            sort_reverse = True

    Attributes:
        content_path: Directory to scan for content files
        content_type: Page class to instantiate for each content file
        template: Template for individual pages in the collection
        archive_template: Template for archive/pagination pages
        Feed: Feed class for RSS/Atom generation
        feed_title: Title for the generated feed
        include_suffixes: File patterns to include (default: ["*.md", "*.html"])
        items_per_page: Number of items per archive page (enables pagination)
        Parser: Parser class for processing content files
        parser_extras: Additional parser configuration
        required_themes: Themes that must be loaded for this collection
        routes: Base routes for the collection
        sort_by: Attribute(s) to sort pages by
        sort_reverse: Whether to reverse sort order
        plugin_manager: Manages collection-specific plugins
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
    sort_by: str | list = "_title"
    sort_reverse: bool = False
    template_vars: dict[str, Any]
    template: str | None
    plugin_manager: PluginManager | None

    def __init__(self) -> None:
        """
        Initialize the Collection with configuration and setup archive generation.

        Initialization Steps:
        1. Handle deprecated PageParser attribute (backwards compatibility)
        2. Set up archive generation if pagination is configured
        3. Initialize title from class name or custom title
        4. Set up template variables for archive pages
        5. Validate configuration and log warnings for deprecated features
        """
        # Backwards compatibility: handle deprecated PageParser attribute
        if parser := getattr(self, "PageParser", None):
            logging.warning(
                DeprecationWarning(
                    f"The deprecated`PageParser` attribute is used in `{self.__class__.__name__}`. \
                         Use the `Parser` attribute instead."
                )
            )
            self.Parser = parser

        # Enable archive generation if pagination is configured
        if getattr(self, "items_per_page", False):
            self.has_archive = True

        # Set title for display and URL generation
        self.title = self._title

        # Initialize template variables for archive pages
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
        Extract and normalize date values for consistent sorting.

        Date Sorting Challenges:
        1. Page dates may be strings (from frontmatter) or datetime objects
        2. Timezone-aware datetimes need conversion to naive for comparison
        3. Missing dates should be handled gracefully

        Normalization Process:
        - Parse string dates using dateutil (handles various formats)
        - Copy datetime objects to avoid modifying originals
        - Strip timezone info for consistent comparison
        - Return original value if not a datetime object

        Args:
            page: The Page object containing date information

        Returns:
            datetime: Timezone-naive datetime for sorting, or original value
        """
        date = getattr(page, "date")
        _date = dateparse.parse(date) if isinstance(date, str) else copy.copy(date)
        return _date.replace(tzinfo=None) if isinstance(_date, datetime.datetime) else _date

    def _sort_key(self, key: str | list[str]) -> Callable:
        """
        Dynamically generate the sorting key

        :param key: The key to use
        """
        if isinstance(key, str):
            return self._date_key if key == "date" else lambda page: getattr(page, key)
        return lambda page: [getattr(page, attr) for attr in key]

    @property
    def sorted_pages(self):
        """
        Returns pages in the collection sorted by the `self.sort_by` attribute.

        Exceptions:
            AttributeError: This is raised when the attribute is missing from one or more pages
            TypeError: This happens when the values being compared are of two different types

        """
        try:
            return sorted(
                (page for page in self.__iter__()),
                key=self._sort_key(self.sort_by),
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

        # Archive Generation Logic:
        # 1. Get all sorted pages from the collection
        # 2. If pagination is enabled (items_per_page set), split into chunks
        # 3. Create Archive objects for each page group
        # 4. First archive is the main index, others are paginated pages

        sorted_pages = list(self.sorted_pages)
        items_per_page = getattr(self, "items_per_page", len(sorted_pages))
        archives = [sorted_pages]  # Start with all pages as first archive

        if items_per_page != len(sorted_pages):
            # Pagination enabled: split sorted pages into chunks
            paginated_archives = list(batched(sorted_pages, items_per_page))
            archives.extend(paginated_archives)
            self.template_vars["num_of_pages"] = len(paginated_archives)
        else:
            # No pagination: single archive with all pages
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

    def render(self) -> None:
        """
        Render all pages in the collection, including archives and feeds.

        Rendering Process:
        1. Iterate through each page in the collection
        2. Set up page-specific plugin manager (inherits from collection)
        3. Establish site reference for cross-page linking
        4. Render each page to its specified routes
        5. Generate and render archive pages if pagination is enabled
        6. Generate and render RSS/Atom feeds if configured

        Plugin Inheritance:
        - Each page gets a copy of the collection's plugin manager
        - Collection plugins override site-level plugins
        - Page-specific plugins can further override collection plugins
        """
        # Render individual pages
        for entry in self:
            entry.plugin_manager = copy.deepcopy(self.plugin_manager)

            for route in entry.routes:
                entry.site = self.site
                entry.render(route, self.site.theme_manager)

        if getattr(self, "has_archive", False):
            for archive in self.archives:
                archive.site = self.site
                logging.debug("Adding Archive: %s", archive.__class__.__name__)

                for _ in self.routes:
                    archive.render(self.routes[0], self.site.theme_manager)

                if archive.is_index:
                    archive.slug = "index"
                    archive.render(self.routes[0], self.site.theme_manager)
        feed: RSSFeed
        if hasattr(self, "Feed"):
            feed = self.feed
            feed.site = self.site
            feed.render(route="./", theme_manager=self.site.theme_manager)


def render_archives(archive, **kwargs) -> list[Archive]:
    return [archive.render(pages=archive.pages, **kwargs) for archive in archive]
