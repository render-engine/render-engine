Module render_engine.site
=========================

Classes
-------

`Site(strict=False)`
:   

    ### Class variables

    `SITE_LINK`
    :   str(object='') -> str
        str(bytes_or_buffer[, encoding[, errors]]) -> str
        
        Create a new string object from the given object. If encoding or
        errors is specified, then the object must expose a data buffer
        that will be decoded using the given encoding and error handler.
        Otherwise, returns the result of object.__str__() (if defined)
        or repr(object).
        encoding defaults to sys.getdefaultencoding().
        errors defaults to 'strict'.

    `SITE_TITLE`
    :   str(object='') -> str
        str(bytes_or_buffer[, encoding[, errors]]) -> str
        
        Create a new string object from the given object. If encoding or
        errors is specified, then the object must expose a data buffer
        that will be decoded using the given encoding and error handler.
        Otherwise, returns the result of object.__str__() (if defined)
        or repr(object).
        encoding defaults to sys.getdefaultencoding().
        errors defaults to 'strict'.

    `collections`
    :   dict() -> new empty dictionary
        dict(mapping) -> new dictionary initialized from a mapping object's
            (key, value) pairs
        dict(iterable) -> new dictionary initialized as if via:
            d = {}
            for k, v in iterable:
                d[k] = v
        dict(**kwargs) -> new dictionary initialized with the name=value pairs
            in the keyword argument list.  For example:  dict(one=1, two=2)

    `output_path`
    :   Path subclass for non-Windows systems.
        
        On a POSIX system, instantiating a Path should return this object.

    `routes`
    :   Built-in mutable sequence.
        
        If no argument is given, the constructor creates a new empty list.
        The argument must be an iterable if specified.

    `static_path`
    :   Path subclass for non-Windows systems.
        
        On a POSIX system, instantiating a Path should return this object.

    ### Methods

    `register_collection(self, collection_cls)`
    :

    `register_feed(self, feed, collection)`
    :

    `register_route(self, cls)`
    :

    `render(self, dry_run=False)`
    :

    `route(self, cls)`
    :