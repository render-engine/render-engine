import pluggy
import pytest

from render_engine.collection import Collection
from render_engine.feeds import RSSFeed
from render_engine.page import Page
from render_engine.parsers.markdown import MarkdownPageParser

pm = pluggy.PluginManager("fake_test")


def test_can_manually_set_slug():
    """Test that the feed slug can be set manually"""

    class feed(RSSFeed):
        pages = []
        slug = "test-feed-slug"

    assert feed(pm=pm).slug == "test-feed-slug"


def test_rss_feed_title_from_collection():
    """Test that the feed title is set from the collection"""

    class TestCollection(Collection):
        feed_title = "Test Feed Title"
        Feed = RSSFeed
        pages = [Page(pm=pm)]

    collection = TestCollection(pm=pm)

    assert collection._feed.title == "Test Feed Title"


def test_rss_feed_inherites_from_collection(tmp_path):
    """Test that the feed title is set from the collection"""

    tmp_dir = tmp_path / "content"
    tmp_dir.mkdir()
    file = tmp_dir / "test.md"
    file.write_text("test")

    class BasicCollection(Collection):
        content_path = tmp_dir.absolute()
        archive_template = None
        Feed = RSSFeed

    collection = BasicCollection(pm=pm)

    assert collection._feed.title == "BasicCollection"
    assert collection._feed.url == "basiccollection.rss"
