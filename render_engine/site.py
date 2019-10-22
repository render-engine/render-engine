from pathlib import Path
from .engine import Engine
from .route import Route

class Site:
    default_engine = Engine()

    def __init__(self, output_path="output"):
        self.engines = {}
        self.routes = {}
        self.output_path = Path(output_path)

    def register_engine(self, cls):
        self.engines[cls.__class__.__name__] = cls

    def register_collection(self, cls):
        for page in cls().pages:
            self.register_route(cls=page)

    def register_route(self, cls):
        output_path = self.output_path.joinpath(cls.__class__.__name__)
        self.routes[output_path] = cls

    def get_engine(self, engine):
        if engine:
            return self.engines[engine]

        else:
            return self.default_engine

    def render(self, dry_run: bool=False):
        for route, page in self.routes.items():
            engine = self.get_engine(page.engine)
            content = engine.render(page)

            if not dry_run:
                filepath = route.with_suffix(engine.extension)
                return filepath.write_text(content)
