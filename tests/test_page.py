from jinja2 import Markup
from render_engine import Page
from datetime import datetime, tzinfo, timezone
import pytest
import re


@pytest.mark.parametrize('page, page_content',
            [(Page(), ''),
            (Page(content='foo'), 'foo')])
def test_Page_content_None_by_default(page, page_content):
    assert page.content == page_content


def test_page_kwargs_become_properties(page_with_content_path):
    """Custom Parameters can be passed in as Properties"""
    assert page_with_content_path.custom == 'Testing 1,2,3'


def test_page_content_separated_from_attrs(page_with_content_path):
    """When given markdown for content convert it to html and return it as markup"""
    p = page_with_content_path
    assert """# Test Header
Test Paragraph""" == p.content


def test_page_content_converts_to_html(page_with_content_path):
    """When given markdown for content convert it to html and return it as markup"""
    assert page_with_content_path.markup == \
            Markup('<h1>Test Header</h1>\n<p>Test Paragraph</p>')
