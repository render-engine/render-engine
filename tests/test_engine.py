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


def test_engine_markup_returns_content_with_template(base_engine):
    pass
