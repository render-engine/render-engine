from jinja2 import Markup
from render_engine import Page
from datetime import datetime, tzinfo, timezone
import pytest
import re


def test_page_kwargs_become_properties(page_with_content_path):
    """Custom Parameters can be passed in as Properties"""
    assert page_with_content_path.custom == 'Testing 1,2,3'


def test_page_content_separated_from_attrs(page_with_content_path):
    """When given markdown for content convert it to html and return it as markup"""
    p = page_with_content_path
    assert """# Test Header
Test Paragraph""" == p._content


def test_page_content_converts_to_html(page_with_content_path):
    """When given markdown for content convert it to html and return it as markup"""
    assert page_with_content_path.html== \
            Markup('<h1>Test Header</h1>\n<p>Test Paragraph</p>')
