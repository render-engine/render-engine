import jinja2
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


def test_page_from_template(tmp_path):
    """Tests that page attributes are set from a template"""
    page = Page()
    page.title = "Test Page"
    page.template = "test.html"

    environment = jinja2.Environment(
        loader=jinja2.DictLoader({"test.html": "{{ title }}"})
    )

    assert page._render_content(engine=environment) == "Test Page"


def test_page_from_template_with_content(tmp_path):
    """Tests that page attributes are set from a template"""
    page = Page()
    page.title = "Test Page"
    page.template = "test.html"
    page.content = "This is a test page"

    environment = jinja2.Environment(
        loader=jinja2.DictLoader({"test.html": "{{ content }}"}),
    )

    assert page._render_content(engine=environment) == "<p>This is a test page</p>\n"
