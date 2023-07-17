import typing
import logging
import pytest
from render_engine.hookspecs import hook_impl
from render_engine.page import Page
from render_engine.site import Site
from render_engine.collection import Collection


class FakePlugin:
    """Clean the output folder before rendering"""
    default_settings = {
        "test": "default",
    }

    @hook_impl
    def pre_build_site(
        site: type[Site],
        settings: dict[str, typing.Any]|None,
        ):
        """Test Pre Build Site"""
        if settings:
            logging.info(settings['FakePlugin']['test'])
        else:
            raise ValueError("FAIL")

@pytest.fixture
def site():
    site = Site()
    site.register_plugins(FakePlugin)
    return site

def test_plugin_is_registered(site: Site):
    """Check that the plugin is registered"""
    assert [site._pm.get_name(x) for x in site.plugins] == ['FakePlugin']


def test_pages_in_collection_inherit_pugins():
    """Check that collection plugins are inherited by pages in the collection"""

    collection = Collection()
    collection.register_plugins([FakePlugin])
    page = collection.get_page()
    # Check that a plugin was registered in the page
    assert page._pm.list_name_plugin()[0][0] == 'FakePlugin' 

    # Check that the plugin is the same as the one in the collection
    assert page._pm.get_plugins() == collection._pm.get_plugins()


def test_page_ignores_plugin(site: Site):
    """Check that the plugin is not registered in the page if it is ignored"""
       
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

    

def test_plugin_settings_from_site(caplog, site: Site):
    """Check that the plugin settings are passed from the site to the plugin"""

    with caplog.at_level(logging.INFO):
        site._pm.hook.pre_build_site(
            site=site,
            settings=site.site_settings['plugins']
        )
    assert 'default' in caplog.text
    