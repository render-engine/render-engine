import pluggy

from render_engine.collection import Collection
from render_engine.feeds import RSSFeed
from render_engine.page import Page
from render_engine.engine import engine

pm = pluggy.PluginManager("fake_test")


def test_can_manually_set_slug():
    """Test that the feed slug can be set manually"""

    class feed(RSSFeed):
        pages = []
        slug = "test-feed-slug"

    assert feed().slug == "test-feed-slug"


def test_feed_path_name():
    """Test that the feed path name is set correctly"""

    class feed(RSSFeed):
        pages = []

    assert feed().path_name == "feed.rss"

def test_rss_feed_title_from_collection():
    """Test that the feed title is set from the collection"""

    class TestCollection(Collection):
        feed_title = "Test Feed Title"
        Feed = RSSFeed
        pages = [Page()]

    collection = TestCollection()

    assert collection._feed.title == "Test Feed Title"


def test_rss_feed_inherites_from_collection():
    """Test that the feed title is set from the collection"""

    class BasicCollection(Collection):
        pages = [Page()]
        archive_template = None
        Feed = RSSFeed

    collection = BasicCollection()

    assert collection._feed.title == "BasicCollection"

def test_rss_feed_item_url(tmp_path):
    """Test that the feed item url is set correctly"""
    tmp_dir = tmp_path / "content"
    tmp_dir.mkdir()
    file = tmp_dir / "#"
    file.write_text("test")

    class TestCollection(Collection):
        pages = [Page(content_path=file)]
        Feed = RSSFeed

    collection = TestCollection()
    print(collection._feed.template)
    assert "http://localhost:8000//page.html" in collection._feed._render_content(engine=engine)