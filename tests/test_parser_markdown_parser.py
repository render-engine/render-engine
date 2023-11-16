import pytest

from render_engine.page import Page
from render_engine.parsers.markdown import MarkdownPageParser


@pytest.fixture()
def markdown_content():
    return """# Test"""


def test_parser_parse_content(markdown_content):
    assert (
        MarkdownPageParser.parse(
            content=markdown_content,
            page=Page(),
        )
        == "<h1>Test</h1>\n"
    )
