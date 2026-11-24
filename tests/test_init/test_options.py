"""Tests for `InitOptions`: the answers used to create a new site.

These tests call `InitOptions` directly and check the rules for each answer: which values
are accepted, how they are cleaned up (e.g. stripped, slugified) and which are rejected
with which error.

How the command asks the questions and handles invalid answers is tested in
`test_command.py`.
"""

import re
from dataclasses import fields

import pytest

from render_engine.init import InitOptions

SAFE_SLUG = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")


@pytest.mark.parametrize(
    "site_title",
    [
        "Česká stránka",  # Czech
        "Мой блог",  # Russian
        "我的博客",  # Chinese
        "मेरा ब्लॉग",  # Hindi
        "የእኔ ብሎግ",  # Amharic
        "บล็อกของฉัน",  # Thai
        "Ελληνικό ιστολόγιο",  # Greek
        "مدونتي",  # Arabic
        "블로그",  # Korean
        "Мой блог 我的博客 🎉",  # mixed
    ],
)
def test_site_title_and_slug_in_any_script(site_title):
    """Titles in any script are kept, and still give a safe project slug."""
    options = InitOptions(site_title=site_title)

    assert options.site_title == site_title
    assert SAFE_SLUG.fullmatch(options.project_slug)


def test_defaults():
    """The defaults are valid and the project slug is derived from the default title."""
    options = InitOptions()

    assert options.site_title == "Untitled Site"
    assert options.site_url == "https://example.com"
    assert options.project_slug == "untitled-site"
    assert options.app_filename == "app.py"
    assert options.site_variable == "app"
    assert options.output_path == "output"
    assert options.include_collection is True
    assert options.include_blog is True
    assert options.include_cli is True


# Site title


def test_site_title_is_stripped():
    """Spaces around the site title are removed."""
    assert InitOptions(site_title="  My Blog  ").site_title == "My Blog"


def test_site_title_using_emojis():
    """Emojis in the site title are kept."""
    assert InitOptions(site_title="🎉 My Blog 🎉").site_title == "🎉 My Blog 🎉"


def test_site_title_using_special_characters():
    """Punctuation and symbols in the site title are kept."""
    assert InitOptions(site_title="My Blog!@#$%^&*()").site_title == "My Blog!@#$%^&*()"


@pytest.mark.parametrize("site_title", ["", "   "])
def test_empty_site_title_is_rejected(site_title):
    """An empty or blank site title is rejected."""
    with pytest.raises(ValueError, match="The site title can't be empty. Please enter a title, e.g. 'My Blog'."):
        InitOptions(site_title=site_title)


# Site URL


@pytest.mark.parametrize(
    "site_url",
    ["https://example.com", "http://example.com", "http://localhost:8000", "https://my-site.dev/blog/", "https://eee"],
)
def test_valid_site_url(site_url):
    """http and https URLs, with or without a port or path, are accepted."""
    assert InitOptions(site_url=site_url).site_url == site_url


@pytest.mark.parametrize("site_url", ["", "ffff", "example.com", "ftp://example.com", "https://"])
def test_invalid_site_url_is_rejected(site_url):
    """URLs without http:// or https:// and a host are rejected."""
    with pytest.raises(ValueError, match="must start with http:// or https://"):
        InitOptions(site_url=site_url)


# Project slug


@pytest.mark.parametrize("site_title, expected_slug", [("My Blog", "my-blog"), ("🎉 My Blog 🎉", "my-blog")])
def test_project_slug_is_derived_from_site_title(site_title, expected_slug):
    """Without a project slug, it's made from the site title."""
    assert InitOptions(site_title=site_title).project_slug == expected_slug


def test_given_project_slug_is_kept():
    """A given project slug is used instead of the title."""
    assert InitOptions(site_title="My Blog", project_slug="custom").project_slug == "custom"


def test_given_project_slug_is_slugified():
    """A given project slug is cleaned up into a safe folder name."""
    assert InitOptions(project_slug="My Site!").project_slug == "my-site"


def test_empty_project_slug_falls_back_to_site_title():
    """An empty project slug falls back to the site title."""
    assert InitOptions(site_title="My Blog", project_slug="").project_slug == "my-blog"


@pytest.mark.parametrize("kwargs", [{"site_title": "!!!"}, {"site_title": "🎉🎉"}, {"project_slug": "!!!"}])
def test_unusable_project_slug_is_rejected(kwargs):
    """A slug without any letter or number is rejected."""
    with pytest.raises(ValueError, match="Can't make a project folder name"):
        InitOptions(**kwargs)


# App filename


@pytest.mark.parametrize("app_filename", ["app.py", "main.py", "my_site.py", "my-app.py", "1app.py", "My App.py"])
def test_valid_app_filename(app_filename):
    """Usual app filenames are accepted as they are."""
    assert InitOptions(app_filename=app_filename).app_filename == app_filename


@pytest.mark.parametrize(
    "app_filename, message",
    [
        ("app.txt", "can't contain a '.' before '.py'"),
        ("my.app.py", "can't contain a '.' before '.py'"),
        ("src/app.py", "without a folder"),
        ("json.py", "already the name of a Python module"),
        ("render_engine.py", "already the name of a Python module"),
    ],
)
def test_invalid_app_filename_is_rejected(app_filename, message):
    """App filenames that can't be imported, or would hide a module the site needs, are rejected."""
    with pytest.raises(ValueError, match=message):
        InitOptions(app_filename=app_filename)


@pytest.mark.parametrize("app_filename, expected", [("app", "app.py"), ("main", "main.py"), ("app.py", "app.py")])
def test_py_is_added_to_app_filename(app_filename, expected):
    """A missing '.py' is added to the app filename."""
    assert InitOptions(app_filename=app_filename).app_filename == expected


