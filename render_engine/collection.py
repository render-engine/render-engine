from typing import (
    Optional,
    Type,
    Union,
    Sequence,
    )
from collections import defaultdict
from itertools import zip_longest
from render_engine.page import Page
from pathlib import Path
import json
import logging

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

    def __init__(
            self,
            *,
            includes: Sequence=['*.md', '*.html'],
            excludes: Optional[Sequence]=None,
            template: Optional[PathString]=None,
            content_path: Optional[PathString]=None,
            page_content_type: Type[Page]=Page,
            template_vars: Optional[dict]=None,
            pages: Optional[Sequence]=None,
            recursive: bool=False,
            # Index properties
            index_name: Optional[str]=None,
            index_template: Optional[PathString]=None,
            index_page_content_type: Type[Page]=Page,
            index_template_vars: Optional[dict]=None,
            ):
        """initialize a collection object"""

        self.template = template
        self.template_vars = template_vars or {}
        self.pages = set(pages) if pages else set()

        if content_path:
            self.content_path = Path(content_path)

            if excludes:
                includes = [f'!{x}' for x in excludes]

            glob_start = '**' if recursive else ''

            # This will overwrite any pages that are called
            globs = [self.content_path.glob(f'{glob_start}{x}') for x in
                    includes]

            for glob in globs:
                for page in glob:
                    self.pages.add(
                        page_content_type(
                            content_path=page,
                            template=template,
                            ),
                        )

        self.index_name = index_name
        self.index_template = index_template
        self.index_template_vars = index_template_vars
        self.index_page_content_type = index_page_content_type


    @property
    def index(self):
        if self.index_name:
            return self.index_page_content_type(
                    slug=self.index_name,
                    template=self.index_template,
                    pages=self.pages)
        else:
            return None

    def __iter__(self):
        return self.pages

    def __len__(self):
        return len(self.pages)
