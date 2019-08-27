import pytest
from render_engine import Page, Collection


@pytest.fixture()
def base_page():
    return Page(slug='base_page')
