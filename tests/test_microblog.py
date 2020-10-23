import feedparser
import pytest
from render_engine.microblog import MicroBlog, MicroBlogPost
from render_engine import Site

def test_get_microblog_title_is_blank():

    class test_post(MicroBlogPost):
        _content  = 'This is a test'
        date = '28 Aug 2020 23:00'
        title = 'No title Please'

    t = test_post()
    assert t.title == ''


def test_microblog_url():
    """Ensure that the slug isn't overwritten by the title"""

    class test_post(MicroBlogPost):
        _content  = 'This is a test'
        date = '28 Aug 2020 23:00'
        title = 'No title Please'
        slug = 'foo foo'

    t = test_post()
    assert t.slug == '20200828230000'

def test_microblog_rss_feed_item_values():
    pass


def test_microblog_rss_feed_link_is_url():
    """The microblog feed link should match that of the microblog item"""


    class testPost(MicroBlogPost):
        _content  = 'This is a test'
        date = '28 Aug 2020 23:00'
        title = 'No title Please'
        slug = 'foo foo'
        description = 'This is a description'
        site = Site()

    t = testPost()
    
    class testMicroblog(MicroBlog):
        content_items = [t]
        site = Site()

    tm = testMicroblog()
    assert t.site.SITE_URL == 'https://example.com'
    assert tm.site.SITE_URL == 'https://example.com'

    items = tm.feeds[0].items

    assert items[0].link == 'https://example.com/20200828230000'
