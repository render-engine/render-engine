from render_engine.site import Site

import os
import pytest

def test_site_environment_var():
    class TestSite(Site):
        timezone = 'US/Eastern'

    TestSite()
    assert os.environ['render_engine_timezone'] == 'US/Eastern'



def test_register_route():
    pass

def test_register_collection():
    pass

def test_register_feed():
    pass

