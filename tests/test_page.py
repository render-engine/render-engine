import pathlib

import jinja2
import pytest

from render_engine import Page


@pytest.fixture
def page_from_file(tmp_path: pathlib.Path):
    d = tmp_path / "test_page.md"
    content = """---
title: Test Page
custom: "test"
---

# Test Page
This is a test page
"""

    d.write_text(content)
    return Page(content_path=d)


def test_page_attrs_from_file(page_from_file: Page):
    """
    Tests that expected page attrsibutes are set from the file.
    Currently this is handled by the BasePageParser and the logic in the Page.
    """
    assert page_from_file._title == "Test Page"


def test_page_custom_attrs_from_file(page_from_file: Page):
    """Tests that unique page attrsibutes are set from the file"""
    assert page_from_file.custom == "test"


def test_page_from_template(tmp_path: pathlib.Path):
    """Tests that page attributes are set from a template"""

    class CustomPage(Page):
        template = "test.html"
        title = "Test Page"
        template = "test.html"

    environment = jinja2.Environment(loader=jinja2.DictLoader({"test.html": "{{ title }}"}))

    page = CustomPage()
    assert page._render_content(engine=environment) == "Test Page"


def test_page_content_renders_jinja():
    """Tests that page content is rendered with jinja"""

    class CustomPage(Page):
        content = "Test Page"

    page = CustomPage()
    assert page.content == "Test Page"
    assert page._content == "Test Page"


def test_rendered_page_from_template_has_attributes():
    """Tests that selected page attributes are available in a template"""
    template = "{{title}}-{{slug}}-{{url}}"

    environment = jinja2.Environment(loader=jinja2.DictLoader({"test.html": template}))

    class CustomPage(Page):
        template = environment.get_template("test.html")

    assert CustomPage()._render_from_template(template=CustomPage.template) == "CustomPage-custompage-/custompage.html"
