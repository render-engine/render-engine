from .base_config import config
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

def paginate(iterable, items_per_page, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * items_per_page
    iterable = zip_longest(*args, fillvalue=fillvalue)
    return iterable


def write_paginated_pages(name, pagination, *, route, **kwargs):
    paginated_pages = []
    for block in enumerate(pagination):
        r = add_route(
                    Page,
                    template='archive.html',
                    route=route,
                    post_list=[b for b in block[1] if b],
                    **kwargs,
                    ),
        return {f'{name}_{block[0]}': r}
        write_page(f'{path}/{name}_{block[0]}.html', render)

def add_route(
            content_type: Type[Page],
            *,
            template: str,
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

        return {route: content}

class Engine:
    """This is the engine that is builds your static site.
    Use `Engine.run()` to output the files to the designated output path."""
    content_path = Path(content_path)
    output_path = Path(output_path)
    static_path = Path(static_path)
    routes_items = dict()

    def build(self, content_type, *, template, routes, base_file=None):
        """Used to get **kwargs for `add_route`"""
        def inner(func, routes=routes):
            kwargs = func() or {}

            if isinstance(routes, str):
                routes = routes.split(',')

            for route in routes:
                self.routes_items.update(add_route(
                    content_type,
                    route=route,
                    template=template,
                    **kwargs,
                    ))

            return func

        return inner

    def add_collection(
            self,
            content_type: Type[Page],
            *,
            template: PathString,
            content_path: PathString,
            routes: Iterable[PathString]=['./'],
            extension: str='.md',
            archive: bool=True,
            name: str='',
            **kwargs,
            ):
        """Iterate through the provided content path building the desired
        content_type and storing in routes to be created on run"""
        content_path = Path(content_path)
        collection_files = list(content_path.glob(f'*{extension}'))
        route_items = []

        if isinstance(routes, str):
            routes = routes.split(',')

        for route in routes:
            if archive:
                pages = paginate(collection_files, 10)
                self.routes_items.update(
                        write_pagingated_pages(name, pages, route=route),
                        )

            for collection_item in collection_files:
                r = Path(route).joinpath(collection_item.stem)
                route_item = add_route(
                        content_type,
                        template=template,
                        route=r,
                        base_file=collection_item,
                        **kwargs,
                        )

                self.routes_items.update(route_item)

    def run(self, overwrite=True):
        """Builds the Site Objects
        1. Generate Static Pages
        2. Generate Collections
        3. Generate Custom Pages

        TODO: Add Skips to ByPass Certain Steps
        """
        print(self.routes_items)
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

        for path, content in self.routes_items.items():
            filename = Path(f'{self.output_path}/{path}.html').resolve()
            base_dir = filename.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                    )

            if filename.exists():
                with filename.open() as f:
                    if f.read() == content:
                        continue

                    else:
                        filename.unlink()

            with filename.open('w') as f:
                f.write(content.html)
