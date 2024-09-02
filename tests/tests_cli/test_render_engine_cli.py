import time

import httpx
import pytest

from render_engine.cli.event import ServerEventHandler
from render_engine.page import Page
from render_engine.site import Site


@pytest.fixture(scope="module")
def site(tmp_path_factory):
    """Base Site Object"""

    test_site = Site()
    test_output_path = tmp_path_factory.mktemp("output")
    test_site.output_path = test_output_path

    @test_site.page
    class Index(Page):
        content = "Hello World!"

    test_site.render()
    return test_site


@pytest.fixture(scope="module")
def event_handler(site):
    class Handler(ServerEventHandler):
        def stop_watcher(self):  # Stop the
            time.sleep(2)
            return True

    handler = Handler(
        server_address=("localhost", 8000),
        import_path="tests.tests_cli.test_render_engine_cli",
        site=site,
        dirs_to_watch=None,
    )

    return handler


def test_server_build(event_handler):
    """Asserts you can start and stop the server"""
    event_handler.start_server()
    response = httpx.get("http://localhost:8000")
    event_handler.stop_server()
    assert response.status_code == 200
    assert response.text == "Hello World!"


# @pytest.mark.skip("This cannot be tested with pytest")
def test_as_a_context_manager(event_handler):
    """Asserts you can start and stop the server with a context manager"""
    with event_handler:
        response = httpx.get("http://localhost:8000")
        assert response.status_code == 200
        assert response.text
