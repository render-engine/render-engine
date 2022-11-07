import logging
from pathlib import Path

import pytest
from markdown2 import markdown
from markupsafe import Markup

from render_engine import Page

logger = logging.getLogger("Test Logger")
logger.setLevel(logging.INFO)


class TestPageWithContentPath:
    def test_page_content_converts_markdown_to_html(self, with_path):
        """Tests that `Page.html` is converted to html"""

        assert (
            with_path.content
            == """<h1>Test Header</h1>

<p>Test Paragraph</p>

<p><code>&lt;p&gt;Raw HTML&lt;/p&gt;</code></p>
"""
        )

    def test_with_path(self, with_path):
        assert with_path.custom_list == ["foo", "bar", "biz"]

    def test_path_and_content(self, temp_path, caplog):
        """tests a logging warning is raised if you supply both a markdown attr and a content_path"""
        fake_path = Path(temp_path / "fake_path.md")
        fake_path.write_text("")

        class HasBothContentPaths(Page):
            content_path = fake_path
            markdown = "This is some text"

        HasBothContentPaths()
        assert caplog.record_tuples[0][1] == logging.WARNING


class TestPageWithAttrs:
    def test_page_with_attrs_gets_attrs_from_class(self, p_attrs):
        assert p_attrs.title == "Page with Attrs"

    def test_page_slug_is_slugified(self, p_attrs):
        """Test basic_page text is slugified"""
        assert p_attrs.slug == "page-slug-with-attrs"

    def test_base_page_html_with_content_is_converted_from_markdown(self, p_attrs):
        """If there is no content then the html will be None"""

        assert p_attrs.markdown == "# Test Header\nTest Paragraph"


class TestBasePage:
    def test_base_page_name_is_slug(self, basic_page):
        """Tests if a slug is not provided then the slug will be a slugified
        version of the the class name"""
        assert basic_page.slug == "basepage"  # basic_page._slug
        assert str(basic_page) == "basepage"
        assert basic_page.url == Path("./basepage.html")

    def test_page_html_with_no_content_or_template_is_none(self, basic_page):
        """If there is no content then the html will be None"""

        assert basic_page.markdown == None
        assert hasattr(basic_page, "template") == False
        assert basic_page.content == None


def test_custom_page_accepts_vars_in_init():
    basic_page = Page(foo="bar")

    assert basic_page.foo == "bar"


class TestPageWritesToFile:
    def test_page_writes_to_file(self, no_template):
        """Given a Path with"""
        assert no_template.exists()

    def test_page_content_no_template_is_html(self, no_template, p_attrs):
        assert no_template.read_text() == p_attrs.content

    def test_page_with_tempate_is_rendered(self, with_template, p_attrs):
        assert with_template.read_text() == f"{p_attrs.content}"
