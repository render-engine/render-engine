from markupsafe import Markup
from markdown2 import markdown
from render_engine import Page
from pathlib import Path
import logging
import pytest

logger = logging.getLogger('Test Logger')
logger.setLevel(logging.INFO)


class TestPageWithContentPath:
    def test_page_defines_attrs_and_content_from_frontmatter(self, page_with_content_path):
        """
        Tests when given a file as the content_path, parse it into data.
        This is done using fronmatter and should pass as long as frontmatter is parser
        """

        assert page_with_content_path.markdown =="""# Test Header

Test Paragraph

`<p>Raw HTML</p>`"""

        assert page_with_content_path.title == 'Test Title'

    def test_page_content_converts_markdown_to_html(self, page_with_content_path):
        """Tests that `Page.html` is converted to html"""

        assert page_with_content_path.content == """<h1>Test Header</h1>

<p>Test Paragraph</p>

<p><code>&lt;p&gt;Raw HTML&lt;/p&gt;</code></p>
"""

    def test_page_with_content_path(self, page_with_content_path):
        assert page_with_content_path.custom_list == ['foo', 'bar', 'biz']


class TestPageWithAttrs:
    def test_page_with_attrs_gets_attrs_from_class(self, page_with_attrs):
        assert page_with_attrs.title == "Page with Attrs"

    def test_page_slug_is_slugified(self, page_with_attrs):
        """Test page text is slugified"""
        assert page_with_attrs.slug == 'page-slug-with-attrs'


    def test_base_page_html_with_content_is_converted_from_markdown(self, page_with_attrs):
        """If there is no content then the html will be None"""

        assert page_with_attrs.markdown == '# Test Header\nTest Paragraph'


class TestBasePage:
    def test_base_page_is_slug(self, base_page):
        """Tests if a slug is not provided then the slug will be a slugified
        version of the the class name"""
        assert base_page.slug == 'basepage'


    def test_page_html_with_no_content_is_empty_string(self, base_page):
        """If there is no content then the html will be None"""
        
        assert base_page.markdown == None
        
        with pytest.raises(ValueError) as e:
            base_page.content



class TestPageWritesToFile():
    
    def test_page_writes_to_file(self, render_page_no_template):
        """Given a Path with """
        assert render_page_no_template.exists()
        
    def test_page_content_no_template_is_html(self, render_page_no_template, page_with_attrs):
        assert render_page_no_template.read_text() == page_with_attrs.content

    def test_page_with_tempate_is_rendered(self, render_page_template, page_with_attrs):
        assert render_page_template.read_text() == f'foo{page_with_attrs.content}'