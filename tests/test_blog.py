import datetime

import pytest

from render_engine.blog import Blog
from render_engine.page import Page


@pytest.fixture()
def blog_with_pages():
    class Page1(Page):
        title = "Older Blog Post"
        date = datetime.datetime(2024, 1, 1)
        content = """Newer Page"""

    class Page2(Page):
        title = "Newer Blog Post"
        date = datetime.datetime(2024, 1, 2)
        content = """Newer Page"""

    class CustomBlog(Blog):
        pages = [Page1, Page2]

    return CustomBlog()


def test_blog_has_feed():
    """Tests that the Blog class has a Feed attribute."""
    blog = Blog()
    assert hasattr(blog, "Feed")


def test_blog_metadata():
    metadata = Blog._metadata_attrs()
    # title should not be affected
    assert metadata["title"] == "Untitled Entry"
    # metadata should have date now
    assert isinstance(metadata["date"], datetime.datetime)


def test_blog_sorted_pages_is_in_reverse(blog_with_pages):
    assert [page.title for page in blog_with_pages.sorted_pages] == [
        "Newer Blog Post",
        "Older Blog Post",
    ]


def test_blog_feed_is_sorted_in_reverse(blog_with_pages):
    """#838 Newest Blog Posts should be listed first to conform with many services that don't retrieve all the posts"""

    assert blog_with_pages.feed.pages[0].title == "Newer Blog Post"
