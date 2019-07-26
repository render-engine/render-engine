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
            content_path: PathString,
            route: Union[PathString, Sequence[PathString]],
            url_root: str,
            url_suffix: str='.html',
            extension: str='.md',
            template: str='page.html',
            pages: Sequence[PathString]=None,
            content_type=Page,
            **kwargs,
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
        self.extension = extension
        self.content_path = Path(content_path)
        self.route = Path(route)

        # Build the URL so that it can be used as reference
        if 'url' in kwargs:
            self.url = url

        else:
            url_stem = str(route)
            url_suffix = url_suffix
            print(url_stem)
            self.url = f'{url_root}/{url_stem}{url_suffix}'

        # make properties for all attrs
        for key, attr in kwargs.items():
            setattr(self, key, attr)

        if not pages:
            print(self.content_path)
            page_glob = list(self.content_path.glob(f'*{self.extension}'))
            pages = [content_type(
                        route=content_path.joinpath(route),
                        content_path=content_path,
                        template=template,
                        ) for content_path in page_glob ]
            self.pages = sorted(
                    pages,
                    key=lambda page:page.date_modified or page.title,
                    reverse=True,
                    )

    def __iter__(self):
        print(self.pages)
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

    def to_json(self, pages=None, next_url=None):
        """Gets/Sets Data for dictionary feed metadata"""
        title = self.FEED_TITLE
        description = self.description
        home_page_url = self.SITE_URL
        feed_url = f'{self.absolute_url}{self.name}.json'
        version = 'https://jsonfeed.org.version/1'
        icon = config.get('FEED_ICON','')
        user_comment = config.get('user_comment')
        next_url = next_url # needs pagination
        favicon = config.get('SITE_FAVICON')
        author = config.get('AUTHOR')
        expired = getattr('self', 'expired')
        hubs = config.get('JSON_FEED_HUB')

        feed_data = {
                'title': title,
                'home_page_url': home_page_url,
                'feed_url': feed_url,
                'version': version,
                'icon': icon,
                'description': description,
                'user_comment': user_comment,
                'next_url': next_url,
                'favicon': favicon,
                'author': author,
                'expired': expired,
                'hubs': hubs,
                'items': [],
                }

        if not pages:
            for page in collections:
                feed_data['items'].append(page.to_json())

        return json.dumps(feed_data)


    def to_rss(self, env, pages=None, html=True, full_text=True):
        """Applies feed Metadata into a RSS file.
        TODO: Move data to jinja2 Template
        """
        channel = json.loads(self.to_json())
        channel['items'] = list(
                map(
                    lambda item:_to_rss_item(
                        item, html=html,
                        full_text=full_text,
                        ),
                    ),
                )
        template = env.get_template('templates/rss/blog.rss')
        template.render(channel)

    @staticmethod
    def _to_rss_item(item, html=True, full_text=True):
        if date_published in item:
            item['pubDate'] = maya.parse(item['date_published']).rfc2822()

        if full_text:
            if html:
                item['description'] = item['content_html']
            else:
                item['description'] = item['content_text']
        else:
            item['description'] = item['summary']

        return item
