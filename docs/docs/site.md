::: src.render_engine.site.Site

### Adding Static Paths

Static paths are stored in a set. This means you would add to the static paths like you would a set:

```python
site.static_paths.add('path/to/static')
site.static_paths.add('path/to/other/static')
```

You can also add a list of paths:

```python
site.static_paths.update(['path/to/static', 'path/to/other/static'])
```
