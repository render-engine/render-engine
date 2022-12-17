import itertools
import typing
from collections import defaultdict
from pathlib import Path

import jinja2
from more_itertools import chunked

from .page import Page


class Archive(Page):
    """Custom Page object used to make archive pages"""

    def __init__(self, /, pages: list, template: str, **kwargs) -> None:
        """Create a `Page` object for the pages in the collection"""
        super().__init__(**kwargs)
        self.pages = pages
        self.template = template


def gen_collection(
    pages: typing.Iterable[Page],
    template: jinja2.Template,
    title: str,
    items_per_page: typing.Optional[int] = None,
    routes: list[Path | str] = [],
) -> list[Archive]:
    """Returns a list of Archive pages containing the pages of data for each archive."""

    if not items_per_page:
        return [
            Archive(
                engine=template.environment,
                pages=pages,
                template=template,
                title=title,
                routes=routes,
            )
        ]

    page_chunks = chunked(pages, items_per_page)

    pages = [
        Archive(
            engine=template.environment,
            pages=pages,
            template=template,
            slug=f"{title}_{i}",
            title=title,
            routes=routes,
        )
        for i, pages in enumerate(page_chunks)
    ]
    return pages


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

        @site.register_collection
        class BasicCollection(Collection):
            pass
    """

    content_path: Path
    content_type: Page = Page
    template: typing.Optional[str] = None
    includes: list[str] = ["*.md", "*.html"]
    markdown_extras = ["fenced-code-blocks", "footnotes"]
    items_per_page: typing.Optional[int] = None
    sort_by: str = "title"
    sort_reverse: bool = False
    has_archive: bool = False
    archive_template: typing.Optional[str] = None
    subcollections: list[str | list[str]] = None
    routes = ["./"]

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        if not hasattr(self, "title"):
            self.title = self.__class__.__name__

        if any([self.items_per_page, self.archive_template]):
            self.has_archive is True
            self.archive_template = self.engine.get_template(self.archive_template)

            if hasattr(self, "subcollections") and not getattr(
                self, "subcollections_template", None
            ):
                self.subcollection_template = self.archive_template

        self.routes = [Path(route) for route in self.routes]

    @property
    def collection_vars(self):
        return {f"collection_{key}".upper(): val for key, val in vars(self).items()}

    @property
    def pages(self):
        if Path(self.content_path).is_dir():
            pages = self._pages(self.content_type, routes=self.routes)

            return pages
        else:
            raise ValueError(f"invalid {Path=}")

    def _pages(self, content_type: Page, **kwargs) -> list[Page]:
        page_groups = map(
            lambda pattern: Path(self.content_path).glob(pattern), self.includes
        )
        return [
            content_type(
                engine=self.engine,
                content_path=page_path,
                template=self.template,
                subcollections=getattr(self, "subcollections", []),
                subcollection_template=getattr(self, "subcollection_template", []),
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
        if self.has_archive:
            return gen_collection(
                pages=self.sorted_pages,
                template=self.archive_template,
                title=self.title,
                items_per_page=self.items_per_page,
                routes=self.routes,
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
