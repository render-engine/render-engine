from render_engine.site import Site, get_subcollections
from render_engine.collection import Collection
from render_engine.page import Page
from render_engine.feeds import RSSFeed
from render_engine.engine import Engine

import os
import shutil
import pytest
from pathlib import Path

def test_site_environment_var():
    class TestSite(Site):
        timezone = 'US/Eastern'

    TestSite()
    assert os.environ['render_engine_timezone'] == 'US/Eastern'


def test_register_route():
    class TestSite(Site):
       routes = []

    t = TestSite()

    assert not t.routes # Verify that the site routes are empty on creation

    @t.register_route
    class TestPage(Page):
        pass

    # The contents of TestCollection.content_items should be added to t.routes

    assert t.routes[0].title == 'TestPage'


def test_site_registers_each_archive_page():
    pass

def test_get_subcollections_adds_to_set():
    class TestPage(Page):
        foo = 'bar'

    class AnotherTestPage(Page):
        foo = ['biz']

    class TestCollection(Collection):
        content_items = [TestPage(), AnotherTestPage()]
        subcollections = ['foo']


    assert get_subcollections(TestCollection()) == {('foo', 'bar'), ('foo',
        'biz')}

def test_output_path_error_raised_when_targeting_file(tmp_path):
    temp = tmp_path / 'error_file.txt'
    Path(temp).touch()

    class TestSite(Site):
        output_path = temp
        strict = True

    with pytest.raises(ValueError):
        t = TestSite()


def test_output_path_is_cleared_when_new_site_is_created(tmp_path):
    temp = tmp_path
    test_file = temp.joinpath('test_file.txt')
    test_file.touch()

    class TestSite(Site):
        output_path = temp
        strict = True

    assert test_file.exists() == True

    t = TestSite()

    assert test_file.exists() == False


def test_static_path_copied_into_output_path():
    """Tests that static directory is copied into the output directory"""

    test_path = Path('./tests/test_folder')
    test_path.mkdir(parents=True, exist_ok=True)

    test_static_path = test_path.joinpath('static')
    test_static_path.mkdir(exist_ok=True)

    test_file = test_static_path.joinpath('test_file')
    test_file.touch(exist_ok=True)

    class TestSite(Site):
        output_path = test_path.joinpath('output')
        static_path = test_static_path

    t = TestSite()

    assert test_path.joinpath('static/test_file').is_file()

    # Cleanup
    shutil.rmtree('./tests/test_folder')


def test_register_collection_adds_collection_to_site_collections_dict():
    class TestSite(Site):
        pass

    t = TestSite()

    @t.register_collection
    class TestCollection(Collection):
        pass

    assert 'TestCollection' in t.collections


def test_register_collection():
    class TestSite(Site):
        routes = []

    t = TestSite()

    assert not t.routes # Verify that the site routes are empty on creation

    @t.register_collection
    class TestCollection(Collection):
        content_items = [Page()]

    # The contents of TestCollection.content_items should be added to t.routes

    assert t.routes[0].title == 'Page'


def test_register_collection_archive_added_to_routes():
    """If your registered collection has an archive, Add the archive to
    site.routes"""
    class TestSite(Site):
        routes = []

    t = TestSite()

    assert not t.routes # Verify that the site routes are empty on creation

    @t.register_collection
    class TestCollection(Collection):
        content_items = []
        has_archive = True

    # The archive of TestCollection be added to t.routes

    assert t.routes[0].title == 'TestCollection'


def test_collection_subcollection_adds_new_subcollection():
    """Tests subcollections are added to sites"""

    class TestSite(Site):
        routes = []

    class TestPage(Page):
        foo = 'bar'

    t = TestSite()

    @t.register_collection
    class TestCollection(Collection):
        content_items = [TestPage()]
        subcollections = ['foo']

    assert t.subcollections['foo'][0].title == 'bar'

def test_collection_subcollection_appends_subcollection_route():
    """Tests subcollections are added to sites"""

    class TestSite(Site):
        routes = []
        collections = []
        subcollections = []

    class TestPage(Page):
        foo = 'bar'

    class TestAnotherPage(Page):
        foo = 'biz'

    t = TestSite()

    @t.register_collection
    class TestCollection(Collection):
        content_items = [TestPage(), TestAnotherPage()]
        subcollections = ['foo']

    subcollection_titles = [x.title for x in t.subcollections['foo']]
    assert 'biz' in subcollection_titles
    assert 'bar' in subcollection_titles


def test_collection_feed_adds_feed_object_to_route():
    """Tests subcollections are added to sites"""

    class TestSite(Site):
        routes = []
        SITE_TITLE = 'The Test Site'

    t = TestSite()

    @t.register_collection
    class TestCollection(Collection):
        feeds = [RSSFeed]

    assert t.routes[0].title == f'{t.SITE_TITLE} - RSS Feed'


def test_site_render_pulls_site_engine_if_not_found(tmp_path):
    class MyEngine(Engine):
        def render(self, **kwargs):
            return 'My Test Engine'

    class TestSite(Site):
        output_path = tmp_path

    t = TestSite()

    @t.register_route
    class TestPageWithEngine(Page):
        engine = MyEngine

    @t.register_route
    class TestPageNoEngine(Page):
        pass

    t.render()
    assert len([x for x in tmp_path.iterdir()]) == 2
    assert tmp_path.joinpath('testpagewithengine.html').read_text() == 'My Test Engine'
    assert tmp_path.joinpath('testpagenoengine.html').read_text() == ''


def test_site_render_page_attrs_are_clean(tmp_path):
    """When two items in a collection"""

    temp_content = tmp_path.joinpath('content')
    temp_content.mkdir()

    temp_page_1 = temp_content.joinpath('page1.md')
    temp_page_1.write_text('title: Test Page1\nfoo: bar This is Test Page 1')

    temp_page_2 = temp_content.joinpath('page2.md')
    temp_page_2.write_text('title: Test Page2\nbiz: baz This is Test Page 2')

    class TestMultipleAttrsCollection(Collection):
        content_path = temp_content

    c = TestMultipleAttrsCollection()

    for page in c._pages:
        assert page.foo
        assert page.biz
