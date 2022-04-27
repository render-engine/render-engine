import json

import pytest

from render_engine.parsers.json_parser import frontmatter_json_attr


def test_json_parser(temp_path, temp_json_data):
    filename = temp_path / "test_json_parser.json"

    with open(filename, "w") as jfile:
        json.dump(temp_json_data, jfile)

    assert frontmatter_json_attr(f"json({filename})") == temp_json_data
