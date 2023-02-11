import jinja2
import pluggy
import pytest

from render_engine import Page

pm = pluggy.PluginManager("fake_test")


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

    return CustomPage(pm=pm)


def test_page_attrs_from_file(page_from_file):
    """Tests that expected page attrsibutes are set from the file"""
    assert page_from_file.title == "Test Page"


def test_page_custom_attrs_from_file(page_from_file):
    """Tests that unique page attrsibutes are set from the file"""
    assert page_from_file.custom == "test"


def test_page_from_template(tmp_path):
    """Tests that page attributes are set from a template"""

    class CustomPage(Page):
        template = "test.html"
        title = "Test Page"
        template = "test.html"

    environment = jinja2.Environment(
        loader=jinja2.DictLoader({"test.html": "{{ title }}"})
    )

    page = CustomPage(pm=pm)
    assert page._render_content(engine=environment) == "Test Page"


def test_page_from_template_with_content(tmp_path):
    """Tests that page attributes are set from a template"""

    class CustomPage(Page):
        title = "Test Page"
        template = "test.html"
        content = "This is a test page"

    environment = jinja2.Environment(
        loader=jinja2.DictLoader({"test.html": "{{ content }}"}),
    )

    page = CustomPage(pm=pm)
    assert page._render_content(engine=environment) == "This is a test page"
