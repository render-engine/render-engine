import typing
import logging
import pytest
from render_engine.hookspecs import hook_impl
from render_engine.page import Page
from render_engine.site import Site
from render_engine.collection import Collection


class FakePlugin:
    """Clean the output folder before rendering"""

    @hook_impl
    def pre_build_site(
        site: type[Site],
        settings: dict[str, typing.Any]|None,
        ):
        """Clean the output folder before rendering"""
        if settings:
            logging.info(settings['FakePlugin']['test'])
        else:
            print(settings)
            raise ValueError("FAIL")

@pytest.fixture
def site():
    class TestSite(Site):
        plugins = [
            FakePlugin,
        ]

    return TestSite()

def test_register_plugins(site: "TestSite"):
    """Check that the plugin is registered"""
    assert site._pm.list_name_plugin()[0][0] == 'FakePlugin' 

def test_pages_in_collection_inherit_pugins():
    """Check that collection plugins are inherited by pages in the collection"""

    collection = Collection()
    collection.register_plugins([FakePlugin])
    page = collection.get_page()
    # Check that a plugin was registered in the page
    assert page._pm.list_name_plugin()[0][0] == 'FakePlugin' 

    # Check that the plugin is the same as the one in the collection
    assert page._pm.get_plugins() == collection._pm.get_plugins()


def test_page_ignores_plugin():
    """Check that the plugin is not registered in the page if it is ignored"""
    class testSite(Site):
        plugins = [
            FakePlugin,
        ]

    site = testSite()
    
    @site.page
    class testPage(Page):
        ignore_plugins = [
            FakePlugin,
        ]
    
    assert site.route_list['testpage']._pm.list_name_plugin() == []

def test_collection_ignores_plugin():
    """Check that the plugin is not registered in the collection if it is ignored"""
    class testSite(Site):
        plugins = [
            FakePlugin,
        ]

    site = testSite()
    
    @site.collection
    class testCollection(Collection):
        ignore_plugins = [
            FakePlugin,
        ]
    
    assert site.route_list['testcollection']._pm.list_name_plugin() == []

    

def test_plugin_settings_from_site(caplog):
    """Check that the plugin settings are passed from the site to the plugin"""
    
    class testSite(Site):
        plugins = [
            FakePlugin,
        ]
        site_settings = {
            "plugins": {
                "FakePlugin": {
                    "test": "Testing the plugin settings"
                }
            }
        }

    
    site = testSite()
    with caplog.at_level(logging.INFO):
        site._pm.hook.pre_build_site(
            site=site,
            settings=site.site_settings['plugins']
        )
    assert 'Testing the plugin settings' in caplog.text
    