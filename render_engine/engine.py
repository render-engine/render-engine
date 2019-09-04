from render_engine.collection import Collection, Page
from itertools import zip_longest
from jinja2 import Environment, FileSystemLoader, select_autoescape, Markup
from pathlib import Path
from typing import Type, Optional, Union, TypeVar, Sequence

import logging
import os
import shutil
import yaml

# Currently all of the Configuration Information is saved to Default
logging.basicConfig(level=os.environ.get('LOGGING_LEVEL', logging.WARNING))

PathString = Union[str, Type[Path]]

class Engine:
    """This is the engine that is builds your static site.
    Use `Engine.run()` to output the files to the designated output path."""

    def __init__(self,
            output_path:PathString=Path('output'),
            static_path:PathString=Path('static'),
            strict: bool=False,
            env_variables: dict={},
            templates_dir: Union[str, Sequence]='templates', #Jinja2.FileSystemLoader takes str or iterable not Path
            ):

        self.output_path = Path(output_path)

        if strict and output_path.is_dir():
                shutil.rmtree(self.output_path)

        self.output_path.mkdir(exist_ok=True)
        self.static_path = Path(static_path)

        if self.static_path.is_dir():
            output_static_path = self.output_path.joinpath(self.static_path)

            if output_static_path.exists():
                shutil.rmtree(output_static_path)
                shutil.copytree(src=static_path, dst=output_static_path)

        self.Environment = Environment(
               loader=FileSystemLoader(templates_dir),
               autoescape=select_autoescape(['html', 'xml', 'rss']),
               )

        if env_variables:
            self.Environment.globals = env_variables

    def Markup(self, page_object):
        """Takes a Page-based Content-Type and returns templated or raw Markup"""
        if getattr(page_object, 'template', None):
            template = self.Environment.get_template(page_object.template)
            page_object.template_vars['content'] = page_object.html
            return template.render(**page_object.template_vars)

        else:
            return  Markup(page_object.html)

    def page(self, page_object=Page, **kwargs):
        page = page_object(**kwargs)
        path = Path(f'{self.output_path}/{page_object.slug}.html')
        return path.write_text(self.Markup(page))
