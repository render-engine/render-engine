import datetime
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from typer.testing import CliRunner

from render_engine.cli.cli import app, new_entry


@pytest.fixture
def runner():
    """CLI test runner fixture"""
    return CliRunner()


@pytest.fixture
def test_site_module(tmp_path):
    """Creates a test site module file"""
    site_content = """
from render_engine import Site, Page, Collection

site = Site()
site.output_path = "output"

@site.page
class TestPage(Page):
    content = "Test content"

@site.collection
class TestCollection(Collection):
    content_path = "content"
"""
    site_file = tmp_path / "test_app.py"
    site_file.write_text(site_content)
    return tmp_path, "test_app:site"


def test_build_command_success(runner, test_site_module, monkeypatch):
    """Tests build command with valid module:site"""
    tmp_path, module_site = test_site_module
    monkeypatch.chdir(tmp_path)

    with patch("render_engine.cli.cli.get_site") as mock_get_site:
        mock_site = Mock()
        mock_site.render = Mock()
        mock_get_site.return_value = mock_site

        result = runner.invoke(app, ["build", module_site])

        assert result.exit_code == 0
        mock_get_site.assert_called_once_with("test_app", "site")
        mock_site.render.assert_called_once()


def test_build_command_with_clean(runner, test_site_module, monkeypatch):
    """Tests build command with --clean flag"""
    tmp_path, module_site = test_site_module
    monkeypatch.chdir(tmp_path)

    with (
        patch("render_engine.cli.cli.get_site") as mock_get_site,
        patch("render_engine.cli.cli.remove_output_folder") as mock_remove,
    ):
        mock_site = Mock()
        mock_site.render = Mock()
        mock_site.output_path = "output"
        mock_get_site.return_value = mock_site

        result = runner.invoke(app, ["build", module_site, "--clean"])

        assert result.exit_code == 0
        mock_remove.assert_called_once()
        mock_site.render.assert_called_once()


def test_build_command_invalid_module_site(runner):
    """Tests build command with invalid module:site format"""
    result = runner.invoke(app, ["build", "invalid_format"])

    assert result.exit_code != 0
    assert "module_site must be of the form" in result.output


def test_templates_command_success(runner, test_site_module, monkeypatch):
    """Tests templates command with valid module:site"""
    tmp_path, module_site = test_site_module
    monkeypatch.chdir(tmp_path)

    with patch("render_engine.cli.cli.get_site") as mock_get_site:
        mock_site = Mock()
        mock_theme_manager = Mock()
        mock_prefix = Mock()
        mock_prefix.list_templates.return_value = ["template1.html", "template2.html"]
        mock_theme_manager.prefix = {"test_theme": mock_prefix}
        mock_site.theme_manager = mock_theme_manager
        mock_get_site.return_value = mock_site

        result = runner.invoke(app, ["templates", module_site, "--theme-name", "test_theme"])

        assert result.exit_code == 0
        mock_get_site.assert_called_once_with("test_app", "site")


def test_templates_command_no_theme_specified(runner, test_site_module, monkeypatch):
    """Tests templates command without theme name (lists all themes)"""
    tmp_path, module_site = test_site_module
    monkeypatch.chdir(tmp_path)

    with patch("render_engine.cli.cli.get_site") as mock_get_site:
        mock_site = Mock()
        mock_theme_manager = Mock()
        mock_prefix = Mock()
        mock_prefix.list_templates.return_value = ["template1.html", "template2.html"]
        mock_theme_manager.prefix = {"theme1": mock_prefix, "theme2": mock_prefix}
        mock_site.theme_manager = mock_theme_manager
        mock_get_site.return_value = mock_site

        result = runner.invoke(app, ["templates", module_site])

        assert result.exit_code == 0
        assert "No theme name specified" in result.output


def test_new_entry_command_success(runner, test_site_module, monkeypatch):
    """Tests new_entry command with valid parameters"""
    tmp_path, module_site = test_site_module
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("render_engine.cli.cli.os.getenv", lambda *_: {})

    # Create content directory
    content_dir = tmp_path / "content"
    content_dir.mkdir()

    with (
        patch("render_engine.cli.cli.get_site") as mock_get_site,
        patch("render_engine.cli.cli.create_collection_entry") as mock_create_entry,
    ):
        mock_site = Mock()
        mock_collection = Mock()
        mock_collection.content_path = str(content_dir)
        type(mock_collection).__name__ = "TestCollection"
        mock_site.route_list = {"test": mock_collection}
        mock_get_site.return_value = mock_site
        mock_create_entry.return_value = "---\ntitle: Test Entry\n---\nTest content"

        result = runner.invoke(
            app,
            [
                "new-entry",
                module_site,
                "testcollection",
                "test.md",
                "--content",
                "Test content",
            ],
        )

        assert result.exit_code == 0
        mock_create_entry.assert_called_once()

        # Check that the file was created
        created_file = content_dir / "test.md"
        assert created_file.exists()


def test_new_entry_command_with_args(runner, test_site_module, monkeypatch):
    """Tests new_entry command with --args parameter"""
    tmp_path, module_site = test_site_module
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("render_engine.cli.cli.os.getenv", lambda *_: {})

    content_dir = tmp_path / "content"
    content_dir.mkdir()

    with (
        patch("render_engine.cli.cli.get_site") as mock_get_site,
        patch("render_engine.cli.cli.create_collection_entry") as mock_create_entry,
    ):
        mock_site = Mock()
        mock_collection = Mock()
        mock_collection.content_path = str(content_dir)
        type(mock_collection).__name__ = "TestCollection"
        mock_site.route_list = {"test": mock_collection}
        mock_get_site.return_value = mock_site
        mock_create_entry.return_value = "---\ntitle: Custom Title\nauthor: Test Author\n---\nTest content"

        result = runner.invoke(
            app,
            [
                "new-entry",
                module_site,
                "testcollection",
                "test.md",
                "--args",
                "author=Test Author",
                "--title",
                "Custom Title",
            ],
        )

        assert result.exit_code == 0
        mock_create_entry.assert_called_once()


