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


def test_blog_index_sorted_by_created_time(base_blog):
    """blogs have a customer default sort field"""
    assert base_blog.default_sort == 'date_published'

@pytest.mark.parametrize('date',
        ["date_published", "date", "publish_date", "date_modified",
        "modified_date"])
def test_blog_date_published_order(base_blog_post, date):
    """blog date_published"""
    blog = base_blog_post()
    val = pendulum.now().to_rfc2822_string()
    setattr(blog, date, val)
    assert blog.date_published == val
