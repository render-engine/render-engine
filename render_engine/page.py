from pathlib import Path
from markdown import markdown
from typing import (
        Optional,
        Union,
        )
import re
import logging


class Page():
    """Base component used to make web pages
        content = the data that will be used to create a page object
        extension = tells the Engine what extension to use when creating the page
        slug = the name of the document. Used as the filename of the output path
        template = the template filepath that the engine will use to build the
        page
        template_vars= accepts a dictionary and saves items as properties to be
        """
    def __init__(
            self,
            *,
            slug: Optional[str]=None,
            content: Optional[str]=None,
            content_path: Optional[Union[str, Path]]=None,
            extension: str=".html",
            template: Optional[Union[str, Path]]=None,
            **template_vars,
            ):
        """
        initializes a new Page object
        --------
        content_path = filepath to get content and attributes. Attributes added
        to template_vars. Will overwrite content
        used in template rendering.
        """
        self.extension = extension

        # Set Content from content and/or content_path
        if content_path:
            content = Path(content_path).read_text()

        if content:
            _ = load_content(content)
            template_vars.update(_['attrs'])
            content = _.get('content')

        self.content = content
        self.template = template
        self.template_vars = template_vars
        self.slug = slug or template_vars.get('slug')
        logging.debug(f'slug - {self.slug}')

    @property
    def html(self):
        """html = rendered html (not marked up). Is None if content is none"""
        if self.content:
            return markdown(self.content)

        else:
            return None


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
