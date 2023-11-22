<!-- markdownlint-disable MD052 -->
# Archive

Archives are a [`BasePage`][src.render_engine.page.BasePage] object used to display a list of [`Page`][src.render_engine.page.Page] objects in a [`Collection`][src.render_engine.collection.Collection].

Archive objects create a customizeable page that can be controlled via its parent Collction.

::: src.render_engine.archive.Archive

Collection.archives yields a generator of Archive objects. Each Archive object will have a `pages` attribute that is a list of Page objects referenced in that Archive Page. The number of pages is determined by the `Collection.items_per_page` attribute.

## Enabling Archive Pages

By default render engine will only create the archive page is either of the following conditions are met:

- The `Collection.items_per_page` attribute is set to a value greater than 0.
- The `Collection.has_archive` attribute is set to True.

## Archive Page Numbers

Archive pages are numbered starting at `0`. **The first page is always a list containing all the items.**

If `items_per_page` is greater than `0`, the remaining will contain the items in the collection, split into groups of `items_per_page`.

You can get the total number of `Archive` pages by grabbing the `Archive.num_archive_pages` attribute.
