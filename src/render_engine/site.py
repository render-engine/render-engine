import pdb
import shutil
import typing
from curses import wrapper
from distutils.command.build import build
from pathlib import Path
from re import sub

from jinja2 import Environment, FileSystemLoader
from rich import print as rprint
from rich import progress
from rich.padding import Padding
from rich.panel import Panel
from rich.pretty import pprint
from rich.progress import Progress

from .collection import Archive, Collection


def render_archives(archive, **kwargs) -> list[Archive]:
    return [archive.render(pages=archive.pages, **kwargs) for archive in archive]


p = Progress(
    progress.SpinnerColumn(),
    progress.TextColumn("|{task.description}"),
    progress.BarColumn(),
    progress.TimeElapsedColumn(),
    progress.MofNCompleteColumn(),
)


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
        rprint(Panel(f"Rendering {self.__class__.__name__}"))
        pad = Padding(f"Site Config Keys Imported: {[x for x in self.site_vars]}", 1)
        rprint(pad)

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

        build_collection = p.add_task(
            f"[deep_sky_blue3]Rendering {collection.__name__}", total=4
        )

        _collection = collection()
        collection_path = self.path / _collection.output_path
        creating_output_path = p.add_task(
            f"[dark_olive_green1]- creating {collection_path=}", total=1
        )
        collection_path.mkdir(exist_ok=True, parents=True)
        p.update(creating_output_path, completed=1)

        page_count = len(_collection.pages)
        rendering_pages = p.add_task(
            f"[sky_blue1]- rendering {page_count} {collection.content_type.__name__} objects",
            total=page_count,
        )
        collection_vars = {
            f"collection_{key}".upper(): val for key, val in vars(collection).items()
        }

        for page in _collection.pages:
            page.render(
                path=collection_path,
                engine=self.engine,
                **self.site_vars,
            )
            p.update(rendering_pages, advance=1)

        p.update(build_collection, advance=1)

        if hasattr(_collection, "feed"):
            create_feed = p.add_task(
                f"[gold3]- creating {_collection.feed.__name__} for [sky_blue3]{collection.__name__}",
                total=1,
            )
            feed = _collection.feed(
                title=f"{self.site_vars['SITE_TITLE']} - {_collection.title}",
                link=self.site_vars["SITE_URL"],
                pages=_collection.pages,
            )
            feed.render(path=self.path, engine=self.engine, **self.site_vars, **collection_vars)
            p.update(create_feed, completed=1)

        p.update(build_collection, advance=1)

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
            p.update(create_archives, completed=1)

        p.update(build_collection, advance=1)

        if hasattr(_collection, "subcollections"):
            created_subcollections = p.add_task(
                f"[dark_goldenrod]- creating SubCollections {[x for x in _collection.subcollections]}!",
                total=len(_collection.subcollections),
            )
            for subcollection in _collection.subcollections:
                created_subcollections_x = p.add_task(
                    f"[misty_rose1]-- creating {subcollection.key} paths",
                    total=1,
                )
                subcollection_path = collection_path / subcollection.key
                subcollection_path.mkdir(exist_ok=True, parents=True)
                p.update(created_subcollections_x, completed=1)

                subgroups = _collection._gen_subpages(subcollection)
                created_subcollections_x_subgroups = p.add_task(
                    f"[light_goldenrod2]-- creating {subcollection.key} archives",
                    total=len(subgroups),
                )

                for subgroup in subgroups:
                    render_archives(
                        path=subcollection_path,
                        engine=self.engine,
                        archive=subgroup,
                        **self.site_vars,
                        **collection_vars,
                    )
                    p.update(created_subcollections_x_subgroups, advance=1)
                p.update(created_subcollections, advance=1)

        p.update(build_collection, advance=1)
        return _collection

    def render_page(self, page) -> None:
        """Create a Page object and add it to self.routes"""
        with p:
            
            _page = page(**self.site_vars)
            _page.render(path=self.path, engine=self.engine, **page.__dict__)

    def render_static(self, directory) -> None:
        """Copies a Static Directory to the output folder"""
        return shutil.copytree(directory, self.path / Path(directory).name, dirs_exist_ok=True)
