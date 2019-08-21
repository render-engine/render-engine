from pathlib import Path
from markdown import markdown
from jinja2 import Markup
import maya
import re
import shlex
import subprocess
import logging


class Page():
    """Base component used to make web pages"""
    def __init__(
            self,
            *,
            slug=None,
            content='',
            content_path=None,
            template=None,
            extension='.html',
            **kwargs,
            ):
        """
        initialize a new Page object
        --------
        - slug [string or pathlib.Path] (Required): the relative url for the Page.
        - content [string] (Optional): the raw content to be processed into html. Must have this or 'content_path'
        - content_path [string or pathlib.Path] (Optional): The path to the content file. Must have this or 'content'.
        - template [string or pathlib.Path] (Optional): The template file that will be used to generate an html file.
        - extension [string] (Optional, Default: html): used to tell what extension the markup file should have. Often used to make web-compatible non-html text files.
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

        # Set Slug of Page to slug or name or id or content_path name
        if not slug:
            slug = getattr(self, 'name', None) \
                or getattr(self, 'id', None) \
                or Path(getattr(self, 'content_path', '/')).stem()
        self.slug = slug

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
