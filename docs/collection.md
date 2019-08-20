# Collection Objects

A collection object is a group of pages that share a root path and other attributes.

## Collection.slug
The root path of all items in the collection.

## Collection.content_from_path
A path you can use to load a set of Pages (loaded using [content_from_file])

## Collection.pages
		The building blocks of collections. This is an iterable of [Page] objects.

## Additional Collection Attrs
Collection Attrs are similar to page attrs except they are passed to ALL PAGES IN THE COLLECTION

Additional attrs can be _anything_ but common attrs include:

* Author
* Category
* tags
* Link
* Intro
* Content Footer


