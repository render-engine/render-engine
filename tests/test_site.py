from render_engine.site import Site

import os
import pytest

def test_site_environment_var():
    class TestSite(Site):
        timezone = 'US/Eastern'

    TestSite()
    assert os.environ['render_engine_timezone'] == 'US/Eastern'


@pytest.mark.skip()
def test_register_route():
    pass

@pytest.mark.skip()
def test_register_collection():
    pass

@pytest.mark.skip()
def test_register_feed():
    pass


def test_site_registers_each_archive_page()
    pass
