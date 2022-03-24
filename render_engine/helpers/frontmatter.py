# Frontmatter Helpers
# IDEAS:
#   - Create New Content Template
#   - Preview Frontmatter to HTML


def _convert_to_frontmatter(content):
    """if not formatted for frontmatter, add lines"""
    if not content.startswith("---"):
        content = f"---\n{content}"
        content = content.replace("\n\n", "\n---\n\n", 1)
    return content
