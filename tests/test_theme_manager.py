from jinja2.environment import Environment
from jinja2.loaders import ChoiceLoader, DictLoader

from render_engine.themes import Theme, ThemeManager


def test_ThemeManager_registers_theme():
    loader1 = DictLoader({"test1.html": "This is a TeSt"})
    loader2 = DictLoader({"test2.html": "This is a {{'TeSt'|test_up}}"})
    loader3 = DictLoader({"test3.html": "This is a {{'TeSt'|test_down}}"})

    loader2theme = Theme(loader=loader2, static_dir="test", filters={"test_up": lambda x: x.upper()}, plugins=[])

    loader3theme = Theme(loader=loader3, static_dir="test", filters={"test_down": lambda x: x.lower()}, plugins=[])

    loader4theme = Theme(loader=loader1, filters={}, plugins=[])

    thememgr = ThemeManager(
        engine=Environment(loader=ChoiceLoader([])),
        output_path="test",
    )
    for x in (loader2theme, loader3theme, loader4theme):
        thememgr.register_theme(x)
        
    assert "test2.html" in thememgr.engine.list_templates()
    assert thememgr.engine.get_or_select_template("test2.html").render(test="test") == "This is a TEST"
    assert "test3.html" in thememgr.engine.list_templates()
    assert thememgr.engine.get_or_select_template("test3.html").render(test="test") == "This is a test"
