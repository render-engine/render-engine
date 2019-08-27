from render_engine import Page
import pytest
import re



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
            [(Page(slug='no_content'), None),
            (Page(slug='content_exists', content='foo'), 'foo')])
def test_Page_content_None_by_default(page, page_content):
    assert page.content == page_content


def test_can_create_Page_with_only_slug():
    """Page only needs a slug object"""
    assert Page(slug='foo')


def test_page_kwargs_become_properties(base_page):
    """Custom Parameters can be passed in as Properties"""
    assert base_page.template_vars['custom'] == 'Testing 1,2,3'


def test_page_content_separated_from_attrs(base_page):
    """When given markdown for content convert it to html and return it as markup"""
    assert """# Test Header
This is a test""" in base_page.content
    assert """title: Base Page""" not in base_page.content


def test_page_content_converts_to_html(base_page):
    """When given markdown for content convert it to html and return it as markup"""
    assert '<h1>Test Header</h1>' in base_page.html
