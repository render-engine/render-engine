---
title: "Enhancing Functionality with Content Managers"
description: "Guide to using creating Content Managers to use alternate content storage systems."
date: August 22, 2024
tags: ["content_manager", "render-engine", "customization"]
---

Content Managers are a way to control how and where your content is stored.

## Introduction

Render Engine `Collection` uses a `ContentManager` to manage the storage of content for site generation. By default
content is stored in the file system with each piece of content existing in a discrete file. With an alternate
`ContentManager` the content can be stored in a database, JSON file, or other alternate data store.

## Selecting a `ContentManager`

The `ContentManager` for a given [`Collection`](collection.md) is controlled by the `ContentManager` attribute. When
the class is instantiated the `ContentManager` is also instantiated with any `content_manager_extras` being passed
as arguments. To access the `ContentManager` of a given `Collection` use the `content_manager` attribute.

## Creating a `ContentManager`

To create a `ContentManager` create a sub-class of `ContentManager` that implements the following methods:

```python
@property
@abstractmethod
def pages(self) -> Iterable:
    """The Page objects managed by the content manager"""
    ...

@abstractmethod
def create_entry(self, filepath: Path = None, editor: str = None, metadata: dict = None, content: str = None):
    """Create a new entry"""
    ...
```

### `pages`

The `pages` property is how the `Collection` accesses its content. It is a method that _must_ be implemented by
every `ContentManager`. An example `pages` implementation (from the
[`FileContentManger`](https://github.com/render-engine/render-engine/blob/main/src/render_engine/content_managers/file_content_manager.py)) is:

```python
@property
def pages(self) -> Iterable:
    if self._pages is None:
        self._pages = [self.collection.get_page(page) for page in self.iter_content_path()]
    yield from self._pages
```

### `create_entry`

The `create_entry` method is used by the Render Engine CLI tool to add new entries. It is responsible for adding
the new entry to the datastore and, if an `editor` is specified, giving the user the ability to edit the new entry
prior to committing the entry to the datastore.

#### Arguments

- `filepath: Path`: The path on the filesystem to store the new entry.
- `editor: str`: The text editor to open for editing the new entry.
- `content: str`: The initial content for the new entry.
- `metadata: dict`: The metadata for the new entry.

!!! Note
    Not every `ContentManager` actually needs all the arguments that are passed.

### `find_entry`

The `find_entry` method is used to find a specific page in a `Collection`. It will search through all the pages
known to the `ContentManager` until it finds one that has all the attributes specified. Even if multiple entries
would satisfy the criteria, only the first found will be returned.

### `update_entry`

The `update_entry` is used to update an existing entry in a `ContentManager`.

Parameters:

```python
page: Page  # The Page to update
content: str = None  # Updated content
**kwargs: dict  # The other attributes for the updated page
```
