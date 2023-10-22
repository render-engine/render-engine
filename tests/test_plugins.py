import logging
import pathlib
import typing

import pytest

from render_engine.collection import Collection
from render_engine.hookspecs import hook_impl
from render_engine.page import Page
from render_engine.site import Site


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

    @hook_impl
    def render_content(
        page: Page,
        settings: dict[str, typing.Any],
    ):
        print("Render Content Called!")

@pytest.fixture(scope="module")
def site(tmp_path_factory):
    
    tmp_output_path = tmp_path_factory.getbasetemp() / "plugin_test_output"
    class testSite(Site):
        output_path = tmp_output_path
        
        
    site = testSite()
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

    

def test_plugin_render_content_runs_from_archive(tmp_path, mocker):
    """Mock a plugin that runs from archive and assert that plugin's render_content is called"""

    tmp_output_path = tmp_path / "plugin_test_output"
    tmp_content_path = tmp_path / "content"
    tmp_content_path.mkdir()
    tmp_file = tmp_content_path / "test.md"
    tmp_file.write_text("test")
    
    class TestPluginSite(Site):
        output_path = tmp_output_path

    site = TestPluginSite()
    site.register_plugins(FakePlugin)
    
    @site.collection
    class testCollection(Collection):
        content_path = tmp_content_path
        has_archive = True

    mock_render_content = mocker.patch.object(site._pm.hook, 'render_content')
    site.render()

    assert pathlib.Path(tmp_output_path).exists()
    assert pathlib.Path(tmp_output_path / "page.html").exists()
    assert pathlib.Path(tmp_output_path / "testcollection.html").exists()
    assert mock_render_content.call_count == 2