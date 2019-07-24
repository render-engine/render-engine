from collections import defaultdict
from itertools import zip_longest
from .page import Page
from pathlib import Path
import json
import arrow

rfc3339 = 'YYYY-MM-DDTHH:MM:SSZZ'
rfc2822 = 'ddd, DD MMM YYYY HH:MM:SS Z'
default_time_format = 'MMMM DD, YYYY HH:mm'

def feed_time(time, time_format, user_time_format=default_time_format):
    rfc_time = arrow.get(
            time,
            user_time_format,
            ).format(time_format)
    return rfc_time


class Collection:
    def __init__(self, paginate: bool=False, **kwargs):
        """
        Create a Collection of Similar Page Objects
        -----------
        - name is used to create a slug object
        - content_type the type of pages that you are bundling (Currently all
          collections have to be of the same type)

        TODO: Figure out how to collect items of different types (Perhaps for
        courses)

        - extension tells collection what types of documents to look at,
          usually (HTML or Markdown files)
        TODO: Add ignore param that looks are all files that don't contain the
        ignored type - (e.g. Collection(ignored=".tmp"))
        """
        self.name = kwargs.get('name')
        self.content_type = kwargs.get('content_type', Page)
        self.extension = kwargs.get('extension', '.md')

        if self.extension[0] != '.':
            self.extension = f'.{self.extension}'



        # Content Path is were all the content is stored before being processed
        self.content_path = kwargs.get('content_path')

        # Output Path is where the output content is stored
        output_path = kwargs.get('output_path', '')
        self.output_path = Path(output_path)

        page_glob = self.content_path.glob(f'*{self.extension}')

        pages = [self.content_type(
                    base_file=base_file,
                    output_path=self.output_path,
                    ) for base_file in page_glob ]

        self.pages = sorted(
                pages,
                key=lambda page: arrow.get(
                    page.date_published,
                    default_time_format,
                    ),
                reverse=True,
                )

        self.json_feed = self.generate_feed_metadata()
        self.rss_feed = self.generate_rss_feed()

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


    def generate_feed_metadata(self, pages=None, **config):
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
        expired = config.get('expired')
        hubs = config.get('hubs')

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
                }

        filled_feed_data = {x:y for x,y in feed_data.items()}

        feed_items = []

        filled_feed_data['items'] = [self.item_values(feed_item,
            time_format=rfc3339) for feed_item in pages]
        return filled_feed_data

    def generate_rss_feed(self, pages=None, **config):
        """Applies feed Metadata into a RSS file.
        TODO: Move data to jinja2 Template
        """

        SITE_URL = config.get('SITE_URL')
        pages = pages or self.pages
        feed_items = self.generate_feed_metadata()
        channel_info = f'''<title>{feed_items['title']}</title>
<description>{feed_items['description']}</description>
<link>{feed_items['home_page_url']}</link>
<atom:link href="{SITE_URL}/{self.name}/{self.name}.rss" rel="self" type="application/rss+xml" />
'''
        items = [self.item_values(feed_item, time_format=rfc2822) for feed_item in pages]
        item_string = ''

        for item in items:
            item_time = item['date_published']
            item_info = f'''<item>
<title>{item['title']}</title>
<description><![CDATA[{item['content_html']}]]></description>
<guid>{SITE_URL}/{item['url']}</guid>
<pubDate>{item_time}</pubDate>
</item>
'''
            item_string += item_info

        return f'''<?xml version="1.0"?>
<!-- RSS Generated by Render Engine v0.2.0 -->
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
{channel_info}
{item_info}
</channel>
</rss>
'''

    def item_values(self, item, time_format, **config):
        SITE_URL = config.get('SITE_URL', '')
        items_values = {
           'id':item.id,
           'url': f"{SITE_URL}/{self.name}/{item.id}",
           'title': item.title,
           'content_html': item.markup,
           'summary': item.summary,
           'date_published': feed_time(item.date_published,
               time_format=time_format),
           'date_modified': feed_time(item.date_modified,
               time_format=time_format),
           }

        other_item_values = (
                ('image', config.get('DEFAULT_POST_IMAGE', '')),
                ('banner_image', config.get('DEFAULT_POST_BANNER')),
                ('author', None),
                ('external_url', None),
            )

        for other_value in other_item_values:
            if other_value[0] in item.__dict__.keys():
                item_values[other_value[0]] = item.__dict__[other_value[0]]
            elif other_value[1]:
                item_values[other_value[0]] = other_value[1]
            else:
                continue

        return items_values
