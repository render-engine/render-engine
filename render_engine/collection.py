import itertools
import typing
from pathlib import Path

from more_itertools import chunked

from .feeds import RSSFeed
from .page import Page


class Archive(Page):
    """Custom Page object used to make archive pages"""

    def __init__(self, /, pages: list, template: str, **kwargs) -> None:
        """Create a `Page` object for the pages in the collection"""
        super().__init__(**kwargs)
        self.pages = pages
        self.template = template


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
    content_path: Path
    content_type: Page = Page
    template: typing.Optional[str] = None
    includes: list[str] = ["*.md", "*.html"]
    subcollections: list[str] = list
    markdown_extras = ["fenced-code-blocks", "footnotes"]
    items_per_page: typing.Optional[int] = None
    sort_by: str = "title"
    sort_reverse: bool = False
    has_archive: bool = False
    archive_template: typing.Optional[str] = None

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        if not hasattr(self, "title"):
            self.title = self.__class__.__name__

        if any([self.items_per_page, self.archive_template]):
            self.has_archive == True

    @property
    def collection_vars(self):
        return {f"collection_{key}": val for key, val in vars(self).items()}

    @property
    def pages(self):
        if Path(self.content_path).is_dir():

            pages = self._pages(self.content_type)

            return pages
        else:
            raise ValueError(f"invalid {Path=}")

    def _pages(self, content_type: Page, **kwargs) -> list[Page]:
        page_groups = map(
            lambda pattern: Path(self.content_path).glob(pattern), self.includes
        )

        return [
            content_type(
                content_path=page_path,
                template=self.template,
                **self.collection_vars,
                **kwargs,
            )
            for page_path in itertools.chain.from_iterable(page_groups)
        ]

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
        if not self.items_per_page:
            return [
                Archive(
                    pages=self.sorted_pages,
                    template=self.archive_template,
                    title=self.title,
                )
            ]

        page_chunks = enumerate(chunked(self.sorted_pages, self.items_per_page))
        return [
            Archive(
                pages=pages,
                template=self.archive_template,
                slug=f"{self.title}_{i}",
                title=self.title,
            )
            for i, pages in page_chunks
        ]

    def render_archives(self, **kwargs) -> list[Archive]:
        return [
            archive.render(pages=archive.pages, **kwargs) for archive in self.archives
        ]

    def render_feed(self, feed_type: RSSFeed, **kwargs) -> RSSFeed:
        return RSSFeed(pages=self.pages, **kwargs)
