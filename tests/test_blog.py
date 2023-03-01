import pytest

from render_engine.blog import Blog


def test_blog_has_feed():
    blog = Blog()
    assert hasattr(blog, "Feed")
