import pytest
from render_engine import Page


def test_can_create_Page_with_only_slug():
    """Page only needs a slug object"""
    assert Page(slug='foo')


def test_Page_slug(base_page):
    """Pages should always have slugs"""
    assert base_page.slug == 'base_page'


def test_Page_slug_is_string():
    """Page slugs must be strings otherwise raise Value Error"""
    with pytest.raises(TypeError):
        Page(slug=12345)


def test_Page_raw_False_by_default(base_page):
    """Unless specified page objecst are false"""
    assert Page(slug='has_raw').raw == True
    assert base_page.raw == False
