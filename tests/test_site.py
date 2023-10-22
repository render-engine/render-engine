import pathlib

import pluggy
import pytest
from jinja2 import FileSystemLoader

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

    class CustomPage1(Page):
        pass


    class CustomPage2(Page):
        pass

    class collection(Collection):
        pages = [CustomPage1(), CustomPage2()]

    collection = site.collection(collection)

    assert site.route_list["collection"] == collection
    assert len(site.route_list) == 1
    assert 'custompage1' in [getattr(page, page._reference) for page in site.route_list["collection"]]


def test_site_page_with_multiple_routes_has_one_entry_in_routes_list():
    """Tests a page with multiple routes only has one entry in the routes list"""
    site = Site()

    class CustomPage(Page):
        test_value = "test"
        routes = ["customroute", "customroute2"]

    site.page(CustomPage)

    assert len(site.route_list) == 1

def test_url_for_Page_in_site(tmp_path):
    """Tests that url_for a page is added to a template"""
    test_template = pathlib.Path(tmp_path / "template.html")
    test_template.write_text("The URL is '{{ 'custompage'|url_for }}'")
    site = Site()
    site.engine.loader.loaders.insert(0, FileSystemLoader(tmp_path))
    site.output_path = tmp_path

    @site.page
    class CustomPage(Page):
        template = test_template.name

    site.render()
    custom_page = (tmp_path / "custompage.html")
    assert custom_page.exists()
    assert custom_page.read_text() == "The URL is '/custompage.html'"


def test_collection_archive_in_route_list(tmp_path):
    """Given a collection with an archive, the archive should be in the route list and accessible with url_for"""
    test_collection_archive_template = pathlib.Path(tmp_path / "archive_template.html")
    test_collection_archive_template.write_text("This is the collection archive")

    test_collection_template = pathlib.Path(tmp_path / "collection_archive_item_template.html")
    test_collection_template.write_text("The collection archive route is at '{{ 'customcollection' |url_for }}'")

    site = Site()
    site.engine.loader.loaders.insert(0, FileSystemLoader(tmp_path))
    site.output_path = tmp_path


    class CustomCollectionPage(Page):
        template = test_collection_template.name
        

    @site.collection
    class CustomCollection(Collection):
        archive_template = test_collection_archive_template.name
        has_archive = True
        pages = [CustomCollectionPage()]


    site.render()
    assert pathlib.Path(tmp_path / "customcollection.html").exists()
    assert pathlib.Path(tmp_path / "customcollectionpage.html").exists()
    assert pathlib.Path(tmp_path / "customcollection.html").read_text() == "This is the collection archive"
    assert pathlib.Path(tmp_path / "customcollectionpage.html").read_text() == "The collection archive route is at '/customcollection.html'"

@pytest.mark.parametrize(
        "page_number,expected_url",
        [
            (0, "custompagescollection.html"),
            (1, "custompagescollection1.html"),
            (2, "custompagescollection2.html"),
        ]
)
def test_collection_archive_pages_in_route_list(tmp_path, page_number, expected_url):
    """Given a collection with an archive, the archive should be in the route list and accessible with url_for"""
    test_collection_pages_template = pathlib.Path(tmp_path / f"collection_archive_item_pages_template{page_number}.html")
    test_collection_pages_template.write_text(
        f"The collection archive route is at {{{{ 'custompagescollection' | url_for(page={page_number})}}}}",
    )

    site = Site()
    site.engine.loader.loaders.insert(0, FileSystemLoader(tmp_path))
    site.output_path = tmp_path


    class CustomCollectionPages1(Page):
        content = 'test'
    class CustomCollectionPages2(Page):
        content = 'test'

    @site.collection
    class CustomPagesCollection(Collection):
        archive_template = test_collection_pages_template.name
        has_archive = True
        pages = [CustomCollectionPages1(), CustomCollectionPages2()]
        items_per_page = 1


    site.render()
    expected_path = pathlib.Path(tmp_path / expected_url)
    assert expected_path.exists()
    assert expected_path.read_text() == f"The collection archive route is at /{expected_url}"


def test_url_for_Collection_in_site(tmp_path):
    """
    Tests that url_for a page in a collection is added to a template
    """
    test_template = pathlib.Path(tmp_path / "custom_template.html")
    test_template.write_text("The URL is '{{ 'customcollection.customcollectionpage' | url_for }}'")
    
    site = Site()
    site.engine.loader.loaders.insert(0, FileSystemLoader(tmp_path))
    site.output_path = tmp_path


    class CustomCollectionPage(Page):
        template  = test_template.name

    @site.collection
    class CustomCollection(Collection):
        template = test_template.name
        pages = [CustomCollectionPage()]

    site.render()
    custom_page = (tmp_path / "customcollectionpage.html")
    assert custom_page.exists()
    assert custom_page.read_text() == "The URL is '/customcollectionpage.html'"


def test_site_output_path(tmp_path):
    """Tests site outputs to output_path"""

    output_tmp_dir = tmp_path / "output"
    output_tmp_dir.mkdir()

    class CustomSite(Site):
        output_path = output_tmp_dir

    site = CustomSite()
    @site.page
    class CustomPage(Page):
        content = "this is a test"

    site.render()

    assert (output_tmp_dir / "custompage.html").exists()


def test_site_static_renders_in_static_output_path(tmp_path, site):
    """
    Tests that a static file is rendered in the static output path.
    """

    static_tmp_dir = tmp_path / "static"
    output_tmp_dir = tmp_path / "output"
    output_tmp_dir.mkdir()
    static_tmp_dir.mkdir()
    pathlib.Path(static_tmp_dir / pathlib.Path("test.txt")).write_text("test")

    site.output_path = output_tmp_dir
    site.static_paths.add(static_tmp_dir)
    site.render() 

    assert (output_tmp_dir / "static" / "test.txt").exists()

def tests_site_nested_static_paths(tmp_path, site):
    """given a static path with nested directories, the output should be the same"""
    static_tmp_dir = tmp_path / "static"
    output_tmp_dir = tmp_path / "output"
    output_tmp_dir.mkdir()
    static_tmp_dir.mkdir()
    pathlib.Path(static_tmp_dir / "nested").mkdir()
    pathlib.Path(static_tmp_dir / "nested" / pathlib.Path("test.txt")).write_text("test")
    pathlib.Path(static_tmp_dir / pathlib.Path("test.txt")).write_text("test")

    site.output_path = output_tmp_dir
    site.static_paths.add(static_tmp_dir)
    site.render() 
    assert (output_tmp_dir / "static" / "test.txt").exists()
    assert (output_tmp_dir / "static" / "nested" / "test.txt").exists()

def tests_site_multiple_static_paths(tmp_path, site):
    """given a static path with nested directories, the output should be the same"""
    static_tmp_dir = tmp_path / "static"
    output_tmp_dir = tmp_path / "output"
    output_tmp_dir.mkdir()
    static_tmp_dir.mkdir()
    pathlib.Path(static_tmp_dir / pathlib.Path("test.txt")).write_text("test")

    second_static_tmp_dir = tmp_path / "static2"
    second_static_tmp_dir.mkdir()
    pathlib.Path(second_static_tmp_dir / pathlib.Path("test2.txt")).write_text("test")

    site.output_path = output_tmp_dir
    site.static_paths.update([static_tmp_dir, second_static_tmp_dir])
    site.render() 
    assert (output_tmp_dir / "static" / "test.txt").exists()
    assert (output_tmp_dir / "static2" / "test2.txt").exists()