import pytest
from render_engine.collection import Collection
from pathlib import Path

def test_collections_discovers_title(base_collection, custom_collection):
    assert base_collection.title == "MyCollection"
    assert custom_collection.title == "My Custom Title"

def test_collections_accept_custom_vars(custom_collection):
    assert custom_collection.foo == "bar"

def test_collection_passes_vars_to_page(base_collection, temp_dir_collection):
    assert base_collection.pages[Path(temp_dir_collection/'fake_path_0.md')].collection_title == "MyCollection"

