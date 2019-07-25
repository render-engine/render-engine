from datetime import datetime
from jinja2 import Markup
from pathlib import Path
from markdown import markdown
from .environment import env
from .utils import git_log_date
import re
import maya

def get_ct_time(md_file):
    return maya.when(git_log_date(md_file, 'head'))

def get_md_time(md_file):
    return maya.when(git_log_date(md_file, 'tail'))

def load_from_file(base_file):
    matcher = r'^\w+:'
    _ = base_file.read_text()
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
            base_file=None,
            content='',
            content_format='markdown',
            **kwargs,
            ):
        # self.id looks for us
        self._id = None
        self._slug = None
        self._date_published = None
        self._date_modified = None
        self._category = 'Uncategorized'
        self._image = None
        self.summary = None
        self.attrs = kwargs.copy()

        if base_file:
            _ = load_from_file(base_file)
            self.attrs.update(_['attrs'])
            self.content = _['content']

        else:
            self.content = content

        # self.date_published looks for us
        self._date = None
        self._updated = None

        self.base_file = base_file

        self.title = getattr(self, '_title', '')
        self.date_published = self.get_date_published()
        self.date_modified = self.get_date_modified()
        self.markup = markdown(self.content)

    @property
    def id(self):
        base_file_stem = self.base_file.stem if self.base_file else None
        return self._id or self._slug or base_file_stem or ''


    def get_date_published(self):
        """Returns the value of _date_published or _date, or created_datetime from
the system if not defined. NOTE THE SYSTEM DATE IS KNOWN TO CAUSE
ISSUES WITH FILES THAT WERE COPIED OR TRANSFERRED WITHOUT THEIR
METADATA BEING TRANSFER READ AS WELL"""

        if self.base_file:

            if self._date_published:
                date = maya.when(self._date_published)

            elif self._date:
                date = maya.when(self._date)

            else:
                 date = get_ct_time(self.base_file)

            return date

    def get_date_modified(self):
        """Returns the value of _date_modified or _update, or the
modified_datetime from the system if not defined. NOTE THE SYSTEM 
DATE IS KNOWN TO CAUSE ISSUES WITH FILES THAT WERE COPIED OR 
TRANSFERRED WITHOUT THEIR METADADTA BEING TRANSFERRED AS WELL"""

        if self.base_file:
            print(self.base_file)

            if self._date_modified:
                print(self._date_modified)
                date = maya.when(self._date_modified)

            elif self._updated:
                date = maya.when(self._date)

            else:
                date = get_md_time(self.base_file)

            return date

    @property
    def image(self):
        return self._image

