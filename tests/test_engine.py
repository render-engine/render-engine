from jinja2 import Markup
from pathlib import Path
from render_engine import Engine, Page
import pytest

@pytest.fixture
def base_engine():
    return Engine()


def test_engine_defaults(base_engine):
    assert base_engine.output_path == Path('output')
