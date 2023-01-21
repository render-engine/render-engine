import pluggy

from .blog import Blog
from .collection import Collection
from .page import Page
from .site import Site

_PROJECT_NAME = "render_engine"

hook_impl = pluggy.HookimplMarker(project_name=_PROJECT_NAME)
