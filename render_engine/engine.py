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
logging.basicConfig(level=os.environ.get('LOGGING_LEVEL', logging.INFO))

PathString = Union[str, Type[Path]]

class Engine:
    """This is the engine that is builds your static site.
    Use `Engine.run()` to output the files to the designated output path."""

    def __init__(
            self,
            output_path:PathString=Path('output'),
            static_path:PathString=Path('static'),
            strict: bool=False,
            templates_dir: Union[str, Sequence]='templates', #Jinja2.FileSystemLoader takes str or iterable not Path
            **env_variables,
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
        """Takes a Page-based Content-Type and returns templated or raw
        Markup"""

        template = getattr(page_object, 'template', None)
        content = getattr(page_object, 'html', None) or page_object.content

        if template:
            template = self.Environment.get_template(page_object.template)
            markup = template.render(content=content, **page_object.template_vars)

        else:
            logging.info('No template found')
            markup = content

        logging.debug(f'content - {content}')
        logging.debug(f'markup - {markup}')

        return Markup(markup)

    def route(self, *slugs, template=None, page_object=Page, extension='.html'):
        """with functionality similar to flask and a name to match. This is to
        help with transitions to static generation.

        This decorator is what makes the static pages. While you could just
        call `Markup` and then write the output this is the thing that makes
        life easier."""

        def build_page(func, **kwargs):

            for slug in slugs:
                if slug == '/' or not slug:
                    slug = '/index'
                func_kwargs = func(**kwargs)
                p = page_object(slug=slug, template=template, **func_kwargs)
                logging.info(p.__dict__)

                with open(f'{self.output_path}/{slug}{extension}', 'w') as fp:
                    fp.write(self.Markup(p))
            return func

        return build_page


    def collection(
            self,
            *output_paths,
            content_path,
            template=None,
            collection_object=Collection,
            extension='.html',
            **kwargs,
            ):
        """This is a way to make similar items based on markdown content that
        you can save in a content_path This iterates through the
        content_path and creates the page object for you.

        For this to work some assumptions are made:
            All objects are the same content type and use the same template.

        TODO: Allow for a custom collection to be used.
        """

        content_path = collection_object(
                content_path=content_path,
                template=template,
                **kwargs,
                )

        for page in content_path.pages:
            for output_path in output_paths:
                base_dir = Path(f'{self.output_path}{output_path}')
                base_dir.mkdir(exist_ok=True)

                logging.debug(f'output_path - {output_path}')
                filepath = base_dir.joinpath(f'{page.slug}{extension}')

                logging.debug(f'filepath - {filepath}')
                filepath.write_text(self.Markup(page))
