from render_engine.collection import Collection
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

    def markup(self, content_type):
        """Takes a Page-based Content-Type and returns templated or raw Markup"""
        filename = content_type.slug

        if getattr(content_type, 'template', None):
            template = self.Environment.get_template(content_type.template)
            content_type.template_vars['content'] = content_type.html
            return template.render(**content_type.template_vars)

        else:
            return  Markup(content_type.html)

    def page(self, markup, content_type=Page, **kwargs):
        page = content_type(**kwargs)
        path = Path(f'{self.output_path}/{content_type.slug}.html')
        return path.write_text(self.markup(page)):
