import pytest
import render_engine.content_parser as parser

def test_parse_content_splits_text():
    content = 'title: Some Title\n\nThis is the content.'
    parsed_content = parser.parse_content(content, r"(^\w+: \b.+$)")
    print(parsed_content)
    assert parsed_content == (
            ['title: Some Title'],
            'This is the content.',
            )

def test_parse_content_splits_text_break_at_content():
    actual_content = '''This is the content.

This: is also content

And even more content'''
    attrs = 'title: Some Title'
    content = attrs + '\n\n' + actual_content
    parsed_content = parser.parse_content(content, r"(^\w+: \b.+$)")

    assert 'This' not in parsed_content[0]
    assert parsed_content[1] == actual_content
