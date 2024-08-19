import importlib
import typing

import pytest

from render_engine.collection import Collection
from render_engine.page import Page
from render_engine.plugins import PluginManager, hook_impl
from render_engine.site import Site


class FakePlugin:
    """Clean the output folder before rendering"""

    default_settings = {
        "test": "default",
    }

    @hook_impl
    @staticmethod
    def pre_build_site(
        site: type[Site],
        settings: dict[str, typing.Any] | None,
    ):
        """Test Pre Build Site"""
        pass

    @hook_impl
    @staticmethod
    def render_content(
        page: Page,
        settings: dict[str, typing.Any],
    ):
        pass

    @hook_impl
    @staticmethod
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

    assert site.route_list["fakecollection"].plugin_manager._pm.list_name_plugin()[0][0] == "FakePlugin"


def test_page_ignores_plugin(site: Site):
    """Check that the plugin is not registered in the page if it is ignored"""

    assert site.route_list["testpage"]._pm.list_name_plugin() == []


def test_collection_ignores_plugin(site):
    """Check that the plugin is not registered in the collection if it is ignored"""
    assert site.route_list["ignoredplugincollection"].plugin_manager._pm.list_name_plugin() == []


def test_collection_archive_inherits_plugins(site: Site, mocker):
    """Check that the archive inherits the pludef test_plugin_render_content_runs_from_archive(site, mocker):
    gins from the collection"""

    assert site.route_list["fakecollection"].plugin_manager._pm.list_name_plugin()[0][0] == "FakePlugin"


def test_collection_archive_runs_render_content_calls(site, mocker):
    mocker_render_content = mocker.patch.object(
        list(site.route_list["fakecollection"].archives)[0].plugin_manager._pm.hook,
        "render_content",
    )
    mocker_post_render_content = mocker.patch.object(
        list(site.route_list["fakecollection"].archives)[0].plugin_manager._pm.hook,
        "post_render_content",
    )

    site.render()
    assert mocker_render_content.called
    assert mocker_post_render_content.called


def test_page_plugins_registered():
    app = Site()

    @app.page
    class TestPage(Page):
        plugins = [FakePlugin]

    assert app.route_list["testpage"]._pm.list_name_plugin()[0][0] == "FakePlugin"


def test_deperecated_warning():
    import warnings

    with warnings.catch_warnings(record=True) as w:
        importlib.import_module("render_engine.hookspecs")
        assert any(isinstance(i.message, DeprecationWarning) for i in w)


def test_plugin_multiple_plugins():
    """Asserts that if a plugin is registered multiple times, it is only registered once"""

    plugin_mgr = PluginManager()
    plugin_mgr.register_plugin(FakePlugin)
    plugin_mgr.register_plugin(FakePlugin)


def test_plugin_override_settings_from_site_register_plugins():
    """Asserts that the settings passed into `register_plugins` override the default settings"""

    site = Site()
    site.register_plugins(FakePlugin, FakePlugin={"test": "override"})
    assert site.plugin_manager.plugin_settings.get("FakePlugin")["test"] == "override"


def test_collection_default_empty_plugin_setting(site: Site):
    """Asserts that the collection default plugin settings are set to an empty dict"""

    assert site.route_list["fakecollection"].plugin_settings == {"plugins": {}}


def test_collection_override_default_plugin_setting(site: Site):
    """Asserts that the collection default plugin settings are overridden"""

    site.route_list["fakecollection"].plugin_settings = {"FakePlugin": {"test2": "override2"}}
    assert site.route_list["fakecollection"].plugin_settings.get("FakePlugin") == {"test2": "override2"}
