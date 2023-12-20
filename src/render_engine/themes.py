import dataclasses
import logging
import pathlib
import shutil

import slugify
from jinja2 import BaseLoader, Environment


@dataclasses.dataclass
class Theme:
    """
    Base Theme Class for Render Engine

    Attributes:
        prefix: prefix to pass into the prefixLoader
        loader: Jinja2 Loader for the theme
        filters: dictionary of filters to add to the jinja2 environment
        plugins: list of plugins to add to the site
        plugin_settings: dictionary of settings to pass to the plugins
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
    template_globals: dataclasses.field(default_factory=dict) = None
    prefix: str | None = None
    static_dir: str | pathlib.Path | None = None

    def __post_init__(self):
        if self.prefix:
            self.prefix = slugify.slugify(self.prefix.lower())
        else:
            self.prefix = slugify.slugify(self.__class__.__name__.lower())


@dataclasses.dataclass
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

    def default_template_globals():
        return {
            "head": set(),
            "body_class": set(),
        }

    engine: Environment
    output_path: str
    prefix: dict[str, str] = dataclasses.field(default_factory=dict)
    static_paths: set = dataclasses.field(default_factory=set)
    template_globals: dict[str:set] = dataclasses.field(default_factory=default_template_globals)

    def register_theme(self, theme: Theme):
        """
        Register a theme.

        Args:
            theme: Theme objects to register
        """

        logging.info(f"Registering theme: {theme}")
        self.prefix[theme.prefix] = theme.loader

        if theme.static_dir:
            logging.debug(f"Adding static path: {theme.static_dir}")
            self.static_paths.add(theme.static_dir)
        self.engine.filters.update(theme.filters)

        if theme.template_globals:
            for key, value in theme.template_globals.items():
                if isinstance(value, set) and isinstance(self.engine.globals.get(key), set):
                    self.engine.globals.setdefault(key, set()).update(value)
                if isinstance(self.engine.globals.get(key), set):
                    self.engine.globals[key].add(value)

                else:
                    self.engine.globals[key] = value

    def _render_static(self) -> None:
        """Copies a Static Directory to the output folder"""
        for static_path in self.static_paths:
            logging.debug(f"Copying Static Files from {static_path}")
            if pathlib.Path(static_path).exists():
                shutil.copytree(
                    static_path,
                    pathlib.Path(self.output_path) / pathlib.Path(static_path).name,
                    dirs_exist_ok=True,
                )
