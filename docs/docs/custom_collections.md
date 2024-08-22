---
title: "Custom Collections"
description: "Guide to creating and managing custom collections in Render Engine, including attributes, methods, and installation steps."
date: August 22, 2024
tags: ["collection", "render-engine", "custom-collections"]
---

Custom collections are a way for you to create collections for distribution.

If you have something that could be represented as a group of individual pages, then potentially you could make a custom collection.

## Creating a Custom Collection

### Install the render_engine package

You will need to ensure that you're using render_engine version 2023.1.3 or higher

```bash
pip install render_engine
```

### Creating your Collection Object

Import the collection class from render_engine and create your custom Collection object

```python
from render_engine.collection import Collection

class MyCustomCollection(Collection):
    pass
```

### Collection Attributes and Methods

While you can set any of the attributes and override any methods on the Collection object, there are a few exposed specifically for custom collection types.

#### Attributes

`content_path: str | Iterable`: Perhaps most important, this is the iterable that will be used to create the collection object. `iter_content_path` is the method that will be used to parse the content path. This method is called in the `__init__` method of the Collection object.

`content_type: Type[Page]`: Some custom collections may want to create a different type of Page object. This attribute allows you to set the type of page that will be created for each item in the collection.

`Feed: Type[RSSFeed]`: The type of feed that will be created for the collection. By default, this is the RSSFeed class, but you can set this to any class that inherits from the RSSFeed class.

`feed_title: str`: The title of the feed that will be created for the collection. By default, this is the title of the collection, but you can set this to any string, or leave it to the user to set.

`include_suffixes: list[str]`: List of extensions that will be used to filter a file-based content-path. **NOTE**: This is only used if `iter_content_path` is not overridden.

`PageParser: Type[BasePageParser]`: PageParser that is used by the generated `Page` Objects.

`parser_extras: dict[str, Any]`: Extra attributes that will be passed to the `PageParser` class.

`required_themes: list[Theme]`: Some collections may require a specific theme to be used. This attribute allows you to set a list of themes that will be required for the collection. These will be installed when @site.collection is called.

`sort_by: str`: The attribute that will be used to sort the collection `Page` objects. By default, this is the title of the page, but you can set this to any attribute that is available on the page object, or leave it to the user to set.

`sort_reverse: bool`: Whether or not the collection should be sorted in reverse order. By default, this is False, but you can set this to True, or leave it to the user to set.

#### Methods

`iter_content_path(self) -> Iterable`: This method is used to parse the `content_path` attribute. By default, this performs a `pathlib.Path.glob` that will use the `include_suffixes` attribute to filter the files.

`get_page(self) -> Page`: This method is used when creating a page from the collection. The usual flow is to create an instance of the page object and then add any attributes that you would like to additionally set (perhaps from the collection).
