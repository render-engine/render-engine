import pytest
from render_engine import Page


@pytest.fixture()
def site_url():
    return 'https://example.com/'

@pytest.fixture()
def base_page(site_url):
    """Tests can a simple Page be created given no Parameters"""
    content = """title: Base Page
subtitle: This is a test object

# Test Header
Test Paragraph"""
    slug = 'test'
    url_suffix = '.html'
    return Page(
            slug=slug,
            url_root=site_url,
            url_suffix=url_suffix,
            content=content,
            custom_val='custom',
            )

