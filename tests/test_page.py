import logging
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


def test_rendered_page_from_template_has_content():
    """Tests that selected page attributes are available in a template"""
    template = "{{content}}"

    environment = jinja2.Environment(loader=jinja2.DictLoader({"test.html": template}))

    class CustomPage(Page):
        template = environment.get_template("test.html")
        content = "This is a custom page"

    assert CustomPage()._render_from_template(template=CustomPage.template) == "This is a custom page"


def test_rendered_page_from_template_has_data():
    """Tests that selected page attributes are available in a template"""
    template = "{% for d in data %}{{d}}{% endfor %}"

    environment = jinja2.Environment(loader=jinja2.DictLoader({"test.html": template}))

    class CustomPage(Page):
        template = environment.get_template("test.html")
        data = [1, 2, 3, 4]

    assert CustomPage()._render_from_template(template=CustomPage.template) == "1234"


def test_page_fails_to_render_content_as_template(caplog):
    """Tests handling content that fails to render as a template"""
    caplog.set_level(logging.INFO)

    template = "{% for d in data %}{{d}}{% endfor %}\n{{content}}"

    environment = jinja2.Environment(loader=jinja2.DictLoader({"test.html": template}))

    class CustomPage(Page):
        template = environment.get_template("test.html")
        data = [1, 2, 3, 4]
        content = "{{ site_map.find('test') }}"

    assert CustomPage()._render_from_template(template=CustomPage.template) == "1234\n{{ site_map.find('test') }}"
    assert "Failed to pre-render" in caplog.messages[0]


def test_braces_ignored_without_sitemap():
    """Tests that braces in content are ignored without `site_map`"""
    template = "{% for d in data %}{{d}}{% endfor %}\n{{content}}"

    environment = jinja2.Environment(loader=jinja2.DictLoader({"test.html": template}))

    class CustomPage(Page):
        template = environment.get_template("test.html")
        data = [1, 2, 3, 4]
        content = "{{ example }}"

    assert CustomPage()._render_from_template(template=CustomPage.template) == "1234\n{{ example }}"


def test_exception_in_parsing_content_as_template(monkeypatch, caplog):
    """Test failing to parse content as template"""

    def mock_template():
        raise jinja2.exceptions.UndefinedError("Mocked error")

    monkeypatch.setattr("render_engine.page.Template", mock_template)
    caplog.set_level(logging.INFO)

    template = "{% for d in data %}{{d}}{% endfor %}\n{{content}}"

    environment = jinja2.Environment(loader=jinja2.DictLoader({"test.html": template}))

    class CustomPage(Page):
        template = environment.get_template("test.html")
        data = [1, 2, 3, 4]
        content = "{{ site_map.find('test') }}"

    assert CustomPage()._render_from_template(template=CustomPage.template) == "1234\n{{ site_map.find('test') }}"
    assert "Failed to parse" in caplog.messages[0]


def test_no_prerender():
    """Test pre-rendering does not occur when no_prerender is True"""
    template = "{% for d in data %}{{d}}{% endfor %}\n{{content}}"

    environment = jinja2.Environment(loader=jinja2.DictLoader({"test.html": template}))

    class CustomPage(Page):
        template = environment.get_template("test.html")
        data = [1, 2, 3, 4]
        content = "{{ site_map.find('test') }}"
        no_prerender = True

    assert CustomPage()._render_from_template(template=CustomPage.template) == "1234\n{{ site_map.find('test') }}"
