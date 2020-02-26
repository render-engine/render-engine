import logging
from pathlib import Path
from typing import Optional, Sequence, Type

import jinja2
from jinja2 import FileSystemLoader, select_autoescape

from .page import Page


class Engine:
    """
    This is the engine that is builds your static site.
    Use `Engine.run()` to output the files to the designated output path.

    Attributes:
        extension : str
            the extension to use in the rendered files
            default '.html'
        environment : Any
            the environment renderer that you want to use. You can use any environment that you like. Environments
            should support a `get_template` and `render`

    Todos:
        * Create default template
        * Method to build template directory
    """

    extension: str = ".html"
    environment = jinja2.Environment(
        autoescape=select_autoescape(), loader=FileSystemLoader("templates")
    )

    def get_template(self, template: str):
        """
        fetches the requested template from the environment. Purely a
        convenience method

        Parameters:
            template : str
                the template file to look for
        """
        return self.environment.get_template(template)

    def render(self, page: Type[Page], **kwargs):
        """
        generates the rendered HTML from from environment

        Parameters:
            page : Page
                the page object to render into html
        """
        if page.template:
            template = self.get_template(page.template)
            kwargs.update({"content": page.content})
            kwargs.update(page.__dict__)

            return template.render(**kwargs)

        else:
            return page.content
