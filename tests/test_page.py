import pdb
import re

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

    class CustomPage(Page):
        template = "test.html"
        title = "Test Page"
        template = "test.html"

    environment = jinja2.Environment(
        loader=jinja2.DictLoader({"test.html": "{{ title }}"})
    )

    page = CustomPage()
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

    page = CustomPage()
    assert page._render_content(engine=environment) == "This is a test page"


def find_all_curly_boys(content):
    the_boys = re.findall(r"{{(.+)}}", content)
    for value in the_boys:
        print(value)


def test_page_template_supports_mustache_vars():
    class CustomPage(Page):
        title = "Test Page"
        template = "test.html"
        content = "This is the {{title}}"

    page = CustomPage()

    environment = jinja2.Environment(
        loader=jinja2.DictLoader({"test.html": "{{ content }}"}),
    )

    assert page._render_content(engine=environment) == "This is the Test Page"
