with .render_engine import Page, Engine

from typingi import Type


class Route:
    def __init__(self, Page: Type[Page], Engine: Type[Engine]):
        self.Page = Page
        self.Engine = Engine
