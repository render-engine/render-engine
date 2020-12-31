import logging
import typing
from pathlib import Path

import jinja2
from jinja2 import FileSystemLoader, select_autoescape

from .page import Page


class Engine:
    """
    This is the jinja2 engine that is builds your static site.
    Use `Engine.run()` to output the files to the designated output path.
    """

    extension: str = ".html"
    """the extension to use in the rendered files"""

    template_path: Path = "templates"
    """the directory to find templates for :func:`render_engine.page.Page`-like objects"""

    @property
    def environment(self):
        """The jinja2 environment class that controls which templates should be called and applied."""

        return jinja2.Environment(
            autoescape=select_autoescape(), loader=FileSystemLoader(self.template_path)
        )

    def get_template(self, template: str):
        """fetches the requested template from the environment. Purely a
        convenience method
        """
        return self.environment.get_template(template)
