import pytest
import typer

from render_engine.cli import cli


def test_module_site_raises_error_if_not():
    """Asserts a typer BadParameter is raised if the module_site is not a module"""
    with pytest.raises(typer.BadParameter):
        cli.split_module_site("Not Correct Format")


def test_cli_author_owner(default_cli, tmp_path_factory):
    """Asserts there is a `OWNER` key"""
    temp_app = tmp_path_factory.getbasetemp() / "test_default_cli_app" / "app.py"
    assert '"OWNER":' in temp_app.read_text()


def test_cli_author_name(default_cli, tmp_path_factory):
    """Asserts there is a `name` key in the OWNER value"""
    temp_app = tmp_path_factory.getbasetemp() / "test_default_cli_app" / "app.py"
    assert '"name": "Test Site Author"' in temp_app.read_text()


def test_cli_author_email(default_cli, tmp_path_factory):
    """Asserts there is a `email` in the OWNER value"""
    temp_app = tmp_path_factory.getbasetemp() / "test_default_cli_app" / "app.py"
    assert '"email": "hello@example.com"' in temp_app.read_text()


def test_cli_static_path(default_cli, tmp_path_factory):
    """Asserts there is a SITE_STATIC_PATH in the author patch"""
    temp_app = tmp_path_factory.getbasetemp() / "test_default_cli_app" / "app.py"
    assert 'app.static_paths.add("static")' in temp_app.read_text()


def test_cli_skips_static(skip_static_cli, tmp_path_factory):
    """Asserts the static path is not in the app.py if the skip_static flag is set"""
    temp_app = tmp_path_factory.getbasetemp() / "test_skip_static_cli_app" / "app.py"
    assert 'app.static_paths.add("static")' not in temp_app.read_text()

    assert "static" not in list((tmp_path_factory.getbasetemp() / "test_skip_static_cli_app").iterdir())


@pytest.mark.parametrize(
    "cli, exists",
    [
        (
            pytest.lazy_fixture("skip_collection_cli"),
            False,
        ),
        (
            pytest.lazy_fixture("default_cli"),
            True,
        ),
    ],
)
def test_collection_in_init(tmp_path_factory, cli, exists):
    """Asserts a collection in the init"""
    if exists:
        collection_path = tmp_path_factory.getbasetemp() / "test_default_cli_app" / "pages"
        assert collection_path.exists()
        assert "sample_page.md" in [str(path.name) for path in collection_path.iterdir()]
    else:
        collection_path = tmp_path_factory.getbasetemp() / "test_skip_collection_cli_app" / "pages"
        assert not collection_path.exists()


def test_site_has_NAVIGATION(tmp_path_factory, default_cli):
    """Assert the generated site has a NAVIGATION item in site_vars"""
    site = tmp_path_factory.getbasetemp() / "test_default_cli_app" / "app.py"
    assert site.exists()
    assert '"NAVIGATION":' in site.read_text()


@pytest.mark.parametrize(
    "cli, exists",
    [
        (
            pytest.lazy_fixture("skip_collection_cli"),
            False,
        ),
        (
            pytest.lazy_fixture("default_cli"),
            True,
        ),
    ],
)
def test_path_NAVIGATION_includes_collection_if_not_skipped(tmp_path_factory, cli, exists):
    """Tests that the path to the generated collection page exists if the collection is not skipped"""
    if exists:
        app = tmp_path_factory.getbasetemp() / "test_default_cli_app" / "app.py"

    else:
        app = tmp_path_factory.getbasetemp() / "test_skip_collection_cli_app" / "app.py"

    app_content = app.read_text()
    assert "NAVIGATION" in app_content
    assert ("/example-page.html" in app_content) == exists


def tests_project_folder_not_exists_error():
    """Asserts that a project folder that does not exist raises an error"""
    with pytest.raises(FileNotFoundError):
        cli.init(
            project_folder="does-not-exist",
            collection_path="foo",
            site_title="foo",
            site_url="foo",
            owner_email="foo",
            owner_name="foo",
        )
