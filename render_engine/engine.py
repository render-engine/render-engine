import logging
import os
import shutil
from pathlib import Path
from typing import Optional, Sequence, Type
from .helpers import PathString

from jinja2 import FileSystemLoader, select_autoescape
import jinja2

from .page import Page

# Currently all of the Configuration Information is saved to Default
logging.basicConfig(level=os.environ.get("LOGGING_LEVEL", logging.WARNING))


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

    def get_template(self, template):
        return self.environment.Template(template)

    def render(self, page):
        if page.template:
            template = self.get_template(template)
            kwargs = {'content': page.content}
            kwargs.update(page.__dict__)
            return template.render(**kwargs)

        else:
            return page.content
