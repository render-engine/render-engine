Theme Management

Themes are managed by your Site. You can provide your own theme by adding a `templates` folder to your project_path.

::: src.render_engine.themes.ThemeManager

### Adding themes

`Themes` can be added to your site by registering them.

```python
from SOMETHEME import SomeTheme

app = Site()
app.register_theme(SomeTheme)
```

## Theme

::: src.render_engine.themes.Theme
