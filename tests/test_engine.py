from render_engine import Engine
import pytest
import yaml

@pytest.fixture()
def base_engine(site_url):
    return Engine(site_url=site_url)

def test_engine_has_internal_env():
    """This ensures that each Engine instance has its own environment.
    This allows you have different settings apply to each engine"""

    engine1 = Engine()
    engine2 = Engine()

    engine1.env.name = 'engine1'
    engine2.env.name = 'engine2'

    assert engine1.env.name == 'engine1'
    assert engine2.env.name == 'engine2'

def test_engine_kwargs_become_environment_global_properties():
    """Pass all wildcard kwargs into the environment as global variables to use
    in templates"""
    engine = Engine(custom_val='custom')
    assert engine.env.globals['custom_val'] == 'custom'

def test_engine_route_adds_route_items(base_engine):
    """Each engine starts with no routes and routes are added with the @route
    decorator"""
    assert not base_engine.routes

    @base_engine.route('about', './pages/about')
    def about():
        pass

    assert base_engine.routes[0].absolute_url == 'https://example.com/about.html'

def test_engine_config_path_added_to_env(mocker):
    """When a config_path is provided parse the yaml file and add it to configs
    and further the environment globals"""

    custom_val='CUSTOM_KEY: CUSTOM_VALUE'
    mocker.patch('pathlib.Path.read_text', return_value=custom_val)

    env = Engine(config_path="config.yaml").env.globals
    assert env['CUSTOM_KEY'] == 'CUSTOM_VALUE'

def test_engine_build_collection(base_engine, base_page):
    """Setup a Collection using the build_collection decorator"""

    @base_engine.build_collection(routes=['/'], pages=(base_page, base_page, base_page))
    def base_page_build():
        pass


