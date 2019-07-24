from .blog import BlogPost
from .collection import Collection
from .page import Page
from .paginate import write_paginated_pages

from dataclasses import dataclass
from itertools import zip_longest
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from typing import Type, Optional, Union, TypeVar, Iterable

import json
import shutil
import yaml

# Currently all of the Configuration Information is saved to Default

PathString = Union[str, Type[Path]]

class Engine:
    """This is the engine that is builds your static site.
    Use `Engine.run()` to output the files to the designated output path."""
    def __init__(self, config=None, **kwargs):
        if config:
            self.config = yaml.safe_load(Path(config).read_text())
            print(self.config)
        self.config.update(kwargs.copy())
        self.env = Environment(
            loader=FileSystemLoader(''),
            autoescape=select_autoescape(['html', 'xml']),
            )
        self.env.globals = self.config

        # These fields are called a lot. So we pull them from config. Also,
        # make it a path
        self.base_content_path = Path(self.config.get('content_path', ''))
        self.base_output_path = Path(self.config.get('output_path', ''))
        self.base_static_path = Path(self.config.get('static_path', ''))
        self.routes_items = []

    def build(self, content_type, *, template, routes, content_path=None):
        """Used to get **kwargs for `add_route`"""
        def inner(func, routes=routes):
            kwargs = func() or {}

            if isinstance(routes, str):
                routes = routes.split(',')

            for route in routes:
                content_path=self.base_content_path.joinpath(Path(content_path))
                output_path = self.base_output_path.joinpath(Path(route))
                self.routes_items.append(
                        content_type(
                            config=self.config,
                            content_path=content_path,
                            output_path=output_path,
                            **kwargs,
                            )
                        )

            return func

        return inner

    def build_collection(
            self,
            content_type,
            *,
            template,
            routes,
            content_path=('./'),
            feeds=False,
            paginate=False,
            extension='.md',
            name=None,
            **kwargs,
            ):
        """creates a collection of objects"""
        for route in routes:
            collection = Collection(
                    name=name,
                    content_type=content_type,
                    content_path=self.base_content_path.joinpath(content_path),
                    output_path=self.base_output_path.joinpath(route),
                    paginate=paginate,
                    extension=extension,
                    config=self.config,
                    **kwargs,
                    )

            for collection_item in collection:
                self.routes_items.append(r)

            if paginate:
                paginated_pages = write_paginated_pages(
                        name,
                        collection.paginate,
                        route=route,
                        )

                self.routes_items.extend(paginated_pages)

            if feeds:
                rss_feed = Page(
                        template=None,
                        output_path=f'{name}.rss',
                        content=collection.generate_rss_feed(),
                        )

                self.routes_items.append(rss_feed)

                json_feed = Page(
                    template=None,
                    content=json.dumps(
                        collection.generate_feed_metadata(),
                        indent=2),
                    output_path=f'{name}.json',
                    )

                self.routes_items.append(json_feed)

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

        shutil.copytree(self.static_path, static_output)

        for route in self.routes_items:
            template_path = self.template_path.joinpath(route.template)
            template = env.get(template_path, route)

            # Get filename from route
            if route.raw_content:
                filename = Path(f'{self.output_path}/{route.content_path}')
                content = route.content.content
            else:
                filename = Path(f'{self.output_path}/{route.content_path}.html')
                content = Markdown(route.content.content)

            filename = filename.resolve()

            base_dir = filename.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                    )

            if filename.exists():
                if filename.read_text == route.content:
                    continue

                else:
                    filename.unlink()

            if route.raw_content:
                content = route.content

            else:
                content = route.content.html

            filename.write_text == content
