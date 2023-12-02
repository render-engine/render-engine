import logging
import pathlib
import typing

import git
from more_itertools import batched, flatten
from slugify import slugify

from ._base_object import BaseObject
from .archive import Archive
from .feeds import RSSFeed
from .page import Page
from .parsers import BasePageParser
from .parsers.markdown import MarkdownPageParser
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
        Feed: Type[RSSFeed]
        feed_title: str
        include_suffixes: list[str] = ["*.md", "*.html"]
        items_per_page: int | None
        PageParser: Type[BasePageParser] = MarkdownPageParser
        parser_extras: dict[str, Any]
        required_themes: list[callable]
        routes: list[str] = ["./"]
        sort_by: str = "title"
        sort_reverse: bool = False
        title: str
        template: str | None

        archive_template str | None: The template to use for the archive pages.

    """

    archive_template: str | pathlib.Path = "archive.html"
    content_path: pathlib.Path | str
    content_type: Page = Page
    Feed: RSSFeed
    feed_title: str
    include_suffixes: list[str] = ["*.md", "*.html"]
    items_per_page: int | None
    PageParser: BasePageParser = MarkdownPageParser
    parser_extras: dict[str, any]
    required_themes: list[typing.Callable]
    routes: list[str] = ["./"]
    sort_by: str = "title"
    sort_reverse: bool = False
    template: str | None
    plugins: list[typing.Callable] | None
    plugin_manager: PluginManager | None

    def __init__(
        self,
    ) -> None:
        if getattr(self, "items_per_page", False):
            self.has_archive = True

        self.title = self._title

    def iter_content_path(self):
        """Iterate through in the collection's content path."""

        return flatten([pathlib.Path(self.content_path).glob(suffix) for suffix in self.include_suffixes])

    def _generate_content_from_modified_pages(self) -> typing.Generator[Page, None, None]:
        """
        Check git status for newly created and modified files.
        Returns the Page objects for the files in the content path
        """

        repo = git.Repo()

        changed_files = [
            *repo.untracked_files,  # new files not yet in git's index
            *repo.index.diff(),  # modified files in git index
        ]

        return (
            self.get_page(pathlib.Path(changed_path))
            for changed_path in changed_files
            if pathlib.Path(changed_path).parent == pathlib.Path(self.content_path)
        )

    def get_page(
        self,
        content_path: str | None = None,
    ) -> type[Page]:
        """Returns the page Object for the specified Content Path"""
        _page = self.content_type(
            content_path=content_path,
            Parser=self.PageParser,
        )

        if getattr(self, "_pm", None):
            _page.register_plugins(self.plugins)
        _page.parser_extras = getattr(self, "parser_extras", {})
        _page.routes = self.routes
        _page.template = getattr(self, "template", None)
        _page.collection = self.to_dict()
        return _page

    @property
    def sorted_pages(self):
        return sorted(
            (page for page in self.__iter__()),
            key=lambda page: getattr(page, self.sort_by, self._title),
            reverse=self.sort_reverse,
        )

    @property
    def archives(self) -> typing.Generator[Archive, None, None]:
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
        num_archive_pages = len(archives)

        for index, pages in enumerate(archives):
            yield Archive(
                pages=pages,
                template=getattr(self, "archive_template", None),
                title=self._title,
                routes=self.routes,
                archive_index=index,
                num_archive_pages=num_archive_pages,
                plugin_manager=getattr(self, "plugin_manager", None),
            )

    @property
    def feed(self):
        feed = self.Feed()
        feed.pages = [page for page in self]
        feed.title = getattr(self, "feed_title", self._title)
        feed.slug = self._slug
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
