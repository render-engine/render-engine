from pathlib import Path

import pluggy
import pytest
from jinja2 import DictLoader, FileSystemLoader

from render_engine.collection import Collection
from render_engine.page import Page
from render_engine.plugins import SiteSpecs
from render_engine.site import Site
from render_engine.themes import Theme

pm = pluggy.PluginManager("fake_test")


@pytest.fixture
def site(tmp_path: Path):
    _site = Site()
    _site.output_path = tmp_path / "output"
    _site.static_paths.add(tmp_path / "static")
    return _site


def test_site_defaults(site):
    """
    Tests that a site can be created with default variables.
    Those values are:
        - SITE_TITLE: "Untitled Site"
        - SITE_URL: "http://example.com"
    """

    assert site.site_vars["SITE_TITLE"] == "Untitled Site"
    assert site.site_vars["SITE_URL"] == "http://localhost:8000/"


def test_site_site_vars_override_defaults_via_class():
    """
    Tests that a site can be created with default variables.
    """

    site_vars = {
        "SITE_TITLE": "My Site",
        "SITE_URL": "https://my-site.com",
    }

    site.site_vars = site_vars

    assert site.site_vars["SITE_TITLE"] == "My Site"
    assert site.site_vars["SITE_URL"] == "https://my-site.com"


def test_site_page_in_route_list(site, tmp_path: Path):
    tmp_dir = tmp_path / "content"
    tmp_dir.mkdir()
    file = tmp_dir / "test.md"
    file.write_text("test")

    # assert that the route list is empty
    assert len(site.route_list) == 0

    class CustomPage(Page):
        test_value = "test"
        content_path = file.absolute()

    site.page(CustomPage)

    assert site.route_list["custompage"].test_value == "test"


def test_site_collection_in_route_list(site):
    """Tests that when a collection is added to the route_list it is only the colleciton"""
    # assert that the route list is empty
    assert len(site.route_list) == 0

    class CustomPage1(Page):
        pass

    class CustomPage2(Page):
        pass

    class collection(Collection):
        pages = [CustomPage1(), CustomPage2()]

    collection = site.collection(collection)

    assert site.route_list["collection"] == collection
    assert len(site.route_list) == 1
    assert "custompage1" in [getattr(page, page._reference) for page in site.route_list["collection"]]


def test_site_page_with_multiple_routes_has_one_entry_in_routes_list(site):
    """Tests a page with multiple routes only has one entry in the routes list"""

    class CustomPage(Page):
        test_value = "test"
        routes = ["customroute", "customroute2"]

    site.page(CustomPage)

    assert len(site.route_list) == 1


def test_url_for_Page_in_site(site, tmp_path: Path):
    """Tests that url_for a page is added to a template"""
    test_template = Path(tmp_path / "template.html")
    test_template.write_text("The URL is '{{ 'custompage'|url_for }}'")
    site.theme_manager.engine.loader.loaders.insert(0, FileSystemLoader(tmp_path))

    @site.page
    class CustomPage(Page):
        template = test_template.name

    site.render()
    custom_page = site.output_path / "custompage.html"
    assert custom_page.exists()
    assert custom_page.read_text() == "The URL is '/custompage.html'"


def test_collection_archive_in_route_list(site, tmp_path: Path):
    """Given a collection with an archive, the archive should be in the route list and accessible with url_for"""
    test_collection_archive_template = Path(tmp_path / "archive_template.html")
    test_collection_archive_template.write_text("This is the collection archive")

    test_collection_template = Path(tmp_path / "collection_archive_item_template.html")
    test_collection_template.write_text("The collection archive route is at '{{ 'customcollection' |url_for }}'")

    site.theme_manager.engine.loader.loaders.insert(0, FileSystemLoader(tmp_path))

    class CustomCollectionPage(Page):
        template = test_collection_template.name

    @site.collection
    class CustomCollection(Collection):
        archive_template = test_collection_archive_template.name
        has_archive = True
        pages = [CustomCollectionPage()]

    site.render()
    assert site.output_path.joinpath("customcollection.html").exists()
    assert site.output_path.joinpath("customcollectionpage.html").exists()
    assert site.output_path.joinpath("customcollection.html").read_text() == "This is the collection archive"
    assert (
        site.output_path.joinpath("customcollectionpage.html").read_text()
        == "The collection archive route is at '/customcollection.html'"
    )


@pytest.fixture(scope="module")
def site_with_collection(tmp_path_factory: pytest.TempPathFactory):
    collection_archive_path = tmp_path_factory.getbasetemp() / "collection_archive_items"
    collection_archive_output_path = collection_archive_path / "output"
    static_tmp_dir = collection_archive_path / "static"
    static_tmp_dir.mkdir(parents=True)
    Path(static_tmp_dir / Path("test.txt")).write_text("test")

    _site = Site()
    _site.output_path = collection_archive_output_path
    _site.static_paths.add(static_tmp_dir)

    class CustomCollectionPages1(Page):
        content = "test"

    class CustomCollectionPages2(Page):
        content = "test"

    @_site.collection
    class CustomPagesCollection(Collection):
        has_archive = True
        pages = [CustomCollectionPages1(), CustomCollectionPages2()]
        items_per_page = 1

    _site.render()
    return _site


