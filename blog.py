from jinja2 import Markup
from string import punctuation
from markdown import markdown
from .page import Page


class BlogPost(Page):
    def __init__(self, base_file, template='blog.html'):
        super().__init__(
                base_file=base_file,
                template=template,
                )
        self.tags = self.get_tags()

    def get_tags(self):
        tags = getattr(self, '_tags', '')
        return tags.split(',')
