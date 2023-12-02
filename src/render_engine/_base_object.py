"""Shared Properties and methods across render_engine objects."""

from slugify import slugify


class BaseObject:
    """
    Shared properties for render_engine objects.

    This ensures that the behavior around the title, slug, and path_name are consistent

    This is not intended to be used directly.
    """

    title: str
    template_vars: dict
    plugins: list

    @property
    def _title(self) -> str:
        """
        The title of the Page
        If no title is provided, use the class name.
        """
        return getattr(self, "title", self.__class__.__name__)

    @property
    def _slug(self) -> str:
        """The slugified path of the page"""
        return slugify(getattr(self, "slug", self._title))

    @property
    def extension(self) -> str:
        """The extension of the page"""
        return getattr(self, "_extension", ".html")

    @extension.setter
    def extension(self, extension: str) -> None:
        """Ensures consistency on extension"""
        self._extension = f".{extension.lstrip('.')}"

    @property
    def path_name(self) -> str:
        """
        Returns the [`url_for`][src.render_engine.page.Page.url_for] for the page including the first route.
        """
        return f"{self._slug}{self.extension}"

    def url_for(self):
        pass

    def to_dict(self):
        """
        Returns a dict of the page's attributes.

        This is often used to pass attributes into the page's `template`.

        """
        base_dict = {
            **vars(self),
            "title": self._title,
            "slug": self._slug,
            "url": self.url_for(),
            "path_name": self.path_name,
        }

        # Pull out template_vars
        if hasattr(self, "template_vars"):
            for key, value in self.template_vars.items():
                base_dict[key] = value

        return base_dict
