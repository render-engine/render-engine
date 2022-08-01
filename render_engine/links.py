from dataclasses import dataclass, field


@dataclass
class Link:
    """
    An opinionated format to reference links. Great for creating links that you will pass into multiple page objects.

    Jinja will pass the string representation of the link to the template.

    .. code-block:: python

        link = Link(
                name="Render Engine",
                url="https://render-engine.site",
                meta={"class"="link-class", "id"="custom-link-id"}
                )

        # When rendered in a template, this will be:

        <a href="https://render-engine.site" class="link-class" id="custom-link-id">Render Engine</a>
    """

    text: str = field(default_factory=str)
    url: str = field(default="#")
    meta: dict[str, str] = field(default_factory=dict)
    """Meta variables translate to attributes on the html element"""

    def __str__(self):
        if self.meta:
            attrs = " ".join([f'{k}="{v}"' for k, v in self.meta.items()])
            starting_path = f'<a href="{self.url}" {attrs}>'

        else:
            starting_path = f'<a href="{self.url}">'

        return f"{starting_path}{self.text}</a>"


@dataclass
class Image(Link):
    """
    Link object formatted as an image

    .. code-block:: python

        myImage = Link(
            text="Render Engine",
            url="https://render-engine.site",
            meta={"class"="link-class", "id"="custom-link-id"}
            )

        # When rendered in a template

        <img src="https://render-engine.site" alt="example image" id="custom-link-id" class="link-class" />
    """

    def __str__(self):
        """prints the image point"""

        if self.meta:
            attrs = " ".join([f'{k}="{v}"' for k, v in self.meta.items()])
            return f'<img src="{self.url}" alt="{self.text}" {attrs} />'

        else:
            return f'<img src="{self.url}" alt="{self.text}" />'
