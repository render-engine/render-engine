import keyword
import shutil
import sys
import unicodedata
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from urllib.parse import urlparse

from jinja2 import Environment, StrictUndefined, TemplateError, TemplateSyntaxError
from slugify import slugify

SITE_TEMPLATE = Path(__file__).parent / "site_template"
# Files and folders in a template that never belong in a new project:
# version control, OS junk, caches, virtual environments and secrets.
IGNORED_NAMES = {".git", ".hg", ".svn", ".DS_Store", "Thumbs.db", "__pycache__", ".venv", ".env"}
# Modules a new site imports. An app file with one of these names would hide them.
TAKEN_MODULE_NAMES = sys.stdlib_module_names | {"render_engine", "render_engine_cli"}
# Names the generated app file already uses. A site variable with one of these names would replace them.
APP_FILE_NAMES = {"Page", "Site", "Collection", "BaseBlog", "MarkdownPageParser", "Index", "Pages", "Blog"}


class TemplateFileError(ValueError):
    """A file in a site template couldn't be rendered."""


@dataclass
class InitOptions:
    """Answers used to create a new site with `render-engine init`."""

    site_title: str = "Untitled Site"
    site_url: str = "https://example.com"
    project_slug: str = ""
    app_filename: str = "app.py"
    site_variable: str = "app"
    output_path: str = "output"
    include_collection: bool = True
    include_blog: bool = True
    include_cli: bool = True

    def _validate_site_title(self) -> None:
        self.site_title = self.site_title.strip()
        if not self.site_title:
            raise ValueError("The site title can't be empty. Please enter a title, e.g. 'My Blog'.")
        if {"Cc", "Zl", "Zp"}.intersection(map(unicodedata.category, self.site_title)):
            raise ValueError(f"The site title {self.site_title!r} must be on one line, without tabs or line breaks.")

    def _validate_site_url(self) -> None:
        self.site_url = self.site_url.strip()
        parsed_url = urlparse(self.site_url)

        if not parsed_url.hostname or parsed_url.scheme not in ["http", "https"]:
            raise ValueError(
                f"The site URL {self.site_url!r} must start with http:// or https://, e.g. 'https://example.com'."
            )
        if any(char.isspace() for char in self.site_url):
            raise ValueError(f"The site URL {self.site_url!r} can't contain spaces. Use '-' or '%20' instead.")
        try:
            _ = parsed_url.port
        except ValueError:
            raise ValueError(
                f"The site URL {self.site_url!r} has an invalid port: it must be a number, e.g. 'http://localhost:8000'."
            ) from None

    def _validate_project_slug(self) -> None:
        source = self.project_slug or self.site_title
        self.project_slug = slugify(source)

        if not self.project_slug:
            raise ValueError(
                f"Can't make a project folder name from {source!r}: it needs at least one letter or number. "
                "Use a different title, or set the folder name with "
                """-e '{"project_slug": "my-site"}'."""
            )

    def _validate_app_filename(self) -> None:
        if not self.app_filename.endswith(".py"):
            self.app_filename += ".py"
        path = Path(self.app_filename)

        if path.name != self.app_filename:
            raise ValueError(
                f"The app filename {self.app_filename!r} must be a file name without a folder, e.g. 'app.py'."
            )
        elif "." in path.stem:
            raise ValueError(
                f"The app filename {self.app_filename!r} can't contain a '.' before '.py': the CLI would read "
                "it as a package path. Try e.g. 'my_app.py'."
            )
        elif path.stem in TAKEN_MODULE_NAMES:
            raise ValueError(
                f"The app filename {self.app_filename!r} can't be used: {path.stem!r} is already the name of "
                "a Python module, and your file would hide it. Try e.g. 'app.py'."
            )

    def _validate_output_path(self) -> None:
        path = Path(self.output_path)

        if not any(char.isalnum() for char in self.output_path):
            raise ValueError(
                f"The output path {self.output_path!r} needs at least one letter or number, e.g. 'output'. "
                "Without a folder name, it points to your project or a folder above it, "
                "and cleaning the output would delete it."
            )
        elif path.parts[0].lower() in {"content", "templates", "static"}:
            raise ValueError(
                f"The output path {self.output_path!r} can't be used: the {path.parts[0]!r} folder holds your "
                "site's own files, and cleaning the output would delete them. Try e.g. 'output'."
            )
        elif path.parts[0].startswith(".") and path.parts[0] != "..":
            raise ValueError(
                f"The output path {self.output_path!r} can't be used: folders starting with '.' hold tools and "
                "settings like Git, and cleaning the output would delete them. Try e.g. 'output'."
            )
        elif path.parts[0].lower() in {self.app_filename.lower(), "pyproject.toml", "readme.md"}:
            raise ValueError(
                f"The output path {self.output_path!r} can't be used: {path.parts[0]!r} is a file of your "
                "project, and cleaning the output would delete it. Try e.g. 'output'."
            )
        elif any(char.isspace() for char in self.output_path):
            raise ValueError(f"The output path {self.output_path!r} can't contain spaces. Use '-' or '_' instead.")

    def _validate_site_variable(self) -> None:
        if not self.site_variable.isidentifier() or keyword.iskeyword(self.site_variable):
            raise ValueError(
                f"The site variable {self.site_variable!r} must be a Python name: letters, numbers and "
                "underscores, not starting with a number, e.g. 'app' or 'site'."
            )
        elif self.site_variable in APP_FILE_NAMES:
            raise ValueError(
                f"The site variable {self.site_variable!r} can't be used: the app file already uses that name. "
                "Try e.g. 'app'."
            )

    def _validate_types(self) -> None:
        for field in fields(self):
            value = getattr(self, field.name)
            label = field.name.replace("_", " ")
            if isinstance(field.default, bool) and not isinstance(value, bool):
                raise TypeError(f"The {label} answer must be True or False, not {value!r}.")
            if isinstance(field.default, str) and not isinstance(value, str):
                raise TypeError(f"The {label} must be text, not {value!r}.")

    def __post_init__(self) -> None:
        self._validate_types()
        self._validate_site_title()
        self._validate_site_url()
        self._validate_project_slug()
        self._validate_app_filename()
        self._validate_site_variable()
        self._validate_output_path()


