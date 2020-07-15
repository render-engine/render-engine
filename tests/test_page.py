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


def test_page_content_path_defined_in_object_caught_with_fake_path(tmp_path, content):
    """Tests when given a file as the content_path, parse it into data """

    fake_path = tmp_path / 'fake_path.md'
    fake_path.write_text(content)

    class TestPage(Page):
        content_path = fake_path

    t = TestPage()

    assert t.content == '# Test Header\nTest Paragraph'


def test_page_slug_is_slugified():
    class TestPage(Page):
        slug = 'This is a slugged slug'

    t = TestPage()
    assert t.slug == 'this-is-a-slugged-slug'


def test_page_name_as_str_is_slug():
    class TestPage(Page):
        slug = 'test-page'

    t = TestPage()
    assert str(t) == 'test-page'


def test_page_html_with_no_content_is_empty_string():
    """If there is no content then the html will be None"""
    class TestPage(Page):
        pass

    t = TestPage()
    assert not t.html
    assert not t.markup


def test_page_html_with_content_is_converted_from_markdown():
    """If there is no content then the html will be None"""

    class TestPage(Page):
        content = '# Test Title'

    t = TestPage()
    assert t.html == '<h1>Test Title</h1>\n'
    assert t.markup == Markup(t.html)


def test_page_attrs_from_content_path_(tmp_path, content):
    """Tests when given a file as the content_path, parse it into data """

    fake_path = tmp_path / 'fake_path.md'
    fake_path.write_text(content)

    class TestPage(Page):
        content_path = fake_path

    t = TestPage()

    assert t.title== 'Test Title'


def test_page_list_attrs_from_content_path(tmp_path, content):
    """Tests when given a file as the content_path, parse it into data """

    fake_path = tmp_path / 'fake_path.md'
    fake_path.write_text(content)

    class TestPage(Page):
        content_path = fake_path
        list_attrs = ['custom']

    t = TestPage()

    assert t.custom == ['1', '2', '3']


def test_page_from_content_path(tmp_path, content):
    fake_path = tmp_path / 'fake_path.md'
    fake_path.write_text(content)


    t = Page.from_content_path(fake_path)
    assert t.content_path == fake_path
