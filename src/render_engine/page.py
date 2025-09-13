from pathlib import Path
from typing import Any

from jinja2 import Environment, Template
from render_engine_parser.base_parsers import BasePageParser

from render_engine.themes import ThemeManager

from ._base_object import BaseObject
from .plugins import PluginManager


class BasePage(BaseObject):
    """
    Base class for all page objects in Render Engine.

    This foundational class provides the core functionality for content pages,
    establishing the relationship between pages and the site rendering system.
    It should not be used directly - use the Page class instead.

    Architecture Role:
    - Represents individual content pieces that get rendered to specific URLs
    - Maintains a reference to the parent Site during rendering
    - Handles content parsing, template rendering, and URL generation
    - Supports plugin system integration for content modification

    Key Relationships:
    - Belongs to a Site (via site attribute set during rendering)
    - Uses a PluginManager for content processing hooks
    - Renders through a ThemeManager for template resolution
    - Can be part of a Collection or exist as standalone pages

    Attributes:
        slug (str): URL-safe identifier, auto-generated from title
        content: Raw or parsed content to be rendered
        parser: Content parser for processing raw content
        reference: Attribute used as key in site's route_list (default: "_slug")
        extension (str): File extension for output (default: ".html")
        routes (list[str | Path]): URL paths where page should be accessible
        template (str | Template | None): Jinja2 template for rendering
        plugin_manager: Manages plugins that modify page content
        site: Reference to parent Site object (set during rendering)
    """

    extension: str = ".html"
    routes: list[str | Path] = ["./"]
    template: str | Template | None
    rendered_content: str | None
    _reference: str = "_slug"
    plugin_manager: PluginManager | None
    site = None

    @property
    def _content(self) -> any:
        """returns the content of the page."""
        return getattr(self, "content", None)

    @property
    def _data(self) -> any:
        """returns the content of the page."""
        return getattr(self, "data", None)

    def url_for(self) -> str:
        """
        Generate the relative URL path for this page.

        URL Generation Logic:
        - If route is "./": Use page's path_name directly (/page-slug)
        - If route is custom: Combine route with path_name (/custom-route/page-slug)

        Route Examples:
        - routes=["./"] with path_name="about" → "/about"
        - routes=["blog"] with path_name="post-1" → "/blog/post-1"
        - routes=["2024/01"] with path_name="hello-world" → "/2024/01/hello-world"

        Path Name Generation:
        - Derived from page's slug attribute
        - Auto-generated from title if slug not provided
        - Includes file extension (.html by default)

        Limitations:
        - Returns relative URLs only (no domain)
        - Use {{ SITE_URL }} in templates for absolute URLs
        - Cannot access site configuration directly

        Template Usage:
        <a href="{{ page.url_for() }}">Link Text</a>
        <link rel="canonical" href="{{ SITE_URL }}{{ page.url_for() }}">

        Returns:
            str: Relative URL path for the page
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
                **{"content": self._content, "data": self._data},
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
                f"{self} does not have a content attribute. You must either provide a template or content."
            )

    def __str__(self):
        return self._slug

    def __repr__(self) -> str:
        return f"<Page: {self._title}>"

    def render(self, route: str | Path, theme_manager: ThemeManager) -> int:
        """Render the page to the file system"""
        path = Path(self.site.output_path) / Path(route) / Path(self.path_name)
        path.parent.mkdir(parents=True, exist_ok=True)
        settings = dict()
        if (pm := getattr(self, "plugin_manager", None)) and pm is not None:
            settings = {**self.site.plugin_manager.plugin_settings, "route": route}
            pm.hook.render_content(page=self, settings=settings, site=self.site)
        self.rendered_content = self._render_content(theme_manager.engine)
        # pass the route to the plugin settings
        if pm is not None:
            pm.hook.post_render_content(page=self.__class__, settings=settings, site=self.site)

        return path.write_text(self.rendered_content)


class Page(BasePage):
    """
    Concrete implementation of BasePage for creating web pages.

    This is the primary class users extend to create content pages for their site.
    Pages can be created from templates, file content, or direct content strings.

    Content Sources:
    - Template-based: Define template and variables in the class
    - File-based: Specify content_path to load content from a file
    - Direct content: Provide content directly as a string

    Site Integration:
    - Registered with Site via @site.page decorator or site.page() method
    - Inherits site's plugin manager with page-specific overrides
    - Gets site reference during rendering for cross-page linking
    - Accessible in templates via site.routes[page_slug]

    Example Usage:
        @site.page
        class Home(Page):
            title = "Welcome"
            content = "Hello World!"
            template = "page.html"

        @site.page
        class About(Page):
            content_path = "content/about.md"
            template = "page.html"

    Attributes:
        content_path: Path to file for content generation (optional)
        extension: Output file extension (default: ".html")
        engine: Custom Jinja2 engine (rarely used, site engine preferred)
        reference: Route list key attribute (default: "_slug")
        routes: URL paths for the page (default: ["./"])
        template: Jinja2 template name for rendering
        Parser: Content parser class (default: BasePageParser)
        title: Page title (default: class name)
        content: Direct content string (alternative to content_path)
        parser_extras: Additional parser configuration
        inherit_plugins: Whether to inherit site plugins (default: True)
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
