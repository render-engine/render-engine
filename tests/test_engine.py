import datetime

import jinja2
import pytest

from render_engine.engine import format_datetime, to_pub_date


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


@pytest.mark.parametrize(
    "pubdate",
    (
        (datetime.date(2025, 1, 1)),  # Test given value in jinja global
        (datetime.datetime(2025, 1, 1)),  # Test given value in jinja global
    ),
)
def test_to_pubdate(pubdate):
    """
    Tests that the datetime filter works with the following format:

    """
    assert to_pub_date(pubdate) == "Wed, 01 Jan 2025 00:00:00 -0000"
