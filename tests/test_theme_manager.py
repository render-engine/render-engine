from jinja2.environment import Environment
from jinja2.loaders import ChoiceLoader, DictLoader, FileSystemLoader, PrefixLoader

from render_engine.themes import Theme, ThemeManager


def test_ThemeManager_registers_theme():
    loader1 = DictLoader({"test1.html": "This is a TeSt"})
    loader2 = DictLoader({"test2.html": "This is a {{'TeSt'|test_up}}"})
    loader3 = DictLoader({"test3.html": "This is a {{'TeSt'|test_down}}"})

    loader2theme = Theme(
        prefix="l1",
        loader=loader2,
        static_dir="test",
        filters={"test_up": lambda x: x.upper()},
        plugins=[],
    )

    loader3theme = Theme(
        prefix="l2",
        loader=loader3,
        static_dir="test",
        filters={"test_down": lambda x: x.lower()},
        plugins=[],
    )

    loader4theme = Theme(
        prefix="l3",
        loader=loader1,
        filters={},
        plugins=[],
        template_globals={"head": "index.html"},
    )

    thememgr = ThemeManager(
        engine=Environment(loader=ChoiceLoader([FileSystemLoader("templates"), PrefixLoader({})])),
        output_path="test",
    )
    for x in (loader2theme, loader3theme, loader4theme):
        thememgr.register_theme(x)

    assert loader2theme.prefix in thememgr.prefix
    assert "test3.html" in thememgr.prefix[loader3theme.prefix].list_templates()
    assert isinstance(thememgr.engine.loader, ChoiceLoader)
    assert loader3theme.static_dir in thememgr.static_paths
