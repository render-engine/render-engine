from jinja2 import Markup
from render_engine import Page
import pytest
import re



@pytest.mark.skip(reason="SLUG CAN BE PULLED FROM CONTENT")
def test_Page_slug(base_page):
    """Pages should always have slugs"""
    with pytest.raises(TypeError):
        Page()


@pytest.mark.skip(reason="HOLD TILL POST v1 Milestone")
def test_Page_slug_is_string():
    """Page slugs must be strings otherwise raise Value Error"""
    with pytest.raises(TypeError):
        Page(slug=12345)


def test_Page_extension_html_by_default(base_page):
    """Unless specified page objecst are false"""
    assert base_page.extension == '.html'


@pytest.mark.parametrize('page, page_content',
            [# (Page(slug='no_content'), None), ## Error no raw_content exists
            (Page(slug='content_exists', content='foo'), 'foo')])
def test_Page_content_None_by_default(page, page_content):
    assert page.raw_content == page_content


def test_can_create_Page_with_only_slug():
    """Page only needs a slug object"""
    assert Page(slug='foo')


def test_page_kwargs_become_properties(page_with_content_path):
    """Custom Parameters can be passed in as Properties"""
    assert page_with_content_path.custom == 'Testing 1,2,3'


def test_page_content_separated_from_attrs(page_with_content_path):
    """When given markdown for content convert it to html and return it as markup"""
    p = page_with_content_path
    assert """# Test Header
Test Paragraph""" == p.raw_content


def test_page_content_converts_to_html(page_with_content_path):
    """When given markdown for content convert it to html and return it as markup"""
    assert \
            page_with_content_path.content == \
            Markup('<h1>Test Header</h1>\n<p>Test Paragraph</p>')
