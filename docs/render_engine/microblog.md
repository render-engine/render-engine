Module render_engine.microblog
==============================

Classes
-------

`MicroBlog()`
:   Custom Blog Class pointing to custom templates

    ### Ancestors (in MRO)

    * render_engine.blog.Blog
    * render_engine.collection.Collection

    ### Class variables

    `page_content_type`
    :   Page Like Object with slight modifications to work with BlogPosts
        
        Attribtues:
            title : str
                default ''. Leave blank.
        
            slug : str
                the name for the file for that will
        
            rss_feed_item : RSSFeedItem
                the content in an rss format

`MicroBlogPost(**kwargs)`
:   Page Like Object with slight modifications to work with BlogPosts
    
    Attribtues:
        title : str
            default ''. Leave blank.
    
        slug : str
            the name for the file for that will
    
        rss_feed_item : RSSFeedItem
            the content in an rss format
    
    checks published options and accepts the first that is listed

    ### Ancestors (in MRO)

    * render_engine.blog.BlogPost
    * render_engine.page.Page

    ### Class variables

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

    ### Instance variables

    `rss_feed_item`
    :