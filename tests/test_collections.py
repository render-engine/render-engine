import pathlib

import pluggy
import pytest
from render_engine_parser import BasePageParser

from render_engine.collection import Collection
from render_engine.page import Page

pm = pluggy.PluginManager("fake_test")


def test_collection_information_parser_passes_to_page(tmp_path):
    """
    Tests that information page parser is passed into the page
    """

    class SimpleBasePageParser(BasePageParser):
        pass

    class BasicCollection(Collection):
        Parser = SimpleBasePageParser
        content_type = Page

    collection = BasicCollection()
    page = collection.get_page()
    assert page.Parser == SimpleBasePageParser


def test_pages_generate_from_collection_content_path(tmp_path: pathlib.Path):
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
    assert len([page for page in collection]) == len(content)

    for page in collection:
        # Order is not guaranteed
        assert page.content in content


def test_collection_archive_no_items_per_page(caplog, tmp_path: pathlib.Path):
    """
    Tests that archive generates a single page if items_per_page is not set
    """

    tmp_dir = tmp_path / "content"
    tmp_dir.mkdir()
    file = tmp_dir / "test.md"
    file.write_text("test")

    class BasicCollection(Collection):
        content_path = tmp_dir.absolute()

    with caplog.at_level("WARNING"):
        collection = BasicCollection()
        assert len(list(collection.archives)) == 1
        assert "`has_archive` is set to `False`" in caplog.text
        assert "BasicCollection" in caplog.text


def test_collection_context(tmp_path: pathlib.Path):
    """
    Tests that `collection` context is passed to the page objects
    """

    tmp_dir = tmp_path / "content"
    tmp_dir.mkdir()
    file = tmp_dir / "test.md"
    file.write_text("test")

    class BasicCollection(Collection):
        content_path = tmp_dir.absolute()
        archive_template = None

    collection = BasicCollection()

    for page in collection:
        assert page.collection["title"] == collection._title


def test_collection_archives_has_title_of_collection(tmp_path: pathlib.Path):
    """
    Tests that the title of the Archive Collection is the same as the parent Collection.

    This should be the case with all archive pages generated

    Issue #105
    """
    tmp_dir = tmp_path / "content"
    tmp_dir.mkdir()

    file1 = tmp_dir / "test.md"
    file1.write_text("test1")

    file2 = tmp_dir / "test2.md"
    file2.write_text("test")

    class BasicCollection(Collection):
        content_path = tmp_dir.absolute()
        items_per_page = 1

    collection = BasicCollection()
    assert len(list(collection.archives)) == 3
    for archive in collection.archives:
        assert archive._title == collection._title


def test_collection_paginated_archives_start_at_1(tmp_path: pathlib.Path):
    """Tests that the first archive page is page 1 and not page 0"""

    tmp_dir = tmp_path / "content"
    tmp_dir.mkdir()

    file1 = tmp_dir / "test.md"
    file1.write_text("test1")

    file2 = tmp_dir / "test2.md"
    file2.write_text("test")


@pytest.mark.parametrize(
    "attr,attrval",
    [
        ("template", "test.html"),
        ("routes", ["/test/long/route"]),
    ],
)
def test_collection_attrs_pass_to_page(tmp_path, attr: str, attrval: str | list[str]):
    """Tests that the template attribute for the collection is passed to the page"""

    class SimpleBasePageParser(BasePageParser):
        pass

    class BasicCollection(Collection):
        PageParser = SimpleBasePageParser
        content_type = Page

    setattr(BasicCollection, attr, attrval)

    collection = BasicCollection()
    page = collection.get_page()

    assert getattr(page, attr) == attrval
