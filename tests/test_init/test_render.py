import pytest

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

    assert static_files(site_path) == static_files(SITE_TEMPLATE)


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
