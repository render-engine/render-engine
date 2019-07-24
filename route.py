from typing import Type, Optional
from dataclasses import dataclass

@dataclass
class Route:
    content_path: Path
    content: any=Page
    template: Path="page.html"
    raw_content: bool=False

def add_route(
            content_type: Type[Page],
            *,
            template: str='page.html',
            route: str='',
            base_file: Optional[str]=None,
            **kwargs,
            ):
        """Used to Create the HTML that will be added to Routes. Usually not
        called on it's own."""

        content = content_type(
                template=template,
                base_file=base_file,
                **kwargs,
                )

        if content.id:
            route.joinpath(content.id)

        return Route(content_path=route, content=content)