def test_new_entry_command_missing_required_args(runner):
    """Tests new_entry command with missing required arguments"""
    result = runner.invoke(app, ["new-entry"])

    assert result.exit_code != 0


@pytest.mark.parametrize(
    "options, expected",
    [
        (
            {
                "collection": "testcollection",
                "filename": "test.md",
                "args": ["date=May 23, 2025"],
                "title": "New Entry",
                "slug": "slug1",
                "content": "content",
            },
            {"date": datetime.datetime.fromisoformat("2025-05-23T00:00:00"), "slug": "slug1", "content": "content"},
        ),
        (
            {
                "collection": "testcollection",
                "filename": "test.md",
                "args": ["date=May 23, 2025"],
                "title": "New Entry",
                "slug": "slug1",
                "content": "content",
                "include_date": True,
            },
            {"date": datetime.datetime.fromisoformat("2025-05-23T00:00:00"), "slug": "slug1", "content": "content"},
        ),
        (
            {
                "collection": "testcollection",
                "filename": "test.md",
                "title": "New Entry",
                "slug": "slug1",
                "content": "content",
            },
            {"slug": "slug1", "content": "content"},
        ),
    ],
)
def test_new_entry_date_options(options, expected, monkeypatch, test_site_module, runner):
    """Test arg parsing and handling is correct"""
    passed_args = {}

    def mock_create_collection_entry(**kwargs):
        """Preserve the arguments passed to create_collection_entry for inspection"""
        nonlocal passed_args
        passed_args = kwargs
        return "---\ntitle: Custom Title\nauthor: Test Author\n---\nTest content"

    tmp_path, module_site = test_site_module
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("render_engine.cli.cli.os.getenv", lambda *_: {})
    monkeypatch.setattr("render_engine.cli.cli.create_collection_entry", mock_create_collection_entry)
    content_dir = tmp_path / "content"
    content_dir.mkdir()

    with (
        patch("render_engine.cli.cli.get_site") as mock_get_site,
    ):
        mock_site = Mock()
        mock_collection = Mock()
        mock_collection.content_path = str(content_dir)
        type(mock_collection).__name__ = "TestCollection"
        mock_site.route_list = {"test": mock_collection}
        mock_get_site.return_value = mock_site

        new_entry(module_site=module_site, **options)
        # Pop the collection from the passed arguments since it's not relevant.
        passed_args.pop("collection")

        # include_date needs some special handling.
        if "include_date" in options:
            if not any(arg.startswith("date=") or arg.startswith("date:") for arg in options.get("args", [])):
                assert "date" in passed_args
                assert (
                    datetime.datetime.fromisoformat(passed_args.pop("date")).date() == datetime.datetime.today().date()
                )

        assert passed_args == expected


def test_new_entry_content_and_content_file(runner):
    """Test failure with both content and content-file"""
    result = runner.invoke(
        app,
        [
            "new-entry",
            "app:app",
            "testcollection",
            "test.md",
            "--content",
            "lorem ipsum",
            "--content-file",
            "llama.txt",
        ],
    )

    assert result.exit_code != 0


def test_serve_command_basic(runner, test_site_module, monkeypatch):
    """Tests serve command basic functionality"""
    tmp_path, module_site = test_site_module
    monkeypatch.chdir(tmp_path)

    with (
        patch("render_engine.cli.cli.get_site") as mock_get_site,
        patch("render_engine.cli.cli.ServerEventHandler") as mock_handler_class,
    ):
        mock_site = Mock()
        mock_site.render = Mock()
        mock_site.output_path = "output"
        mock_get_site.return_value = mock_site

        mock_handler = Mock()
        mock_handler.__enter__ = Mock(return_value=mock_handler)
        mock_handler.__exit__ = Mock(return_value=None)
        mock_handler_class.return_value = mock_handler

        result = runner.invoke(app, ["serve", module_site, "--port", "8080"])

        assert result.exit_code == 0
        mock_get_site.assert_called_once_with("test_app", "site")
        mock_site.render.assert_called_once()
        mock_handler_class.assert_called_once()


def test_serve_command_with_reload(runner, test_site_module, monkeypatch):
    """Tests serve command with --reload flag"""
    tmp_path, module_site = test_site_module
    monkeypatch.chdir(tmp_path)

    with (
        patch("render_engine.cli.cli.get_site") as mock_get_site,
        patch("render_engine.cli.cli.ServerEventHandler") as mock_handler_class,
        patch("render_engine.cli.cli.get_site_content_paths") as mock_get_paths,
    ):
        mock_site = Mock()
        mock_site.render = Mock()
        mock_site.output_path = "output"
        mock_get_site.return_value = mock_site
        mock_get_paths.return_value = [Path("content")]

        mock_handler = Mock()
        mock_handler.__enter__ = Mock(return_value=mock_handler)
        mock_handler.__exit__ = Mock(return_value=None)
        mock_handler_class.return_value = mock_handler

        result = runner.invoke(app, ["serve", module_site, "--reload"])

        assert result.exit_code == 0
        mock_get_paths.assert_called_once_with(mock_site)
