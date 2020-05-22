from typing import List, Any
from dataclasses import dataclass

@dataclass
class Link:
    """
    An opinionated format to reference links. Great for creating headers

    Attributes
    ----------
    name : str
        the content of the link. 

    url : str
        the href that points to a webpage

    links : List[Any]
        Can be used to embed other link objects (userful for submenus)

    image : str, optional
        the source url for the image link

    icon : str, optional
        similar to image, but allows for custom html for icons
    """
    name: str
    url: str
    links: List = List[Any]
    image: str = ''
    icon: str = ''
