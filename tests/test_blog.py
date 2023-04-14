import datetime
import pytest

from render_engine.blog import (
    Blog,
    BlogPost,
    _check_date_values,
)


def test_blog_has_feed():
    blog = Blog()
    assert hasattr(blog, "Feed")

def test_blog_post_datetime_parses_common_US_formats(date_attr: str):
    """
    Test that the date_published matches the expected common dates.
    # TODO: test for other localizations
    """

    class CustomBlogPost(BlogPost):
        def __init__(self):
            super().__init__()
            setattr(self, f"_{date_attr}", "2020-01-01")
        
    blog = CustomBlogPost()
    assert getattr(blog, date_attr, datetime.date(2020,1,1))

def test_blog_post_datetime_compares_as_naive():
    """Test that the datetime objects are naive."""

    class CustomBlogPost1(BlogPost):
        date: datetime.datetime = datetime.datetime(2020, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
    
    class CustomBlogPost2(BlogPost):
        date: datetime.datetime = datetime.datetime(2019, 1, 1, 0, 0, 0)    
    
    class CustomBlog(Blog):
        pages = [CustomBlogPost1(), CustomBlogPost2()]

    blog = CustomBlog()
    assert blog.pages[0].date_published > blog.pages[1].date_published