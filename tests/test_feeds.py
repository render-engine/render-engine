import pytest
import logging
from render_engine.feeds import RSSFeedItem, RSSFeedEngine
from render_engine.blog import Blog, BlogSite
from render_engine.page import Page
import pathlib


@pytest.fixture()
def base_rss_engine():
    class baseEngine(RSSFeedEngine):
        engine = Engine()

    return baseEngine


@pytest.mark.skip()
def test_render_engine_templates_path(base_rss_engine):
    loader = base_rss_engine().environment.loader.searchpath[0]
    assert pathlib.Path(loader).is_dir()


@pytest.mark.skip()
def test_render_engine_templates_path_has_rss_file(base_rss_engine):
    loader = base_rss_engine().environment.loader.searchpath[0]
    rss_item = pathlib.Path(loader)
    assert len(list(rss_item.glob("*.rss"))) >= 1


def test_render_feed_renders():
    rss_site = BlogSite(
            title = 'Demo Site',
            description = 'Site Description',
            link = 'https://example.com/site.rss',
            )

    class page(RSSFeedItem):
        title = 'Demo Page Title'

    rss_item = rss_site.feed_engine.render_feed([page])
