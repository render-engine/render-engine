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

    def register_feed(self, feed, collection: Collection) -> None:
        feed.slug = ''.join([collection.__class__.__name__.lower(), feed.slug])
        feed.items = [page.rss_feed_item for page in collection.pages]
        feed.title = ' - '.join([self.SITE_TITLE, feed.title])
        feed.link = ''.join([self.SITE_LINK, feed.link])
        self.route(cls=feed)

    def register_collection(self, collection_cls: typing.Type[Collection]) -> None:
        collection = collection_cls()

        for page in collection.pages:
            self.route(cls=page)

        if collection.has_archive:
            self.route(cls=collection.archive)

            for _, feed in collection.feeds.items():
                if feed:
                    self.register_feed(feed=feed, collection=collection)

    def route(self, cls) -> None:
        self.routes.append(cls)

    def register_route(self, cls) -> None:
        self.routes.append(cls())

    def render(self, dry_run: bool = False) -> None:
        for page in self.routes:
            engine = self.engines.get(page.engine, self.engines["default_engine"])
            content = engine.render(page, **vars(self))

            for route in page.routes:
                route = self.output_path.joinpath(route.strip("/"))
                route.mkdir(exist_ok=True)

                if not dry_run:
                    filename = Path(page.slug).with_suffix(engine.extension)
                    filepath = route.joinpath(filename)
                    filepath.write_text(content)
