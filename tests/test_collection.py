from render_engine import Collection
import pytest

@pytest.fixture()
def base_collection():
    return Collection()


# @pytest.mark.skip(reason='CollectionRefactored')
def test_collection_can_add_pages(base_page, base_collection):
    assert len(base_collection) == 0
    base_collection.add(base_page)

    assert len(base_collection) == 1

def test_collection_default_sort_field(base_collection):
    assert base_collection._default_sort_field == 'title'
