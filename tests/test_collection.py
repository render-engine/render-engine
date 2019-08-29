from render_engine import Collection
import pytest

@pytest.fixture()
def base_collection():
    return Collection()

def test_collection(base_collection):
    assert not base_collection.template
    assert not base_collection.template_vars

@pytest.mark.parametrize('collection, template_var', [
    (Collection(template='foo_path.html'), {}),
    (Collection(), None)],
    )
def test_collection_if_template_then_vars(collection, template_var):
    assert getattr(collection, 'template_var', None) is None
