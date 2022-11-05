import pytest

from render_engine.site import Site


@pytest.fixture(
    scope="session",
)
def base_site(temp_path):
    class BaseSite(Site):
        path = temp_path

    yield BaseSite()
