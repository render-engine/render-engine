import ast
import tomllib

import pytest
from jinja2 import UndefinedError

from render_engine.init import SITE_TEMPLATE, InitOptions, create_site


def is_hidden(relative_path):
    """True if any part of the path (a file or one of its folders) starts with a dot."""
    return any(part.startswith(".") for part in relative_path.parts)


def static_files(folder):
    """All copy-only files in `folder` as {relative path: contents}: no `.jinja` files, nothing hidden."""
    return {
        path.relative_to(folder): path.read_bytes()
        for path in folder.rglob("*")
        if path.is_file() and path.suffix != ".jinja" and not is_hidden(path.relative_to(folder))
    }


@pytest.fixture
def options() -> InitOptions:
    return InitOptions(site_title="My Blog")


@pytest.fixture
def template_dir(tmp_path):
    """A small custom template with nested files, a Jinja file and hidden files and folders."""
    template = tmp_path / "template"
    (template / "nested" / "deeper").mkdir(parents=True)
    (template / "top.txt").write_text("top")
    (template / "nested" / "deeper" / "file.txt").write_text("deep")
    (template / "page.html.jinja").write_text("{{ site_title }}")
    # hidden files and folders, at the top and nested
    (template / ".DS_Store").write_text("hidden")
    (template / ".env").write_text("SECRET=1")
    (template / "nested" / ".hidden").write_text("hidden")
    (template / ".git").mkdir()
    (template / ".git" / "config").write_text("[core]")
    return template


# Project folder


def test_create_site_creates_project_folder(options, tmp_path):
    site_path = create_site(options, tmp_path)

    assert site_path == tmp_path / "my-blog"
    assert site_path.is_dir()


def test_create_site_accepts_destination_as_string(options, tmp_path):
    site_path = create_site(options, str(tmp_path))

    assert site_path == tmp_path / "my-blog"
    assert site_path.is_dir()


def test_create_site_creates_missing_destination(options, tmp_path):
    destination = tmp_path / "sites" / "personal"

    site_path = create_site(options, destination)

    assert site_path == destination / "my-blog"
    assert site_path.is_dir()


def test_existing_project_folder_is_rejected(options, tmp_path):
    (tmp_path / "my-blog").mkdir()

    with pytest.raises(FileExistsError, match="already exists"):
        create_site(options, tmp_path)


# Copying the built-in template


def test_all_static_template_files_are_copied(options, tmp_path):
    site_path = create_site(options, tmp_path)

    assert static_files(SITE_TEMPLATE).items() <= static_files(site_path).items()


@pytest.mark.parametrize(
    "relative_path",
    [
        "static/style.css",
        "static/render-engine-logo.png",
        "templates/_base.html",
        "templates/page.html",
        "templates/archive.html",
        "content/blog/example_blog_post.md",
        "content/pages/example_page.html",
    ],
)
def test_essential_files_are_copied(options, tmp_path, relative_path):
    site_path = create_site(options, tmp_path)

    assert (site_path / relative_path).is_file()


def test_jinja_files_are_not_copied(options, tmp_path):
    site_path = create_site(options, tmp_path)

    assert list(site_path.rglob("*.jinja")) == []


# Copying a custom template


def test_custom_template_dir_is_used(options, tmp_path, template_dir):
    site_path = create_site(options, tmp_path / "sites", template_dir=template_dir)

    assert (site_path / "top.txt").read_text() == "top"
    assert (site_path / "nested" / "deeper" / "file.txt").read_text() == "deep"


def test_hidden_files_and_folders_are_not_copied(options, tmp_path, template_dir):
    site_path = create_site(options, tmp_path / "sites", template_dir=template_dir)

    hidden = [path.relative_to(site_path) for path in site_path.rglob("*") if is_hidden(path.relative_to(site_path))]
    assert hidden == []


# Rendering the built-in template


def read_pyproject(site_path):
    return tomllib.loads((site_path / "pyproject.toml").read_text(encoding="utf-8"))


@pytest.mark.parametrize("relative_path", ["app.py", "pyproject.toml", "README.md", "templates/index.html"])
def test_jinja_files_are_rendered(options, tmp_path, relative_path):
    site_path = create_site(options, tmp_path)

    assert (site_path / relative_path).is_file()


def test_app_file_is_valid_python(options, tmp_path):
    site_path = create_site(options, tmp_path)

    ast.parse((site_path / "app.py").read_text(encoding="utf-8"))


def test_pyproject_uses_the_answers(options, tmp_path):
    site_path = create_site(options, tmp_path)

    pyproject = read_pyproject(site_path)
    assert pyproject["project"]["name"] == "my-blog"
    assert pyproject["tool"]["render-engine"]["cli"]["module"] == "app"


def test_custom_app_filename_is_used(tmp_path):
    site_path = create_site(InitOptions(site_title="My Blog", app_filename="main.py"), tmp_path)

    assert (site_path / "main.py").is_file()
    assert not (site_path / "app.py").exists()
    assert read_pyproject(site_path)["tool"]["render-engine"]["cli"]["module"] == "main"


@pytest.mark.parametrize("include_cli", [True, False])
def test_cli_dependency_follows_the_answer(tmp_path, include_cli):
    site_path = create_site(InitOptions(site_title="My Blog", include_cli=include_cli), tmp_path)

    dependencies = read_pyproject(site_path)["project"]["dependencies"]
    assert ("render-engine-cli" in dependencies) is include_cli


@pytest.mark.parametrize("site_title", ["Мой блог", "我的博客", 'My "quoted" Blog', "Back\\slash"])
def test_any_site_title_is_rendered_safely(tmp_path, site_title):
    site_path = create_site(InitOptions(site_title=site_title), tmp_path)

    ast.parse((site_path / "app.py").read_text(encoding="utf-8"))
    assert read_pyproject(site_path)["project"]["description"] == f"A Render Engine site: {site_title}"
    assert site_title in (site_path / "README.md").read_text(encoding="utf-8")


# Rendering a custom template


def test_custom_jinja_file_is_rendered(options, tmp_path, template_dir):
    site_path = create_site(options, tmp_path / "sites", template_dir=template_dir)

    assert (site_path / "page.html").read_text(encoding="utf-8") == "My Blog"


def test_unknown_template_variable_is_rejected(options, tmp_path, template_dir):
    (template_dir / "typo.txt.jinja").write_text("{{ site_tilte }}")

    with pytest.raises(UndefinedError, match="site_tilte"):
        create_site(options, tmp_path / "sites", template_dir=template_dir)
