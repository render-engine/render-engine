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
    Theme configuration for customizing site appearance and behavior.

    A Theme encapsulates all the components needed to style and extend a Render Engine site:
    templates, static assets, custom filters, plugins, and global template variables.
    Themes are registered with the site's ThemeManager and integrated into the template
    processing pipeline.

    Template Resolution Hierarchy:
    1. User templates (highest priority - from site's template_path)
    2. Theme templates (accessed via prefix, e.g., 'mytheme/page.html')
    3. Built-in templates (lowest priority - from render_engine package)

    Static File Handling:
    - Theme static directories are automatically copied to output during build
    - Multiple themes can contribute static files
    - Files are merged; later themes can override earlier ones

    Plugin Integration:
    - Theme plugins are automatically registered when theme is loaded
    - Plugins get access to theme-specific settings and context
    - Theme plugins follow same inheritance rules as site plugins

    Attributes:
        loader: Jinja2 loader providing access to theme's template files
        prefix: Namespace prefix for theme templates (auto-generated from class name if not provided)
        filters: Custom Jinja2 filters to add to the rendering environment
        plugins: List of plugin classes to register when theme is loaded
        static_dir: Path to directory containing theme's static assets (CSS, JS, images)
        template_globals: Global variables available in all templates (can include template includes)

    Example:
        custom_theme = Theme(
            loader=FileSystemLoader("themes/mytheme/templates"),
            prefix="mytheme",
            static_dir="themes/mytheme/static",
            template_globals={"brand_color": "#ff0000"},
            plugins=[MyThemePlugin]
        )
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
    Central coordinator for template processing and theme management.

    The ThemeManager orchestrates the entire template processing pipeline, managing
    the Jinja2 environment, theme registration, static file handling, and template
    resolution. It serves as the bridge between the site's content and its visual
    presentation.

    Template Processing Pipeline:
    1. Theme Registration: Themes are registered, adding loaders and static paths
    2. Environment Setup: Jinja2 environment is configured with loaders and filters
    3. Global Injection: Site variables and theme globals are injected into templates
    4. Template Resolution: Multi-tier loader system resolves template requests
    5. Static Copying: Theme and site static files are copied to output directory
    6. Rendering: Pages and collections are rendered using resolved templates

    Loader Hierarchy (in order of precedence):
    - User templates (FileSystemLoader from site's template_path)
    - Theme templates (PrefixLoader with theme prefixes)
    - Built-in templates (PackageLoader from render_engine.templates)

    Static File Management:
    - Collects static paths from all registered themes
    - Copies files during site build process
    - Supports recursive directory copying
    - Merges files from multiple themes (later themes can override)

    Template Global Management:
    - Maintains global variables available in all templates
    - Supports both single values and sets (for extensible globals like 'head')
    - Merges globals from site configuration and themes
    - Provides default globals like 'head' and 'body_class'

    Attributes:
        engine: Jinja2 Environment instance for template rendering
        output_path: Directory where rendered content and static files are written
        prefix: Maps theme prefixes to their Jinja2 loaders for template resolution
        static_paths: Set of directories to copy to output during build
        template_globals: Global variables injected into all template contexts
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
        Integrate a theme into the template processing pipeline.

        This method performs the complete theme integration process:
        1. Adds theme's template loader to the prefix mapping for template resolution
        2. Registers theme's static directory for copying during build
        3. Adds theme's custom filters to the Jinja2 environment
        4. Merges theme's template globals with existing globals
        5. Logs the registration for debugging purposes

        Template Resolution Impact:
        After registration, templates can reference theme templates using the prefix:
        {% extends "themeprefix/template.html" %}

        Static File Impact:
        Theme static files will be copied to output/theme_static_dir_name/

        Filter Impact:
        Theme filters become available in all templates: {{ value | custom_filter }}

        Global Impact:
        Theme globals are merged with site globals and become available in all templates

        Args:
            theme: The Theme object to integrate into the processing pipeline
        """
        logging.info(f"Registering theme: {theme}")

        # Add theme loader to prefix mapping for template resolution
        self.prefix[theme.prefix] = theme.loader

        # Register static directory for copying during build
        if theme.static_dir:
            logging.debug(f"Adding static path: {theme.static_dir}")
            self.static_paths.add(theme.static_dir)

        # Add theme's custom filters to Jinja2 environment
        self.engine.filters.update(theme.filters)

        # Merge theme template globals with existing globals
        if theme.template_globals:
            for key, value in theme.template_globals.items():
                # Handle set-type globals (like 'head' for extensible content)
                if isinstance(value, set) and isinstance(self.engine.globals.get(key), set):
                    self.engine.globals.setdefault(key, set()).update(value)
                elif isinstance(self.engine.globals.get(key), set):
                    # Convert single value to set member
                    self.engine.globals[key].add(value)
                else:
                    # Simple value replacement
                    self.engine.globals[key] = value

    def _render_static(self) -> None:
        """
        Copy all registered static directories to the site output.

        This method is called during the site build process to copy static assets
        from themes and site configuration to the output directory. It handles:

        - Multiple static directories from different themes
        - Recursive copying of entire directory trees
        - Overwriting of files when directories have conflicting names
        - Safe handling of missing source directories

        Static File Pipeline:
        1. Collect static paths from all registered themes
        2. For each path, verify it exists on filesystem
        3. Copy entire directory tree to output/static_dir_name/
        4. Later themes can override files from earlier themes
        5. Site's static_paths are also processed through this method

        Directory Structure:
        Input:  themes/mytheme/static/css/style.css
        Output: output/static/css/style.css

        The static files are copied before template rendering so they're
        available when generating links in templates.
        """
        for static_path in self.static_paths:
            logging.debug(f"Copying Static Files from {static_path}")
            source_path = pathlib.Path(static_path)

            if source_path.exists():
                # Copy entire directory tree to output
                destination = pathlib.Path(self.output_path) / source_path.name
                shutil.copytree(
                    source_path,
                    destination,
                    dirs_exist_ok=True,  # Allow overwriting existing files
                )
            else:
                logging.warning(f"Static path does not exist: {static_path}")
