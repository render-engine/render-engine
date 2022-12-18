import logging
from pathlib import Path
from typing import Generator, Optional

import frontmatter
import jinja2
from markdown2 import markdown
from slugify import slugify

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

    markdown_extras: list[str] = ["fenced-code-blocks", "footnotes"]
    """Plugins that will be used with the markdown parser (default parser is [Markdown2](https://github.com/trentm/python-markdown2)).
     You can see a list of all the plugins [here](https://github.com/trentm/python-markdown2/wiki/Extras).

     The default plugins fenced-code-blocks and footnotes provide a way to add code blocks and footnotes to your markdown.
     """

    markdown: str | None = None
    """This is base markdown that will be used to render the page.

    !!! warning

        This will be overwritten if a `content_path` is provided.
    """

    content_path: _route | None = None
    """
    The path to the file that will be used to generate the page.

    !!! note

        This overrides the `markdown` attribute.
    """

    extension: str = ".html"
    """Extension to use for the rendered page output."""

    reference: str = "slug"

    routes: list[_route] = ["./"]

    template: str | None = None

    def __init__(self, engine: jinja2.Environment | None = None, **kwargs) -> None:
        if not hasattr(self, "engine"):
            self.engine = engine

        for key, val in kwargs.items():
            setattr(self, key, val)

        if self.markdown and self.content_path is not None:
            logging.warning(
                "both `Page.markdown` and `content_path` selected. the content from `content_path` will be used."
            )

        if self.content_path:
            post = frontmatter.load(Path(self.content_path))
            valid_attrs, self.markdown = post.metadata, post.content
            logging.info(f"content_path found! {valid_attrs=}, {self.markdown=}")

            for name, value in valid_attrs.items():
                # comma delimit attributes.
                if name.lower() in getattr(self, "list_attrs", []):
                    value = [attrval.lower() for attrval in value.split(", ")]

                setattr(self, name.lower(), value)

        if not hasattr(self, "title"):
            self.title = self.__class__.__name__
            logging.info(f"No Title. Assigning {self.title=}")

        if not hasattr(self, "slug"):
            logging.info(f"No slug. Will slugify {self.title=}")
            self.slug = self.title  # Will Slugify in Next Step

        if not self.routes:
            self.routes = []

        self.slug = slugify(self.slug)

    @property
    def url(self) -> Path:
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
    def content(self) -> Optional[str]:
        """html = rendered HTML (not marked up).
        Is `None` if `content == None`
        This is referred to as `content` because it is intended to be applied in the jinja template as {{content}}.
        When referring to the raw content in the Page object use `markdown`.
        """

        if not self.markdown:
            return None

        return markdown(self.markdown, extras=self.markdown_extras)

    @property
    def url_for(self):
        """Returns the url for the page"""
        return self.slug

    def __str__(self):
        return self.slug

    def __repr__(self) -> str:
        return f"<Page {self.title}>"

    def _render_content(self, **kwargs) -> str:
        template = None

        if self.template:
            logging.debug(f"Using %s for %s", self.template, self)
            template = self.engine.get_template(self.template)

        if template:
            if self.content:
                logging.debug(
                    "content found. rendering with content: %s, %s, %s",
                    self.content,
                    self.__dict__,
                    kwargs,
                )
                return template.render(
                    content=self.content, **{**self.__dict__, **kwargs}
                )

            else:
                logging.debug(
                    "No content found. rendering with content: %s, %s",
                    self.__dict__,
                    kwargs,
                )
                return template.render(**{**self.__dict__, **kwargs})

        elif self.content:
            return self.content

        else:
            raise ValueError(f"{self=} must have either content or template")

    def __iter__(self):
        """Good for getting the route objects"""
        yield from self.render()

    def render(
        self, *, engine=None, **kwargs
    ) -> Generator[dict[_route, "Page"], None, None]:
        """Build the route based on content instructions"""

        for route in self.routes:
            yield {str("Path(_route) / self.url"): self}
