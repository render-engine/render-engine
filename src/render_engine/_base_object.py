"""Shared Properties and methods across render_engine objects."""

from collections import defaultdict
from collections.abc import Callable

from slugify import slugify


class BaseObject:
    """
    Shared properties for render_engine objects.

    This ensures that the behavior around the title, slug, and path_name are consistent

    This is not intended to be used directly.

    Attributes:
        title (str): The title of the object. If no title is provided, the class name is used.
        template_vars (dict): A dictionary of template variables for the object.
        plugins (list): A list of plugins associated with the object.
        plugin_settings (dict): A dictionary of plugin settings for the object.

    """

    title: str
    template_vars: dict
    plugins: list[Callable] | None
    plugin_settings: dict = {"plugins": defaultdict(dict)}

    @property
    def _title(self) -> str:
        """
        The title of the object.

        If no title is provided, the class name is used.

        Returns:
            str: The title of the object.
        """
        return getattr(self, "title", self.__class__.__name__)

    @property
    def _slug(self) -> str:
        """
        The slugified path of the object.

        Returns:
            str: The slugified path of the object.

        """
        return slugify(getattr(self, "slug", self._title))

    @staticmethod
    def _metadata_attrs() -> dict[str, str]:
        """attrs used as metadata by the parser"""
        return {"title": "Untitled Entry"}

    @property
    def extension(self) -> str:
        """
        The extension of the object.

        Returns:
            str: The extension of the object.

        """
        return getattr(self, "_extension", ".html")

    @extension.setter
    def extension(self, extension: str) -> None:
        """
        Set the extension of the object.

        Args:
            extension (str): The extension to set.

        """
        self._extension = f".{extension.lstrip('.')}"

    @property
    def path_name(self) -> str:
        """
        Returns the URL path for the object including the extension.

        Returns:
            str: The URL path for the object.

        """
        return f"{self._slug}{self.extension}"

    def url_for(self):
        """
        Placeholder method for generating the URL for the object.

        This method should be implemented in subclasses.

        """
        pass

    def to_dict(self):
        """
        Returns a dictionary of the object's attributes.

        This method is often used to pass attributes into the object's template.

        Returns:
            dict: A dictionary of the object's attributes.

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

        # Pull out plugin_settings
        if hasattr(self, "plugin_settings"):
            for key, value in self.plugin_settings.items():
                base_dict[key] = value

        return base_dict
