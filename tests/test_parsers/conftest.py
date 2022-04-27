import pytest


@pytest.fixture
def temp_json_data():
    yield {"foo": "bar", "biz": "baz"}
