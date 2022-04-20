from collections import defaultdict
import typing
from pathlib import Path

from .collection import Collection
from .feeds import RSSFeedEngine
from .page import Page
from .sitemap import _render_sitemap
from jinja2 import Environment, FileSystemLoader


class Site:
    """The site stores your pages and collections to be rendered.

    Pages are stored in :py:attr:`routes` and created with `site.render()`.
    Collections and subcollections are stored to be used for future use.

    Sites also contain global variables that can be applied in templates.

    Attributes:
        routes: typing.List[typing.Type[Page]]
            routes are stored prior to being caled with :py:meth:`site.render()`.
    """

    output_path: Path = Path("output")
    """Path to write rendered content."""

    static_path: Path = Path("static")
    """Top Level Directory for static files.

    **ALL** files in this path will be copied into the ``output_path``.
    """

    SITE_TITLE: str = "Untitled Site"
    """Title for the site. To be used in templates"""

    SITE_URL: str = "https://example.com"
    """Title for the site. To be used in templates"""


    engine: typing.Type[Environment] = Environment(loader=FileSystemLoader('templates'))
    """``Engine`` to generate web pages"""

    rss_engine: typing.Type[RSSFeedEngine] = RSSFeedEngine()
    """``Engine`` to generate RSS Feeds"""

    cache_file: Path = Path(".routes_cache")
    """File that hash id's will be stored.

    The ``cache_file`` is checked for values to determine if new pages should be written
    """

    def __init__(self):
        """Clean Directory and Prepare Output Directory"""
        self.output_path:Path = Path(self.output_path)
        self.routes = defaultdict(list)


    def add_collection(self, collection: typing.Type[Collection]) -> None:
        """Add a class to your ``self.collections``
        iterate through a classes ``content_path`` and create a classes ``Page``-like
        objects, adding each one to ``routes``.

        Use a decorator for your defined classes.

        Examples::

            @register_collection
            class Foo(Collection):
                pass
        """
        _collection = collection()
        for page in _collection.pages.values():
            self._build_route(page)
        
        if _collection.has_archive:
            for archive in _collection.archives:
                self._build_route(archive)


    def add_feed(self, feed: RSSFeedEngine, collection: Collection) -> None:
        """Create a Page object that is an RSS feed and add it to self.routes"""

        extension = self.rss_engine.extension
        _feed = feed
        _feed.slug = collection.slug
        _feed.title = f"{self.SITE_TITLE} - {_feed.title}"
        _feed.link = f"{self.SITE_URL}/{_feed.slug}{extension}"
        self.add_routes(feed)

    def add_route(self, page: Page) -> None:
        """Create a Page object and add it to self.routes"""
        _page = page()
        self._build_route(_page)
        
    def _build_route(self, _page: Page) -> None:
        self.routes[_page.route].append(_page)

    def render(self) -> None:
        """Writes page markup to file"""
        for page_route, pages in self.routes.items():
            output_path = self.output_path / page_route
            output_path.mkdir(exist_ok=True)

            for page in pages:
                page.render(engine=self.engine, path=output_path, **{**vars(page), **vars(self)})
            
#        _render_sitemap(self.routes, output_path=self.output_path, SITE_URL=self.SITE_URL,)


    def _render_subcollections(self):
        """Generate subcollection pages to be added to routes"""
        for collection in self.collections.values():

            if collection.subcollections:

                for subcollection_group in collection.get_subcollections():
                    _subcollection_group = collection.get_subcollections()[
                        subcollection_group
                    ]
                    sorted_group = sorted(
                        _subcollection_group,
                        key=lambda x: (len(x.pages), x.title),
                        reverse=True,
                    )

                    for subcollection in sorted_group:

                        # Check for subcollection_min
                        subc_min = getattr(self, "SUBCOLLECTION_MIN", 2)

                        if len(subcollection.pages) < subc_min:
                            continue

                        for archive in subcollection.archive:
                            self.routes.append(archive)