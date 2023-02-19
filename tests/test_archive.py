import pytest
from render_engine.page import Page
from render_engine.archive import Archive
from render_engine.collection import Collection


def test_archive_slug_name_with_pages():
    """tests that if num_archive_pages is greater than 1, the slug is appended with the archive_index"""

    archive = Archive(
        title="archive",
        pages=[Page()],
        template="",
        routes = ["./"],
        archive_index=1,
        num_archive_pages=2,
    )

    assert archive.slug == "archive1"
