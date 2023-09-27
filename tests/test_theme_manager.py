import pytest
from jinja2.environment import Environment
from jinja2.loaders import DictLoader, ChoiceLoader
from render_engine.utils.themes import ThemeManager, Theme



def test_ThemeManager_builds():
    loader=DictLoader(
            {"test1.html": "This is a test"}
    )
    class TestThemeManager(ThemeManager):
        engine = Environment(loader=loader)

    thememgr = TestThemeManager()
    assert thememgr.output_path == "output"
    assert "static" in thememgr.static_paths
    assert 'test1.html' in thememgr.engine.list_templates()
    assert thememgr.engine.get_or_select_template('test1.html').render() == "This is a test"

def test_ThemeManager_registers_theme():
    loader1=DictLoader({"test1.html": "This is a TeSt"})
    loader2=DictLoader({"test2.html": "This is a {{'TeSt'|test_up}}"})
    loader3=DictLoader({"test3.html": "This is a {{'TeSt'|test_down}}"})

    loader2theme = Theme(
        loader=loader2,
        static_dir="test",
        filters={"test_up": lambda x: x.upper()}
    )

    loader3theme = Theme(
        loader=loader3,
        static_dir="test",
        filters={"test_down": lambda x: x.lower()}
    )
    class TestThemeManager(ThemeManager):
        engine = Environment(loader=ChoiceLoader(loaders=[loader1]))

    thememgr = TestThemeManager()
    thememgr.register_themes(loader2theme, loader3theme)
    assert "test2.html" in thememgr.engine.list_templates()
    assert thememgr.engine.get_or_select_template('test2.html').render(test="test") == "This is a TEST"
    assert "test3.html" in thememgr.engine.list_templates()
    assert thememgr.engine.get_or_select_template('test3.html').render(test="test") == "This is a test"