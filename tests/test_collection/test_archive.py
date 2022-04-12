import pytest


def test_archive_name_from_collection(base_collection):
    assert base_collection.archives[0].title == base_collection.title


def test_paginated_archive_name_from_collection(custom_collection):
    assert custom_collection.archives[0].title == f'{custom_collection.title}_0'


def tests_archive_is_single_page_listing_if_items_per_page_is_falsy(base_collection):
    pages = base_collection.archives
    assert len(pages) == 1
    assert len(pages[0].pages) == 5

def tests_archive_is_paginated_if_items_per_page(custom_collection):
    pages = custom_collection.archives
    assert len(pages) == 3
    assert len(pages[0].pages) == 2