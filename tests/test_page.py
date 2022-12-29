import pytest

from render_engine import Page


@pytest.fixture()
def page_from_file(tmp_path):
    d = tmp_path / "test_page.md"

    content = """---
title: Test Page
custom: "test"
---

# Test Page
This is a test page
"""
    d.write_text(content)

    class CustomPage(Page):
        content_path = d

    return CustomPage()


def test_page_attrs_from_file(page_from_file):
    """Tests that expected page attrsibutes are set from the file"""
    assert page_from_file.title == "Test Page"


def test_page_custom_attrs_from_file(page_from_file):
    """Tests that unique page attrsibutes are set from the file"""
    assert page_from_file.custom == "test"
