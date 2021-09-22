def _convert_to_frontmatter(content): # TODO: Move this to a helper script.
    """if not formatted for frontmatter, add lines"""
    if not content.startswith("---"):
        content = f"---\n{content}"
        content = content.replace("\n\n", "\n---\n\n", 1)
    return content