def test_collection_archives_generates_by_items_per_page(site_with_collection: Site):
    """
    Archive pages should be created using the items_per_page value

    Example:
        If items_per_page is 1, and there are 2 pages then there should be 3 archive pages.
        0: all page items
        1: first page item
        2: second page item
    """

    assert len(list(site_with_collection.route_list["custompagescollection"].archives)) == 3


def test_collection_archive_pages_in_route_list(site_with_collection: Site):
    """Given a collection with an archive, the archive should be in the route list and accessible with url_for"""

    for page in site_with_collection.route_list["custompagescollection"].archives:
        assert Path(site_with_collection.output_path / page.path_name).exists()


def test_url_for_Collection_in_site(site: Site, tmp_path: Path):
    """
    Tests that url_for a page in a collection is added to a template
    """
    test_template = Path(tmp_path / "custom_template.html")
    test_template.write_text("The URL is '{{ 'customcollection.customcollectionpage' | url_for }}'")
    if site.theme_manager.engine.loader is not None:
        site.theme_manager.engine.loader.loaders.insert(0, FileSystemLoader(tmp_path))

    class CustomCollectionPage(Page):
        template = test_template.name

    @site.collection
    class CustomCollection(Collection):
        template = test_template.name
        pages = [CustomCollectionPage()]

    site.render()
    custom_page = site.output_path / "customcollectionpage.html"
    assert custom_page.exists()
    assert custom_page.read_text() == "The URL is '/customcollectionpage.html'"


def test_site_output_path(site, tmp_path: Path):
    """Tests site outputs to output_path"""

    @site.page
    class CustomPage(Page):
        content = "this is a test"

    site.render()

    assert (site.output_path / "custompage.html").exists()


def test_site_static_renders_in_static_output_path(site_with_collection: Site):
    """
    Tests that a static file is rendered in the static output path.
    """

    assert Path(site_with_collection.output_path, "static", "test.txt").exists()


def tests_site_nested_static_paths(tmp_path: Path, site: Site):
    """given a static path with nested directories, the output should be the same"""
    static_tmp_dir = tmp_path / "static"
    output_tmp_dir = tmp_path / "output"
    output_tmp_dir.mkdir()
    static_tmp_dir.mkdir()
    Path(static_tmp_dir / "nested").mkdir()
    Path(static_tmp_dir / "nested" / Path("test.txt")).write_text("test")
    Path(static_tmp_dir / Path("test.txt")).write_text("test")

    site.output_path = output_tmp_dir
    site.static_paths.add(static_tmp_dir)
    site.render()
    assert (output_tmp_dir / "static" / "test.txt").exists()
    assert (output_tmp_dir / "static" / "nested" / "test.txt").exists()


def tests_site_multiple_static_paths(tmp_path: Path, site: Site):
    """given a static path with nested directories, the output should be the same"""
    static_tmp_dir = tmp_path / "static"
    output_tmp_dir = tmp_path / "output"
    output_tmp_dir.mkdir()
    static_tmp_dir.mkdir()
    Path(static_tmp_dir / Path("test.txt")).write_text("test")

    second_static_tmp_dir = tmp_path / "static2"
    second_static_tmp_dir.mkdir()
    Path(second_static_tmp_dir / Path("test2.txt")).write_text("test")

    site.output_path = output_tmp_dir
    site.static_paths.update([static_tmp_dir, second_static_tmp_dir])
    site.render()
    assert (output_tmp_dir / "static" / "test.txt").exists()
    assert (output_tmp_dir / "static2" / "test2.txt").exists()


def test_site_theme_update_settings(site, tmp_path: Path):
    """Tests that the theme manager updates the settings"""
    site = Site()

    assert "theme" in site.site_vars
    assert "test" not in site.site_vars
    site.update_theme_settings(test="test")
    assert site.site_vars["theme"]["test"] == "test"


def test_plugin_in_theme_added_to_plugins(site):
    """Tests that a plugin added to a theme is added to the site"""

    class plugin(SiteSpecs):
        pass

    class theme(Theme):
        loader = DictLoader({"test.html": "test"})
        prefix = "test"
        plugins = [plugin]
        filters = []

    site.register_theme(
        theme,
    )
    assert plugin in site.plugin_manager.plugins


def test_collection_archive_0_is_index(site, tmp_path: Path):
    test_collection_archive = Path(tmp_path / "archive_template")
    site.output_path = test_collection_archive

    class CustomCollectionPage(Page):
        content = "Test"

    @site.collection
    class CustomCollection(Collection):
        routes = ["test"]
        has_archive = True
        pages = [CustomCollectionPage()]

    site.render()
    assert Path(test_collection_archive / "test" / "index.html").exists()


def test_custom_template_path_assignment(site, tmp_path):
    """
    asserts that you can assign a new template path to an initialized site

    Template paths are used to find templates when rendering pages.

    The attribute is saved in the template_manager's ChoiceLoader.
    """

    test_custom_template_path = Path(tmp_path / "custom_template_path")
    test_custom_template_path.mkdir()
    test_custom_template = test_custom_template_path / "test_custom_template.html"
    test_custom_template.touch()
    site = Site()
    site.template_path = str(test_custom_template_path)
    assert site.theme_manager.engine.get_template("test_custom_template.html")
