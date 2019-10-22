from .page import Page
from .engine import Engine

from typing import Type


class Route:
    def __init__(self, page: Type[Page], engine: str=''):
        self.page = page
        self.engine = engine
