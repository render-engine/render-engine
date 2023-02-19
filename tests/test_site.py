import pluggy
import pytest

from render_engine.collection import Collection
from render_engine.page import Page
from render_engine.site import Site

pm = pluggy.PluginManager("fake_test")


def test_site_defaults():
    """
    Tests that a site can be created with default variables.
    Those values are:
        - SITE_TITLE: "Untitled Site"
        - SITE_URL: "http://example.com"
    """

    site = Site()

    assert site.site_vars["SITE_TITLE"] == "Untitled Site"
    assert site.site_vars["SITE_URL"] == "http://localhost:8000/"


def test_site_site_vars_orrider_defaults_via_class():
    """
    Tests that a site can be created with default variables.
    """

    site = Site()
    site_vars = {
        "SITE_TITLE": "My Site",
        "SITE_URL": "https://my-site.com",
    }

    site.site_vars = site_vars

    assert site.site_vars["SITE_TITLE"] == "My Site"
    assert site.site_vars["SITE_URL"] == "https://my-site.com"


def test_site_page_in_route_list(tmp_path):
    tmp_dir = tmp_path / "content"
    tmp_dir.mkdir()
    file = tmp_dir / "test.md"
    file.write_text("test")

    site = Site()

    # assert that the route list is empty
    assert len(site.route_list) == 0

    class CustomPage(Page):
        test_value = "test"
        content_path = file.absolute()

    site.page(CustomPage)

    assert site.route_list["custompage"].test_value == "test"


def test_site_collection_in_route_list():
    """Tests that when a collection is added to the route_list it is only the colleciton"""
    site = Site()

    # assert that the route list is empty
    assert len(site.route_list) == 0

    class CustomPage(Page):
        test_value = "test"

    class collection(Collection):
        pages = [CustomPage(), CustomPage()]

    collection = site.collection(collection)

    assert site.route_list["collection"] == collection
    assert len(site.route_list) == 1


def test_site_page_with_multiple_routes_has_one_entry_in_routes_list():
    site = Site()

    class CustomPage(Page):
        test_value = "test"
        routes = ["customroute", "customroute2"]

    site.page(CustomPage)

    assert len(site.route_list) == 1
