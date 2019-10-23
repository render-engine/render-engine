import logging
from pathlib import Path
from typing import Optional, Sequence, Type

import jinja2
from jinja2 import FileSystemLoader, select_autoescape

from .page import Page

class Engine:
    """This is the engine that is builds your static site.
    Use `Engine.run()` to output the files to the designated output path."""

    def __init__(
            self,
            templates_path: str = "templates",
            extension: str = ".html",
            autoescape: Sequence = ["html"],
            ):
        self.environment = jinja2.Environment(
                loader=FileSystemLoader(templates_path),
                autoescape=select_autoescape(autoescape),
            )
        self.extension = extension

    def get_template(self, template: str):
        return self.environment.get_template(template)

    def render(self, page: Type[Page]):
        logging.debug(f'page - {page.__class__.__name__}')
        logging.debug(f'template - {page.template}')
        logging.debug(f'content - {page.content}')
        if page.template:
            template = self.get_template(page.template)
            kwargs = {'content': page.content}
            kwargs.update(page.__dict__)
            return template.render(**kwargs)

        else:
            return page.content
