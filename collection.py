from typing import Type, Union, Sequence
from collections import defaultdict
from itertools import zip_longest
from .page import Page
from pathlib import Path
import json
import maya


PathString = Union[str, Type[Path]]

class Collection:
    """Create a Collection of Similar Page Objects"""
    def __init__(
            self,
            *,
            paginate: bool,
            name: str,
            content_type: Type[Page],
            content_path: PathString,
            output_path: Union[PathString, Sequence[PathString]],
            extension: str,
            pages: Sequence[PathString]=None,
            **attrs,
            ):
        """
        ___________
        - name is used to create a slug object
        - content_type the type of pages that you are bundling (Currently all
          collections have to be of the same type)
        - extension tells collection what types of documents to look at,
          usually (HTML or Markdown files)
        TODO: Add ignore param that looks are all files that don't contain the
        ignored type - (e.g. Collection(ignored=".tmp"))
        """
        self.name = name
        self.content_type = content_type
        self.extension = extension
        self.content_path = content_path
        self.output_path = Path(output_path)

        if not pages:
            page_glob = self.content_path.glob(f'*{self.extension}')

            pages = [self.content_type(
                        output_path=self.output_path,
                        content_path=content_path
                        ) for content_path in page_glob ]

            self.pages = sorted(
                    pages,
                    key=lambda page:page.date_modified or page.title,
                    reverse=True,
                    )
        else:
            self.pages = pages

        self.json_feed = self.to_json()
        self.rss_feed = self.to_rss()

    def __iter__(self):
        return iter(self.pages)

    @property
    def paginate(self):
        "Collect data into fixed-length chunks or blocks"
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
        args = [iter(self.pages)] * 10
        iterable = zip_longest(*args, fillvalue=None)
        return iterable

    @property
    def categories(self):
        d = defaultdict(list)
        for p in self.pages:
            d[p._category].append(p)
        return d

    @property
    def tags(self):
        d = defaultdict(list)

        for p in self.pages:
            for tag in p.tags:
                d[tag].append(p)
        return d


    def to_json(self, pages=None, **config):
        """Gets/Sets Data for dictionary feed metadata"""
        pages = pages or self.pages
        title = config.get('title', 'Untitled Site')
        home_page_url = config.get('home_page_url', 'https://example.com')
        feed_url = config.get('feed_url', 'https://example.com/feed.json')
        version = config.get('version', 'https://jsonfeed.org.version/1')
        icon = config.get('icon','')
        description = config.get('description', '')
        user_comment = config.get('user_comment')
        next_url = config.get('next_url', ) # needs pagination
        favicon = config.get('favicon')
        author = config.get('author',{
                        'name': 'Jane Doe',
                        'avatar': '',
                        'url': '',
                        })
