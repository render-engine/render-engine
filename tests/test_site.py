import pytest

from src.render_engine.site import Site


def test_site_defaults(site):
    """
    Tests that a site can be created with default variables.
    Those values are:
        - SITE_TITLE: "Untitled Site"
        - SITE_URL: "http://example.com"
    """

    assert site.site_vars["SITE_TITLE"] == "Untitled Site"
    assert site.site_vars["SITE_URL"] == "https://example.com"


def test_site_site_vars_orrider_defaults_via_class(site):
    """
    Tests that a site can be created with default variables.
    """

    class site(Site):
        site_vars = {
            "SITE_TITLE": "My Site",
            "SITE_URL": "https://my-site.com",
        }

    assert site.site_vars["SITE_TITLE"] == "My Site"
    assert site.site_vars["SITE_URL"] == "https://my-site.com"
