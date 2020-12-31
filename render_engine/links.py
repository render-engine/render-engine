from dataclasses import dataclass
from typing import Any, List


@dataclass
class Link:
    """
    An opinionated format to reference links. Great for creating headers
    """

    name: str
    url: str
    links: List = List[Any]
    image: str = ""
    icon: str = ""
