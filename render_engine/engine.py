from render_engine.collection import Collection
from render_engine.page import Page
from render_engine.paginate import write_paginated_pages
from render_engine.config_loader import load_config

from dataclasses import dataclass
from itertools import zip_longest
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from typing import Type, Optional, Union, TypeVar, Iterable

import logging
import json
import maya
import shutil
import yaml

# Currently all of the Configuration Information is saved to Default
logging.basicConfig(level=logging.DEBUG)

PathString = Union[str, Type[Path]]

class Engine:
    """This is the engine that is builds your static site.
    Use `Engine.run()` to output the files to the designated output path."""
    def __init__(
            self,
            *,
            site_url=None,
            template_path='./templates',
            config={},
            config_path=None,
            content_path='content',
            static_path='static',
            output_path='output',
            routes=[],
            **kwargs,
            ):

        # Check for configurations in config_path or kwargs
        if config_path:
            logging.info(f'{config_path} detected checking for engine variables')
            config.update(load_config(config_path, 'Engine'))
            logging.debug(f'config={config}')

        if 'Environment' not in config:
            config['Environment'] = {}

        config['Environment'].update(kwargs)


        # Create a new environment and set the global variables to the config
        # items called in environment variables
        self.env = Environment(
            loader=FileSystemLoader(template_path),
            autoescape=select_autoescape(['html', 'xml']),
            )

        if 'Environment' in config:
            logging.info(f'Environment section detected')
            logging.debug(config['Environment'])
            self.env.globals.update(config['Environment'])

        # These fields are called a lot. So we pull them from config. Also,
        # make it a path
        self.base_content_path = config.get('content_path', content_path)
        self.base_static_path = config.get('static_path', static_path)
        self.base_output_path= config.get('output_path', output_path)
        self.site_url = config.get('site_url', site_url)
        self.routes = routes
        logging.debug(f'base_content_path - {self.base_content_path}')
        logging.debug(f'base_output_path - {self.base_output_path}')
        logging.debug(f'base_static_path - {self.base_static_path}')
        logging.debug(f'site_url - {self.site_url}')
        logging.debug(f'routes - {self.routes}')

    def route(self, *routes, content_path=None, template=None, content_type=Page):
        """Used to get **kwargs for `add_route`"""
        def inner(func, routes=routes, content_path=content_path):
            kwargs = func() or {}

            for route in routes:
                self.routes.append(
                        content_type(
                            content_path=content_path,
                            url_root=self.site_url if self.site_url else './',
                            template=template,
                            slug=route.lstrip('/'),
                            **kwargs,
                            )
                        )

            return func

        return inner

    def build_collection(
            self,
            *routes,
            pages=None,
            template='page.html',
            content_path=None,
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
                    content_path=Path(self.base_content_path) \
                            .joinpath(content_path if content_path else './'),
                    pages=pages,
                    route=route,
                    paginate=paginate,
                    extension=extension,
                    url_root=self.site_url,
                    template=template,
                    **kwargs,
                    )

            self.routes.extend(iter(collection))

            if paginate:
                paginated_pages = write_paginated_pages(
                        name,
                        collection.paginate,
                        content_type=Page,
                        route=route,
                        )

                self.routes.extend(paginated_pages)

            if feeds:
                build_date = maya.now()
                rss_feed = Page(
                        template='feeds/rss/blog.rss',
                        route=name,
                        url_root=self.SITE_URL,
                        url_suffix='.rss',
                        content=collection.to_rss(engine=self),
                        name=self.FEED_TITLE,
                        description=self.FEED_DESCRIPTION,
                        build_date=build_date.rfc2822(),
                    copyright=f'Copyright ©️  {build_date.year} {self.COPYRIGHT}',
                    generator='https://github.com/kjaymiller/render-engine',
                    language='en-US',
                        items=iter(collection),
                        )

                self.routes.append(rss_feed)

                json_feed = Page(
                    template=None,
                    content=collection.to_json(engine=self),
                    route=name,
                    url_suffix='.json',
                    )

                self.routes.append(json_feed)

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
            shutil.copytree(self.base_static_path, static_output)

        except:
            pass


        for route in self.routes:
            # Get filename from route
            filename = Path(self.base_output_path +
                    str(route.url).split(self.base_content_path)[-1])
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
