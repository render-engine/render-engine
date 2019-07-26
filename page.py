from datetime import datetime
from jinja2 import Markup
from pathlib import Path
from markdown import markdown
import maya
import re
import shlex
import subprocess


class Page():
    def __init__(
            self,
            *,
            output_path,
            content_path=None,
            content='',
            content_format='markdown',
            template="page.html",
            **attrs,
            ):

        self.content_path = Path(content_path)
        if content_path:
            _ = self._load_from_file(content_path)
            attrs.update(_['attrs'])
            self.content = _['content']

        self.template = template
        self.markup = markdown(self.content)
        self.date_published = self._check_for_date_attr(
                'date_published',
                attrs,
                optional_location = self.content_path,
                log_index = -1,
                )

        self.date_modified = self._check_for_date_attr(
                'date_modified',
                attrs,
                optional_location = self.content_path,
                log_index = 0,
                )

        self.id = self._check_for_attr(
                attrs,
                optional_keys=['id', 'slug'],
                fallback=self.content_path.stem,
                )

        # make properties for all attrs
        for key, attr in attrs.items():
            setattr(self, key, attr)

    @staticmethod
    def _git_log_date(filepath, branch: str="origin/master", message: str=""):
        """
        The Git log Command Ran as a Subprocess to Pull date information from history.
        git log -b [branch] --date=rfc -- [filepath] | [head/tail] -1
        ------
        - filepath (Path or str) - the filepath of the document
        - post (str: Either 'head' or 'tail') tells to get either the first (Creation) or the Last(Modification)
        - branch (str: default='origin/master') filters results to only include the specified branch. Remove '-b' if None
        - message (str: message before the preformated date

        The results of this command can be given to maya or datetime.strptime as the format is Mon, Jan 01, 2019 19:00 -0800
        """

        if branch:
            branch = f'-b {branch}'
        else:
            branch = ''

        command = f'git log {branch} --format="%ad" -- {filepath}'
        output = subprocess.check_output(shlex.split(command))
        return output.decode().strip().split('\n')

    @staticmethod
    def _load_from_file(content_path):
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

    @staticmethod
    def _check_for_attr(attrs, optional_keys, fallback=None):
        """Check the attrs for the desired keys.
        If none, use fallback"""

        for key in optional_keys:
            if key in attrs:
                return key

        return fallback

    def _check_for_date_attr(
            self,
            key,
            attrs,
            log_index,
            optional_location=None,
            ):
        """first it checks in attrs, then it checks the optional location"""
        if key in attrs:
            key_setter = attrs[key]

        elif optional_location:
            key_setter = self._git_log_date(optional_location)[log_index]

        if key_setter:
            return maya.when(key_setter)

    def __dict__(self):
        base_feed_items = {
            id: self.absolute_url,
            url: id,
            external_url: getattr('self', 'external_url', None),
            title: getattr('self', 'title', None),
            content_html: Markup(self.markup),
            content_text: self.content,
            summary: getattr('self', 'summary', self.content[:40]),
            image: getattr('self', 'featured_image', None),
            banner_image: getattr('self', 'banner_image', image),
            date_published: self.date_published.rfc3339() if date_published else None,
            date_modified: self.date_modified.rfc3339() if date_modified else None,
            author: getattr('self', 'author'),
            tags: getattr('self', 'tags', []),
            attachments: getattr('self', 'attachments'),
            }
        return dict(filter(lambda item: item[1], base_feed_items.items()))

    def to_rss(self, env, html=True, full_text=True):
        items = self.__dict__

        if date_published in items:
            items['pubDate'] = maya.parse(items['date_published']).rfc2822()

        if full_text:
            if html:
                items['description'] = items['content_html']
            else:
                items['description'] = items['content_text']
        else:
            items['description'] = items['summary']

        return items
