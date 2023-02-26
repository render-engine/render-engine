"""
Feed Objects for Generating RSS Feeds
"""



from .page import BasePage


class RSSFeed(BasePage):
    """
    Creates an RSS feed [`Page`][render_engine.Page] Object.

    !!! Note
        This is the base object type and should only contain the params identified by the standards defined in the [RSS 2.0 Specification](http://www.rssboard.org/rss-specification)

    This is built using the built-in `rss2.0.xml` jinja template.

    !!! Note
        Some browsers may not support the `rss` extension. If you are having issues with your feed, try changing the extension to `xml`.

        ```python
        from render_engine import Site, RSSFeed

        class MyFeed(RSSFeed):
            extension = "xml"

        site = Site()

        @site.collection
        class MyCollection(Collection):
            Feed = MyFeed
        ```
    """

    template = "rss2.0.xml"
    extension: str = ".rss"
