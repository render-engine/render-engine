import pytest

from render_engine.collection import Collection
from render_engine.feeds import RSSFeed
from render_engine.parsers.markdown import MarkdownPageParser


def test_can_manually_set_slug():
    """Test that the feed slug can be set manually"""

    class feed(RSSFeed):
        pages = []
        slug = "test-feed-slug"

    assert feed().slug == "test-feed-slug"


def test_rss_feed_title():
    """Test that the feed title can be set manually"""

    feed = RSSFeed(pages=[], title="Test Feed Title")
    assert feed.title == "Test Feed Title"
    assert feed.slug == "test-feed-title"


def test_rss_feed_title_from_collection():
    """Test that the feed title is set from the collection"""

    class TestCollection(Collection):
        feed_title = "Test Feed Title"
        feed = RSSFeed

    collection = TestCollection()

    print(collection.feed)
    assert collection._feed.title == "Test Feed Title"


def test_rss_feed_inherites_from_collection():
    """Test that the feed title is set from the collection"""

    class TestCollection(Collection):
        feed = RSSFeed

    collection = TestCollection()

    assert collection._feed.title == "TestCollection"
    assert collection._feed.url == "testcollection.rss"


def test_rss_feed_pages_use_page_parser():
    """Test that the feed pages use the page parser"""

    class TestCollection(Collection):
        feed = RSSFeed

    collection = TestCollection()

    assert collection.PageParser == collection._feed.Parser
