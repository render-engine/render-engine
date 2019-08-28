from render_engine import Collection
import pytest

@pytest.fixture()
def base_collection():
    return Collection()

def test_collection(base_collection):
    assert not base_collection.template_vars
    assert not base_collection.index_template_vars
    assert not base_collection.template
    assert not base_collection.index_template
    assert not base_collection.no_index

