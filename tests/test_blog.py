from render_engine import Blog
import pytest

@pytest.fixture()
def base_blog():
    return Blog()

def test_blog_index_sorted_by_created_time(base_blog):
    base_blog.default_sort_field='created_time'
