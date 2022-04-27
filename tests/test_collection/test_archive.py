import pytest
from slugify import slugify


def test_archive_name_from_collection(base_collection):
    assert base_collection.archives[0].title == base_collection.title


def test_paginated_archive_name_from_collection(custom_collection):
    assert custom_collection.archives[0].title == f"{custom_collection.title}"


def test_paginated_archive_slug(custom_collection):
    assert custom_collection.archives[0].slug == slugify(f"{custom_collection.title}-0")


def tests_archive_page_listings_based_on_items_per_page_is(
    base_collection, custom_collection
):
    collections = [(base_collection, 1, 5), (custom_collection, 3, 2)]

    for collection, page_length, page_count in collections:
        pages = collection.archives
        assert len(pages) == page_length
        assert len(pages[0].pages) == page_count