def test_app_filename_check_ignores_local_files(tmp_path, monkeypatch):
    """A local file like app.py doesn't make 'app.py' a taken name."""
    (tmp_path / "app.py").write_text("")
    monkeypatch.syspath_prepend(tmp_path)

    assert InitOptions(app_filename="app.py").app_filename == "app.py"


# Site variable


@pytest.mark.parametrize("site_variable", ["app", "site", "my_site", "_site", "stránka"])
def test_valid_site_variable(site_variable):
    """Any Python name can be the site variable."""
    assert InitOptions(site_variable=site_variable).site_variable == site_variable


@pytest.mark.parametrize("site_variable", ["", "my-site", "1site", "my site", "class", "None"])
def test_site_variable_that_isnt_a_python_name_is_rejected(site_variable):
    """The site variable must be usable as a Python name in the app file."""
    with pytest.raises(ValueError, match="must be a Python name"):
        InitOptions(site_variable=site_variable)


@pytest.mark.parametrize("site_variable", ["Page", "Site", "Collection", "Blog", "Pages", "Index"])
def test_site_variable_used_by_app_file_is_rejected(site_variable):
    """A name the app file already uses would be replaced by the site, so it's rejected."""
    with pytest.raises(ValueError, match="the app file already uses that name"):
        InitOptions(site_variable=site_variable)


# Output path


@pytest.mark.parametrize(
    "output_path",
    [
        "output",
        "public",
        "build/site",
        "../docs",
        "/tmp/my-site",
        "app.py/site",
        "my site",
        "./README.md/site",
        "content/output",
        ".output",
        "output/.well-known",
    ],
)
def test_valid_output_path(output_path):
    """The output folder can be anywhere, inside or outside the project."""
    assert InitOptions(output_path=output_path).output_path == output_path


@pytest.mark.parametrize("output_path", ["", ".", "./", "..", "../..", "/"])
def test_output_path_around_project_is_rejected(output_path):
    """An output path without a folder name (the project or a folder above it) is rejected."""
    with pytest.raises(ValueError, match="needs at least one letter or number"):
        InitOptions(output_path=output_path)


@pytest.mark.parametrize("output_path", ["app.py", "pyproject.toml", "README.md", "readme.md", "./README.md/"])
def test_output_path_on_project_file_is_rejected(output_path):
    """The project's files can't be the output folder."""
    with pytest.raises(ValueError, match="is a file of your project"):
        InitOptions(output_path=output_path)


def test_output_path_on_custom_app_filename_is_rejected():
    """A custom app filename is protected like the default one."""
    with pytest.raises(ValueError, match="is a file of your project"):
        InitOptions(app_filename="main.py", output_path="main.py")


# Answer types


@pytest.mark.parametrize(
    "field", ["site_title", "site_url", "project_slug", "app_filename", "site_variable", "output_path"]
)
@pytest.mark.parametrize("value", [None, 42, True])
def test_non_text_answer_is_rejected(field, value):
    """Text answers given as another type are rejected."""
    with pytest.raises(TypeError, match="must be text"):
        InitOptions(**{field: value})


@pytest.mark.parametrize("field", ["include_collection", "include_blog", "include_cli"])
@pytest.mark.parametrize("value", ["no", "yes", "", 0, 1, None])
def test_non_bool_answer_is_rejected(field, value):
    """Yes/no answers given as anything but True or False are rejected."""
    with pytest.raises(TypeError, match="must be True or False"):
        InitOptions(**{field: value})


def test_site_url_is_stripped():
    """Spaces around the site URL are removed."""
    assert InitOptions(site_url="  https://example.com  ").site_url == "https://example.com"


@pytest.mark.parametrize(
    "site_url", ["https://my site.com", "https://example.com/my page", "https://example.com/\tblog"]
)
def test_site_url_with_spaces_is_rejected(site_url):
    """Site URLs with spaces inside are rejected."""
    with pytest.raises(ValueError, match="can't contain spaces"):
        InitOptions(site_url=site_url)


@pytest.mark.parametrize("site_url", ["https://example.com:abc", "http://localhost:99999", "http://localhost:-1"])
def test_site_url_with_invalid_port_is_rejected(site_url):
    """Site URLs with a port that isn't a valid number are rejected."""
    with pytest.raises(ValueError, match="invalid port"):
        InitOptions(site_url=site_url)


@pytest.mark.parametrize(
    "site_title", ["My\nBlog", "My\tBlog", "My\rBlog", "My\x00Blog", "My\u2028Blog", "My\u2029Blog"]
)
def test_site_title_with_control_characters_is_rejected(site_title):
    """Site titles with tabs or line breaks are rejected."""
    with pytest.raises(ValueError, match="must be on one line"):
        InitOptions(site_title=site_title)


@pytest.mark.parametrize("site_title", ["👨‍👩‍👧 Family Blog", "Café ☕", "Blog — 2026"])
def test_site_title_with_special_unicode_is_kept(site_title):
    """Joined emojis, accents and dashes in the site title are kept."""
    assert InitOptions(site_title=site_title).site_title == site_title


def test_output_path_with_hidden_subfolder_is_kept():
    """A hidden folder inside the output folder is fine."""
    assert InitOptions(output_path="output/.well-known").output_path == "output/.well-known"


def test_every_answer_has_a_type_check():
    """Every answer needs a text or True/False default, so `_validate_types` knows which type to check."""
    for field in fields(InitOptions):
        assert isinstance(field.default, (str, bool)), f"{field.name} has no text or True/False default"
