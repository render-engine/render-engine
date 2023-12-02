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
        settings: dict[str, typing.Any] | None,
    ):
        """Test Pre Build Site"""
        pass

    @hook_impl
    def render_content(
        page: Page,
        settings: dict[str, typing.Any],
    ):
        pass

    @hook_impl
    def post_render_content(
        page: Page,
        settings: dict[str, typing.Any],
    ):
        pass

@pytest.fixture(scope="module")
def site(tmp_path_factory):
    tmp_output_path = tmp_path_factory.getbasetemp() / "plugin_test_output"

    class testSite(Site):
        output_path = tmp_output_path

    site = testSite()
    site.register_plugins(FakePlugin)

    @site.collection
    class FakeCollection(Collection):
        pages = [Page(content="test")]
        has_archive = True


    @site.collection
    class IgnoredPluginCollection(Collection):
        ignore_plugins = [
            FakePlugin,
        ]
        pages = []
    @site.page
    class testPage(Page):
        ignore_plugins = [
            FakePlugin,
        ]
        content = "test"

    return site


def test_plugin_is_registered(site: Site):
    """Check that the plugin is registered"""
    assert [site.plugin_manager._pm.get_name(x) for x in site.plugin_manager.plugins] == ["FakePlugin"]


def test_pages_in_collection_inherit_pugins(site: Site):
    """Check that collection plugins are inherited by pages in the collection"""

    assert site.route_list["fakecollection"].plugin_manager._pm.list_name_plugin()[0][0] == 'FakePlugin'


def test_page_ignores_plugin(site: Site):
    """Check that the plugin is not registered in the page if it is ignored"""



    assert site.route_list["testpage"]._pm.list_name_plugin() == []


def test_collection_ignores_plugin(site):
    """Check that the plugin is not registered in the collection if it is ignored"""
    assert site.route_list["ignoredplugincollection"].plugin_manager._pm.list_name_plugin() == []

def test_collection_archive_inherits_plugins(site: Site, mocker):
    """Check that the archive inherits the pludef test_plugin_render_content_runs_from_archive(site, mocker):
gins from the collection"""

    assert site.route_list["fakecollection"].plugin_manager._pm.list_name_plugin()[0][0] == 'FakePlugin'

def test_collection_archive_runs_render_content_calls(site, mocker):
    mocker_render_content = mocker.patch.object(list(site.route_list['fakecollection'].archives)[0].plugin_manager._pm.hook, "render_content")
    mocker_post_render_content = mocker.patch.object(list(site.route_list['fakecollection'].archives)[0].plugin_manager._pm.hook, "post_render_content")

    site.render()
    assert mocker_render_content.called
    assert mocker_post_render_content.called
