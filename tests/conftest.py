from pathlib import Path
import pytest
from render_engine import Page

@pytest.fixture()
def content():
    return """title: Test Title
custom: Testing 1,2,3

# Test Header
Test Paragraph"""

@pytest.fixture()
def base_page():
    """Tests can a simple Page be created given no Parameters"""
    return Page()


@pytest.fixture()
def page_with_content_path(mocker, content):
    mocker.patch('pathlib.Path.read_text', lambda _:content)
    return Page(content_path=Path('fake_path.md'))
