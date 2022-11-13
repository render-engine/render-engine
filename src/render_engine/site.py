import pdb
import shutil
import typing
from curses import wrapper
from distutils.command.build import build
from pathlib import Path
from re import sub

from jinja2 import Environment, FileSystemLoader

from .collection import Archive, Collection


def render_archives(archive, **kwargs) -> list[Archive]:
    return [archive.render(pages=archive.pages, **kwargs) for archive in archive]


class Site:
    """The site stores your pages and collections to be rendered.

    Pages are stored in :py:attr:`routes` and created with `site.render()`.
    Collections and subcollections are stored to be used for future use.

    Sites also contain global variables that can be applied in templates.
    """

    path: Path = Path("output")
    """Path to write rendered content."""

    # Vars that will be passed into the render functions
    site_vars: dict = {"SITE_TITLE": "Untitled Site", "SITE_URL": "https://example.com"}

    engine: typing.Type[Environment] = Environment(loader=FileSystemLoader("templates"))
    """``Engine`` to generate web pages"""

    def __init__(self, static: typing.Optional[str] = None, **kwargs):
        self.site_vars.update(kwargs)

        if static:
            self.render_static(directory=static)

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
        collection_path = self.path / _collection.output_path
        collection_path.mkdir(exist_ok=True, parents=True)

        page_count = len(_collection.pages)
        collection_vars = {
            f"collection_{key}".upper(): val for key, val in vars(collection).items()
        }

        for page in _collection.pages:
            page.render(
                path=collection_path,
                engine=self.engine,
                **self.site_vars,
            )

        if hasattr(_collection, "feed"):
            feed = _collection.feed(
                title=f"{self.site_vars['SITE_TITLE']} - {_collection.title}",
                link=self.site_vars["SITE_URL"],
                pages=_collection.pages,
            )
            feed.render(
                path=self.path, engine=self.engine, **self.site_vars, **collection_vars
            )

        if _collection.has_archive:
            create_archives = p.add_task(
                f"[orange3]- creating {_collection.archives[0].__class__.__name__}",
                total=1,
            )
            render_archives(
                path=collection_path,
                engine=self.engine,
                archive=_collection.archives,
                **self.site_vars,
            )

        if hasattr(_collection, "subcollections"):
            for subcollection in _collection.subcollections:
                subcollection_path = collection_path / subcollection.key
                subcollection_path.mkdir(exist_ok=True, parents=True)

                subgroups = _collection._gen_subpages(subcollection)

                for subgroup in subgroups:
                    render_archives(
                        path=subcollection_path,
                        engine=self.engine,
                        archive=subgroup,
                        **self.site_vars,
                        **collection_vars,
                    )

        return _collection

    def render_page(self, page) -> None:
        """Create a Page object and add it to self.routes"""
        _page = page(**self.site_vars)
        _page.render(path=self.path, engine=self.engine, **page.__dict__)

    def render_static(self, directory) -> None:
        """Copies a Static Directory to the output folder"""
        return shutil.copytree(
            directory, self.path / Path(directory).name, dirs_exist_ok=True
        )
