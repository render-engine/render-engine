import re

def _convert_to_frontmatter(content): # TODO: Move this to a helper script.
    """if not formatted for frontmatter, add lines"""
    if not content.startswith("---"):
        content = f"---\n{content}"
        content = content.replace("\n\n", "\n---\n\n", 1)
    return content

def _parse_content(content: str, matcher: str):
    """
    split content into attributes and content text

    Parameters:
        content:
            The content to be parsed
        matcher:
            A compiled regular expression that splits the content.
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
    return {"metadata": attrs, "content": content}
