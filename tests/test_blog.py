from render_engine.blog import Blog


def test_blog_has_feed():
    """Tests that the Blog class has a Feed attribute."""
    blog = Blog()
    assert hasattr(blog, "Feed")
