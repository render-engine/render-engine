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

    Attributes:
        extension : str
            the extension to use in the rendered files
            default '.html'
    """

    extension: str = ".html"
    template_path = "templates"

    @property
    def environment(self):
        """The jinja2 environment class that controls which templates should be called and applied."""

        return jinja2.Environment(
            autoescape=select_autoescape(), loader=FileSystemLoader(self.template_path)
        )

    def get_template(self, template: str):
        """fetches the requested template from the environment. Purely a
        convenience method

        Parameters:
            template : str
                the name of the file to look for
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
            page : Page
                the page object to render into html
            template :
                the name of a template to render
            kwargs : any
                values that would be passed into the called template. If no template value
        """

        if (_template := template or page.template) :
            template = self.get_template(_template)
            return template.render(**kwargs)

        else:
            return page.content
