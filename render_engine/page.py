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
    """Base component used to make web pages
        content = the data that will be used to create a page object
        extension = tells the Engine what extension to use when creating the page
        html = rendered html (not marked up). Is None if content is none
        slug = the name of the document. Used as the filename of the output path
        template = the template filepath that the engine will use to build the
        page
        template_vars= accepts a dictionary and saves items as properties to be
        """
    def __init__(
            self,
            *,
            slug: str,
            content: Optional[str]=None,
            content_path: Optional[Union[str, Path]]=None,
            extension: str=".html",
            template: Optional[Union[str, Path]]=None,
            template_vars: Optional[dict]={},
            ):
        """
        initializes a new Page object
        --------
        content_path = filepath to get content and attributes. Attributes added
        to template_vars. Will overwrite content
        used in template rendering.
        """
        self.slug = slug
        self.extension = extension

        # Set Content from content and/or content_path
        if content_path:
            content = Path(content_path).read_text()

        if content:
            _ = load_content(content)
            template_vars.update(_['attrs'])
            content = _.get('content', None)

        self.content = content
        self.template = template
        self.template_vars = template_vars

    @property
    def html(self):
        if self.content:
            return markdown(self.content)

        else:
            return None


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
