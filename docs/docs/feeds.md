# RSS Feed

Feed Objects for Generating RSS Feeds

## Classes

`RSSFeed`

Bases: [`BasePage`](./page?id=basepage)

Creates an RSS feed [Page](./page) Object.

> [!NOTE]
> This is the base object type and should only contain the params identified by the standards defined in the [RSS 2.0 Specification](http://www.rssboard.org/rss-specification).

This is built using the built-in `rss2.0.xml` jinja template.

> [!NOTE]
> Some browsers may not support the `rss` extension. If you are having issues with your feed, try changing the extension to `xml`.
>
> ```Python
> from render_engine import Site, RSSFeed
>
> class MyFeed(RSSFeed):
>    extension = "xml"
>
> site = Site()
>
> @site.collection
> class MyCollection(Collection):
>    Feed = MyFeed
> ```
