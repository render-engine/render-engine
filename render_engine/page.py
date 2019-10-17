import logging
import re
from pathlib import Path
from typing import Optional, Union

from jinja2 import Markup
from markdown import markdown

from .helpers import PathString


class Page:
    """Base component used to make web pages"""

    def __init__(
        self,
        *,
        content: Optional[str] = None,
        content_path: Optional[PathString] = None,
    ):
        """
        initializes a new Page object
        --------
        content = raw content to be loaded
        content_path = filepath to get content and attributes. Attributes added
        to template_vars.
        """

        if content and content_path:
            error_msg = "Supply either content or content_path. Not Both"
            raise AttributeError(error_msg)

        if content:
            self._content = content

        elif content_path:
            self._load_content(content_path.read_text())

        self.filename = self.__class__.__name__

    @property
    def _filename(self):
        return self.filename

    @property
    def html(self):
        """the text from self._content converted to html"""
        return markdown(self._content)

    @property
    def content(self):
        """html = rendered html (not marked up). Is None if content is none"""
        return Markup(self.content)

    def _load_content(self, content):
        matcher = r"^\w+:"
        md_content = content.splitlines(keepends=True)

        if len(md_content) > 1:
            while re.match(matcher, md_content[0]):
                line = md_content.pop(0)
                line_data = line.split(": ", 1)
                key = line_data[0].lower()
                value = line_data[-1].rstrip()
                setattr(self, key, value)

        self._content = "".join(md_content)
