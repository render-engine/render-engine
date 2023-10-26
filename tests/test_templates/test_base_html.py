from jinja2 import DictLoader
from render_engine.page import Page
from render_engine.site import Site
from render_engine.utils.themes import Theme


def test_base_html_body_class():
    """body class is added to base html template"""
    
    site = Site()

    @site.page
    class TestPage(Page):
        template = "base.html"

    class TestTheme(Theme):
        globals = {"body_class": "my-class"}
        loader = DictLoader({})
        filters = {}
        plugins = []
        
