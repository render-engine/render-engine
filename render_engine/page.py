import logging
from pathlib import Path
from typing import Any, Optional

import frontmatter
from jinja2 import Environment, FileSystemLoader, Template
from markdown2 import markdown
from slugify import slugify


class Page:
    """Base component used to make web pages. Pages can be rendered directly from a template or generated from a file. Page objects can be used to extend existing page objects.

    .. note::
        Not all attributes are defined by default (those that are marked *optional*) but
        will be checked for in other areas of the code.

    When you create a page, you can specify variables that will be passed into rendering template.
    """

    route: str = "./"

    markdown_extras: list[str] = ["fenced-code-blocks", "footnotes"]
    """Plugins that will be used with Markdown2"""

    markdown: Optional[str] = None
    """This is base markdown that will be used to render the page.

    .. warning:: this will be overwritten if a content_path is provided.
    """

    extension: str = ".html"
    """Extension to use for the rendered page output."""

    engine: Environment = Environment(loader=FileSystemLoader("templates"))
    """The engine to generate web pages. This is a jinja2 engine by default.

    .. Note: You can provide a custom engine by setting the this attribute, but render engine expects the template to be called with `get_template`.
    """

    def __init__(self, **kwargs) -> None:
        for key, val in kwargs.items():
            setattr(self, key, val)

        if self.markdown and hasattr(self, "content_path"):
            logging.warning(
                "both `Page.markdown` and `content_path` selected. the content from `content_path` will be used."
            )

        if hasattr(self, "content_path") and not self.markdown:
            post = frontmatter.load(self.content_path)
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

        self.slug = slugify(self.slug)

    @property
    def url(self) -> str:
        """The first route and the slug of the page."""
        return f"{self.route}{self.slug}{self._extension}"

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
    def _template(self) -> Optional[Template]:
        if template := getattr(self, "template", None):
            return self.engine.get_template(template)

    def __str__(self):
        return self.slug

    def __repr__(self) -> str:
        return f"<Page {self.title}>"

    def _render_content(self, **kwargs) -> str:
        template = self._template

        if template:
            if self.content:
                return template.render(
                    content=self.content, **{**self.__dict__, **kwargs}
                )

            else:
                return template.render(**{**self.__dict__, **kwargs})

        elif self.content:
            return self.content

        else:
            raise ValueError(f"{self=} must have either content or template")

    def render(self, **kwargs) -> Path:
        """Build the page based on content instructions"""

        markup = self._render_content(**kwargs)
        path = Path(kwargs.get("path", "")).joinpath(f"{self.slug}{self._extension}")
        return path.write_text(markup)
