from render_engine.subcollections import SubCollection
from render_engine import Collection
from render_engine import Page

from pathlib import Path
import tempfile
import render_engine
import pytest

@pytest.fixture()
def test_collection():
    page_1 = Page()
    page_2 = Page()

    page_1.title = 'Page 1'
    page_1.slug = 'page1'

    page_2.title = 'Page 2'
    page_2.slug = 'page2'


    class TestCollection(Collection):
        content_items = [page_1, page_2]

    return TestCollection()

def test_collection_content_items_equals_pages_if_nothing_else_exists(test_collection):
    """Test that the collections content_items are visible in pages"""
    assert test_collection.content_items == test_collection.pages


def test_collection_archive_page_pages_sorted_by_default_sort(test_collection):
    """By default the sort uses the slug"""
    assert test_collection.archive_default_sort(test_collection.pages[0]) == 'page1'


def test_collection_raises_warning_if_content_path_is_root(mocker):
    class DangerousCollection(Collection):
        content_path = '/'

    mocker.patch.object(render_engine.collection, 'logging')

    dc = DangerousCollection()
    dc.pages
    render_engine.collection.logging.warning.assert_called_with(
            "self.content_path='/'! Accessing Root Directory is Dangerous..."
            )


def test_collection_page_content_type_is_passed_to_content_path_items():
    with tempfile.TemporaryDirectory() as tmpdirname:

        with tempfile.NamedTemporaryFile(mode="w", suffix='.md', dir=tmpdirname) as tpfile:
            tpfile.write('''slug: test\n\nThis is some test data''')

            class TestCollection(Collection):
                content_path = tmpdirname

            test_collection = TestCollection()
            print(test_collection.pages)
            assert isinstance(test_collection.pages[0], Page)
