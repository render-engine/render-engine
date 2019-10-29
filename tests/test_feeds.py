from render_engine.feeds import RSSFeedItem
import pytest

def test_rssfeeditem_has_title_but_no_description():
    # Must have either a title or description
    class Page:
        title = 'This is a Test Item Title'
        content = ''

    test_page = Page()
    assert RSSFeedItem(test_page)


def test_rssfeeditem_has_description_but_no_title():
    # Must have either a title or description
    class Page:
        content = 'This is a Test Item Content'
        title = ''

    test_page = Page()
    assert RSSFeedItem(test_page)


def test_rssfeeditem_with_no_title_or_description_raises_error():
    # Must have either a title or description
    with pytest.raises(AttributeError):
        class Page:
            title = ''
            content = ''
        RSSFeedItem(Page())


