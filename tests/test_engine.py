from jinja2 import Markup
from pathlib import Path
from render_engine import Engine, Page
import pytest

@pytest.fixture
def base_engine():
    return Engine()


def test_engine_defaults(base_engine):
    assert base_engine.output_path == Path('output')


def test_engine_markup_returns_content_with_no_template(base_engine):
    page = Page(slug='foo', content="#Foo")
    assert base_engine.Markup(page) == Markup('<h1>Foo</h1>')

@pytest.mark.skip(reason="NOT SURE HOW TO WRITE - ISSUE SUBMITTED")
def test_engine_markup_returns_content_with_template(base_engine):
    pass

@pytest.mark.skip(reason="NOT SURE HOW TO WRITE - ISSUE SUBMITTED")
def test_engine_page_writes_markup(base_engine)
    """Not Sure How to Write this Test"""
    pass
