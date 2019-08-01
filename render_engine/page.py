from datetime import datetime
from pathlib import Path
from markdown import markdown
from jinja2 import Markup
import maya
import re
import shlex
import subprocess
import urllib.parse

class Page():
    def __init__(
            self,
            *,
            slug=None,
            content_path=None,
            content='',
            content_format='.md',
            template="page.html",
            url_root="/", # often used to make links
            url_suffix=".html",
            **kwargs,
            ):
        """
        initializing a new Page
        --------
        Required:
        slug [string or pathlib.Path]: the relative url for the Page,
        """

        if content:
            _ = self._load_content(content)
            kwargs.update(_['attrs'])
            self.content = _['content']

        if content_path:
            self.content_path = Path(content_path)
            _ = self._load_from_file(content_path)
            kwargs.update(_['attrs'])
            self.content = _['content']

            # Check for Date Published and convert to RFC2822
            date_published = self._check_for_date_attr(
                    'date_published',
                    kwargs,
                    optional_location = self.content_path,
                    log_index = -1,
                    )
            if date_published:
                self.date_published = maya.parse(date_published).iso8601()

            date_modified = self._check_for_date_attr(
                    'date_modified',
                    kwargs,
                    optional_location = self.content_path,
                    log_index = 0,
                    )
            if date_modified:
                self.date_modified = maya.parse(date_modified).iso8601()

            else:
                self.date_modified = self.date_published or None

        self.template = template

        # make properties for all attrs
        for key, attr in kwargs.items():
            setattr(self, key, attr)

        if getattr(self, 'content', None):
            self.markup = Markup(markdown(self.content))

        if slug:
            slug = slug.lstrip('/')
        else:
            slug = getattr(self, 'name', None) \
                or getattr(self, 'id', None) \
                or getattr(self, 'content_path', '/')
        self.slug = Path(slug)


        self.relative_url = f'{self.slug.parent}{self.slug.with_suffix(url_suffix)}'

        # Build the URL so that it can be used as reference
        if not getattr(self, 'absolute_url', None):
            _ = '/'.join((url_root, Path(self.relative_url).name))
            self.absolute_url = urllib.parse.urlsplit(_).geturl()


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
    def _load_content(content):
        matcher = r'^\w+:'
        md_content = content.splitlines()
        attrs = {}

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

    def _load_from_file(self, content_path):
        return self._load_content(content_path.read_text())


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
            return maya.when(key_setter).rfc2822()

    def to_json(self):
        date_published = getattr(self, 'date_published', None)
        date_modified = getattr(self, 'date_modified', date_published)
        base_feed_items = {
            'id': self.url,
            'url': id,
            'external_url': getattr(self, 'external_url', None),
            'title': getattr(self, 'title', None),
            'content_html': getattr(self, 'markup', None),
            'content_text': self.content,
            'summary': getattr(self, 'summary', self.content[:40]),
            'image': getattr(self, 'featured_image', None),
            'banner_image': getattr(self, 'banner_image', None),
            'date_published': self.date_published.rfc3339() if date_published
                else None,
            'date_modified': self.date_modified.rfc3339() if date_modified
                else None,
            'author': getattr(self, 'author', None),
            'tags': getattr(self, 'tags', []),
            'attachments': getattr(self, 'attachments', None),
            }
        return dict(filter(lambda item: item[1], base_feed_items.items()))

    def to_rss(self, html=True, full_text=True):
        if getattr(self, 'date_published', ''):
            self.pubDate = maya.parse(self.date_published).rfc2822()

        if full_text:
            if html:
                self.description = self.markup
            else:
                self.description = self.content
        else:
            self.description = self.summary
