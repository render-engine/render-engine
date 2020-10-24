from copy import copy
from progress.bar import Bar
import itertools
import inspect
import logging
import os
import shutil
import typing
import pendulum
from pathlib import Path
from slugify import slugify


import more_itertools

from ._type_hint_helpers import PathString
from .collection import Collection
from .engine import Engine
from .feeds import RSSFeedEngine
from .links import Link
from .page import Page
from . import search


class Site:
    """
    The site stores your pages and collections to be rendered.

    Pages are stored and created with `site.render()`.
    Collections are stored to be used for future use.
    Sites also contain global variables that can be applied in templates.

    Attributes:
        routes (list):
            storage of registered_routes
        collections (dict):
            storage of registered collections
        output_path (str or pathlib.Path):
            the path to directory which all rendered html pages will be stored.
            default `./output`
        static_path (str or pathlib.Path):
            the path to directory for static content. This will be copied over
            into the `output_path`
        SITE_TITLE (str):
            configuration variable title of the site. This is only used in your
            environment template variables. While Optional you will be warned
            if you do not supply a new variable. default: 'Untitled Site'
        SITE_URL (str):
            configuration variable url of the of the site. While Optional you will be
            warned if you do not supply a new variable. default: 'Untitled Site'
            default 'https://example.com'

    Todo:
        - remove SITE_LINK
        - make SITE_URL accesible as a Page variable and allow for switch for
            Relative and Absolute URLS
    """

    routes: typing.List[Page] = []
    output_path: Path = Path("output")
    static_path: Path = Path("static")
    SITE_TITLE: str = "Untitled Site"
    SITE_URL: str = "https://example.com"
    strict: bool = False
    default_engine: typing.Type[Engine] = Engine()
    rss_engine: typing.Type[Engine] = RSSFeedEngine()
    search: typing.Optional[str] = None
    search_params: typing.List[str] = {}
    search_client = None
    timezone: str = ""

    def __init__(self):
        """Clean Directory and Prepare Output Directory"""

        self.collections = {}
        self.subcollections = {}
        self.output_path = Path(self.output_path)

        # strict deletes the directory and rebuilds it from scratch
        if self.output_path.exists() and not self.output_path.is_dir():
            raise ValueError("output path cannot point to an existing file")

        # sets the timezone environment variable to the local timezone if not present
        os.environ["render_engine_timezone"] = (
            self.timezone or pendulum.local_timezone().name
        )

    def register_collection(self, collection_cls: typing.Type[Collection]) -> None:
        """
        Add a class to your `self.collections`
        iterate through a classes `content_path` and create a classes
        `Page`-like objects, adding each one to `routes`.

        Use a decorator for your defined classes.

        Examples:
            ```
            @register_collection
            class Foo(Collection):
                pass
            ```

        Args:
            collection_cls (Collection):
                Collection to parse
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

    def register_feed(self, feed, collection: Collection) -> None:
        """Create a Page object that is an RSS feed and add it to self.routes

        Parameters
        ----------
        feed: RSSFeedEngine
            the type of feed to generate
        collection: Collection
            the collection to

        Returns
        -------
        None
        """

        extension = self.rss_engine.extension
        _feed = feed
        _feed.slug = collection.slug
        _feed.title = f"{self.SITE_TITLE} - {_feed.title}"
        _feed.link = f"{self.SITE_URL}/{_feed.slug}{extension}"
        self.routes.append(_feed)

    def register_route(self, cls) -> None:
        route = cls()
        self.routes.append(route)

    def _remove_output_path(self):
        if self.output_path.exists():
            return shutil.rmtree(self.output_path)

    def _render_output(self, page):
        """Writes the page to a file"""
        engine = page.engine if page.engine else self.default_engine
        template_attrs = self.get_public_attributes(page)
        content = engine.render(page, **template_attrs)
        route = self.output_path.joinpath(page.routes[0].strip("/"))
        route.mkdir(exist_ok=True)
        filename = Path(page.slug).with_suffix(engine.extension)
        filepath = route.joinpath(filename)
        filepath.write_text(content)
        route_count = len(page.routes)

        if route_count > 1:

            # create a directory and path for each alternate route
            for new_route in page.routes[1:]:
                new_route = self.output_path.joinpath(new_route.strip("/"))
                new_route.mkdir(exist_ok=True)
                new_filepath = new_route.joinpath(filename)
                shutil.copy(filepath, new_filepath)

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

                        self.subcollections[subcollection_group] = sorted_group

                        for archive in subcollection.archive:
                            self.routes.append(archive)

    def render(self, dry_run: bool = False, strict: bool = False) -> None:
        # removes the output path is strict is set
        if self.strict or strict:
            self._remove_output_path

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
        page_count = len(self.routes)

        with Bar(
            f"Rendering {page_count} Pages",
            max=page_count,
            suffix="%(percent).1f%% - %(elapsed_td)s",
        ) as bar:

            for page in self.routes:
                suffix = "%(percent).1f%% - %(elapsed_td)s"
                bar.suffix = suffix + f" ({page.title})"

                self._render_output(page)

                bar.next()

        if self.search:
            search_fields = {
                "title": {
                    "type": "text",
                },
                "content": {
                    "type": "text",
                },
                "slug": {
                    "type": "text",
                },
                "date_published": {
                    "type": "date",
                },
                "date_modified": {
                    "type": "date",
                },
                "tags": {
                    "type": "text",
                    "default": [""],
                },
                "category": {
                    "type": "keyword",
                },
            }
            self.search_params["id_fields"] = ["slug", "date_created"]
            self.search_params["fields"] = search_fields
            self.search_params['site_url'] = self.SITE_URL
            filtered_routes = itertools.filterfalse(lambda x: x.no_index, self.routes)
            self.search(
                search_client=self.search_client,
                pages=filtered_routes,
                **self.search_params,
            )

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
