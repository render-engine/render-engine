import re


def parse_content(content: str, matcher: str):
    """
    split content into attributes and content text

    Parameters:
        content : str
            The content to be parsed
        matcher : str, optional
            A compiled regular expression that splits the content.
            default `base_matcher`
    """

    matchmaker = re.compile(matcher, flags=re.M)
    split_content = content.split("\n\n", maxsplit=1)
    attr_section = split_content[0]

    if len(split_content) == 2:
        base_content = split_content[1]

    else:
        base_content = ""

    parsed_attrs = re.split(matchmaker, attr_section)
    content = base_content.strip()

    attrs = list(filter(lambda x: x.strip(), parsed_attrs))
    return attrs, content
