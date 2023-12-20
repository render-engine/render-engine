import pytest

from render_engine import Collection, Page, Site
from render_engine.feeds import RSSFeed


@pytest.fixture()
def site(tmp_path):
    tmp_dir = tmp_path / "content"
    tmp_dir.mkdir()
    file = tmp_dir / "#"
    file.write_text("test")

    site = Site()

    @site.collection
    class TestCollection(Collection):
        pages = [Page(content_path=file)]
        Feed = RSSFeed
        has_archive = True

    return site


@pytest.fixture()
def feed_test_site(tmp_path):
    tmp_dir = tmp_path / "content"
    tmp_dir.mkdir()
    file = tmp_dir / "#"
    file.write_text("test")

    site = Site()

    @site.collection
    class TestCollection(Collection):
        pages = [Page(content_path=file)]
        Feed = RSSFeed
        routes = ["feed"]

    feed = site.route_list["testcollection"].feed
    feed_content = feed._render_content(engine=site.theme_manager.engine, SITE_URL="http://localhost:8000")
    return feed_content
