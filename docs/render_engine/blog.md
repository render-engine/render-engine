Module render_engine.blog
=========================

Classes
-------

`Blog()`
:   Custom Collection Class with Archiving Enabled and the RSS Feed
    
    Todos:
        - Add Support for JSON Feeds
        - Rename the archive items so they are not private

    ### Ancestors (in MRO)

    * render_engine.collection.Collection

    ### Descendants

    * render_engine.microblog.MicroBlog

    ### Class variables

    `feeds`
    :   Built-in mutable sequence.
        
        If no argument is given, the constructor creates a new empty list.
        The argument must be an iterable if specified.

    `page_content_type`
    :   Page Like object with slight modifications to work with BlogPosts.
        
        Attributes:
            template : str
                the default template that the site will look for
            rss_feed_item : RSSFeedItem
                the content in an rss format
            date : pendulum.datetime
                date parsed in datetime format. usesul for sorting and things
            date_published : str
                date formated for `RSSFeed`
            date_friendly : str
                an easy to read string version of the date

`BlogPost(**kwargs)`
:   Page Like object with slight modifications to work with BlogPosts.
    
    Attributes:
        template : str
            the default template that the site will look for
        rss_feed_item : RSSFeedItem
            the content in an rss format
        date : pendulum.datetime
            date parsed in datetime format. usesul for sorting and things
        date_published : str
            date formated for `RSSFeed`
        date_friendly : str
            an easy to read string version of the date
    
    checks published options and accepts the first that is listed
    
    Attributes:
        date : pendulum.datetime
            date parsed in datetime format. usesul for sorting and things
        date_published : str
            date formated for `RSSFeed`
        date_friendly : str
            an easy to read string version of the date

    ### Ancestors (in MRO)

    * render_engine.page.Page

    ### Descendants

    * render_engine.microblog.MicroBlogPost

    ### Instance variables

    `rss_feed_item`
    :