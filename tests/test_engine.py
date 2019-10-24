from jinja2 import Markup
from pathlib import Path
from render_engine import Engine, Page
import pytest

@pytest.fixture
def base_engine():
    return Engine()

