from pathlib import Path
from typing import Any

from jinja2 import Environment, Template
from render_engine_parser.base_parsers import BasePageParser

from ._base_object import BaseObject


class BasePage(BaseObject):
    """
    This is the Base Page object.

    It was created to allow for the creation of custom page objects.

    This is not intended to be used directly.

    Attributes:
        slug (str): The slug of the page. Defaults to the `title` slugified.
        content: The content to be rendered by the page.
        parser: The Parser used to parse the page's content. Defaults to `BasePageParser`.
        reference: The attribute to use as the reference for the page in the site's route list.
            Defaults to `slug`.
        extension (str): The file extension for the page. Defaults to ".html".
        routes (list[str] | Path): The list of routes for the page. Defaults to ["./"].
        template (str | Template | None): The template to use for rendering the page.
    """

    extension: str = ".html"
    routes: list[str | Path] = ["./"]
    template: str | Template | None
    rendered_content: str | None
    _reference: str = "_slug"

    @property
    def _content(self) -> Any:
        """Returns the content of the page."""
        return getattr(self, "content", None)

    def url_for(self) -> str:
        """
        Returns the URL for the page including the first route.

        This gets the relative URL for a page.

        !!! note

            Pages don't have access to the `Site` attrs.
            You cannot get an abolute URL from a Page object.
            Use {{SITE_URL}} in your templates to get the absolute URL.


        This is the preferred way to reference a page inside of a template.
        """
        if (route := self.routes[0]) == "./":
            return f"/{self.path_name}"
        else:
            return f"/{route}/{self.path_name}"

    def _render_from_template(self, template: Template, **kwargs) -> str:
        """Renders the page from a template."""
        return template.render(
            **{
                **self.to_dict(),
                **{"content": self._content},
                **kwargs,
            },
        )

    def _render_content(self, engine: Environment | None = None, **kwargs) -> str:
        """
        Renders the content of the page.

        If there is not content or a template attribute, an error will be raised.
        """
        engine = getattr(self, "engine", engine)
        template = getattr(self, "template", None)

        # Parsing with a template
        if template and engine:
            template = engine.get_template(template)
            return self._render_from_template(template, **kwargs)

        # Parsing without a template
        try:
            if isinstance(self._content, str):
                return self._content

            else:
                raise ValueError(
                    f"Error rendering {self}. \
                                 The returned content attribute must be a string. Got {type(self._content)}"
                )

        except AttributeError:
            raise AttributeError(
                f"{self} does not have a content attribute. " "You must either provide a template or content."
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

    When you create a page, you specify variables passed into rendering template.

    Attributes:
        content_path:
            The path to the file that will be used to generate the Page's `content`.
        extension: The suffix to use for the page. Defaults to `.html`.
        engine:
            If present, the engine to use for rendering the page.

            !!! note
                **This is normally not set and the `Site`'s engine will be used.**

        reference:
            Used to determine how to reference the page in the `Site`'s route_list.
            Defaults to `slug`.
        routes: The routes to use for the page. Defaults to `["./"]`.
        template:
            The template used to render the page.
            If not provided, the `Site`'s `content` will be used.
        Parser:
            The parser to generate the page's `raw_content`.
            Defaults to `BasePageParser`.
        title: The title of the page. Defaults to the class name.

    """

    content: Any
    content_path: Path | str | None
    Parser: type[BasePageParser] = BasePageParser
    inherit_plugins: bool
    parser_extras: dict[str, Any] | None
    title: str

    def __init__(
        self,
        content_path: Path | str | None = None,
        content: Any | None = None,
        Parser: type[BasePageParser] | None = None,
    ) -> None:
        """
        Initializes a new Page object.

        Args:
            content_path (Path, str, optional): The path to the file that will be used to generate the Page's `content`.
            content (Any, optional): The content of the page.
            Parser (type[BasePageParser], optional): The parser to generate the page's `raw_content`.
                Defaults to `BasePageParser`.
        """
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

    @property
    def _content(self) -> Any:
        """
        Returns the parsed content of the page.

        Returns:
            Any: The parsed content of the page.
        """
        return self.Parser.parse(self.content, extras=getattr(self, "parser_extras", {}))
