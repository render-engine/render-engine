import pytest

from render_engine.site import Collection, Page, Site


def test_site_defaults():
    """
    Tests that a site can be created with default variables.
    Those values are:
        - SITE_TITLE: "Untitled Site"
        - SITE_URL: "http://example.com"
    """

    site = Site()

    assert site.site_vars["SITE_TITLE"] == "Untitled Site"
    assert site.site_vars["SITE_URL"] == "https://example.com"


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


def test_site_page_in_route_list():
    site = Site()

    # assert that the route list is empty
    assert len(site.route_list) == 0

    class CustomPage(Page):
        test_value = "test"

    site.page(CustomPage)

    assert site.route_list["custompage"].test_value == "test"


def test_site_collection_in_route_list():
    site = Site()

    # assert that the route list is empty
    assert len(site.route_list) == 0

    class CustomPage(Page):
        test_value = "test"

    class collection(Collection):
        pages = [CustomPage()]

    site.collection(collection)

    assert site.route_list["custompage"].test_value == "test"
