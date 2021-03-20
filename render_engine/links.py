import typing
from dataclasses import dataclass


@dataclass
class Link:
    """
    An opinionated format to reference links. Great for creating headers

    Look at the example::

        myImage = Link(
            name="Render Engine",
            url="https://render-engine.site"
            )


    In this case the name and url give you enough information that you can supply to your template::

        <a href="{{myImage.url}}">{{myImage.name}}</a>

    Any attribute could be applied but here are some that you can supply on initialization.
    """

    name: str
    url: str
    links: typing.Optional[typing.List[typing.Any]] = None
    image: str = ""
    icon: str = ""
    alt: str = ""
