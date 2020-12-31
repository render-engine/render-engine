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

    def render(
        self,
        page: typing.Type[Page],
        template: typing.Optional[str] = None,
        **kwargs,
    ):
        """generate rendered HTML from from the called template

        This is what builds the pages into HTML.

        If a template attribute is defined or passed in then load the template and return the output. Otherwise return the content as HTML.

        Parameters:
            page :
                the page object to render into html
            template :
                the name of a template to render
            kwargs :
                values that would be passed into the called template. If no template value
        """

        if (_template := template or page.template) :
            template = self.get_template(_template)
            return template.render(**kwargs)

        else:
            return page.content
