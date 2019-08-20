# Engine Object #

The engine is what converts the [[page]] and [[collection]] objects into static webpages. 

There are also tools that assist in the creation of [pages](page.md) and [collections](collection.md). 

## Engine.output_path: _Str, Pathlib.Path_  ##

A directory that **ALL RENDERED CONTENT** will be copied to. 

## Engine.static_path: _Str, Pathlib.Path_ ##

A directory that will be copied to the [[output_path]] EXACTLY. This is good for any assets that you may want to include in your site. 
```
# The Static Path
static_path/
	images/
 		logo.png
	    splash_page_image.png
	files/
		ebook.pdf
	js/
		script.js
	css/
		style.css
		
# The Rendered Output Path
output_path/
	static_path/
		images/
 			logo.png
	    		splash_page_image.png
		files/
			ebook.pdf
		js/
			script.js
		css/
			style.css
```

if no static path is defined, and there is no default path, nothing will be loaded.

## Engine.pages: _Sequence_ ##

An iterable of [[page]] objects that makup the invidual pages. 

 ## Engine.collections: _Sequence_ ##

Similar to `Engine.pages` but holds [[collection]] objects instead. When rendering html pages from a [[collection]], the template must also include the collection attrs defined. 

## Engine.template_path: _Str, pathlib.Path_

Path to where template files are stored. This is the root directory for paths for `template` values in [[page]] and [[collection]] objects.

## Engine.environment: _Jinja2 Environment_ ##
The `Engine.environment` is a [Jinja2 environment](https://palletsprojects.com/p/jinja/)*. 

_TODO_: Provide support for multiple objects.

If no Environment is provided, creating a new Engine will create an Engine for you.

## Engine.run(overwrite=None) ##

Calling `Engine.run()` is what starts the process of creating html pages.

Pages are generated in the following order:
*  Static Pages
*  Collection Pages
*  Standalone Pages