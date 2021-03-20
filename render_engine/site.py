import inspect
import itertools
import os
import shutil
import typing
from pathlib import Path

import pendulum
from progress.bar import Bar

from .collection import Collection
from .engine import Engine
from .feeds import RSSFeedEngine
from .page import Page
from .parsers._content_hash import _hash_content


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

    strict: bool = False
    """Force all pages to be rebuilt"""

    default_engine: typing.Type[Engine] = Engine()
    """``Engine`` to generate web pages"""

    rss_engine: typing.Type[RSSFeedEngine] = RSSFeedEngine()
    """``Engine`` to generate RSS Feeds"""

    cache_file: Path = Path(".routes_cache")
    """File that hash id's will be stored.

    The ``cache_file`` is checked for values to determine if new pages should be written
    """

    def __init__(self):
        """Clean Directory and Prepare Output Directory"""

        self.routes: typing.List[str] = []
        self.collections: typing.Dict[str, typing.List[str]] = {}
        self.subcollections: typing.Dict[str, typing.List[str]] = {}
        self.output_path: Path = Path(self.output_path)

        if self.cache_file.exists():
            self.hashes: typing.Set[str] = set(
                self.cache_file.read_text().splitlines(True)
            )
        else:
            self.hashes: typing.Set[str] = set()

    def register_collection(self, collection_cls: typing.Type[Collection]) -> None:
        """Add a class to your ``self.collections``
        iterate through a classes ``content_path`` and create a classes ``Page``-like
        objects, adding each one to ``routes``.

        Use a decorator for your defined classes.

        Examples::

            @register_collection
            class Foo(Collection):
                pass
        """

        collection = collection_cls()
        self.collections.update({collection.title: collection})

        for page in collection.pages:
            self.routes.append(page)

        if collection.has_archive:

            for archive in collection.archive:
                self.routes.append(archive)

        if collection.feeds:

            for feed in collection.feeds:
                self.register_feed(feed=feed, collection=collection)

    def _is_unique(self, filepath: Path, page: Page) -> bool:
        """Checks content if changes are present"""
        if page.always_refresh:
            return True

        if not filepath.exists():
            return True

        return _hash_content(page) not in self.hashes

    def register_feed(self, feed: RSSFeedEngine, collection: Collection) -> None:
        """Create a Page object that is an RSS feed and add it to self.routes"""

        extension = self.rss_engine.extension
        _feed = feed
        _feed.slug = collection.slug
        _feed.title = f"{self.SITE_TITLE} - {_feed.title}"
        _feed.link = f"{self.SITE_URL}/{_feed.slug}{extension}"
        self.routes.append(_feed)

    def register_route(self, cls: Page) -> None:
        """Create a Page object and add it to self.routes"""
        route = cls()
        self.routes.append(route)

    def _render_output(self, page: Page) -> None:
        """Writes page markup to file"""
        engine = page.engine if getattr(page, "engine", None) else self.default_engine
        route = self.output_path.joinpath(page.routes[0].strip("/"))
        route.mkdir(exist_ok=True)
        filename = Path(page.slug).with_suffix(engine.extension)
        filepath = route.joinpath(filename)
        unique_file = self._is_unique(filepath, page)

        if unique_file:
            template_attrs = self.get_public_attributes(page)
            content = engine.render(page, **template_attrs)

            if not page.always_refresh:
                self.hashes.add(_hash_content(page))
            filepath.write_text(content)

            if len(page.routes) > 1:
                for new_route in page.routes[1:]:
                    new_route = self.output_path.joinpath(new_route.strip("/"))
                    new_route.mkdir(exist_ok=True)
                    new_filepath = new_route.joinpath(filename)
                    shutil.copy(filepath, new_filepath)
            return f"{filename} written"

        else:
            return f"{filename} skipped"

    def _render_subcollections(self):
        """Generate subcollection pages to be added to routes"""
        for _, collection in self.collections.items():

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

    def render(
        self, verbose: bool = False, dry_run: bool = False, strict: bool = False
    ) -> None:
        if dry_run:
            strict = False
            verbose = True

        # removes the output path is strict is set
        if self.strict or strict:

            if self.output_path.exists():
                shutil.rmtree(self.output_path)
            self.hashes = set()

        # create an output_path if it doesn't exist
        self.output_path.mkdir(exist_ok=True)

        # copy a defined static path into output path
        if Path(self.static_path).is_dir():
            shutil.copytree(
                self.static_path,
                self.output_path.joinpath(self.static_path),
                dirs_exist_ok=True,
            )

        # render registered subcollections
        self._render_subcollections()

        if verbose:
            page_count = len(self.routes)
            with Bar(
                f"Rendering {page_count} Pages",
                max=page_count,
                suffix="%(percent).1f%% - %(elapsed_td)s",
            ) as bar:

                for page in self.routes:
                    suffix = "%(percent).1f%% - %(elapsed_td)s "
                    msg = self._render_output(page)
                    bar.suffix = suffix + msg
                    bar.next()
        else:
            for page in self.routes:
                self._render_output(page)

        with open(self.cache_file, "w") as f:
            f.write("".join([x for x in self.hashes]))

    def get_public_attributes(self, cls):
        site_filtered_attrs = itertools.filterfalse(
            lambda x: x[0].startswith("__"), inspect.getmembers(self)
        )
        site_dict = {x: y for x, y in site_filtered_attrs}

        cls_filtered_attrs = itertools.filterfalse(
            lambda x: x[0].startswith("__"), inspect.getmembers(cls)
        )

        cls_dict = {x: y for x, y in cls_filtered_attrs}

        return {**site_dict, **cls_dict}
