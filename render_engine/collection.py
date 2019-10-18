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
        content_path: PathString,
        content_type: Type[Page],
        engine: Optional[str] = None,
        glob: Sequence = ['.md', '.html']
        ):
        """initialize a collection object"""
        self.content_path = content_path
        self.content_type = content_type

    @property
    def pages(self):
        return (
                content_type(content_path=p) for p in for i in content_path.glob('i')
                )
