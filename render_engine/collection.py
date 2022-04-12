import collections
import logging
import typing
from pathlib import Path

import itertools
from more_itertools import chunked

from .feeds import RSSFeed
from .page import Page


class Archive(Page):
    """Custom Page object used to make archive pages"""

    template: str = "archive.html"

    def __init__(
            self, /, pages: list, **kwargs
        ) -> None:
        """Create a `Page` object for the pages in the collection"""
        super().__init__(**kwargs)
        self.pages = pages
 

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
    routes: list[str] = list
    subcollections: list[str] = list
    feeds: list[typing.Optional[RSSFeed]] = list
    markdown_extras = ["fenced-code-blocks", "footnotes"]
    items_per_page: typing.Optional[int] = None
    sort_by: str = 'title'
    sort_reverse: bool = False

    
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        if not hasattr(self, 'title'):
            self.title = self.__class__.__name__
        

    @property
    def collection_vars(self):
        return {f'collection_{key}': val for key, val in vars(self).items()}

    @property
    def pages(self):
        if Path(self.content_path).is_dir():
            page_groups = map(lambda pattern:Path(self.content_path).glob(pattern), self.includes)
            return {
                    page_path: Page(content_path=page_path, **self.collection_vars) 
                            for page_path in itertools.chain.from_iterable(page_groups)
                    }
        else:
            raise ValueError(f'invalid {Path=}')

    def render_pages(self, / , output_path, filenames: typing.Optional[typing.Sequence[Path]]=None):
        if filenames:
            return [page.render(output_path=output_path) for path, page in self.pages.items() if path in filenames]

        else:
            return [page.render(output_path=output_path) for page in self.pages.values()] 

    @property
    def sorted_pages(self):
        return sorted(self.pages.values(), key=lambda page: getattr(page, self.sort_by))

    @property
    def archives(self) -> list[Archive]:
        """Returns a list of Archive pages containing the pages of data for each archive."""
        if not self.items_per_page:
            return [Archive(pages=self.sorted_pages, title=self.title)]

        page_chunks = enumerate(chunked(self.sorted_pages, self.items_per_page))
        return [Archive(pages=pages, title=f"{self.title}_{i}") for i, pages in page_chunks]

    def render_archives(self, /, output_path: Path) -> list[Archive]:
        for archive in self.archives:
            archive.render(output_path=output_path)
