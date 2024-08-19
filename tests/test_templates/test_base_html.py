import pytest
from jinja2 import DictLoader

from render_engine.page import Page
from render_engine.site import Site
from render_engine.themes import Theme


@pytest.fixture()
def theme_site(tmp_path):
    output_path = tmp_path / "output"
    output_path.mkdir()

    site = Site()
    site.output_path = output_path

    @site.page
    class TestPage(Page):
        template = "base.html"

    return site


def test_base_html_body_class(theme_site):
    """body class is added to base html template"""

    class bodyClassTheme(Theme):
        template_globals = {"body_class": "my-class"}
        loader = DictLoader({})
        filters = {}
        plugins = []
        prefix = "test"

    theme_site.register_themes(bodyClassTheme)
    theme_site._render_output("./", theme_site.route_list["testpage"])

    assert '<body class="my-class">' in (theme_site.output_path / "testpage.html").read_text()


def test_base_html_head_include(theme_site):
    """head can be imported into base html template"""

    class headIncludeTheme(Theme):
        template_globals = {"head": "head.html"}
        loader = DictLoader({"head.html": "<script>console.log('test')</script>"})
        filters = set()
        plugins = []
        prefix = "test"

    theme_site.register_themes(headIncludeTheme)
    theme_site.load_themes()
    theme_site._render_output("./", theme_site.route_list["testpage"])

    assert "<script>console.log('test')</script>" in (theme_site.output_path / "testpage.html").read_text()


def test_base_html_head_reload_theme_count(theme_site):
    """Tests that the theme is only registered once"""

    class headIncludeTheme(Theme):
        template_globals = {"head": "head.html"}
        loader = DictLoader({"head.html": "<script>console.log('test')</script>"})
        filters = set()
        plugins = []
        prefix = "test"

    theme_site.register_themes(headIncludeTheme)
    theme_site.register_themes(headIncludeTheme)
    assert theme_site.site_vars["head"] == {"head.html"}
