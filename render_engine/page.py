import logging
import os
import re
import typing
from pathlib import Path

from jinja2 import Markup
from markdown import markdown

from ._type_hint_helpers import PathString


class Page:
    """Base component used to make web pages"""
    engine: str = ""
    template: str = ""
    match_param: str = r'(^\w+: \b.+$)'
    routes: typing.List = [""]

    def __init__(self, content_path=None):
        """If a content_path exists, check the associated file, processing the
        vars at the top and restitching the remaining lines"""

        if content_path:
            content = Path(content_path).read_text()
            parsed_content = re.split(self.match_param, content, flags=re.M)
            logging.debug(f'{parsed_content=}')
            self._content = parsed_content.pop().strip()
            logging.debug(f'{self._content=}')
            valid_attrs = (x for x in parsed_content if x.strip('\n'))
            logging.debug(valid_attrs)
            # We want to allow leading spaces and tabs so only strip new-lines

            for attr in valid_attrs:
                logging.debug(attr)
                name, value = attr.split(': ')
                logging.debug(f'{name=}, {value=}')
                setattr(self, name.lower(), value.strip())

    def __str__(self):
        if hasattr(self, "slug"):
            string = self.slug

        elif hasattr(self, "title"):
            string = self.title

        else:
            string = self.__class__.__name__

        return string.lower().replace(' ', '_')

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
