import logging
import os
import shutil
import typing
from pathlib import Path

import click

from ._type_hint_helpers import PathString
from .collection import Collection
from .engine import Engine
from .feeds import RSSFeedEngine
from .page import Page
from .route import Route


class Site:
    routes: typing.List[str] = []
    collections = {}
    output_path: Path = Path("output")
    static_path: Path = Path("static")
    SITE_TITLE: str = "Untitled Site"
    SITE_LINK: str = "https://example.com"

    def __init__(self, strict: bool = False):
        # Make Output Path if it doesn't Exist
        self.output_path = Path(self.output_path)

        if strict and self.output_path.is_dir():
            shutil.rmtree(self.output_path)

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
        collection = collection_cls()
        self.collections.update({collection.__class__.__name__: collection})

        for page in collection.pages:
            self.route(cls=page)

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
        for page in self.routes:
            engine = self.engines.get(page.engine, self.engines["default_engine"])
            content = engine.render(page, **vars(self))

            logging.debug(f'{engine=}')
            logging.debug(f'{content=}')

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

