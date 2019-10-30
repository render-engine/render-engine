from render_engine.feeds import RSSFeedItem
import pytest

@pytest.fixture()
def base_feed_item():
    class Page(RSSFeedItem):
        title = 'this is a test item title'
        description = 'this is the test item description'
        content = 'this is the test item content'
        summary = 'this is the test item summary'
        guid = 'this is the test item guid'
        _slug = 'this is the test item _slug'

    return Page


def test_rssfeeditem_has_title_but_no_description(base_feed_item):
    # Must have either a title or description
    assert base_feed_item().description == 'this is the test item description'


def test_rssfeeditem_has_description_from_content(base_feed_item):
    # Must have either a title or description
    class Page(base_feed_item):
        description = ''

    assert Page().description == 'this is the test item content'


def test_description_can_pull_from_content_if_no_description(base_feed_item):
    class Page(base_feed_item):
        description = ''
        content = ''

    assert Page().description == 'this is the test item summary'


def test_rssfeeditem_with_no_title_or_description_raises_error(base_feed_item):
    # Must have either a title or description

    with pytest.raises(AttributeError):
        RSSFeedItem()



def test_rssfeeditem_guid_is_guid_by_default(base_feed_item):
    assert base_feed_item().guid == 'this is the test item guid'


def test_rssfeeditem_guid_is__slug_if_no_guid(base_feed_item):
    class Page(base_feed_item):
        guid = ''

    assert Page().guid == 'this is the test item _slug'



