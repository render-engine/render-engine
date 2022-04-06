from pathlib import Path
import pytest
from render_engine import Page

@pytest.fixture()
def content():
   return """
---   
title: Test Title
custom_list: foo, bar, biz
custom_attr: this is an attribute
---

# Test Header

Test Paragraph

`<p>Raw HTML</p>`"""

@pytest.fixture()
def base_page():
    """Tests can a simple Page be created given no Parameters"""
    class BasePage(Page):
        pass

    return BasePage()

@pytest.fixture()
def page_with_attrs():
    """Supply this page objects with attributes"""

    class PageWithAttrs(Page):
        title = 'Page with Attrs'
        slug = 'Page Slug with Attrs' # invalid slug format but should be caught
        markdown = """# Test Header
Test Paragraph"""
        custom_list = ['foo', 'bar', 'biz']
        custom_attr = "this is an attribute"

    return PageWithAttrs()

@pytest.fixture()
def base_collection():
    return Collection


@pytest.fixture()
def page_with_content_path(tmp_path, content):
    fake_path = tmp_path / 'fake_path.md'
    fake_path.write_text(content)

    class PageWithContentPath(Page):
        content_path = fake_path
        list_attrs = 'custom_list'

    return PageWithContentPath()