import pytest
from render_engine import Page, Collection

@pytest.fixture()
def content():
    return """title: Test Title
custom: Testing 1,2,3

# Test Header
Test Paragraph"""

@pytest.fixture()
def base_page():
    """Tests can a simple Page be created given no Parameters"""
    slug = 'test_page'
    return Page(slug=slug)


@pytest.fixture()
def page_with_content_path(mocker, content):
    mocker.patch('pathlib.Path.read_text', lambda _:content)
    return Page(slug='test_page_with_content_path', content_path='fake_path.md')
