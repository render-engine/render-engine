::: src.render_engine.collection.Collection

# Passing Collection Variables to a Rendered Page

You can access attributes from the `Collection` class inside all of its rendered pages.

Each `Page` in a collection has a `collection` attribute, with a dictionary of key:value pairs similar to `Page.template_vars`. The dictionary includes any additional attributes you have defined within the `Collection` class.