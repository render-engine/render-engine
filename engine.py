from .base_config import config
from dataclasses import dataclass
from itertools import zip_longest
from pathlib import Path
from .page import Page
from typing import Type, Optional, Union, TypeVar, Iterable
import shutil

# Currently all of the Configuration Information is saved to Default
config = config['DEFAULT']
content_path='content'
output_path='output'
static_path='static'

PathString = Union[str, Type[Path]]

def paginate(iterable: any,
        items_per_page: int,
        *,
        fillvalue=None,
        ):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * items_per_page
    return zip_longest(*args, fillvalue=fillvalue)


def write_paginated_pages(name, pagination, *, route, template='blog.html'):
    p_routes = []
    for block in enumerate(pagination):
        block_route = f'{route}/{name}_{block[0]}' # blog_0, blog_1, etc
        r = add_route(
                    Page,
                    template='archive.html',
                    route=block_route,
                    post_list=[x.content for x in list(filter(lambda x:x, block[1]))],
                    )
        p_routes.append(r)

        return p_routes


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

@dataclass
class Route:
    content_path: Path
    content: Page

class Engine:
    """This is the engine that is builds your static site.
    Use `Engine.run()` to output the files to the designated output path."""
    content_path = Path(content_path)
    output_path = Path(output_path)
    static_path = Path(static_path)
    routes_items = []

    def build(self, content_type, *, template, routes, base_file=None):
        """Used to get **kwargs for `add_route`"""
        def inner(func, routes=routes):
            kwargs = func() or {}

            if isinstance(routes, str):
                routes = routes.split(',')

            for route in routes:

                r = add_route(
                    content_type,
                    route=route,
                    template=template,
                    **kwargs,
                    )
                self.routes_items.append(r)

            return func

        return inner

    def add_collection(
            self,
            content_type: Type[Page],
            *,
            template: PathString,
            content_path: PathString,
            routes: Iterable[PathString]=[Path('./')],
            extension: str='.md',
            archive: bool=False,
            name: str='',
            **kwargs,
            ):
        """Iterate through the provided content path building the desired
        content_type and storing in routes to be created on run"""
        content_path = Path(content_path)
        collection_files = content_path.glob(f'*{extension}')

        routes = map(lambda route: Path(route), routes)

        collection_routes = []
        for route in routes:
            # collect first
            for collection_item in collection_files:
                r = Path(route).joinpath(collection_item.stem)
                file_route=add_route(
                            content_type,
                            template=template,
                            route=r,
                            base_file=collection_item,
                            ),
                collection_routes.extend(file_route)
            print(collection_routes)

            if archive:
                pages = paginate(collection_routes, 10)
                self.routes_items.extend(
                    write_paginated_pages(
                        name,
                        pages,
                        route=route,
                        ),
                     )

        self.routes_items += collection_routes

    def run(self, overwrite=True):
        """Builds the Site Objects
        1. Generate Static Pages
        2. Generate Collections
        3. Generate Custom Pages

        TODO: Add Skips to ByPass Certain Steps
        """
        static_output = f"{self.output_path}/{self.static_path}"

        # If overwrite AND THE FILE EXISTS, then remove the entire folder
        if all((overwrite, Path(self.output_path).exists())):
            shutil.rmtree(self.output_path)
            Path(self.output_path).mkdir() # Creates the new folder

        # Instead of trying to analyze the static folder. Just delete the
        # contents
        try:
            shutil.rmtree(static_output)
        except:
            pass

        shutil.copytree(
            self.static_path,
            static_output,
            )

        print(self.routes_items)
        for route in self.routes_items:
            filename = Path(f'{self.output_path}/{route.content_path}.html').resolve()
            base_dir = filename.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                    )

            if filename.exists():
                with filename.open() as f:
                    if f.read() == route.content:
                        continue

                    else:
                        filename.unlink()

            with filename.open('w') as f:
                f.write(route.content.html)
