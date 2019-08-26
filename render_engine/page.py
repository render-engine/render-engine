from pathlib import Path
from markdown import markdown
from jinja2 import Markup
import maya
import re
import shlex
import subprocess
import logging
from typing import (
        Optional,
        Union,
        )


class Page():
    """Base component used to make web pages"""
    def __init__(
            self,
            *,
            slug,
            content: Optional[str]=None,
            content_path: Optional[Union[str, Path]]=None,
            template: Optional[Union[str, Path]]=None,
            extension: str=".html",
            **kwargs,
            ):
        """
        initializes a new Page object
        --------
        extension = tells the Engine what extension to use when creating the page
        template = the template filepath that the engine will use to build the page
        content = the data that will be used to create a page object
        content_path = filepath to get content and attributes. Attributes added
        to kwargs
        html = rendered html (not marked up)
        **kwargs = accepts any kwargs and saves them as properties to be used
        in templates.
        """
        self.slug = slug
        self.extension = extension
        self.content = content

        """
        # Set Content from content and/or content_path
        self.content_path = content_path if content_path else None

        if self.content_path:
            content = Path(self.content_path).read_text()

        _ = load_content(content)

        kwargs.update(_['attrs'])
        self.content = _.get('content', None)
        self.template = template

        # make properties for all attrs
        for key, attr in kwargs.items():
            setattr(self, key, attr)

        if self.content:
            self.markup = Markup(markdown(self.content))
        """

def load_content(content):
    matcher = r'^\w+:'
    md_content = content.splitlines()
    attrs = {}

    if md_content:
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
