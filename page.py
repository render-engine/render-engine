from datetime import datetime
from jinja2 import Markup
from pathlib import Path
from markdown import markdown
from .environment import env
from .utils import git_log_date
import re
import maya

def load_from_file(content_path):
    matcher = r'^\w+:'
    _ = content_path.read_text()
    md_content = _.splitlines()
    attrs = {}

    while re.match(matcher, md_content[0]):
        line = md_content.pop(0)
        line_data = line.split(': ', 1)
        key = line_data[0].lower()
        value = line_data[-1].rstrip()
        attrs[key] = value

    return {
            'attrs': attrs,
            'content': ''.join(md_content).strip('\n'),
            }


class Page():
    env = env

    def __init__(
            self,
            *,
            output_path,
            content_path=None,
            content='',
            content_format='markdown',
            **attrs,
            ):
        self.content_path = Path(content_path)

        if content_path:
            _ = load_from_file(content_path)
            attrs.update(_['attrs'])
            self.content = _['content']

        self.markup = markdown(self.content)

        if 'date_published' in attrs:
            date_published = attrs['date_published']
        elif self.content_path:
            date_published = git_log_date(self.content_path)[-1]
        self.date_published = maya.when(date_published).iso8601()

        if 'date_modified' in attrs:
            date_modified = attrs['date_modified']
        elif self.content_path:
            date_modified = git_log_date(self.content_path)[0]
        self.date_modified = maya.when(date_modified).iso8601()

        if not 'id' in attrs:
            if 'slug' in attrs:
                self.id = attrs['slug']
            elif 'content_path':
                self.id = self.content_path.stem

        # make properties for all attrs
        for key, attr in attrs.items():
            setattr(self, key, attr)

