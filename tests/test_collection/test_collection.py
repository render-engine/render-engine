import pytest
from render_engine.collection import Collection
from render_engine.page import Page
from pathlib import Path

def test_collections_discovers_title(base_collection, custom_collection):
    assert base_collection.title == "MyCollection"
    assert custom_collection.title == "My Custom Title"

def test_collections_accept_custom_vars(custom_collection):
    assert custom_collection.foo == "bar"

def test_collection_passes_vars_to_page(base_collection, temp_dir_collection):
    assert base_collection.pages[Path(temp_dir_collection/'fake_path_0.md')].collection_title == "MyCollection"

def test_collection_pages_are_content_type(temp_dir_collection):
    class CustomPage(Page):
        pass

    class MyCollection(Collection):
        content_type = CustomPage
        content_path = temp_dir_collection
    assert isinstance(MyCollection().pages[Path(temp_dir_collection/'fake_path_0.md')], CustomPage)