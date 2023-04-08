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

@pytest.mark.parametrize(
    "date_key",
    [
        ("date"),
        ("_date_published"),
        ("publish_date"),
    ]
 )
def test_blog_date_published_found_in_expected_parameters(date_key: str):
    class CustomBlogPost(BlogPost):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            setattr(self, date_key, "2020-01-01")

    blog = CustomBlogPost()

    assert blog.date_published == datetime.datetime(2020, 1, 1,0,0,0)


def test__check_date_values_raises_error_if_no_date_value_found():
    with pytest.raises(ValueError):
        _check_date_values("test_date_value", (None, None, None))
        
@pytest.mark.parametrize(
    "date_attr",
    [
        ("date_modified"),
        ("date_published"),
    ]
)
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