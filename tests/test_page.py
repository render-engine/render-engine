import tempfile
import pytest
import pathlib
from jinja2 import Markup
import render_engine
from render_engine import Page
from render_engine.page import parse_content


def test_parse_content_splits_text():
    content = 'title: Some Title\n\nThis is the content.'
    assert parse_content(content, r"(^\w+: \b.+$)") == (
            ['title: Some Title'],
            'This is the content.',
            )


def test_page_kwargs_become_properties(page_with_content_path):
    """Custom Parameters can be passed in as Properties"""
    assert page_with_content_path.custom == "Testing 1,2,3"


def test_page_content_path_defined_in_object_caught(mocker, content):
    mocker.patch.object(render_engine.page, 'Path')
    render_engine.page.Path().read_text.return_value = content

    class tp(Page):
        content_path = 'fake_path.md'

    t = tp()
    assert t._content == '# Test Header\nTest Paragraph'


def test_page_with_attr_with_multiple_values():
    t = Page(content='tags: foo, bar')
    assert t.tags == ['foo', 'bar']

def test_page_as_str_is_slug():
    class tp(Page):
        pass

    t = tp()
    assert str(t) == 'tp'


def test_page_html_with_no_content_is_empty_string():
    class tp(Page):
        pass

    t = tp()
    assert t.html == ''


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

@pytest.mark.parametrize(
    "attr, value, result",
    (
        [None, None, "page"],
        ["title", "Page has Title", "page_has_title"],
        ["slug", "page has slug", "page_has_slug"],
    ),
)
def test_page_slug_can_find_slug(attr, value, result):
    if attr:
        content= f"""{attr}: {value}

Test Content"""
        p = Page(content=content)

    else:
        p = Page()
    assert p.slug == result
