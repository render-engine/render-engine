import shutil
import typing
from curses import wrapper
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from .collection import Collection
from .feeds import RSSFeed


class Site:
    """The site stores your pages and collections to be rendered.

    Pages are stored in :py:attr:`routes` and created with `site.render()`.
    Collections and subcollections are stored to be used for future use.

    Sites also contain global variables that can be applied in templates.

    Attributes:
        routes: typing.List[typing.Type[Page]]
            routes are stored prior to being caled with :py:meth:`site.render()`.
    """

    path: Path = Path("output")
    """Path to write rendered content."""

    # Vars that will be passed into the render functions
    site_vars: dict = {"SITE_TITLE": "Untitled Site", "SITE_URL": "https://example.com"}

    engine: typing.Type[Environment] = Environment(loader=FileSystemLoader("templates"))
    """``Engine`` to generate web pages"""

    def __init__(self, static: typing.Optional[str] = None, **kwargs):
        self.path.mkdir(exist_ok=True)
        self.site_vars.update(kwargs)

        if static:
            self.render_static(static)

    def render_collection(self, collection: typing.Type[Collection]) -> None:
        """Add a class to your ``self.collections``
        iterate through a classes ``content_path`` and create a classes ``Page``-like
        objects, adding each one to ``routes``.

        Use a decorator for your defined classes.

        Examples::

            @register_collection
            class Foo(Collection):
                pass
        """
        _collection = collection()
        collection_path = self.path.joinpath(getattr(_collection, "output_path", ""))
        collection_path.mkdir(exist_ok=True, parents=True)

        for page in _collection.pages:
            page.render(
                path=collection_path,
                **self.site_vars,
            )

        if hasattr(_collection, "feed"):
            feed = _collection.feed(
                title=f"{self.site_vars['SITE_TITLE']} - {_collection.title}",
                link=self.site_vars["SITE_URL"],
                pages=_collection.pages,
            )
            feed.render(path=self.path, **self.site_vars)

        if _collection.has_archive:
            _collection.render_archives(
                path=collection_path,
                **self.site_vars,
                **_collection.collection_vars,
            )

        return _collection

    def render_page(self, page) -> None:
        """Create a Page object and add it to self.routes"""
        _page = page(**self.site_vars)
        _page.render(path=self.path, **page.__dict__)

    def render_static(self, directory) -> None:
        """Copies a Static Directory to the output folder"""
        return shutil.copytree(directory, self.path / directory, dirs_exist_ok=True)
