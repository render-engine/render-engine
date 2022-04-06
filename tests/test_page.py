from markupsafe import Markup
from markdown2 import markdown
from render_engine import Page
import logging


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

    def test_page_html_converts_markdown_to_html(self, page_with_content_path):
        """Tests that `Page.html` is converted to html"""

        assert page_with_content_path.html == """<h1>Test Header</h1>
        
<p>Test Paragraph</p>

<code>&lt;p&gt;Raw HTML&lt;/p&gt;</code>"""

    def test_page_content_is_markup_safe(self, page_with_content_path):

        # TODO: Write Test with Markup data 
        assert page_with_content_path.content == Markup(page_with_content_path.html)

    def test_page_with_content_path(self, page_with_content_path):
        assert page_with_content_path.custom_list == ['foo', 'bar', 'biz']


class TestPageWithAttrs:
    def test_page_with_attrs_gets_attrs_from_class(self, page_with_attrs):
        assert page_with_attrs.title == "Page with Attrs"

    def test_page_slug_is_slugified(page_with_attrs):
        """Test page text is slugified"""
        assert page_with_attrs.slug == 'page-slug-with-attrs'


def test_base_page_is_slug(base_page):
    """Tests if a slug is not provided then the slug will be a slugified
    version of the the class name"""
    assert base_page.slug == 'basepage'


def test_page_html_with_no_content_is_empty_string(base_page):
    """If there is no content then the html will be None"""
    
    assert not base_page.html == ""
    assert not base_page.content == ""


def test_base_page_html_with_content_is_converted_from_markdown(page_with_attrs):
    """If there is no content then the html will be None"""

    assert page_with_attrs.html == markdown('#Test Header\nTest Paragraph')
    assert page_with_attrs.content == Markup(page_with_attrs.html)



