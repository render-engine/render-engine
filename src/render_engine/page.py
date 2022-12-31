import logging
from pathlib import Path
from typing import Generator, Type

import frontmatter
import jinja2
from markdown2 import markdown
from slugify import slugify

from .parsers.base_parsers import BasePageParser
from .parsers.markdown import MarkdownParser

_route = Path | str


class Page:
    """The base object used to make web pages.
    Pages can be rendered directly from a template or generated from a file.

    !!! note

        Not all attributes are defined by default (those that are marked *optional*) but
        will be checked for in other areas of the code.

    When you create a page, you can specify variables that will be passed into rendering template.

    Attributes:

    """

    # TODO: REMOVE THIS
    # markdown: str | None = None
    # """This is base markdown that will be used to render the page.

    # !!! warning

    #     This will be overwritten if a `content_path` is provided.
    # """

    content: str | None
    content_path: _route | None
    """
    The path to the file that will be used to generate the page.

    !!! note

        This overrides the `content` attribute.
    """

    extension: str = ".html"
    """Extension to use for the rendered page output."""
    engine: jinja2.Environment
    reference: str = "slug"
    routes: list[_route] = ["./"]
    template: str | None
    Parser: Type[BasePageParser] = MarkdownParser

    def __init__(self) -> None:
        """Set Attributes that may be passed in from collections"""
        self.parser = self.Parser(self)  # This only pulls the configuration values
        if hasattr(self, "content_path"):
            valid_attrs, self.content = self.parser.attrs_from_content_path(
                content_path=self.content_path
            )

        elif hasattr(self, "content"):
            valid_attrs, self.content = self.parser.attrs_from_content(
                content=self.content
            )

        else:
            valid_attrs = {}

        for name, value in valid_attrs.items():
            # comma delimit attributes using list_attrs.
            if name.lower() in getattr(self, "list_attrs", []):
                value = [attrval.lower() for attrval in value.split(", ")]

            setattr(self, name.lower(), value)

        if not hasattr(self, "title"):
            # If no title is provided, use the class name.
            self.title = self.__class__.__name__
            logging.info(f"No Title. Assigning {self.title=}")

        if not hasattr(self, "slug"):
            # If no slug is provided, use the title.
            logging.info(f"No slug. Will slugify {self.title=}")
            self.slug = self.title  # Will Slugify in Next Step

        # Slugify the slug
        self.slug = slugify(self.slug)

    @property
    def url(self) -> str:
        """The first route and the slug of the page."""
        return f"{self.slug}{self._extension}"

    @property
    def _extension(self) -> str:
        """Ensures consistency on extension"""
        if not self.extension.startswith("."):
            return f".{self.extension}"
        else:
            return self.extension

    @property
    def url_for(self):
        """Returns the url for the page"""
        return self.slug

    def __str__(self):
        return self.slug

    def __repr__(self) -> str:
        return f"<Page {self.title}>"

    @property
    def markup(self) -> str:
        """Returns the markup of the page"""
        if hasattr(self, "content"):
            return self.parser.parse(self.content)

    def _render_content(
        self, engine: jinja2.Environment | None = None, **kwargs
    ) -> str:
        """Renders the content of the page."""
        engine = getattr(self, "engine", engine)

        # Parsing with a tmeplate
        if self.template and engine:
            logging.debug(f"Using %s for %s", self.template, self)

            if hasattr(self, "content"):
                """Content should be converted to before being passed to the template"""
                return engine.get_template(self.template).render(
                    **{
                        **self.__dict__,
                        **{"content": self.markup},
                        **kwargs,
                    },
                )

            else:
                return engine.get_template(self.template).render(
                    **{**self.__dict__, **kwargs},
                )

        # Parsing without a template
        elif hasattr(self, "content"):
            logging.debug(
                "content found. rendering with content: %s",
                self.content,
            )
            return self.markup

        else:
            raise ValueError(f"{self=} must have either content or template")
