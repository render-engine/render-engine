from render_engine import Collection
import pytest

@pytest.fixture()
def base_collection():
    return Collection()

def test_collection_(base_collection):
    assert not base_collection.template
    assert not base_collection.template_vars
