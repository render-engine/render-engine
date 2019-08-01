import pytest
from render_engine import Engine

@pytest.fixture()
def base_engine(site_url):
    return Engine()

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

    assert base_engine.routes[0].absolute_url == './about.html'

