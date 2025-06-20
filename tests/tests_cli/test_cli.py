import frontmatter
import pytest
import toml

from render_engine import Page, Site
from render_engine.cli.cli import (
    create_collection_entry,
    display_filtered_templates,
    get_available_themes,
    get_site_content_paths,
    load_config,
    split_args,
    split_module_site,
)
from render_engine.collection import Collection


@pytest.fixture(scope="module")
def site(tmp_path_factory):
    class FakeSite(Site):
        output_path = tmp_path_factory.getbasetemp() / "output_path"

    site = FakeSite()

    content_path1 = tmp_path_factory.getbasetemp() / "test_content_path1.txt"
    content_path1.write_text("Hello Wold")

    content_path2 = tmp_path_factory.getbasetemp() / "test_content_path2.txt"
    content_path2.write_text("Hello Space")

    @site.page
    class FakePage1(Page):
        content_path = content_path1

    @site.page
    class FakePage2(Page):
        content_path = content_path2

    return site


def test_get_site_content_path(site, tmp_path_factory):
    """Tests that the paths returned from the pages"""

    content_path1 = tmp_path_factory.getbasetemp() / "test_content_path1.txt"
    content_path2 = tmp_path_factory.getbasetemp() / "test_content_path2.txt"

    expected = [content_path1, content_path2]
    expected.extend(site.static_paths)
    expected.append(site.template_path)
    assert get_site_content_paths(site) == expected


@pytest.mark.skip("Not sure how to test importlib")
def test_import_lib_gets_site():
    pass


def test_collection_call():
    """Tests that you can get content from the parser using `new_entry`"""
    test_collection = Collection()
    content = create_collection_entry(content=None, collection=test_collection, foo="bar")
    post = frontmatter.loads(content)

    assert post["title"] == "Untitled Entry"
    assert post["foo"] == "bar"


def test_collection_call_with_content():
    """Tests that you can get content from the parser using `new_entry`"""
    test_collection = Collection()
    content = create_collection_entry(content="This is a test", collection=test_collection, foo="bar")
    post = frontmatter.loads(content)

    assert post["title"] == "Untitled Entry"
    assert post["foo"] == "bar"
    assert post.content == "This is a test"


@pytest.mark.parametrize(
    "args,expected",
    [
        (["key1=value1", "key2=value2"], {"key1": "value1", "key2": "value2"}),
        (["key1:value1", "key2:value2"], {"key1": "value1", "key2": "value2"}),
        (["author=John Doe", "tags:python,testing"], {"author": "John Doe", "tags": "python,testing"}),
        ([], {}),
        (None, {}),
    ],
)
def test_split_args_functionality(args, expected):
    """Tests split_args parsing for custom key-value pairs"""
    result = split_args(args)
    assert result == expected


def test_split_args_error_handling():
    """Tests split_args error handling for invalid formats"""
    with pytest.raises(ValueError, match="Invalid argument"):
        split_args(["invalid_format"])

    with pytest.raises(ValueError, match="already defined"):
        split_args(["key=value1", "key=value2"])


def test_config_loading_with_valid_config(tmp_path, monkeypatch):
    """Tests config loading from pyproject.toml (2025.5.1b1 feature)"""
    config_content = {"render-engine": {"cli": {"module": "myapp", "site": "MySite", "collection": "MyCollection"}}}

    config_file = tmp_path / "pyproject.toml"
    config_file.write_text(toml.dumps(config_content))

    # Change to temp directory for config loading test
    monkeypatch.chdir(tmp_path)

    # Test that load_config doesn't raise an exception
    load_config(str(config_file))


def test_config_loading_missing_file(tmp_path, monkeypatch, capsys):
    """Tests config loading behavior when pyproject.toml is missing"""
    monkeypatch.chdir(tmp_path)

    # Should not raise exception, just print message
    load_config("nonexistent.toml")

    captured = capsys.readouterr()
    assert "No config file found" in captured.out


def test_config_loading_invalid_file(tmp_path, monkeypatch, capsys):
    """Tests config loading behavior when pyproject.toml is malformed"""

    config_file = tmp_path / "pyproject.toml"
    config_file.write_text("Lorem ipsum")

    # Change to temp directory for config loading test
    monkeypatch.chdir(tmp_path)

    # Test that load_config doesn't raise an exception
    load_config(str(config_file))


def test_collection_entry_with_custom_attributes():
    """Tests that custom attributes are passed through to collection entry"""
    test_collection = Collection()
    content = create_collection_entry(
        content="Test content", collection=test_collection, author="Test Author", tags="test,example"
    )
    post = frontmatter.loads(content)

    assert post["author"] == "Test Author"
    assert post["tags"] == "test,example"
    assert post.content == "Test content"


def test_split_module_site_valid():
    """Tests split_module_site with valid input"""
    import_path, site = split_module_site("app:site")
    assert import_path == "app"
    assert site == "site"

    import_path, site = split_module_site("my_module:MySite")
    assert import_path == "my_module"
    assert site == "MySite"


def test_split_module_site_invalid():
    """Tests split_module_site with invalid input"""
    import typer

    with pytest.raises(typer.BadParameter, match="module_site must be of the form"):
        split_module_site("invalid_format")


def test_get_available_themes_with_valid_theme(site):
    """Tests get_available_themes with a valid theme"""
    from unittest.mock import Mock

    from rich.console import Console

    # Mock theme manager
    mock_theme_manager = Mock()
    mock_prefix = Mock()
    mock_prefix.list_templates.return_value = ["template1.html", "template2.html"]
    mock_theme_manager.prefix = {"test_theme": mock_prefix}
    site.theme_manager = mock_theme_manager

    console = Console()
    templates = get_available_themes(console, site, "test_theme")

    assert templates == ["template1.html", "template2.html"]
    mock_prefix.list_templates.assert_called_once()


def test_get_available_themes_with_invalid_theme(site, capsys):
    """Tests get_available_themes with an invalid theme"""
    from unittest.mock import Mock

    from rich.console import Console

    # Mock theme manager
    mock_theme_manager = Mock()
    mock_theme_manager.prefix = {}
    site.theme_manager = mock_theme_manager

    console = Console()
    templates = get_available_themes(console, site, "nonexistent_theme")

    assert templates == []


def test_display_filtered_templates():
    """Tests display_filtered_templates function"""
    from unittest.mock import patch

    templates = ["page.html", "base.html", "archive.html", "sitemap.xml"]

    with patch("render_engine.cli.cli.rprint") as mock_rprint:
        display_filtered_templates("Test Templates", templates, "html")
        mock_rprint.assert_called_once()

        # Check that the table was created with filtered results
        call_args = mock_rprint.call_args[0][0]
        assert call_args.title == "Test Templates"
