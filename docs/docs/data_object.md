---
title: "Data Objects"
description: "Overview of Data Objects in Render Engine"
date: March 15, 2026
tags: ["data_objects"]
---
<!-- markdownlint-disable MD056 -->
While Render Engine is a static site generator, there are times when it might be useful to have machine-readable data
available on your site. For example, if you wish to include a [humans.json] file it might be simpler to maintain as a
Python dictionary and have Render Engine output the JSON.

## DataObject

The `DataObject` base class allows for the rendering of a serializable Python object to the site's file system during
site rendering.

### Attributes

| Name              | Type          | Description                                                               |
|-------------------|---------------|---------------------------------------------------------------------------|
| `data_object`     | `Any`         | The object to serialize.                                                  |
| `serializer`      | 'Callable`    | The function to serialize with.                                           |
| `serializer_args` | dict          | Optional `kwargs` to be passed to the `serializer` along with the object. |
| `routes`          | list          | List of directories to output the serialized object to.                   |
| `path_name`       | `str \| Path` | The filename to output the serialized data to.                            |

The `serializer` is a function that takes a single positional argument and optional `**kwargs`. Should you wish to use
a function with a different signature, you will need to write a wrapper around it.

The default `serialize` function is `json.dumps`.

### Configuring a `DataObject`

There are 2 ways to configure a `DataObject` and add it to your `Site`:

1. Using the `Site.data_object` decorator:

    ```python
    import toml
    from render_engine import Site, DataObject

    app = Site()

    @app.data_object
    class MyDataObject(DataObject):
        data_object = {'foo': 'bar'}
        serializer = toml.dumps
    ```

2. Using the `Site.data_object` method:

    ```python
    import toml
    from render_engine import Site, DataObject

    app = Site()

    class MyDataObject(DataObject):
        data_object = {'foo': 'bar'}
        serializer = toml.dumps

    app.data_object(MyDataObject)
    ```

[humans.json]: https://codeberg.org/robida/human.json
