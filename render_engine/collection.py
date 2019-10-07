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
            include: Sequence=['*.md', '*.html'],
            exclude: Optional[Sequence]=None,
            template: Optional[PathString]=None,
            index_template: Optional[PathString]=None,
            index_page: bool=True,
            content_path: Optional[PathString]=None,
            page_content_type: Type[Page]=Page,
            template_vars: dict={},
            index_template_vars: dict={},
            pages: Sequence=[],
            recursive: bool=False,
            ):
        """initialize a collection object"""

        self.template = template
        self.template_vars = template_vars
        self.pages = pages

        if index_page:
            self.index_template = index_template
            self.index_template_vars = index_template_vars


        if content_path:
            if exclude:
                include = list(map(lambda x: f'!{x}', exclude))

            glob_start = '**' if recursive else ''
            logging.debug(f'filetypes - {include}')

            for extension in include:
                content_pages= list(
                        Path(content_path)\
                                .glob(f'{glob_start}{extension}')
                                )
                logging.info(content_pages)
                for page in content_pages:
                    p = page_content_type(
                                content_path=page,
                                template=template
                                )
                    self.pages.append(p)

    def __iter__(self):
        return self.pages

    def __len__(self):
        return len(self.pages)
