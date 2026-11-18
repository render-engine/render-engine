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
    assert options.output_path == "output"
    assert options.include_collection is True
    assert options.include_blog is True
    assert options.include_cli is True


# Site title


def test_site_title_is_stripped():
    assert InitOptions(site_title="  My Blog  ").site_title == "My Blog"


def test_site_title_using_emojis():
    assert InitOptions(site_title="🎉 My Blog 🎉").site_title == "🎉 My Blog 🎉"


def test_site_title_using_special_characters():
    assert InitOptions(site_title="My Blog!@#$%^&*()").site_title == "My Blog!@#$%^&*()"


@pytest.mark.parametrize("site_title", ["", "   "])
def test_empty_site_title_is_rejected(site_title):
    with pytest.raises(ValueError, match="The site title can't be empty. Please enter a title, e.g. 'My Blog'."):
        InitOptions(site_title=site_title)


# Site URL


@pytest.mark.parametrize(
    "site_url",
    ["https://example.com", "http://example.com", "http://localhost:8000", "https://my-site.dev/blog/", "https://eee"],
)
def test_valid_site_url(site_url):
    assert InitOptions(site_url=site_url).site_url == site_url


@pytest.mark.parametrize("site_url", ["", "ffff", "example.com", "ftp://example.com", "https://"])
def test_invalid_site_url_is_rejected(site_url):
    with pytest.raises(ValueError, match="must start with http:// or https://"):
        InitOptions(site_url=site_url)


# Project slug


@pytest.mark.parametrize("site_title, expected_slug", [("My Blog", "my-blog"), ("🎉 My Blog 🎉", "my-blog")])
def test_project_slug_is_derived_from_site_title(site_title, expected_slug):
    assert InitOptions(site_title=site_title).project_slug == expected_slug


def test_given_project_slug_is_kept():
    assert InitOptions(site_title="My Blog", project_slug="custom").project_slug == "custom"


def test_given_project_slug_is_slugified():
    assert InitOptions(project_slug="My Site!").project_slug == "my-site"


def test_empty_project_slug_falls_back_to_site_title():
    assert InitOptions(site_title="My Blog", project_slug="").project_slug == "my-blog"


@pytest.mark.parametrize("kwargs", [{"site_title": "!!!"}, {"site_title": "🎉🎉"}, {"project_slug": "!!!"}])
def test_unusable_project_slug_is_rejected(kwargs):
    with pytest.raises(ValueError, match="Can't make a project name"):
        InitOptions(**kwargs)


# App filename


@pytest.mark.parametrize("app_filename", ["app.py", "main.py", "my_site.py"])
def test_valid_app_filename(app_filename):
    assert InitOptions(app_filename=app_filename).app_filename == app_filename


@pytest.mark.parametrize(
    "app_filename, message",
    [
        ("app", "must end with '.py'"),
        ("app.txt", "must end with '.py'"),
        ("src/app.py", "without a folder"),
        ("my-app.py", "can only use letters, numbers and underscores"),
        ("1app.py", "can only use letters, numbers and underscores"),
        ("json.py", "already the name of a Python module"),
        ("render_engine.py", "already the name of a Python module"),
        ("__init__.py", "can only use letters, numbers and underscores"),
        ("!!!.py", "can only use letters, numbers and underscores"),
    ],
)
def test_invalid_app_filename_is_rejected(app_filename, message):
    with pytest.raises(ValueError, match=message):
        InitOptions(app_filename=app_filename)


# Output path


@pytest.mark.parametrize("output_path", ["output", "public", "build/site"])
def test_valid_output_path(output_path):
    assert InitOptions(output_path=output_path).output_path == output_path


@pytest.mark.parametrize("output_path", ["", ".", "./", "..", "../out", "a/../..", "/tmp/out"])
def test_output_path_outside_project_is_rejected(output_path):
    with pytest.raises(ValueError, match="must be a folder inside your project"):
        InitOptions(output_path=output_path)


@pytest.mark.parametrize(
    "output_path", ["content", "templates", "static", "content/output", "Content", "STATIC", "Templates/out"]
)
def test_output_path_in_site_folders_is_rejected(output_path):
    with pytest.raises(ValueError, match="holds your site's own files"):
        InitOptions(output_path=output_path)


# Answer types


@pytest.mark.parametrize("field", ["site_title", "site_url", "project_slug", "app_filename", "output_path"])
@pytest.mark.parametrize("value", [None, 42, True])
def test_non_text_answer_is_rejected(field, value):
    with pytest.raises(TypeError, match="must be text"):
        InitOptions(**{field: value})


@pytest.mark.parametrize("field", ["include_collection", "include_blog", "include_cli"])
@pytest.mark.parametrize("value", ["no", "yes", "", 0, 1, None])
def test_non_bool_answer_is_rejected(field, value):
    with pytest.raises(TypeError, match="must be True or False"):
        InitOptions(**{field: value})


def test_site_url_is_stripped():
    assert InitOptions(site_url="  https://example.com  ").site_url == "https://example.com"


@pytest.mark.parametrize(
    "site_url", ["https://my site.com", "https://example.com/my page", "https://example.com/\tblog"]
)
def test_site_url_with_spaces_is_rejected(site_url):
    with pytest.raises(ValueError, match="can't contain spaces"):
        InitOptions(site_url=site_url)


@pytest.mark.parametrize("site_url", ["https://example.com:abc", "http://localhost:99999", "http://localhost:-1"])
def test_site_url_with_invalid_port_is_rejected(site_url):
    with pytest.raises(ValueError, match="invalid port"):
        InitOptions(site_url=site_url)


@pytest.mark.parametrize(
    "site_title", ["My\nBlog", "My\tBlog", "My\rBlog", "My\x00Blog", "My\u2028Blog", "My\u2029Blog"]
)
def test_site_title_with_control_characters_is_rejected(site_title):
    with pytest.raises(ValueError, match="must be on one line"):
        InitOptions(site_title=site_title)


@pytest.mark.parametrize("site_title", ["👨‍👩‍👧 Family Blog", "Café ☕", "Blog — 2026"])
def test_site_title_with_special_unicode_is_kept(site_title):
    assert InitOptions(site_title=site_title).site_title == site_title


@pytest.mark.parametrize("output_path", [".git", ".venv", ".github", ".output", ".git/site"])
def test_hidden_output_path_is_rejected(output_path):
    with pytest.raises(ValueError, match="folders starting with '.'"):
        InitOptions(output_path=output_path)


def test_output_path_with_hidden_subfolder_is_kept():
    assert InitOptions(output_path="output/.well-known").output_path == "output/.well-known"


def test_every_answer_has_a_type_check():
    """Every answer needs a text or True/False default, so `_validate_types` knows which type to check."""
    for field in fields(InitOptions):
        assert isinstance(field.default, (str, bool)), f"{field.name} has no text or True/False default"
