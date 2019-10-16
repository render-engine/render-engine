import logging
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence, Type

from .helpers import PathString
from render_engine.page import Page


class Collection:
    def __init__(
        self,
        content_path: Optional[PathString] = None,
        pages: Optional[Sequence] = None,
        content_type: Type[Page] = Page,
    ):
        """initialize a collection object"""
        self.content_path = content_path
        self.pages = {}
        self.routes = self.__class__.__name__.lower()
        self.template_vars = {}

    @property
    def _pages(self):
        if self.pages:
            return self.pages

        else:
            return [p for p in self.content_path.iter_dir()]
