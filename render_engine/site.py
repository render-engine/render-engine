import logging

from pathlib import Path
from .engine import Engine
from .route import Route
from .helpers import PathString

class Site:
    default_engine = Engine()

    def __init__(self, output_path: PathString="output", strict: bool=False):
        self.engines = {}
        self.routes = []
        self.output_path = Path(output_path)

        # Make Output Path if it doesn't Exist
        self.output_path.mkdir(exist_ok=True)

    def register_engine(self, cls):
        self.engines[cls.__class__.__name__] = cls

    def register_collection(self, cls):
        for page in cls().pages:
            page.routes = cls.routes
            self.register_route(cls=page)

    def register_route(self, cls):
        return self.routes.append(cls)

    def get_engine(self, engine):
        if engine:
            return self.engines[engine]

        else:
            return self.default_engine

    def render(self, dry_run: bool=False):
        for page in self.routes:
            engine = self.get_engine(page.engine)
            content = engine.render(page)

            for route in page.routes:
                route = self.output_path.joinpath(route.strip('/'))
                route.mkdir(exist_ok=True)

                if not dry_run:
                    filename = Path(page.slug).with_suffix(engine.extension)
                    filepath = route.joinpath(filename)
                    filepath.write_text(content)

