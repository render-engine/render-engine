from dataclasses import dataclass, field


@dataclass
class Link:
    """
    An opinionated format to reference links. Great for creating links that you will pass into multiple page objects.

    Jinja will pass the string representation of the link to the template.

    Attributes:
        text (str): The text to be displayed for the link.
        url (str, optional): The URL that the link points to. Defaults to "#".
        meta (dict[str, str], optional): Meta variables that translate to attributes on the HTML element.
            Defaults to an empty dictionary.

    Returns:
        str: The string representation of the link.

    Examples:
        link = Link(
            text="Render Engine",
            url="https://render-engine.site",
            meta={"class": "link-class", "id": "custom-link-id"}
        )

        # When rendered in a template, this will be:
        # <a href="https://render-engine.site" class="link-class" id="custom-link-id">Render Engine</a>
    """

    text: str = field(default_factory=str)
    url: str = field(default="#")
    meta: dict[str, str] = field(default_factory=dict)

    def __str__(self) -> str:
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

    Attributes:
        text (str): The text to be displayed as the image's alternative text.
        url (str): The URL of the image.
        meta (dict, optional): Additional attributes to be added to the image tag.

    Example:
        The following example demonstrates how to create an Image object and render it in a template:

        ```python
        myImage = Link(
            text="Render Engine",
            url="https://render-engine.site",
            meta={"class"="link-class", "id"="custom-link-id"}
        )

        # When rendered in a template

        <img src="https://render-engine.site" alt="Render Engine" id="custom-link-id" class="link-class" />
        ```
    """

    def __str__(self) -> str:
        """Returns the HTML representation of the Image object."""
        if self.meta:
            attrs = " ".join([f'{k}="{v}"' for k, v in self.meta.items()])
            return f'<img src="{self.url}" alt="{self.text}" {attrs} />'
        else:
            return f'<img src="{self.url}" alt="{self.text}" />'
