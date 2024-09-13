import datetime

from render_engine.blog import Blog


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
