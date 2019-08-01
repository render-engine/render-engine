import pytest
from render_engine import Collection

@pytest.fixture()
def base_collection():
    """Tests can a simple Collection be created given no Parameters"""
    return Collection(
            route='/test.html',
            paginate=False,
            name='test collection',
            content_path='./',
            url_root='./',
            custom_val='custom',
            )

def test_Collection_kwargs_become_properties(base_collection):
    assert base_collection.custom_val == 'custom'
