import logging
import os
import shutil
import typing
from pathlib import Path

from ._type_hint_helpers import PathString
from .collection import Collection
from .engine import Engine
from .feeds import RSSFeedEngine
from .page import Page


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

    routes: typing.List[str] = []
    collections = {}
    output_path: Path = Path("output")
    static_path: Path = Path("static")
    SITE_TITLE: str = "Untitled Site"
    SITE_LINK: str = "https://example.com"
    SITE_URL: str = "https://example.com"

    def __init__(self, strict: bool = False):
        """
        Clean Directory and Prepare Output Directory

        Parameters:
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
            strict (bool):
        """

        # Make Output Path if it doesn't Exist
        self.output_path = Path(self.output_path)

        # strict deletes the directory and rebuilds it from scratch
        if strict and self.output_path.is_dir():
            shutil.rmtree(self.output_path)

        # copy a defined static path into output path
        if Path(self.static_path).is_dir():
            self.output_path.mkdir(exist_ok=True)
            shutil.copytree(
                self.static_path,
                self.output_path.joinpath(self.static_path),
                dirs_exist_ok=True,
            )

        self.engines: typing.Dict[str, typing.Type[Engine]] = {
                "default_engine": Engine(),
                "rss_engine": RSSFeedEngine(),
        }

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
        self.collections.update({collection.__class__.__name__: collection})

        for page in collection.pages:
            print(page.template)
            self.route(cls=page)

        for subcollection in collection.subcollections:
            logging.debug(f'{subcollection=}')
            subc = collection.subcollect(subcollection)

            for x in subc:
                sb = Collection()
                sb.content_items = x.items
                sb.title = x.title
                sb._archive_slug = f'all_{x.title}'
                sb.has_archive = True
                self.route(cls=sb.archive)

        if collection.has_archive:
            self.route(cls=collection.archive)

            for feed in collection.feeds:

                if feed:
                    self.register_feed(feed=feed, collection=collection)

    def register_feed(self, feed, collection: Collection) -> None:
        _feed = feed()
        _feed.slug = ''.join([collection.__class__.__name__.lower(), _feed.slug])
        _feed.items = [page.rss_feed_item for page in collection.pages]
        _feed.title = ' - '.join([self.SITE_TITLE, _feed.title])
        _feed.link = ''.join([self.SITE_LINK, _feed.link])

        self.route(cls=_feed)


    def route(self, cls) -> None:
        self.routes.append(cls)

    def register_route(self, cls) -> None:
        self.routes.append(cls())


    def render(self, dry_run: bool = False) -> None:
        # check for errors
        if self.SITE_TITLE == "Untitle Site":
            logging.warning(f"No custom site title defined. Using the {SITE_TITLE=}")

        if self.SITE_URL == "https://example.com":
            logging.warning(f"No custom site URL defined. Using the {self.SITE_URL=}")

        for page in self.routes:
            engine = self.engines.get(page.engine, self.engines["default_engine"])
            content = engine.render(page, **vars(self))

            for route in page.routes:
                logging.info(f'starting on {route=}')
                route = self.output_path.joinpath(route.strip("/"))
                route.mkdir(exist_ok=True)
                filename = Path(page.slug).with_suffix(engine.extension)
                filepath = route.joinpath(filename)

                if not dry_run:
                    filepath.write_text(content)

                else:
                    print(f'{content} writes to {filepath}')
