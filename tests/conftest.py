from jinja2 import Environment, select_autoescape
import pytest

from render_engine.engine import render_engine_templates_loader


@pytest.fixture
def engine() -> Environment:
    return Environment(
        loader=render_engine_templates_loader,
        autoescape=select_autoescape(["xml"]),
        lstrip_blocks=True,
        trim_blocks=True,
    )
