import logging
import os
import shutil
import typing
from pathlib import Path

from ._type_hint_helpers import PathString
from .collection import Collection
from .engine import Engine
from .route import Route

logging.basicConfig(level=logging.INFO)


class Site:
    default_engine: typing.Type[Engine] = Engine()
    engines: typing.Dict[str, typing.Type[Engine]] = {}
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

    def __setattr__(self, name, value) -> None:
        object.__setattr__(self, name, value)
        self.default_engine.environment.globals[name] = value

    def register_engine(self, cls: Engine) -> None:
        self.engines[cls.__class__.__name__] = cls

    def register_collection(self, collection_cls: typing.Type[Collection]) -> None:
        for page in collection_cls().pages:
            self.route(cls=page)

    def route(self, cls) -> None:
        self.routes.append(cls)

    def register_route(self, cls) -> None:
        self.routes.append(cls())

    def get_engine(self, engine) -> typing.Type[Engine]:
        if engine:
            return self.engines[engine]

        else:
            return self.default_engine

    def render(self, dry_run: bool = False) -> None:
        for page in self.routes:
            logging.debug(page.__class__.__name__)
            engine = self.get_engine(page.engine)
            content = engine.render(page)

            logging.debug(f"building {page.routes=}")
            for route in page.routes:
                route = self.output_path.joinpath(route.strip("/"))
                route.mkdir(exist_ok=True)

                if not dry_run:
                    filename = Path(page.slug).with_suffix(engine.extension)
                    filepath = route.joinpath(filename)
                    filepath.write_text(content)
