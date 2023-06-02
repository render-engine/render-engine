import pytest
from src.render_engine.hookspecs import hook_impl
from src.render_engine.page import Page
from src.render_engine.site import Site


class FakePlugin:
    """Clean the output folder before rendering"""

    @hook_impl
    def pre_build_site(site: type[Site]):
        """Clean the output folder before rendering"""
        pass

@pytest.fixture
def site():
    class TestSite(Site):
        plugins = [
            FakePlugin,
        ]

    return TestSite()

def test_register_plugins(site):
    """Check that the plugin is registered"""
    assert site._pm.list_name_plugin()[0][0] == 'FakePlugin' 


def test_page_plugin_inherits_from_page(site):
    
    class TestPage(Page):
        pass


    page = Page()
    page.register_plugins(*site.plugins)
    assert page._pm.list_name_plugin()[0][0] == 'FakePlugin'