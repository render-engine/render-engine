import re
from pathlib import Path
from typing import Optional, Union

from jinja2 import Markup
from markdown import markdown

from .helpers import PathString


class Page:
    """Base component used to make web pages"""

    def __init__(self, content_path: Type[PathString]):
        content = Path(content_path).read_text()
        md_content = content.splitlines(keepends=True)
        matcher = r"^\w+:"

        while re.match(matcher, md_content[0]):
            line = md_content.pop(0)
            line_data = line.split(": ", 1)
            key = line_data[0].lower()
            value = line_data[-1].rstrip()
            setattr(self, key, value)

        self.content = "".join(md_content)

    @property
    def html(self):
        """the text from self._content converted to html"""
        return markdown(self.content)

    @property
    def content(self):
        """html = rendered html (not marked up). Is None if content is none"""
        return Markup(self.html)
