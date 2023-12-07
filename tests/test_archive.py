import pytest

from render_engine.archive import Archive
from render_engine.page import Page


def test_archive_slug_named_after_title():
    """Archives usually get their name from their collection. This tests that the slug is named after the title"""

    archive = Archive(title="test archive", pages=[Page()], template="", routes=["./"], template_vars={})

    assert archive._slug == "test-archive"


@pytest.mark.parametrize(
    "title, expected_slug",
    [("archive", "archive1"), ("collection", "collection1"), ("Test Collection", "test-collection1")],
)
def test_archive_slug_name_with_pages(title, expected_slug):
    """tests that if num_archive_pages is greater than 1, the slug is appended with the archive_index"""

    archive = Archive(
        title=title, pages=[Page()], template="", routes=["./"], archive_index=1, num_archive_pages=2, template_vars={}
    )

    assert archive._slug == expected_slug
