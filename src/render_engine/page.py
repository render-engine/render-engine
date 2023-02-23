from typing import Any, Type

import jinja2

from ._base_object import BaseObject
from .hookspecs import register_plugins
from .parsers.base_parsers import BasePageParser


class BasePage(BaseObject):
    """
    This is the Base Page object.

    It was created to allow for the creation of custom page objects.

    This is not intended to be used directly.

    Attributes:
        slug: The slug of the page. Defaults to the `title` slugified.
        content: The content to be rendered by the page
        parser: The Parser used to parse the page's content. Defaults to `BasePageParser`.

    """

    extension: str = ".html"
    routes: list[str] = ["./"]
    template: str | type[jinja2.Template] | None
    reference: str = "_slug"

    @property
    def _content(self):
        """Returns the content of the page."""
        return getattr(self, "content", None)

    @property
    def _extension(self) -> str:
        """Ensures consistency on extension"""
        if not self.extension.startswith("."):
            return f".{self.extension}"
        return self.extension

    def url_for(self) -> str:
        """
        Returns the URL for the page including the first route.

        Pages don't have access to the `Site` so this is the best way to get a valid URL for a page.

        This is the preferred way to reference a page inside of a template.
        """
        if (route := self.routes[0]) == "./":
            return f"/{self.path_name}"
        else:
            return f"/{route}/{self.path_name}"

    def _render_from_template(self, template: jinja2.Template, **kwargs) -> str:
        """Renders the page from a template."""
        return template.render(
            **{
                **self.to_dict(),
                **{"content": self._content},
                **kwargs,
            },
        )

    def _render_content(self, engine: jinja2.Environment | None = None, **kwargs):
        """Renders the content of the page."""
        engine = getattr(self, "engine", engine)
        template = getattr(self, "template", None)

        # Parsing with a template
        if template and engine:
            template = engine.get_template(template)
            return self._render_from_template(template, **kwargs)

        # Parsing without a template
        try:
            return self._content

        except AttributeError:
            raise AttributeError(
                f"{self} does not have a content attribute. "
                "You must either provide a template or content."
            )

    def __str__(self):
        return self._slug

    def __repr__(self) -> str:
        return f"<Page: {self._title}>"


class Page(BasePage):
    """
    The general BasePage object used to make web pages.

    Pages can be rendered directly from a template or generated from a file.

    !!! note

        Not all attributes are defined by default (those that are marked *optional*) but
        will be checked for in other areas of the code.

    When you create a page, you can specify variables that will be passed into rendering template.

    Attributes:
        content_path: The path to the file that will be used to generate the Page's `content`.
        extension: The suffix to use for the page. Defaults to `.html`.
        engine: If present, the engine to use for rendering the page. **This is normally not set and the `Site`'s engine will be used.**
        reference: Used to determine how to reference the page in the `Site`'s route_list. Defaults to `slug`.
        routes: The routes to use for the page. Defaults to `["./"]`.
        template: The template used to render the page. If not provided, the `Site`'s `content` will be used.
        invalid_attrs: A list of attributes that are not valid for the page. Defaults to `["slug", "content"]`. See [Invalid Attrs][invalid-attrs].
        Parser: The parser to generate the page's `raw_content`. Defaults to `BasePageParser`.
        title: The title of the page. Defaults to the class name.

    """

    content: Any
    content_path: str | None
    Parser: Type[BasePageParser] = BasePageParser
    plugins: list[callable] | None
    inherit_plugins: bool

    def __init__(
        self,
        content_path: str | None = None,
        content: Any | None = None,
        Parser: Type[BasePageParser] | None = None,
        plugins: list = [],
    ) -> None:

        if Parser:
            self.Parser = Parser

        # Parse Content from the Content Path or the Content
        if content_path := (content_path or getattr(self, "content_path", None)):
            attrs, self.content = self.Parser.parse_content_path(content_path)

        elif content := (content or getattr(self, "content", None)):
            attrs, self.content = self.Parser.parse_content(content)

        else:
            attrs = {}
            self.content = None

        # Set the attributes
        for key, val in attrs.items():
            setattr(self, key.lower(), val)

        # Set the plugins
        self.plugins = [*getattr(self, "plugins", []), *plugins]
        self.PM = register_plugins(self.plugins)
        self.PM.hook.render_content(Page=self)

    @property
    def _content(self):
        """Returns the content of the page."""
        return self.Parser.parse(self.content, page=self)
