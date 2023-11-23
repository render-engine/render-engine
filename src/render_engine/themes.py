import dataclasses
import logging
import pathlib
import shutil

from jinja2 import BaseLoader, Environment


@dataclasses.dataclass
class Theme:
    """
    Base Theme Class for Render Engine

    Attributes:
        loader: Jinja2 Loader for the theme
        filters: dictionary of filters to add to the jinja2 environment
        plugins: list of plugins to add to the site
        static_dir: path to static folder
        template_globals: dictionary of template globals to add to the jinja2 environment.
            The key is the name of the global and the value is the value of the global.
            In many cases, this will be a string path to a template file
            or a string of template content.

            Example:
                ```python
                {
                    "head": "head.html",
                    "body_class": "my-class",
                }
                ```
    """

    loader: BaseLoader
    filters: dataclasses.field(default_factory=dict)
    plugins: dataclasses.field(default_factory=list)
    static_dir: str | pathlib.Path | None = None
    template_globals: dataclasses.field(default_factory=dict) = None


class ThemeManager:
    """
    Processes the theme for the site.
    The theme manager is responsible for loading the jinja2 environment and copying static files.

    Attributes:
        engine: Jinja2 Environment used to render pages
        output_path: path to write rendered content
        static_paths: set of filepaths for static folders.
            This will get copied to the output folder.
            Folders are recursive.

    """

    engine: Environment
    output_path: str = "output"
    static_paths: set[str | pathlib.Path] = {"static"}

    def register_theme(self, theme: Theme):
        """
        Register a theme.

        Args:
            *themes: Theme objects to register
        """
        logging.info(f"Registering theme: {theme}")
        self.engine.loader.loaders.insert(0, theme.loader)

        if theme.static_dir:
            logging.debug(f"Adding static path: {theme.static_dir}")
            self.static_paths.add(theme.static_dir)
        self.engine.filters.update(theme.filters)

        if theme.template_globals:
            for key, value in theme.template_globals.items():
                self.engine.globals.setdefault(key, set()).add(value)

    def register_themes(self, *themes: Theme):
        """
        Register multiple themes.

        Args:
            *themes: Theme objects to register
        """
        for theme in themes:
            self.register_theme(theme)

    def _render_static(self) -> None:
        """Copies a Static Directory to the output folder"""
        for static_path in self.static_paths:
            logging.debug(f"Copying Static Files from {static_path}")
            if pathlib.Path(static_path).exists():
                shutil.copytree(
                    static_path, pathlib.Path(self.output_path) / pathlib.Path(static_path).name, dirs_exist_ok=True
                )
