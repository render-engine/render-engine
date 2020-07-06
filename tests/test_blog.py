from render_engine.feeds import RSSFeedItem
from render_engine.blog import Blog, BlogPost
import pytest
import pendulum

@pytest.fixture()
def base_blog_post():
    class BaseBlogPost(BlogPost):
        date_published = pendulum.now()
        date = pendulum.now()
        publish_date = pendulum.now()
        date_modified = pendulum.now()
        modified_date = pendulum.now()

    return BaseBlogPost

@pytest.fixture()
def base_blog():
    class BaseBlog(Blog):
        link='example.com'
        title='Test Blog'
        description='This is a test'

    return BaseBlog


def test_blog_index_sorted_by_date_published(base_blog):
    """blogs have a customer default sort field"""
    class Foo:
        some_other_option = 0
        date = 1
    assert base_blog.archive_default_sort(Foo) == 1


@pytest.mark.parametrize('date',
        [
            "date_published",
            "date",
            "publish_date",
            "date_modified",
            "modified_date",
            ]
        )
def test_blogpost_date_published_order(date):
    """blog date_published"""
    class testBlog(BlogPost):
        def __init__(self, **kwargs):
            setattr(self, date, 'Jan 1, 2020')
            super().__init__(**kwargs)

    tb = testBlog()

    assert tb.date == pendulum.parse('Jan 1, 2020', strict=False).set(tz=pendulum.local_timezone())

def test_assert_blog_rss_feed_item_is_rss_feed_item():
    class testBlog(BlogPost):
        def __init__(self, **kwargs):
            self.date_published='Jan 1, 2020'
            super().__init__(**kwargs)

    tb = testBlog()
    assert isinstance(tb.rss_feed_item, RSSFeedItem)


def test_page_with_attr_with_multiple_values():
    t = BlogPost(content='date: October 1, 2020 8:00\ntags: foo, bar')
    assert t.tags == ['foo', 'bar']

