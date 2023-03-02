"""Shared Properties and methods across render_engine objects."""

from slugify import slugify

class BaseObject:
    """
    Shared properties for render_engine objects.

    This ensures that the behavior around the title, slug, and path_name are consistent

    This is not intended to be used directly.
    """

    title: str

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
        return slugify(getattr(self, 'slug', self._title))

    
    @property
    def extension(self) -> str:
        """The extension of the page"""
        return getattr(self, "_extension", ".html")

    @extension.setter
    def extension(self, extension: str) -> None:
        """Ensures consistency on extension"""
        if not extension.startswith("."):
            self._extension = f".{extension}"
        self._extension = extension


    @property
    def path_name(self) -> str:
        """
        Returns the [`url_for`][src.render_engine.page.Page.url_for] for the page including the first route.
        """
        return f"{self._slug}{self.extension}"

    def to_dict(self):
        """
        Returns a dict of the page's attributes.

        This is often used to pass attributes into the page's `template`.

        """
        return {
            **vars(self),
            **getattr(self, "template_vars", {}),
            "title": self._title,
            "slug": self._slug,
        }
