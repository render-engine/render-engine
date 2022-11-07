import logging
import pdb
from pathlib import Path
from typing import Any, Optional

import frontmatter
from jinja2 import Environment, FileSystemLoader, Template
from markdown2 import markdown
from slugify import slugify


class Page:
    """The base object used to make web pages.
    Pages can be rendered directly from a template or generated from a file.

    Custom attributes can be added to the page by adding them to the frontmatter of the file or by adding them to the page object directly. These attributes will be available to the template.
    """

    markdown_extras: list[str] = ["fenced-code-blocks", "footnotes"]
    """Plugins that will be used with the markdown parser (default parser is [Markdown2](https://github.com/trentm/python-markdown2)).

     You can see a list of all the plugins [here](https://github.com/trentm/python-markdown2/wiki/Extras)."""

    markdown: Optional[str] = None
    """This is base markdown that will be used to render the page.

    > WARNING: This will be overwritten if a content_path is provided.
    """

    content_path: Path | str | None = None
    """The path to the file that will be used to generate the page.

    If this is provided, the content will be parsed from the file and the markdown attribute will be ignored.
    """

    extension: str = ".html"
    """Extension to use for the rendered page output."""

    def __init__(self, **kwargs) -> None:
        for key, val in kwargs.items():
            setattr(self, key, val)

        if self.markdown and self.content_path != None:
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

        self.slug = slugify(self.slug)

    @property
    def url(self) -> Path:
        """The first route and the slug of the page."""
        return (
            getattr(self, "output_path", Path("./"))
            / getattr(self, "route", "./")
            / f"{self.slug}{self._extension}"
        )

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

    def __str__(self):
        return self.slug

    def __repr__(self) -> str:
        return f"<Page {self.title}>"

    def _render_content(self, *, engine: Environment = None, **kwargs) -> str:
        # template = self._template
        template = engine.get_template(self.template)

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

    def render(self, *, engine=None, **kwargs) -> Path:
        """Build the page based on content instructions"""
        markup = self._render_content(engine=engine, **kwargs)
        return Path(kwargs.get("path") / self.url).write_text(markup)
