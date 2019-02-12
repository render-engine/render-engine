"""
Feeds takes objects and creates an arrangement of items and returns a feed.
"""
import json
import config
from pathlib import Path
from environment import env


def generate_from_metadata( items, path,config=config, **kwargs):
    feed_data = {
            'title': kwargs.get('title', config.SITE_TITLE),
            'home_page_url': kwargs.get('home_page_url', config.SITE_URL),
            'feed_url': kwargs.get('feed_url'),
            'version': kwargs.get('version', 'https://jsonfeed.org.version/1'),
            'icon': kwargs.get('icon', config.ICON),
            'description': kwargs.get('description', config.SITE_SUBTITLE),
            'user_comment': kwargs.get('user_comment'),
            'next_url': kwargs.get('next_url', ), # needs pagination
            'favicon': kwargs.get('favicon', config.FAVICON),
            'author': kwargs.get('author',{
                    'name': config.AUTHOR,
                    'avatar': config.AUTHOR_IMAGE,
                    'url': config.AUTHOR_URL,
                    }),
            'expired': kwargs.get('expired'),
            'hubs': kwargs.get('hubs'),
            }

    filled_feed_data = {x:y for x,y in feed_data.items() if y}


    feed_items = []
    for item in items:
        items_values = {
           'id':item.id,
           'url': f'{path}/{item.id}',
           'title': item.title,
           'content_html': item.markup, 
           'summary': item.summary,
           'date_published': item.date_published,
           'date_modified': item.date_modified,
           } 

        other_item_values = (
                ('image', config.DEFAULT_POST_IMAGE), 
                ('banner_image', config.DEFAULT_POST_BANNER),
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

            feed_items.append(item_values)
    filled_feed_data['items'] = feed_items
    return json.dumps(filled_feed_data)
