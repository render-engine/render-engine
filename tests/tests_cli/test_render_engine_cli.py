import time

import ephemeral_port_reserve
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
    hostname = ephemeral_port_reserve.LOCALHOST
    free_port = ephemeral_port_reserve.reserve(hostname)

    class Handler(ServerEventHandler):
        def stop_watcher(self):
            time.sleep(2)
            return True

    handler = Handler(
        server_address=(hostname, free_port),
        import_path="tests.tests_cli.test_render_engine_cli",
        site=site,
        dirs_to_watch=None,
    )

    return {
        "hostname": hostname,
        "port": free_port,
        "handler": handler,
    }


def test_server_build(event_handler):
    """Asserts you can start and stop the server"""
    event_handler["handler"].start_server()
    response = httpx.get(f'http://{event_handler["hostname"]}:{event_handler["port"]}')
    event_handler["handler"].stop_server()
    assert response.status_code == 200
    assert response.text == "Hello World!"


def test_as_a_context_manager(event_handler):
    """Asserts you can start and stop the server with a context manager"""
    with event_handler["handler"]:
        response = httpx.get(f'http://{event_handler["hostname"]}:{event_handler["port"]}')
    assert response.status_code == 200
    assert response.text
