from render_engine import Page
import pytest
import re


def test_page_kwargs_become_properties(base_page):
    """Custom Parameters can be passed in as Properties"""
    assert base_page.custom_val == 'custom'

def test_page_content_detects_args(base_page):
    """Custom Params defined in content can be passed as Properties"""
    assert base_page.title == 'Base Page'

@pytest.mark.parametrize('page',
                        [Page(name='test'),
                         Page(id='test'),
                         ])
def test_page_slug_variants(page):
    """slugs are defined by the following options:
    - slug
    - name
    - id
    - content_path (filename)
    """
    assert page.slug == 'test'

def test_page_url(base_page):
    """page object has a relative and url"""
    assert base_page.url== 'https://example.com/test.html'

def test_page_content_separated_from_attrs(base_page):
    """When given markdown for content convert it to html and return it as markup"""
    assert """# Test Header
Test Paragraph""" in base_page.content

def test_page_content_marked_up(base_page):
    """When given markdown for content convert it to html and return it as markup"""
    assert '<h1>Test Header</h1>' in base_page.markup
