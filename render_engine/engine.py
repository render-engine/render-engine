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

    def render_template(self, template_name):
        def inner (f, *args, **kwargs):
            func = f(*args, **kwargs)
            attrs = func.__dict__
            template = self.Environment.get_template(template_name)
            render = template.render(content=func.markup, **attrs)
            self.output_path.joinpath(func.slug.lstrip('/')).write_text(render)
        return inner


    def collection(
            self,
            name,
            content_path,
            template=None,
            index_template=None,
            collection_type=Collection,
            extension='.html',
            **template_vars,
            ):
        """This iterates through the content_path and creates the page object
        for you"""

        def inner(func, *args, **kwargs):
            f = func(*args, **kwargs)
            f.update(**template_vars)
            return f

        for route in routes:
            collection_object = collection_type(name=name,
                content_path=content_path)

        for page_obj in collection_object.pages:
            page_obj._slug = f'{route}/{page_obj.slug}'
            self.write(
                    page_obj,
                    extension=extension,
                    template=template,
                    **f,
                    )

        if index_template:
            index_template = self.Environment.get_template(index_template)

        for iterator in collection_object._iterators:
            page_obj = Page(title=iterator.name)
            page_obj._slug = f'{route}/{page_obj.slug}'
            self.write(
                    page_obj,
                    extension=extension,
                    template=index_template,
                    **f,
                    )
        return inner


    def write(self, page, template, extension='.html', **template_vars):
        markup = page.markup

        if template:
            content = template.render(content=markup, **template_kwargs)

        else:
            content = markup

        filename = self.output_path.joinpath(
                Path(f'{self.slug}{extension}'.lstrip('/')))
        filename.mkdir(exist_ok=True)
        return filename.write_text(content)

