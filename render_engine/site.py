import logging
import os
import shutil
import typing
from pathlib import Path

from ._type_hint_helpers import PathString
from .collection import Collection
from .engine import Engine
from .feeds import RSSFeedEngine
from .route import Route

default_engine = Engine()
archive_engine = RSSFeedEngine()


class Site:
    engines: typing.Dict[str, typing.Type[Engine]] = {
        "default_engine": default_engine,
        "archive_engine": archive_engine,
    }
    routes: typing.List[str] = []
    output_path: Path = Path("output")
    static_path: Path = Path("static")

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

    def register_engine(self, cls: Engine) -> None:
        self.engines[cls.__class__.__name__] = cls

    def register_collection(self, collection_cls: typing.Type[Collection]) -> None:
        collection = collection_cls()

        for page in collection.pages:
            self.route(cls=page)

        if collection.has_archive:
            self.route(cls=collection.archive)

    def route(self, cls) -> None:
        self.routes.append(cls)

    def register_route(self, cls) -> None:
        self.routes.append(cls())

    def get_engine(self, engine) -> typing.Type[Engine]:
        if engine:
            return self.engines[engine]

        else:
            return self.engines['default_engine']

    def render(self, dry_run: bool = False) -> None:
        for page in self.routes:
            engine = self.get_engine(page.engine)
            content = engine.render(page)

            for route in page.routes:
                route = self.output_path.joinpath(route.strip("/"))
                route.mkdir(exist_ok=True)

                if not dry_run:
                    filename = Path(page.slug).with_suffix(engine.extension)
                    filepath = route.joinpath(filename)
                    filepath.write_text(content)
