import os
import re
import typing
from pathlib import Path

from jinja2 import Markup
from markdown import markdown


class Page:
    """Base component used to make web pages"""

    engine: str = ""
    template: str = ""
    routes: typing.List = [""]

    def __init__(self, content_path: typing.Union[str, of.PathLike] = ""): -> None
        if content_path:
            content = Path(content_path).read_text()
            md_content = content.splitlines(keepends=True)
            matcher = r"^\w+:"

            while re.match(matcher, md_content[0]):
                line = md_content.pop(0)
                line_data = line.split(": ", 1)
                key = line_data[0].lower()
                value = line_data[-1].rstrip()
                setattr(self, key, value)

            self._content = "".join(md_content).strip()

        else:
            self._content = ""

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
        return markdown(self._content)

    @property
    def content(self):
        """html = rendered html (not marked up). Is None if content is none"""
        return Markup(self.html)
