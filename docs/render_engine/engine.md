Module render_engine.engine
===========================

Classes
-------

`Engine()`
:   This is the engine that is builds your static site.
    Use `Engine.run()` to output the files to the designated output path.
    
    Attributes:
        extension : str
            the extension to use in the rendered files
            default '.html'
        environment : Any
            the environment renderer that you want to use. You can use any environment that you like. Environments
            should support a `get_template` and `render`
    
    Todos:
        * Create default template
        * Method to build template directory

    ### Descendants

    * render_engine.feeds.RSSFeedEngine

    ### Class variables

    `environment`
    :   The core component of Jinja is the `Environment`.  It contains
        important shared variables like configuration, filters, tests,
        globals and others.  Instances of this class may be modified if
        they are not shared and if no template was loaded so far.
        Modifications on environments after the first template was loaded
        will lead to surprising effects and undefined behavior.
        
        Here are the possible initialization parameters:
        
            `block_start_string`
                The string marking the beginning of a block.  Defaults to ``'{%'``.
        
            `block_end_string`
                The string marking the end of a block.  Defaults to ``'%}'``.
        
            `variable_start_string`
                The string marking the beginning of a print statement.
                Defaults to ``'{{'``.
        
            `variable_end_string`
                The string marking the end of a print statement.  Defaults to
                ``'}}'``.
        
            `comment_start_string`
                The string marking the beginning of a comment.  Defaults to ``'{#'``.
        
            `comment_end_string`
                The string marking the end of a comment.  Defaults to ``'#}'``.
        
            `line_statement_prefix`
                If given and a string, this will be used as prefix for line based
                statements.  See also :ref:`line-statements`.
        
            `line_comment_prefix`
                If given and a string, this will be used as prefix for line based
                comments.  See also :ref:`line-statements`.
        
                .. versionadded:: 2.2
        
            `trim_blocks`
                If this is set to ``True`` the first newline after a block is
                removed (block, not variable tag!).  Defaults to `False`.
        
            `lstrip_blocks`
                If this is set to ``True`` leading spaces and tabs are stripped
                from the start of a line to a block.  Defaults to `False`.
        
            `newline_sequence`
                The sequence that starts a newline.  Must be one of ``'\r'``,
                ``'\n'`` or ``'\r\n'``.  The default is ``'\n'`` which is a
                useful default for Linux and OS X systems as well as web
                applications.
        
            `keep_trailing_newline`
                Preserve the trailing newline when rendering templates.
                The default is ``False``, which causes a single newline,
                if present, to be stripped from the end of the template.
        
                .. versionadded:: 2.7
        
            `extensions`
                List of Jinja extensions to use.  This can either be import paths
                as strings or extension classes.  For more information have a
                look at :ref:`the extensions documentation <jinja-extensions>`.
        
            `optimized`
                should the optimizer be enabled?  Default is ``True``.
        
            `undefined`
                :class:`Undefined` or a subclass of it that is used to represent
                undefined values in the template.
        
            `finalize`
                A callable that can be used to process the result of a variable
                expression before it is output.  For example one can convert
                ``None`` implicitly into an empty string here.
        
            `autoescape`
                If set to ``True`` the XML/HTML autoescaping feature is enabled by
                default.  For more details about autoescaping see
                :class:`~jinja2.utils.Markup`.  As of Jinja 2.4 this can also
                be a callable that is passed the template name and has to
                return ``True`` or ``False`` depending on autoescape should be
                enabled by default.
        
                .. versionchanged:: 2.4
                   `autoescape` can now be a function
        
            `loader`
                The template loader for this environment.
        
            `cache_size`
                The size of the cache.  Per default this is ``400`` which means
                that if more than 400 templates are loaded the loader will clean
                out the least recently used template.  If the cache size is set to
                ``0`` templates are recompiled all the time, if the cache size is
                ``-1`` the cache will not be cleaned.
        
                .. versionchanged:: 2.8
                   The cache size was increased to 400 from a low 50.
        
            `auto_reload`
                Some loaders load templates from locations where the template
                sources may change (ie: file system or database).  If
                ``auto_reload`` is set to ``True`` (default) every time a template is
                requested the loader checks if the source changed and if yes, it
                will reload the template.  For higher performance it's possible to
                disable that.
        
            `bytecode_cache`
                If set to a bytecode cache object, this object will provide a
                cache for the internal Jinja bytecode so that templates don't
                have to be parsed if they were not changed.
        
                See :ref:`bytecode-cache` for more information.
        
            `enable_async`
                If set to true this enables async template execution which allows
                you to take advantage of newer Python features.  This requires
                Python 3.6 or later.

    `extension`
    :   str(object='') -> str
        str(bytes_or_buffer[, encoding[, errors]]) -> str
        
        Create a new string object from the given object. If encoding or
        errors is specified, then the object must expose a data buffer
        that will be decoded using the given encoding and error handler.
        Otherwise, returns the result of object.__str__() (if defined)
        or repr(object).
        encoding defaults to sys.getdefaultencoding().
        errors defaults to 'strict'.

    ### Methods

    `get_template(self, template)`
    :   fetches the requested template from the environment. Purely a
        convenience method
        
        Parameters:
            template : str
                the template file to look for

    `render(self, page, **kwargs)`
    :   generates the rendered HTML from from environment
        
        Parameters:
            page : Page
                the page object to render into html