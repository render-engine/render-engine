import warnings

from render_engine_markdown import MarkdownPageParser  # noqa: F401

warnings.warn(
    "`render_engine.hookspecs` will be deprecated in version 2024.3.1,  \
        Please use `from render_engine_markdown import MarkdownPageParser` instead.",
    DeprecationWarning,
)
