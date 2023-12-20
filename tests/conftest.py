import pytest
from jinja2 import Environment, select_autoescape

from render_engine.collection import Collection
from render_engine.engine import (
    render_engine_templates_loader,
    to_absolute,
    to_pub_date,
)
from render_engine.page import Page
from render_engine.site import Site


@pytest.fixture
def engine() -> Environment:
    env = Environment(
        loader=render_engine_templates_loader,
        autoescape=select_autoescape(["xml"]),
        lstrip_blocks=True,
        trim_blocks=True,
    )

    env.filters["to_pub_date"] = to_pub_date
    env.filters["to_absolute"] = to_absolute
    return env


@pytest.fixture()
def site(tmp_path):
    tmp_dir = tmp_path / "content"
    tmp_dir.mkdir()
    file = tmp_dir / "#"
    file.write_text("test")

    site = Site()

    @site.collection
    class TestCollection(Collection):
        pages = [Page(content_path=file)]
        has_archive = True

    return site
