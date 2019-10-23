import logging
import shutil
from pathlib import Path

from .engine import Engine
from .helpers import PathString
from .route import Route


class Site:
    default_engine = Engine()
    engines = {}
    routes = []

    def __init__(
        self,
        output_path: PathString = "output",
        static_path: PathString = "static",
        strict: bool = False,
    ):

        # Make Output Path if it doesn't Exist
        self.output_path = Path(output_path)

        if strict and self.output_path.is_dir():
            shutil.rmtree(self.output_path)

        self.output_path.mkdir(exist_ok=True)
        shutil.copytree(
            static_path, self.output_path.joinpath(static_path), dirs_exist_ok=True
        )

    def __setattr__(self, name, value):
        self.default_engine.environment.globals[name] = value
        object.__setattr__(self, name, value)

    def register_engine(self, cls):
        self.engines[cls.__class__.__name__] = cls

    def register_collection(self, cls):
        for page in cls().pages:
            page.routes = cls.routes
            self.route(cls=page)

    def route(self, cls):
        self.routes.append(cls)

    def register_route(self, cls):
        self.routes.append(cls())

    def get_engine(self, engine):
        if engine:
            return self.engines[engine]

        else:
            return self.default_engine

    def render(self, dry_run: bool = False):
        for page in self.routes:
            engine = self.get_engine(page.engine)
            content = engine.render(page)

            for route in page.routes:
                logging.debug(f"page - {page.__class__.__name__}")
                logging.debug(f"template - {page.template}")
                logging.debug(f"content - {content}")
                route = self.output_path.joinpath(route.strip("/"))
                route.mkdir(exist_ok=True)

                if not dry_run:
                    filename = Path(page.slug).with_suffix(engine.extension)
                    filepath = route.joinpath(filename)
                    filepath.write_text(content)
