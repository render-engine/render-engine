import logging
import os
import shutil
from pathlib import Path
from typing import Optional, Sequence, Type, TypeVar, Union

from jinja2 import Environment, FileSystemLoader, Markup, select_autoescape

from render_engine.collection import Collection
from render_engine.page import Page

# Currently all of the Configuration Information is saved to Default
logging.basicConfig(level=os.environ.get('LOGGING_LEVEL', logging.WARNING))

PathString = Union[str, Type[Path]]

class Engine:
    """This is the engine that is builds your static site.
    Use `Engine.run()` to output the files to the designated output path."""

    def __init__(
            self,
            output_path: PathString=Path('output'),
            static_path: PathString=Path('static'),
            #Jinja2.FileSystemLoader takes str or iterable not Path
            templates_path: str='templates',
            strict: bool=False,
            **env_variables,
            ):

        self.output_path = Path(output_path)
        if strict and self.output_path.is_dir():
            shutil.rmtree(self.output_path)

        self.output_path.mkdir(exist_ok=True)

        if Path(static_path).is_dir():
            output_static_path = self.output_path.joinpath(static_path)

            if output_static_path.exists():
                shutil.rmtree(output_static_path)
                shutil.copytree(src=static_path, dst=output_static_path)

        self.Environment = Environment(
               loader=FileSystemLoader(templates_path),
               autoescape=select_autoescape(['html', 'xml', 'rss']),
               )
        self.Environment.globals = env_variables

    def route(
            self,
            *routes,
            template=None,
            page_type=Page,
            extension='.html',
            ):
        """decorator that creates a page and writes it"""
        def inner(func, *args, **kwargs):
            logging.warning('inner-called')
            f = func(*args, **kwargs)
            return f

        if template:
            template = self.Environment.get_template(template)

        f = inner
        for routes in routes:
            page_obj = page_type(slug=slug)
            attrs = {}

            self.write(
                page=page_obj,
                extension=extension,
                markup=markup,
                template=template,
                )




    def collection(
            self,
            *routes,
            name,
            content_path,
            template=None,
            index_template=None,
            collection_type=Collection,
            extension='.html',
            ):
        """This iterates through the content_path and creates the page object
        for you"""

        def inner(func, *args, **kwargs):
            logging.warning('inner-called')

            f = func(*args, **kwargs)

            return f

        for route in routes:
            collection_object = collection_type(name=name,
                content_path=content_path)

        for page_obj in collection_object.pages:
            page_obj._slug = f'{route}/{page_obj.slug}'
            attrs = page_obj.__dict__
            page_obj.write(
                    extension=extension,
                    template=template,
                    **inner,
                    **attrs,
                    )

        if index_template:
            index_template = self.Environment.get_template(index_template)

        for iterator in collection_object._iterators:
            page_obj = Page(title=iterator.name)
            page_obj._slug = f'{route}/{page_obj.slug}'
            attrs = page_obj.__dict__
            page_obj.write(
                    extension=extension,
                    template=index_template,
                    **inner,
                    **attrs,
                    )
        return inner
