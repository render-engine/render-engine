import logging
import os
import re
import typing
from pathlib import Path

from jinja2 import Markup
from markdown import markdown

from ._type_hint_helpers import PathString

logging.basicConfig(level=logging.DEBUG, filename='page_creation.log')

class Page:
    """Base component used to make web pages"""

    engine: str = ""
    template: str = ""
    routes: typing.List = [""]
    match_param: str = r'(\w+: .+)'

    def __init__(self, content_path: PathString="") -> None:
        """If a content_path exists, check the associated file, processing the
        vars at the top and restitching the remaining lines"""

        if content_path:
            content = Path(content_path).read_text()
            parsed_content = re.split(self.match_param, content, flags=re.M)
            logging.debug(f'{parsed_content=}')
            self._content = parsed_content.pop().strip()
            logging.debug(f'{self._content=}')
            valid_attrs = filter(lambda x: x != '\n', parsed_content)

            for attr in valid_attrs:
                name, value = attr.split(': ')
                logging.debug(f'{name=}, {value=}')
                setattr(self, name.lower(), value.strip())

    @property
    def _slug(self):
        if hasattr(self, "slug"):
            return self.slug

        if hasattr(self, "title"):
            return self.title

        return self.__class__.__name__

    @property
    def html(self):
        """the text from self._content converted to html"""

        if hasattr(self, '_content'):
            return markdown(self._content)

        else:
            return ''

    @property
    def content(self):
        """html = rendered html (not marked up). Is None if content is none"""
        return Markup(self.html)

    def __str__(self):
        return self._slug
