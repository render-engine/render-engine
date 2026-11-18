import shutil
import unicodedata
from dataclasses import asdict, dataclass, fields
from importlib.util import find_spec
from pathlib import Path
from urllib.parse import urlparse

from jinja2 import Environment, StrictUndefined
from slugify import slugify

SITE_TEMPLATE = Path(__file__).parent / "site_template"
# Files and folders in a template that never belong in a new project:
# version control, OS junk, caches, virtual environments and secrets.
IGNORED_NAMES = {".git", ".hg", ".svn", ".DS_Store", "Thumbs.db", "__pycache__", ".venv", ".env"}


@dataclass
class InitOptions:
    """Answers used to create a new site with `render-engine init`."""

    site_title: str = "Untitled Site"
    site_url: str = "https://example.com"
    project_slug: str = ""
    app_filename: str = "app.py"
    output_path: str = "output"
    include_collection: bool = True
    include_blog: bool = True
    include_cli: bool = True

    def _validate_site_title(self) -> None:
        self.site_title = self.site_title.strip()
        if not self.site_title:
            raise ValueError("The site title can't be empty. Please enter a title, e.g. 'My Blog'.")
        if any(unicodedata.category(char) in {"Cc", "Zl", "Zp"} for char in self.site_title):
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
        given_slug = self.project_slug
        self.project_slug = slugify(self.project_slug or self.site_title)

        if not self.project_slug:
            source = given_slug or self.site_title
            raise ValueError(
                f"Can't make a project name from {source!r}: it needs at least one letter or number. "
                "Please use a different title, or set a project slug like 'my-site'."
            )

    def _validate_app_filename(self) -> None:
        path = Path(self.app_filename)

        if path.suffix != ".py":
            raise ValueError(f"The app filename {self.app_filename!r} must end with '.py', e.g. 'app.py'.")
        elif path.name != self.app_filename:
            raise ValueError(
                f"The app filename {self.app_filename!r} must be a file name without a folder, e.g. 'app.py'."
            )
        elif path.stem.startswith("__") or not path.stem.isidentifier():
            raise ValueError(
                f"The app filename {self.app_filename!r} can only use letters, numbers and underscores, "
                "and can't start with a number or '__', e.g. 'my_app.py'."
            )
        elif find_spec(path.stem):
            raise ValueError(
                f"The app filename {self.app_filename!r} can't be used: {path.stem!r} is already the name of "
                "a Python module, and your file would hide it. Try e.g. 'app.py'."
            )

    def _validate_output_path(self) -> None:
        path = Path(self.output_path)

        if path.is_absolute() or not path.parts or ".." in path.parts:
            raise ValueError(
                f"The output path {self.output_path!r} must be a folder inside your project, e.g. 'output'."
            )
        elif path.parts[0].lower() in {"content", "templates", "static"}:
            raise ValueError(
                f"The output path {self.output_path!r} can't be used: the {path.parts[0]!r} folder holds your "
                "site's own files, and cleaning the output would delete them. Try e.g. 'output'."
            )
        elif path.parts[0].startswith("."):
            raise ValueError(
                f"The output path {self.output_path!r} can't be used: folders starting with '.' hold tools and "
                "settings like Git, and cleaning the output would delete them. Try e.g. 'output'."
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
        skipped_folders = set()
        created_files = set()

        if not options.include_blog:
            skipped_folders.add(Path("content/blog"))
        if not options.include_collection:
            skipped_folders.add(Path("content/pages"))

        for item in template_items:
            relative_path = item.relative_to(template_dir)
            if not item.is_file():
                continue
            if any(part in IGNORED_NAMES for part in relative_path.parts):
                continue
            if any(relative_path.is_relative_to(folder) for folder in skipped_folders):
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
                template = env.from_string(item.read_text(encoding="utf-8"))
                output.write_text(template.render(context), encoding="utf-8")
            else:
                shutil.copy2(item, output)
    except BaseException:
        shutil.rmtree(created_root)
        raise

    return site_path
