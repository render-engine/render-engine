import logging
import re
import urllib.parse
from pathlib import Path
from typing import Optional, Union

import maya
from jinja2 import Markup
from markdown import markdown


class Page:
    title = None
    _slug = None
    engine = None

    """Base component used to make web pages"""
    def __init__(
            self,
            *,
            self: Optional[str]=None,
            content: Optional[str]=None,
            content_path: Optional[Union[str, Path]]=None
           ):
        """
        initializes a new Page object
        --------
        content = raw content to be loaded
        content_path = filepath to get content and attributes. Attributes added
        to template_vars.
        extension
        """

        if content and content_path:
            error_msg = 'Supply either content or content_path. Not Both'
            raise AttributeError(errorMsg)

        if content_path:
           # content_path will always overwrite the content
           self.content_path = Path(content_path)
           content = content_path.read_text()

        loaded_content = self.load_content(content)
        for key, val in loaded_content['attrs'].items():

            if key == 'slug': # To Avoid Slug Conflicts with Slug Property
                key = '_slug'

            setattr(self, key, val)

        self._content = loaded_content['content']


    @property
    def slug(self):
        slug = self._slug or self.title or self.content_path

        if slug == '/' or not slug:
            slug = '/index'

        return urllib.parse.quote_plus(slug.lower())

    @property
    def html(self):
        """the text from self._content converted to html"""
        return markdown(self._content)

    @property
    def content(self):
        """html = rendered html (not marked up). Is None if content is none"""
        return Markup(self.content)

    @staticmethod
    def load_content(content):
        matcher = r'^\w+:'
        md_content = content.splitlines()
        attrs = {}

        if len(md_content) > 1:
            while re.match(matcher, md_content[0]):
                line = md_content.pop(0)
                line_data = line.split(': ', 1)
                key = line_data[0].lower()
                value = line_data[-1].rstrip()
                attrs[key] = value

        return {
            'attrs': attrs,
            'content': '\n'.join(md_content).strip('\n'),
            }

   def render_template(self, template_name):
        template = self.engine.environment.get_template(template_name)
        kwargs = self.__dict__
        render = render(template.render(content=self.content))
        self.filename.write_text(render)
