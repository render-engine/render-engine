import pytest
from render_engine import Page

@pytest.fixture()
def base_page():
    """Tests can a simple Page be created given no Parameters"""
    content = """title: Base Page
subtitle: This is a test object

# Test Header

Test Paragraph
"""
    slug = '/test'
    url_suffix = '.html'
    url_root = 'https://example.com',
    return Page(
            slug=slug,
            url_suffix=url_suffix,
            content=content,
            custom_val='custom',
            )

def test_page_kwargs_become_properties(base_page):
    """Custom Parameters can be passed in as Properties"""
    assert base_page.custom_val == 'custom'

def test_page_content_detects_args(base_page):
    """Custom Params defined in content can be passed as Properties"""
    assert base_page.title == 'Base Page'

@pytest.mark.parametrize('page',
                    [Page(slug='test'),
                     Page(name='test'),
                     Page(id='test')])
def test_page_slug_variants(page):
    """slugs are defined by the following options:
    - slug
    - name
    - id
    - content_path (filename)
    """
    assert page.slug == 'test.html'
