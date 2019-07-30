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
    def __init__(self, template_path='./templates', config={}, **kwargs):
        if config:
            config = yaml.safe_load(Path(config).read_text())

        config.update(kwargs)

        for key, attr in config.items():
            setattr(self, key, attr)

        # Create a new environment and set the global variables to the config
        # items
        self.env = Environment(
            loader=FileSystemLoader(template_path),
            autoescape=select_autoescape(['html', 'xml']),
            )

        # These fields are called a lot. So we pull them from config. Also,
        # make it a path
        self.base_content_path = config.get('content_path', 'content')
        self.base_output_path = config.get('output_path', 'output/')
        self.base_static_path = config.get('static_path', 'static')
        self.base_url = config['SITE_URL']
        self.routes_items = []
        self.env.globals = self.__dict__

    def build(self, *, routes, content_path=None, template=None, content_type=Page):
        """Used to get **kwargs for `add_route`"""
        def inner(func, content_path=content_path, routes=routes):
            kwargs = func() or {}

            if isinstance(routes, str):
                routes = routes.split(',')

            for route in routes:
                if content_path:
                    content_path=joinpath(Path(content_path))

                self.routes_items.append(
                        content_type(
                            content_path=content_path,
                            url_root=self.SITE_URL,
                            template=template,
                            route=route,
                            **kwargs,
                            )
                        )

            return func

        return inner

    def build_collection(
            self,
            *,
            template,
            routes,
            content_path,
            feeds=False,
            paginate=False,
            extension='.md',
            name=None,
            content_type=Page,
            **kwargs,
            ):
        """creates a collection of objects"""
        for route in routes:
            collection = Collection(
                    name=name,
                    content_path=content_path,
                    route=route,
                    paginate=paginate,
                    extension=extension,
                    url_root=self.SITE_URL,
                    template=template,
                    **kwargs,
                    )

            self.routes_items.extend(iter(collection))

            if paginate:
                paginated_pages = write_paginated_pages(
                        name,
                        collection.paginate,
                        content_type=Page,
                        route=route,
                        )

                self.routes_items.extend(paginated_pages)

            if feeds:
                rss_feed = Page(
                        template='feeds/rss/blog.rss',
                        route=name,
                        url_suffix='.rss',
                        content=collection.to_rss(engine=self),
                        )

                self.routes_items.append(rss_feed)

                json_feed = Page(
                    template=None,
                    content=collection.to_json(engine=self),
                    route=name,
                    url_suffix='.json',
                    )

                self.routes_items.append(json_feed)

    def run(self, overwrite=True):
        """Builds the Site Objects
        1. Generate Static Pages
        2. Generate Collections
        3. Generate Custom Pages

        TODO: Add Skips to ByPass Certain Steps
        """
        static_output = f"{self.base_output_path}/{self.base_static_path}"

        # If overwrite AND THE FILE EXISTS, then remove the entire folder
        if all((overwrite, Path(self.base_output_path).exists())):
            shutil.rmtree(self.base_output_path)
            Path(self.base_output_path).mkdir() # Creates the new folder

        # Instead of trying to analyze the static folder. Just delete the
        # contents
        try:
            shutil.rmtree(static_output)
        except:
            pass

        shutil.copytree(self.base_static_path, static_output)

        for route in self.routes_items:
            # Get filename from route
            filename = Path(self.base_output_path +
                    str(route.route).split(self.base_content_path)[-1])
            base_dir = Path(filename).parent.mkdir(
                    parents=True,
                    exist_ok=True,
                    )

            if filename.exists():
                if filename.read_text == route.content:
                    continue

                else:
                    filename.unlink()

            if route.template:
                template = self.env.get_template(route.template)
                params = dict(route.__dict__)
                content = template.render(**params)

            else:
                content = route.content

            filename.write_text(content)
