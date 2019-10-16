class Site:
    def __init__(self), output_path:
      self.engines = {}
      self.routes = {}

      self.output_path  = output_path
    def register_engine(self, cls):
        self.engines[cls.__class__.__name__] = cls

    def register_collection(self, cls):
        for page in cls.pages:
            self.route(page)

    def route(self, cls):
        self.routes[filename] = cls

    def render_routes():
        for x, y in self.routes.items():
            engine = self.engines[y.engine]
            root_directory = self.output_path().joinpath(engine.output_path)
            filepath = root_directory.joinpath(engine.extension)
            filepath.write_text(y.content)
