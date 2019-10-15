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

    def write_page(self, slug, page, extension='.html', template=None, **template_vars):
        """writes the page object to the output path"""

        if template:
            template = self.Environment.get_template(template)
            html = template.render(
                    content=page.markup,
                    **template_vars,
                    )

        else:
            html = page.markup

        if not extension.startswith('.'):
            extension = f'.{extension}'

        self.output_path.joinpath(f'{slug}{extension}').write_text(html)
        return html

    def route(
            self,
            *slugs,
            template=None,
            page_object=Page,
            extension='.html',
            ):
        """decorator that creates a page and writes it"""

        def inner(func, *args, **kwargs):

            for slug in slugs:
                if slug == '/' or not slug:
                    slug = '/index'

                func_kwargs = func(*args, **kwargs)
                page = page_object()

                self.write_page(
                        slug=slug.lstrip('/'),
                        page = page,
                        extension=extension,
                        template=template,
                        **func_kwargs,
                        )
            return func

        return inner

    def collection(
            self,
            *routes,
            name,
            content_path,
            template=None,
            index_template=None,
            collection_type=Collection,
            extension='.html',
            **collection_kwargs,
            ):
        """This is a way to make similar items based on markdown content that
        you can save in a content_path This iterates through the
        content_path and creates the page object for you.

        For this to work some assumptions are made:
            All objects are the same content type and use the same template.
        """

        for route in routes:
            output_path = self.output_path.joinpath(route.lstrip('/'))
            output_path.mkdir(exist_ok=True)
            collection_object = collection_type(content_path=content_path)


            for page_obj in collection_object.pages:
                self.write_page(
                        page=page_obj,
                        slug=output_path.joinpath(self._get_slug(page_obj)),
                        extension=extension,
                        template=template,
                        **collection_kwargs,
                        )

            for iterator in collection_object._iterators:
                page_obj = Page(title=iterator.name)
                slug = _get_slug(iterator).lstrip('/')
                self.write_page(
                        page=page_obj,
                        slug=output_path.joinpath(slug),
                        extension=extension,
                        template=index_template,
                        pages=iterator.pages,
                        **collection_kwargs,
                        )

    @staticmethod
    def _get_slug(page):
        if not page.slug:
            if page.title:
                return urllib.parse.quote(page.title.lower())

            elif page.content_path:
                return urllib.parse.quote(page.content_path.lower())

            else:
                error_msg = 'Collection content must have a slug, \
                        title or content_path'
                raise AttributeError(error_msg)

        else:
            return page.slug
