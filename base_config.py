from configparser import ConfigParser

config = ConfigParser()
config['DEFAULT'] = {
        'TIME_FORMAT': 'MMMM DD, YYYY HH:mm',
        'OUTPUT_PATH': '',
        'CONTENT_PATH': 'content',
        'OUTPUT_PATH': 'output',
        'STATIC_PATH': 'static',
        'SITE_TITLE': 'Site Title',
        'SITE_SUBTITLE': 'Site Subtitle',
        'SITE_URL':  'localhost',
        'AUTHOR':  'John Doe',
        'AUTHOR_EMAIL':  'jdoe@example.com',
        'AUTHOR_URL':  'https://example.com',
        'AUTHOR_IMAGE': '',
        'REGION':  r'US/Pacific',
        'ICON': '',
        'FAVICON': '',
        'DEFAULT_POST_IMAGE': '',
        'DEFAULT_POST_BANNER': '',
        }
