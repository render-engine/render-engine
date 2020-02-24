from typing import List, Any
from dataclasses import dataclass

@dataclass
class Link:
    """An opinionated format to reference links. Great for creating headers"""
    name: str
    url: str
    links: list = List[Any]
    image: str = ''
