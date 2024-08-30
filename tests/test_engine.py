import datetime

import jinja2
import pytest

from render_engine.engine import format_datetime


@pytest.mark.parametrize(
    "format, override, expected",
    (
        (
            {"DATETIME_FORMAT": "%B %d %Y %H:%M"},
            None,
            "September 27 2023 14:00",
        ),  # Test given value in jinja global
        ({}, None, "27 Sep 2023 14:00 UTC"),  # Test default if no global set
        (
            {"DATETIME_FORMAT": "%B %d %Y %H:%M"},
            "%B %d %Y",
            "September 27 2023",
        ),  # Test override
    ),
)
def test_format_datetime(format, override, expected):
    """
    Tests that the datetime filter works with the following format:

    """
    env = jinja2.Environment()
    env.globals.update(format)
    format_datetime(
        env=env,
        value=datetime.datetime(2023, 9, 27, 14, 0, 0),
        datetime_format=override,
    )
