from render_engine import Collection
import pytest

@pytest.fixture()
def base_collection():
    return Collection()

@pytest.mark.parametrize('collection, template_var', [
    (Collection(template='foo_path.html'), {}),
    (Collection(), None)],
    )
def test_collection_if_template_then_vars(collection, template_var):
    assert getattr(collection, 'template_var', None) is None


@pytest.mark.skip(reason='CollectionRefactored')
def test_collection_can_add_pages(base_page, base_collection):
    assert len(base_collection) == 0
    base_collection.pages.add(base_page)

    assert len(base_collection) == 1

def test_collection_default_sort_field(base_collection):
    assert base_collection.default_sort_field == 'title'
