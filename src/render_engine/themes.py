import dataclasses
import logging
import pathlib
import shutil
from pathlib import Path

import slugify
from jinja2 import BaseLoader, Environment


@dataclasses.dataclass
class Theme:
    """
    Base Theme Class for Render Engine

    Attributes:
        loader (BaseLoader): Jinja2 Loader for the theme.
        filters (dict): Dictionary of filters to add to the jinja2 environment.
        prefix (str): Prefix to pass into the prefixLoader.
        plugins (list): List of plugins to add to the site.
        static_dir (str | pathlib.Path | None): Path to static folder.
        template_globals (dict): Dictionary of template globals to add to the jinja2 environment.
            The key is the name of the global and the value is the value of the global.
            In many cases, this will be a string path to a template file
            or a string of template content.

            Example:
                {
                    "head": "head.html",
                    "body_class": "my-class",
                }
    """

    loader: BaseLoader
    prefix: str
    filters: dict = dataclasses.field(default_factory=dict)
    plugins: list = dataclasses.field(default_factory=list)
    template_globals: dict | None = None
    static_dir: str | pathlib.Path | None = None

    def __post_init__(self) -> None:
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
        engine (Environment): Jinja2 Environment used to render pages.
        output_path (str | Path): Path to write rendered content.
        prefix (dict[str, str]): Dictionary mapping theme prefixes to loader names.
        static_paths (set): Set of filepaths for static folders.
            This will get copied to the output folder. Folders are recursive.
        template_globals (dict[str, set]): Dictionary mapping template global names to sets of values.

    Methods:
        default_template_globals() -> dict[str, set]: Returns the default template globals.
        register_theme(theme: Theme) -> None: Register a theme.
    """

    @staticmethod
    def default_template_globals() -> dict[str, set]:
        return {
            "head": set(),
            "body_class": set(),
        }

    engine: Environment
    output_path: Path | str
    prefix: dict[str, BaseLoader] = dataclasses.field(default_factory=dict)
    static_paths: set = dataclasses.field(default_factory=set)
    template_globals: dict[str, set] = dataclasses.field(default_factory=default_template_globals)

    def register_theme(self, theme: Theme):
        """
        Register a theme.

        Args:
            theme (Theme): Theme object to register.
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
