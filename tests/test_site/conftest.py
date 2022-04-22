import pytest
from render_engine.site import Site
from tests.conftest import gen_content

@pytest.fixture(scope='session',)
def base_site(temp_path):
    class BaseSite(Site):
        path = temp_path

    yield BaseSite()