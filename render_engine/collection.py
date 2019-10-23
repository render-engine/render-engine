from pathlib import Path

import logging

from .page import Page

class Collection:
    template = None
    engine = None
    content_type = Page
    content_path = 'content'
    includes = ["*.md", "*.html"]
    routes = ['']

    def __init__(self, index=False, index_template=''):
        if index and index_template:
            self.index = self.gen_index(index_template)

    @property
    def pages(self):
        pages = []

        for i in self.includes:

            for p in Path(self.content_path).glob(i):
                page = self.content_type(content_path=p)

                if self.template:
                    page.template = self.template

                pages.append(page)

        return pages

    def gen_index(self, template):
        pages = self.pages()
        page = self.content_type
        page.template = template
        return template
