from render_engine.collection import Collection
from render_engine.page import Page
from render_engine.parsers import BasePageParser


def test_collection_generates_page():
    """
    Tests that you can generate a page from a collection.
    Test Currently uses collection.gen_page()
    """

    class BasicCollection(Collection):
        content_type = Page

    collection = BasicCollection()
    page = collection.gen_page("foo")

    assert isinstance(page, Page)
    assert page.content == "foo"


def test_collection_information_parser_passes_to_page():
    """
    Tests that information page parser is passed into the page
    """

    class SimpleBasePageParser(BasePageParser):
        pass

    class BasicCollection(Collection):
        PageParser = SimpleBasePageParser
        content_type = Page

    collection = BasicCollection()
    page = collection.gen_page("foo")

    assert page.Parser == SimpleBasePageParser


def test_pages_generate_from_collection_content_path(tmp_path):
    """
    Tests that pages are generated from a collection
    """

    dir = tmp_path / "content"
    dir.mkdir()

    content = ["foo", "bar", "biz", "baz"]
    for count, val in enumerate(content):
        dir.joinpath(f"test{count}.md").write_text(val)

    class BasicCollection(Collection):
        content_path = dir

    collection = BasicCollection()
    assert len(list(collection.pages)) == len(content)

    for page in collection.pages:
        # Order is not guaranteed
        assert page.content in content


def test_collection_archive_no_items_per_page():
    """
    Tests that archive generates a single page if items_per_page is not set
    """

    class BasicCollection(Collection):
        pass
        archive_template = None

    collection = BasicCollection()
    assert len(list(collection.archives)) == 1
