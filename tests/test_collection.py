from render_engine import Collection
import pytest

@pytest.fixture()
def base_collection():
    return Collection()

def test_collection_defaults(base_collection):
    assert not base_collection.template
    assert not base_collection.template_vars
    assert base_collection.collection_path == Path('content')

@pytest.mark.parametrize('collection, template_var', [
    (Collection(template='foo_path.html'), {}),
    (Collection(), None)],
    )
def test_collection_if_template_then_vars(collection, template_var):
    assert getattr(collection, 'template_var', None) is None


def test_collection_can_add_pages(base_page, base_collection):
    assert len(base_collection) == 0
    for x in range(4):
        base_collection.pages.append(base_page)

    assert len(base_collection) == 4
