import logging
from pathlib import Path
from typing import Optional, Sequence, Type

import jinja2
from jinja2 import FileSystemLoader, select_autoescape

from .page import Page

class Engine:
    """This is the engine that is builds your static site.
    Use `Engine.run()` to output the files to the designated output path."""

    extension: str = ".html"
    environment = jinja2.Environment(
            autoescape=select_autoescape(),
            loader=FileSystemLoader('templates'),
            )

    def get_template(self, template: str):
        return self.environment.get_template(template)

    def render(self, page: Type[Page], **kwargs):
        if page.template:
            template = self.get_template(page.template)
            kwargs.update({'content': page.content})
            kwargs.update(page.__dict__)

            return template.render(**kwargs)

        else:
            return page.content
