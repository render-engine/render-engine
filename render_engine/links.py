import typing
from dataclasses import dataclass, field



@dataclass
class Link:
    """
    An opinionated format to reference links. Great for creating headers

    Look at the example::

        myImage = Link(
            name="Render Engine",
            url="https://render-engine.site"
            alt="example image"
            )


    In this case the name and url give you enough information that you can supply to your template::

        <a href="{{myImage.url}}">{{myImage.text}}</a>

    Any attribute could be applied but here are some that you can supply on initialization.
    """

    text: str = field(kw_only=True, default_factory=str)
    url: str = field(kw_only=True, default="#")
    meta: dict[str, str] = field(default_factory=dict)
    
    def __str__(self):
        """href is the common """

        if self.meta:
            attrs = " ".join([f'{k}="{v}"' for k,v in self.meta.items()])
            starting_path = f'<a href="{self.url}" {attrs}>'
        
        else:
            starting_path = f'<a href="{self.url}">'

        return f'{starting_path}{self.text}</a>'
        

@dataclass
class Image(Link):
    """
    Link object formatted as an image

    Look at the example::

        myImage = Link(
            name="Render Engine",
            url="https://render-engine.site"
            alt="example image"
            )


    In this case the name and url give you enough information that you can supply to your template::

        <a href="{{myImage.url}}">{{myImage.text}}</a>

    Any attribute could be applied but here are some that you can supply on initialization.
    """

    def __str__(self):
        """prints the image point"""

        if self.meta:
            attrs = " ".join([f'{k}="{v}"' for k,v in self.meta.items()])
            return f'<img src="{self.url}" alt="{self.text}" {attrs} />'
        
        else:
            return f'<img src="{self.url}" alt="{self.text}" />'