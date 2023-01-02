import json
from typing import Type

from .collection import Collection
from .parsers import JSONPageParser


class JSONCollection(Collection):
    Parser = JSONPageParser

    def __init__(self, content_path: str | None = None, content: str | None = None):
        if content_path:
            content = self.Parser.parse_content_path(content_path)

        super().__init__(content=content)

    @property
    def pages(self):
        for entry in json.dumps(self.content):
            yield self.gen_page(entry)
