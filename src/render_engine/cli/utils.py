import importlib
import sys

from render_engine import Site


def get_site(import_path: str, site: str, reload: bool = False) -> Site:
    """Split the site module into a module and a class name"""
    sys.path.insert(0, ".")
    imported = importlib.import_module(import_path)
    if reload:
        importlib.reload(imported)
    return getattr(imported, site)
