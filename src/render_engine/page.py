import logging
from pathlib import Path
from typing import Type

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

    content_path: str | None
    """
    The path to the file that will be used to generate the page.

    !!! note

        This overrides the `content` attribute.
    """

    extension: str = ".html"
    engine: jinja2.Environment
    reference: str = "slug"
    routes: list[_route] = ["./"]
    template: str | jinja2.Template
    invalid_attrs: list[str] = ["slug", "content"]
    collection_vars: dict | None
    Parser: Type[BasePageParser] = BasePageParser

    def __init__(
        self,
        pm: pluggy.PluginManager,
        content: str | None = None,
        content_path: str | None = None,
        Parser: Type[BasePageParser] | None = None,
    ) -> None:
        """
        Set Attributes that may be passed in from collections.
        """

        if Parser:
            self.Parser = Parser

        if content_path := (content_path or getattr(self, "content_path", None)):
            content = self.Parser.parse_content_path(content_path)

        if content := (content or getattr(self, "content", None)):
            attrs, self.raw_content = self.Parser.parse_content(content)

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

        self._pm = pm

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
    def slug(self, value: str) -> None:
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
    def content(self):
        """Returns the markup of the page"""
        if self.raw_content:
            self._pm.hook.pre_render_content(page=self)
            return self.Parser.markup(content=self.raw_content, page=self)
        else:
            return ""

    def _render_content(self, engine: jinja2.Environment | None = None, **kwargs):
        """Renders the content of the page."""
        engine = getattr(self, "engine", engine)

        # Parsing with a template
        if hasattr(self, "template") and engine:

            # content should be converted to before being passed to the template
            if hasattr(self, "raw_content"):
                return engine.get_template(self.template).render(
                    **{
                        **self.to_dict,
                        **{"content": self.content},
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
        elif hasattr(self, "raw_content"):
            return self.content

        else:
            raise ValueError(f"{self=} must have either content or template")
