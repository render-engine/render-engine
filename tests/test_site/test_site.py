import pytest
from jinja2 import Template

from render_engine.collection import Collection
from render_engine.page import Page
from render_engine.site import Site


def test_site_default_values(base_site):
    """Testing that sites have some default values"""
    assert base_site.site_vars["SITE_TITLE"] == "Untitled Site"
    assert base_site.site_vars["SITE_URL"] == "https://example.com"


def test_site_rendered_page_has_access_to_site_vars(base_site, temp_path):
    """Testing that site_var values are passed into page templates"""

    @base_site.render_page
    class CustomPageFromSiteWithVars(Page):
        template = Template("{{SITE_TITLE}}")

    test_path = temp_path.joinpath("custompagefromsitewithvars.html")
    assert test_path.exists()
    assert test_path.read_text() == base_site.site_vars["SITE_TITLE"]


def test_site_rendered_collection_extends_path(
    base_site, temp_path, base_content, gen_content
):
    """Tests that output paths can be pushed beyond the root directory"""
    content_test_path = temp_path.joinpath("content")
    content_test_path.mkdir()
    content_test_path.joinpath("foo.md").write_text(gen_content)
    output_test_path = "output/collection"

    @base_site.render_collection
    class CustomCollection(Collection):
        output_path = output_test_path
        content_path = content_test_path
        template = Template("Foo")

    test_path = temp_path.joinpath(output_test_path)
    assert test_path.exists()
    assert [x.name for x in test_path.iterdir()] == ["test-title.html"]
    check_file = temp_path / output_test_path / "test-title.html"
    assert check_file.read_text() == f"Foo"
