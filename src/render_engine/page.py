import logging
import re
from pathlib import Path
from typing import Type

import chevron
import jinja2
import pluggy
from slugify import slugify

from .parsers.base_parsers import BasePageParser

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

    content: str | None
    content_path: str | None
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
    invalid_attrs: list[str] = ["slug"]
    Parser: Type[BasePageParser] = BasePageParser

    def __init__(
        self,
        content: str | None = None,
        content_path: str | None = None,
        Parser: Type[BasePageParser] | None = None,
        pm: pluggy.PluginManager | None = None,
    ) -> None:
        """Set Attributes that may be passed in from collections"""

        if Parser:
            self.Parser = Parser

        if content_path := (content_path or getattr(self, "content_path", None)):
            content = self.Parser.parse_content_path(content_path)

        if content := (content or getattr(self, "content", None)):
            attrs, self.content = self.Parser.parse_content(content)
            self._replace_internal_references()

        else:
            attrs = {}

        invalid_attrs = getattr(self, "invalid_attrs") or []

        for name, value in attrs.items():
            # comma delimit attributes using list_attrs.
            name = name.lower()

            if name in invalid_attrs:
                logging.debug(f"{name=} is not a valid attribute. Setting to _{name}")
                name = f"_{name}"

            setattr(self, name, value)

        if pm:
            pm.hook.post_build_page(page=self)

    @property
    def title(self) -> str:
        # If no title is provided, use the class name.
        if not hasattr(self, "_title"):
            return self.__class__.__name__
        return self._title

    @title.setter
    def title(self, value: str) -> str:
        self._title = value
        return self._title

    @property
    def slug(self) -> str:
        if slug := getattr(self, "_slug", None):
            return slugify(slug)
        return slugify(self.title)

    @slug.setter
    def slug(self, value: str) -> str:
        self._slug = slugify(value)

    @property
    def url_for(self) -> str:
        """Returns the URL for the page"""
        if (route := self.routes[0]) == "./":
            return f"/{self.slug}{self._extension}"
        else:
            return f"/{route}/{self.slug}{self._extension}"

    @property
    def url(self):
        """Returns the URL for the page"""
        return f"{self.slug}{self._extension}"

    @property
    def path(self) -> str:
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
    def to_dict(self):
        """Returns a dict of the page's attributes"""
        return {
            **vars(self),
            **getattr(self, "template_vars", {}),
            "title": self.title,
            "slug": self.slug,
        }

    def __str__(self):
        return self.slug

    def __repr__(self) -> str:
        return f"<Page {self.title}>"

    @property
    def markup(self) -> str:
        """Returns the markup of the page"""
        if hasattr(self, "content"):
            return self.Parser.markup(self, self.content)

    def _render_content(
        self, engine: jinja2.Environment | None = None, **kwargs
    ) -> str:
        """Renders the content of the page."""
        engine = getattr(self, "engine", engine)

        # Parsing with a template
        if hasattr(self, "template") and engine:
            if hasattr(self, "content"):
                """Content should be converted to before being passed to the template"""
                return engine.get_template(self.template).render(
                    **{
                        **self.to_dict,
                        **{"content": self.markup},
                        **kwargs,
                    },
                )

            else:
                template = engine.get_template(self.template)
                content = template.render(
                    **{**self.to_dict, **kwargs},
                )
                return content

        # Parsing without a template
        elif hasattr(self, "content"):
            return self.markup

        else:
            raise ValueError(f"{self=} must have either content or template")

    def _replace_internal_references(self):
        """Finds the curly boys in the content and replaces them with the correct value"""

        return chevron.render(self.content, vars(self))