def create_site(options: InitOptions, destination: Path | str, template_dir: Path | str = SITE_TEMPLATE) -> Path:
    """Create the folder for a new site and return its path.

    The folder is named after `options.project_slug` and created inside `destination`.
    """
    template_dir = Path(template_dir)
    if not template_dir.is_dir():
        raise FileNotFoundError(f"The template folder {str(template_dir)!r} doesn't exist or isn't a folder.")

    site_path = Path(destination) / options.project_slug

    if site_path.exists():
        raise FileExistsError(
            f"The folder {str(site_path)!r} already exists. Use a different project slug or destination folder."
        )

    # The top folder this call creates: the project folder, or its highest missing parent.
    created_root = site_path

    while not created_root.parent.exists():
        created_root = created_root.parent

    template_items = sorted(template_dir.rglob("*"))
    site_path.mkdir(parents=True)

    try:
        env = Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
            undefined=StrictUndefined,
        )
        context = asdict(options)
        skipped_paths = set()
        created_files = set()

        if not options.include_blog:
            skipped_paths.add(Path("content/blog"))
            skipped_paths.add(Path("templates/archive.html"))
        if not options.include_collection:
            skipped_paths.add(Path("content/pages"))

        for item in template_items:
            relative_path = item.relative_to(template_dir)
            if not item.is_file():
                continue
            if any(part in IGNORED_NAMES for part in relative_path.parts):
                continue
            if any(relative_path.is_relative_to(skipped) for skipped in skipped_paths):
                continue

            output = site_path / relative_path
            if item.suffix == ".jinja":
                output = output.with_suffix("")
                if relative_path == Path("app.py.jinja"):
                    output = site_path / options.app_filename

            if output in created_files:
                raise ValueError(
                    f"The template has more than one file that creates {str(output.relative_to(site_path))!r}, "
                    "e.g. 'app.py' and 'app.py.jinja'. Please remove one of them."
                )
            created_files.add(output)
            output.parent.mkdir(parents=True, exist_ok=True)

            if item.suffix == ".jinja":
                try:
                    rendered = env.from_string(item.read_text(encoding="utf-8")).render(context)
                except (TemplateError, UnicodeDecodeError) as error:
                    line = f" (line {error.lineno})" if isinstance(error, TemplateSyntaxError) else ""
                    raise TemplateFileError(
                        f"The template file {str(relative_path)!r} can't be rendered{line}: {error}"
                    ) from error
                output.write_text(rendered, encoding="utf-8")
            else:
                shutil.copy2(item, output)
    except BaseException:
        shutil.rmtree(created_root, ignore_errors=True)
        raise

    return site_path
