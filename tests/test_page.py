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

    def test_path_and_content(self, caplog):
        """tests a logging warning is raised if you supply both a markdown attr and a content_path"""

        class TestPage(Page):
            markdown = "foo"
            content_path = "bar"

        TestPage()
        assert caplog.record_tuples[0][1] == logging.WARNING


class TestPageWithAttrs:
    def test_page_with_attrs_gets_attrs_from_class(self, p_attrs):
        assert p_attrs.title == "Page with Attrs"

    def test_page_slug_is_slugified(self, p_attrs):
        """Test page text is slugified"""
        assert p_attrs.slug == "page-slug-with-attrs"

    def test_base_page_html_with_content_is_converted_from_markdown(self, p_attrs):
        """If there is no content then the html will be None"""

        assert p_attrs.markdown == "# Test Header\nTest Paragraph"


class TestBasePage:
    @pytest.mark.xfail(strict=True)
    def test_base_page_is_slug(self, page):
        """Tests if a slug is not provided then the slug will be a slugified
        version of the the class name"""
        assert page.slug == "basepage"
        assert str(page) == "basepage"
        assert page.url == "./basepage.html"

    def test_page_html_with_no_content_or_template_is_none(self, page):
        """If there is no content then the html will be None"""

        assert page.markdown == None
        assert hasattr(page, "template") == False
        assert page.content == None


def test_custom_page_accepts_vars_in_init():
    page = Page(foo="bar")

    assert page.foo == "bar"


class TestPageWritesToFile:
    @pytest.mark.xfail(strict=True)
    def test_page_writes_to_file(self, no_template):
        """Given a Path with"""
        assert no_template.exists()

    @pytest.mark.xfail(strict=True)
    def test_page_content_no_template_is_html(self, no_template, p_attrs):
        assert no_template.read_text() == p_attrs.content

    @pytest.mark.xfail(strict=True)
    def test_page_with_tempate_is_rendered(self, with_template, p_attrs):
        assert with_template.read_text() == f"{p_attrs.content}"
