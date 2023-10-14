import pytest

from render_engine import collection


def test_cli_author_name(default_cli, tmp_path_factory):
    """Asserts there is a SITE_AUTHOR and SITE_EMAIL in the author patch"""
    temp_app = tmp_path_factory.getbasetemp() / "test_default_cli_app" / "app.py"
    assert "\"name\": \"Test Site Author\"" in temp_app.read_text()

def test_cli_author_email(default_cli, tmp_path_factory):
    """Asserts there is a SITE_AUTHOR and SITE_EMAIL in the author patch"""
    temp_app = tmp_path_factory.getbasetemp() / "test_default_cli_app" / "app.py"
    assert "\"email\": \me@example.com"

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
        )
    ]
)
def test_collection_in_init(tmp_path_factory, cli, exists):
    """Asserts a collection in the init"""
    if exists:
        collection_path = tmp_path_factory.getbasetemp() / "test_default_cli_app" / "pages"
        assert collection_path.exists()
        assert 'sample_page.md' in [str(path.name) for path in collection_path.iterdir()]
    else:
        collection_path = tmp_path_factory.getbasetemp() / "test_skip_collection_cli_app" / "pages"
        assert not collection_path.exists()


def test_site_has_NAVIGATION(tmp_path_factory, default_cli):
    """Assert the generated site has a NAVIGATION item in site_vars"""
    site = tmp_path_factory.getbasetemp() / "test_default_cli_app" / "app.py"
    assert site.exists()
    assert 'NAVIGATION' in site.read_text()

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
        )
    ]
)
def test_path_NAVIGATION_includes_collection_if_not_skipped(
    tmp_path_factory,
    cli,
    exists
):
    """Tests that the path to the generated collection page exists if the collection is not skipped"""
    if exists:
        app = tmp_path_factory.getbasetemp() / "test_default_cli_app" / "app.py"
        
    else:
        app = tmp_path_factory.getbasetemp() / "test_skip_collection_cli_app" / "app.py"

    app_content = app.read_text()
    assert "NAVIGATION" in app_content
    assert ("/example-page.html" in app_content) == exists
