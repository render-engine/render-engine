import pytest

from render_engine.archive import Archive
from render_engine.collection import Collection
from render_engine.page import Page


def test_archive_slug_named_after_title():
    """Archives usually get their name from their collection. This tests that the slug is named after the title"""

    archive = Archive(
        title="test archive",
        pages=[Page()],
        template="",
        routes=["./"],
        template_vars={},
    )

    assert archive._slug == "test-archive"


@pytest.mark.parametrize(
    "title, expected_slug",
    [
        ("archive", "archive1"),
        ("collection", "collection1"),
        ("Test Collection", "test-collection1"),
    ],
)
def test_archive_slug_name_with_pages(title, expected_slug):
    """tests that if num_archive_pages is greater than 1, the slug is appended with the archive_index"""

    archive = Archive(
        title=title,
        pages=[Page()],
        template="",
        routes=["./"],
        archive_index=1,
        template_vars={},
    )

    assert archive._slug == expected_slug


@pytest.mark.parametrize(
    "_items_per_page, num_of_pages",
    [(1, 3), (3, 1)],
)
def test_archive_num_of_pages(_items_per_page: int, num_of_pages: int):
    """Tests that the number of pages in an archive is equal to the number of pages in the archive"""

    class TestCollection(Collection):
        pages = [Page(), Page(), Page()]
        has_archive = True
        items_per_page = _items_per_page

    collection = TestCollection()
    assert list(collection.archives)[0].template_vars["num_of_pages"] == num_of_pages

    if _items_per_page < 1:
        assert list(collection.archives)[1].template_vars["num_of_pages"] == num_of_pages
        assert list(collection.archives)[2].template_vars["num_of_pages"] == num_of_pages


def test_archive_template_is_archive_html():
    """Tests that the template is set to archive.html"""
    archive = Archive(
        title="test archive",
        pages=[Page()],
        routes=["./"],
        template_vars={},
    )
    assert archive.template == "archive.html"
