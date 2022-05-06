import pytest

from render_engine.links import Image, Link


def test_links_values():
    """
    given a link object.
    tests that class and id don't need to be included.
    """

    link_no_options = Link()
    assert str(link_no_options) == '<a href="#"></a>'

    link_with_options = Link(text="test item", meta={"foo": "bar"})

    assert str(link_with_options) == '<a href="#" foo="bar">test item</a>'


def test_images():
    """
    given a link object.
    tests that class and id don't need to be included.
    """

    image_no_options = Image()
    assert str(image_no_options) == '<img src="#" alt="" />'

    image_with_meta = Image(text="test item", meta={"foo": "bar"})

    assert str(image_with_meta) == '<img src="#" alt="test item" foo="bar" />'
