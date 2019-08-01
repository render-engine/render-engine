from typing import Type, Union, Sequence
from collections import defaultdict
from itertools import zip_longest
from render_engine.page import Page
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
        self.url_root = url_root

        # Build the URL so that it can be used as reference
        if 'url' in kwargs:
            self.url = url

        else:
            url_stem = str(route)
            url_suffix = url_suffix
            self.url = f'{url_root}/{url_stem}{url_suffix}'

        # make properties for all attrs
        for key, attr in kwargs.items():
            setattr(self, key, attr)

        if not pages:
            page_glob = list(self.content_path.glob(f'*{self.extension}'))
            pages = [content_type(
                        route=Path(route).joinpath(Path(content_path.name)),
                        content_path=content_path,
                        url_root=self.url_root,
                        template=template,
                        ) for content_path in page_glob ]
            self.pages = sorted(
                    pages,
                    key=lambda page:page.date_modified or
                        page.date_published or page.title,
                    reverse=True,
                    )

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

    def to_json(self, engine, pages=None, next_url=None):
        """Gets/Sets Data for dictionary feed metadata"""
        title = engine.FEED_TITLE
        description = engine.FEED_DESCRIPTION
        home_page_url = engine.SITE_URL
        feed_url = f'{self.route}{self.name}.json'
        version = 'https://jsonfeed.org.version/1'
        icon = getattr(engine, 'FEED_ICON','')
        user_comment = getattr(engine, 'user_comment', '')
        next_url = next_url # needs pagination
        favicon = getattr(engine, 'SITE_FAVICON', '')
        author = getattr(engine, 'AUTHOR', '')
        expired = getattr('self', 'expired', '')
        hubs = getattr(engine, 'JSON_FEED_HUB', '')

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

        # if not pages:
#            pages = list(map(lambda x:x.to_json(), self.pages))
#
#        feed_data['items'].extend(pages)
#        print(feed_data)
        return json.dumps(feed_data)


    def to_rss(self, engine, pages=None, html=True, full_text=True):
        """Applies feed Metadata into a RSS file.
        TODO: Move data to jinja2 Template
        """
        channel = json.loads(self.to_json(engine=engine))
        channel['items'] = list(
                map(
                    lambda item: item.to_rss(
                        html=html,
                        full_text=full_text,
                        ),
                        self.pages),
                        )
        template = engine.env.get_template('feeds/rss/blog.rss')
        template.render(channel=channel)

