import pytest

def test_collection_kwargs_become_properties(base_collection):
    assert base_collection.custom_val == 'custom'

def test_collection_sorts_alphabetically(base_collection):
    assert base_collection.pages[0].slug == 'Title_C'
