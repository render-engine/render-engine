from dataclasses import dataclass
from itertools import zip_longest
from pathlib import Path
from .page import Page
from .collection import Collection
from typing import Type, Optional, Union, TypeVar, Iterable
import json
import shutil

# Currently all of the Configuration Information is saved to Default
content_path='content'
output_path='output'
static_path='static'

PathString = Union[str, Type[Path]]


def write_paginated_pages(name, pagination, *, route, content_type=Page, **kwargs):
    p_routes = []
    for block in enumerate(pagination):
        block_route = f'{route}/{name}_{block[0]}'
        kwargs['post_list'] = [b for b in filter(lambda x:x, block[1])]

        r = add_route(
                    content_type,
                    template='archive.html',
                    route=block_route,
                    post_list=[x for x in list(filter(lambda x:x, block[1]))],
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
    content: any=Page
    raw_content: bool=False

class Engine:
    """This is the engine that is builds your static site.
    Use `Engine.run()` to output the files to the designated output path."""
    content_path = Path(content_path)
    output_path = Path(output_path)
    static_path = Path(static_path)
    routes_items = []

    def __init__(self, config='', **kwargs):
        if config:
            {self.config[x]:y for x,y in kwargs.items}

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

    def Collection(
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


        collection = Collection(
                name=name,
                content_type=content_type,
                content_path=content_path,
                )

        collection_routes = []

        for collection_item in collection.pages:
            for route in routes:
                r = Path(route).joinpath(collection_item.id)
                file_route=add_route(
                        content_type,
                        template=template,
                        route=r,
                        base_file=collection_item.base_file,
                        ),

                collection_routes += file_route

            if archive:
                pages = collection.paginate
                self.routes_items.extend(
                    write_paginated_pages(
                        name,
                        pages,
                        route=route,
                        ),
                     )

                rss_feed = collection.generate_rss_feed()
                json_feed = json.dumps(collection.generate_feed_metadata(), indent=2)
                feeds = [
                        Route(f'{name}.rss', rss_feed, True),
                        Route(f'{name}.json', json_feed, True),
                        ]

                self.routes_items += feeds

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

        for route in self.routes_items:
            if route.raw_content:
                filename = Path(f'{self.output_path}/{route.content_path}').resolve()
            else:
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
                if route.raw_content:
                    f.write(route.content)

                else:
                    f.write(route.content.html)
