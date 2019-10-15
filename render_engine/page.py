import logging
import re
import urllib.parse
from pathlib import Path
from typing import Optional, Union

import maya
from jinja2 import Markup
from markdown import markdown


class Page:
    """Base component used to make web pages"""
    def __init__(
            self,
            *,
            slug = '',
            title = '',
            content: str='',
            content_path: Optional[Union[str, Path]]=None
           ):
        """
        initializes a new Page object
        --------
        content = raw content to be loaded
        content_path = filepath to get content and attributes. Attributes added
        to template_vars.
        extension
        """
        self.title = title
        self.slug = slug

        if content_path:
           # content_path will always overwrite the content
           self.content_path = Path(content_path)
           content = content_path.read_text()

        loaded_content = self.load_content(content)
        for key, val in loaded_content['attrs'].items():
           setattr(self, key, val)

        self.content = loaded_content['content']

    @property
    def markup(self):
        """html = rendered html (not marked up). Is None if content is none"""
        return Markup(markdown(self.content))

    @staticmethod
    def load_content(content):
        matcher = r'^\w+:'
        md_content = content.splitlines()
        attrs = {}

        if len(md_content) > 1:
            while re.match(matcher, md_content[0]):
                line = md_content.pop(0)
                line_data = line.split(': ', 1)
                key = line_data[0].lower()
                value = line_data[-1].rstrip()
                attrs[key] = value

        return {
            'attrs': attrs,
            'content': '\n'.join(md_content).strip('\n'),
            }
