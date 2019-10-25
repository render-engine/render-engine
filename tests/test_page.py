import pytest
from jinja2 import Markup
from render_engine import Page


def test_page_kwargs_become_properties(page_with_content_path):
    """Custom Parameters can be passed in as Properties"""
    assert page_with_content_path.custom == "Testing 1,2,3"


def test_page_content_separated_from_attrs(page_with_content_path):
    """When given markdown for content convert it to html and return it as markup"""
    p = page_with_content_path
    assert (
        """# Test Header
Test Paragraph"""
        == p._content
    )


def test_page_content_converts_to_html(page_with_content_path):
    """When given markdown for content convert it to html and return it as markup"""
    assert page_with_content_path.html == \
        "<h1>Test Header</h1>\n<p>Test Paragraph</p>"

def test_page_content_converts_to_html(page_with_content_path):
    """When given markdown for content convert it to html and return it as markup"""
    assert page_with_content_path.content == \
        Markup("<h1>Test Header</h1>\n<p>Test Paragraph</p>")

@pytest.mark.parametrize(
    "attr, value",
    (
        [None, "page_with_no_title"],
        ["title", "Page has Title"],
        ["slug", "page has slug"],
    ),
)
def test_page__slug_can_find__slug(attr, value):
    class Page_With_No_Title(Page):
        def __init__(self, _attr, _value):

            if _attr:
                setattr(self, _attr, _value)

    p = Page_With_No_Title(attr, value)
    assert p.__str__() == value.lower().replace(" ", "_")
