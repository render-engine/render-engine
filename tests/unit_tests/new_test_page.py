import pytest
from render_engine import Page

@pytest.fixture()
def base_page():
    return Page(slug='base_page')

def test_can_create_Page_with_only_slug():
    """Page only needs a slug object"""
    assert Page(slug='foo')


def test_Page_slug(base_page):
    """Pages should always have slugs"""
    assert base_page.slug == 'base_page'


@pytest.mark.skip(reason="HOLD TILL POST v1 Milestone")
def test_Page_slug_is_string():
    """Page slugs must be strings otherwise raise Value Error"""
    with pytest.raises(TypeError):
        Page(slug=12345)


def test_Page_extension_html_by_default(base_page):
    """Unless specified page objecst are false"""
    assert base_page.extension == '.html'

@pytest.mark.parametrize('page, page_content',
            [(Page(slug='no_content'), None),
            (Page(slug='content_exists', content='foo'), 'foo')])
def test_Page_content_None_by_default(page, page_content):
    assert page.content == page_content
