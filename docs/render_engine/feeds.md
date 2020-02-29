Module render_engine.feeds
==========================
The Feeds Logic That Makes Up RSS and ATOM FeedTypes.

This is the base files and should only contain the params identified by the
standards defined.

RSS: http://www.rssboard.org/rss-specification
JSON: https://jsonfeed.org/version/1

Classes
-------

`RSSFeed(content_path=None, content='', matcher=re.compile('(^\\w+: \\b.+$)', re.MULTILINE))`
:   The RSS Feed Component of an Archive Object
    
    If a content_path exists, check the associated file, processing the
    vars at the top and restitching the remaining lines
    
    Parameters:
        content_path: List[PathString], optional
            the filepath to load content from.
        content: str, optional
            raw text to be processed into HTML
        matcher: str, optional
            A compiled regular expression that splits the content.
            defatul `base_matcher`
    
    TODOs:
        - ADD Documentation for attrs/content
        - Make Slug Conversion Smarter

    ### Ancestors (in MRO)

    * render_engine.page.Page

    ### Class variables

    `link`
    :   str(object='') -> str
        str(bytes_or_buffer[, encoding[, errors]]) -> str
        
        Create a new string object from the given object. If encoding or
        errors is specified, then the object must expose a data buffer
        that will be decoded using the given encoding and error handler.
        Otherwise, returns the result of object.__str__() (if defined)
        or repr(object).
        encoding defaults to sys.getdefaultencoding().
        errors defaults to 'strict'.

    `slug`
    :   str(object='') -> str
        str(bytes_or_buffer[, encoding[, errors]]) -> str
        
        Create a new string object from the given object. If encoding or
        errors is specified, then the object must expose a data buffer
        that will be decoded using the given encoding and error handler.
        Otherwise, returns the result of object.__str__() (if defined)
        or repr(object).
        encoding defaults to sys.getdefaultencoding().
        errors defaults to 'strict'.

    `title`
    :   str(object='') -> str
        str(bytes_or_buffer[, encoding[, errors]]) -> str
        
        Create a new string object from the given object. If encoding or
        errors is specified, then the object must expose a data buffer
        that will be decoded using the given encoding and error handler.
        Otherwise, returns the result of object.__str__() (if defined)
        or repr(object).
        encoding defaults to sys.getdefaultencoding().
        errors defaults to 'strict'.

`RSSFeedEngine()`
:   The Engine that Processes RSS Feed

    ### Ancestors (in MRO)

    * render_engine.engine.Engine

`RSSFeedItem(cls)`
:   The Object to be used with an RSS Feed