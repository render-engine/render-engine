import itertools
import pdb
import typing
from collections import defaultdict, namedtuple
from pathlib import Path

import jinja2
from more_itertools import bucket, chunked

from .feeds import RSSFeed
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
) -> list[Archive]:
    """Returns a list of Archive pages containing the pages of data for each archive."""

    if not items_per_page:
        return [
            Archive(
                pages=pages,
                template=template,
                title=title,
            )
        ]

    page_chunks = chunked(pages, items_per_page)

    pages = [
        Archive(pages=pages, template=template, slug=f"{title}_{i}", title=title)
        for i, pages in enumerate(page_chunks)
    ]
    return pages


SubCollection = namedtuple("subcollection", ["key", "default"])


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

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        if not hasattr(self, "title"):
            self.title = self.__class__.__name__

        if any([self.items_per_page, self.archive_template]):
            self.has_archive == True

    @property
    def collection_vars(self):
        return {f"collection_{key}".upper(): val for key, val in vars(self).items()}

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

    def _gen_subpages(self, SubCollection) -> defaultdict[list[Page]]:
        """given a attribute, bucket all the pages into subcollections"""
        subpages = defaultdict(list)
        for page in self.pages:
            key = getattr(page, SubCollection.key, SubCollection.default)

            if SubCollection.key in getattr(page, "list_attrs", []):
                for k in getattr(page, SubCollection.key, []):
                    subpages[k].append(page)
            else:
                subpages[key].append(page)

        subcollection = []

        for k, v in subpages.items():
            subcollection.append(
                gen_collection(
                    pages=sorted(
                        v,
                        key=lambda page: getattr(page, self.sort_by),
                        reverse=self.sort_reverse,
                    ),
                    template=self.archive_template,
                    title=k,
                    items_per_page=self.items_per_page,
                )
            )
        return subcollection

    @property
    def archives(self) -> list[Archive]:
        """Returns a list of Archive pages containing the pages of data for each archive."""
        return gen_collection(
            pages=self.sorted_pages,
            template=self.archive_template,
            title=self.title,
            items_per_page=self.items_per_page,
        )

    # def render_feed(self, feed_type: RSSFeed, **kwargs) -> RSSFeed:
    #     return feed_type(pages=self.pages, **kwargs)

    def __repr__(self):
        return f"{self}: {__class__.__name__}"

    def __str__(self):
        return f"{self}: {__class__.__name__}"
