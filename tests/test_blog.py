import pluggy
import pytest

from render_engine.blog import Blog


def test_blog_has_feed():
    blog = Blog(pm=pluggy.PluginManager("fake_test"))
    assert hasattr(blog, "Feed")
