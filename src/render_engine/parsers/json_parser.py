import json
import re


def frontmatter_json_attr(attr_val: str) -> dict:
    """return the json of the specified file"""
    json_matcher = re.compile(r"json\([\"\']*(.+\.json)[\"\']*\)")
    matched_attr = json_matcher.match(attr_val)

    with open(matched_attr.group(1)) as jfile:
        return json.load(jfile)
