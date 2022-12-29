import pytest

from render_engine.site import Site


@pytest.fixture
def site():
    return Site()
