import frontmatter
import pytest

from render_engine import Page, Site
from render_engine.cli.cli import create_collection_entry, get_site_content_paths
from render_engine.collection import Collection


@pytest.fixture(scope="module")
def site(tmp_path_factory):
    class FakeSite(Site):
        output_path = tmp_path_factory.getbasetemp() / "output_path"

    site = FakeSite()

    content_path1 = tmp_path_factory.getbasetemp() / "test_content_path1.txt"
    content_path1.write_text("Hello Wold")

    content_path2 = tmp_path_factory.getbasetemp() / "test_content_path2.txt"
    content_path2.write_text("Hello Space")

    @site.page
    class FakePage1(Page):
        content_path = content_path1

    @site.page
    class FakePage2(Page):
        content_path = content_path2

    return site


def test_get_site_content_path(site, tmp_path_factory):
    """Tests that the paths returned from the pages"""

    content_path1 = tmp_path_factory.getbasetemp() / "test_content_path1.txt"
    content_path2 = tmp_path_factory.getbasetemp() / "test_content_path2.txt"

    assert get_site_content_paths(site) == [content_path1, content_path2]


@pytest.mark.skip("Not sure how to test importlib")
def test_import_lib_gets_site():
    pass


def test_collection_call():
    """Tests that you can get content from the parser using `new_entry`"""
    test_collection = Collection()
    content = create_collection_entry(content=None, collection=test_collection, foo="bar")
    post = frontmatter.loads(content)

    assert post["title"] == "Untitled Entry"
    assert post["foo"] == "bar"


def test_collection_call_with_content():
    """Tests that you can get content from the parser using `new_entry`"""
    test_collection = Collection()
    content = create_collection_entry(content="This is a test", collection=test_collection, foo="bar")
    post = frontmatter.loads(content)

    assert post["title"] == "Untitled Entry"
    assert post["foo"] == "bar"
    assert post.content == "This is a test"
