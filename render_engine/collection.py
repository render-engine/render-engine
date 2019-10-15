import json
import logging
from collections import defaultdict
from itertools import zip_longest
from pathlib import Path
from typing import Optional, Sequence, Type, Union

from render_engine.page import Page

PathString = Union[str, Type[Path]]

class Collection:
    """
    Create a Collection of Similar Page Objects

    include: Sequence=['*.md', '*.html'] - list of patterns to include from the
        content path. Uses the syntax as defined in pathlib.Path.glob

    exclude: Optional[Sequence]=None - pattern to exclude from the content_path
        same as include=["!<PATTERN>"]

    template: Optional[Union[str, Type[Path]]=None - the template file that the
        engine will use to build the page (default: None). This will be assigned
        to the iterated pages but not any associated files.

    index_template: Optional[Union[str, Type[Path]]=None the template file that
        will be used to create an index for the pages.

    no_index: bool=False

    content_path = filepath to get content and attributes from if not content.
        attributes will be saved as properties. (defined by load_page_from_file) else None.

    default_content_type: Type[Page]

    template_vars: dict={}

    index_template_vars: dict={}
    """
    _default_sort_field = 'title'
    _reverse_sort = False
    _includes = ['*.md', '*.txt', '*.html']
    _pages = set()
    content_path = None

    def __init__(
            self,
            *,
            title: str='',
            content_path: Optional[PathString]=None,
            page_content_type: Type[Page]=Page,
            pages: [Sequence]=[],
            recursive: bool=False,
            ):
        """initialize a collection object"""
        self.recursive = recursive
        self.page_content_type = page_content_type

        if content_path:
            self.content_path = Path(content_path)

        self._pages = set(pages)

    @property
    def pages(self):
        if self._pages:
            return self._pages

        elif self.content_path:
            # ** is equivalent to rglob
            glob_start = '**' if self.recursive else ''
            globs = [self.content_path.glob(f'{glob_start}{x}') for x in
                    self.includes]


            for glob in globs:
                for page in glob:
                    p = self.page_content_type(content_path=page)
                    pages.add(p)

            self._pages = pages
            return pages

        else:
            return set()

    def add(self, *pages):
        pages = filter(lambda p: isinstance(p, self.page_content_type), pages)
        self._pages.add(pages)
        return self.pages

    @property
    def _iterators(self):
        return self.pages

    def __iter__(self):
        return self._pages

    def __len__(self):
        return len(self._pages)
