from render_engine import Collection
import pytest

@pytest.fixture()
def base_collection():
    return Collection()

def test_collection_pages_of_called_type():
    """Collections create pages based on their content_type"""
    pass
