from pathlib import Path
from .render_engine import Engine

class Route():
    def __init__(self, cls, engine):
        self.cls = cls
        self.engine = engine

    def render(self):
            engine = self.engines
            self.output_path().joinpath(engine.output_path)
            filepath = root_directory.joinpath(engine.extension)
            filepath.write_text(y.content)

class Site:
    default_engine = Engine()

    def __init__(self, output_path="output"):
        self.engines = {}
        self.routes = {}
        self.output_path = Path(output_path)

    def register_engine(self, cls):
        self.engines[cls().__class__.__name__] = cls

    def register_collection(self, cls, engine=None):
        for page in cls()._pages:
            self.register_route(page, engine)

    def register_route(self, cls):
        self.routes[cls.filename] = Route(cls, get_engine())

    def get_engine(self):
      pass

    def render(self):
        for route in self.routes.values():
            route.render()

