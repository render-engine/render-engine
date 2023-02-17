import logging
import typing
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
        content_path: The path to the file that will be used to generate the Page's `content`.
        raw_content: The base content of the page. This content will be passed into the page's Plugin Manager's `render_page_content` hook.
        extension: The suffix to use for the page. Defaults to `.html`.
        engine: If present, the engine to use for rendering the page. **This is normally not set and the `Site`'s engine will be used.**
        reference: Used to determine how to reference the page in the `Site`'s route_list. Defaults to `slug`.
        routes: The routes to use for the page. Defaults to `["./"]`.
        template: The template used to render the page. If not provided, the `Site`'s `content` will be used.
        invalid_attrs: A list of attributes that are not valid for the page. Defaults to `["slug", "content"]`. See [Invalid Attrs][invalid-attrs].
        collection_vars: A dictionary of variables passed in from a collection. See [Collection Vars][collection-vars].
        Parser: The parser to generate the page's `raw_content`. Defaults to `BasePageParser`.
        title: The title of the page. Defaults to the class name.

    """

    content_path: str | None
    raw_content: str | None
    extension: str = ".html"
    engine: jinja2.Environment
    reference: str = "slug"
    _pm: pluggy.PluginManager
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
        """
        The title of the Page
        If no title is provided, use the class name.
        """
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
        """
        Returns the URL for the page including the first route.

        Pages don't have access to the `Site` so this is the best way to get a valid URL for a page.

        This is the preferred way to reference a page inside of a template.
        """
        if (route := self.routes[0]) == "./":
            return f"/{self.slug}{self._extension}"
        else:
            return f"/{route}/{self.slug}{self._extension}"

    @property
    def url(self):
        """
        Returns the [`url_for`][src.render_engine.page.Page.url_for] for the page including the first route.
        """
        return self.url_for

    @property
    def _extension(self) -> str:
        """Ensures consistency on extension"""
        if not self.extension.startswith("."):
            return f".{self.extension}"
        else:
            return self.extension

    @property
    def to_dict(self):
        """
        Returns a dict of the page's attributes.

        This is often used to pass attributes into the page's `template`.

        """
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
