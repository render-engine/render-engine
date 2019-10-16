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
        *,
        content_path: Optional[PathString] = None,
        pages: [Sequence] = {},
        **collection_attrs,
    ):
        """initialize a collection object"""
        if content_path and pages:
            error_msg = "Supply either content_path or pages. Not Both"
            raise AttributeError(error_msg)

        if content_path:
            self.content_path = Path(content_path)

    @property
    def _pages(self):
        if self.pages:
            return self.pages

        else:
            return [p for p in self.content_path.iter_dir()]
