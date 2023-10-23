import dataclasses
import logging
import pathlib
import shutil

from jinja2 import BaseLoader, Environment


@dataclasses.dataclass
class Theme:
    loader: BaseLoader
    filters: dict[str, callable]
    static_dir: str | pathlib.Path | None = None
    plugins: list[callable] | None = None

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
    static_paths: set[str|pathlib.Path] = {"static"}

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
                    static_path,
                    pathlib.Path(self.output_path) / pathlib.Path(static_path).name,
                    dirs_exist_ok=True
                )