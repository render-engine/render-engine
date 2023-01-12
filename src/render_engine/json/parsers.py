import json
import pathlib
from typing import Any, Type

import frontmatter
from markdown2 import markdown
from parsers.base_parsers import BasePageParser


class JSONPageParser(BasePageParser):
    @staticmethod
    def parse_content_path(content_path):
        """Fething content from a content_path and set attributes."""
        with open(content_path) as f:
            return json.load(f)

    @staticmethod
    def parse_content(content: str) -> tuple[dict[str, Any], str]:
        """Fething content and atttributes from a content_path"""

        attrs = json.loads(content)
        content = attrs.pop("content", None)

        return attrs, content
