from copy import copy
from progress.bar import Bar
import itertools
import inspect
import logging
import os
import shutil
import typing
import pendulum
from pathlib import Path
from slugify import slugify


import more_itertools

from ._type_hint_helpers import PathString
from .collection import Collection
from .engine import Engine
from .feeds import RSSFeedEngine
from .links import Link
from .page import Page
from .search import Search

class Site:
    """
    The site stores your pages and collections to be rendered.

    Pages are stored and created with `site.render()`.
    Collections are stored to be used for future use.
    Sites also contain global variables that can be applied in templates.

    Attributes:
        routes (list):
            storage of registered_routes
        collections (dict):
            storage of registered collections
        output_path (str or pathlib.Path):
            the path to directory which all rendered html pages will be stored.
            default `./output`
        static_path (str or pathlib.Path):
            the path to directory for static content. This will be copied over
            into the `output_path`
        SITE_TITLE (str):
            configuration variable title of the site. This is only used in your
            environment template variables. While Optional you will be warned
            if you do not supply a new variable. default: 'Untitled Site'
        SITE_URL (str):
            configuration variable url of the of the site. While Optional you will be
            warned if you do not supply a new variable. default: 'Untitled Site'
            default 'https://example.com'

    Todo:
        - remove SITE_LINK
        - make SITE_URL accesible as a Page variable and allow for switch for
            Relative and Absolute URLS
    """

    routes: typing.List[Page] = []
    output_path: Path = Path("output")
    static_path: Path = Path("static")
    SITE_TITLE: str = "Untitled Site"
    SITE_LINK: str = "https://example.com"
    SITE_URL: str = "https://example.com"
    strict: bool = False
    default_engine: typing.Type[Engine] = Engine()
    rss_engine: typing.Type[Engine] = RSSFeedEngine()
    search: typing.Optional[typing.Type[Search]] = None
    search_index_filename: str = 'search.json'
    search_keys: typing.List[str] = []
    timezone: str=''

    def __init__(self):
        """
        Clean Directory and Prepare Output Directory

        Parameters:
            routes (list):
                storage of registered_routes
            collections (dict):
                storage of registered collections
            output_path (str or pathlib.Path):
                the path to directory which all rendered html pages will be stored.
                default `./output`
            static_path (str or pathlib.Path):
                the path to directory for static content. This will be copied over
                into the `output_path`
            strict (bool):
        """

        self.collections = {}
        self.subcollections = {}

        # Make Output Path if it doesn't Exist
        self.output_path = Path(self.output_path)

        # strict deletes the directory and rebuilds it from scratch
        if self.output_path.exists() and not self.output_path.is_dir():
            raise ValueError('output path cannot point to an existing file')

        if self.strict and self.output_path.exists():
            shutil.rmtree(self.output_path)

        self.output_path.mkdir(exist_ok=True)

        # copy a defined static path into output path
        if Path(self.static_path).is_dir():
            shutil.copytree(
                self.static_path,
                self.output_path.joinpath(self.static_path),
                dirs_exist_ok=True,
            )

        # sets the timezone environment variable to the local timezone if not present

        os.environ['render_engine_timezone'] = self.timezone or pendulum.local_timezone().name


    def register_collection(self, collection_cls: typing.Type[Collection]) -> None:
        """
        Add a class to your `self.collections`
        iterate through a classes `content_path` and create a classes
        `Page`-like objects, adding each one to `routes`.

        Use a decorator for your defined classes.

        Examples:
            ```
            @register_collection
            class Foo(Collection):
                pass
            ```

        Args:
            collection_cls (Collection):
                Collection to parse
        """
        collection = collection_cls()
        self.collections.update({collection.title: collection})

        for page in collection.pages:
            logging.info(page.title)
            self.route(cls=page)

        if collection.has_archive:

            for archive in collection.archive:
                self.route(cls=archive)

        if collection.feeds:

            for feed in collection.feeds:
                self.register_feed(feed=feed, collection=collection)


    def register_feed(self, feed, collection: Collection) -> None:
        extension = self.rss_engine.extension
        _feed = feed()
        _feed.slug = collection.__class__.__name__.lower()
        _feed.items = [page.rss_feed_item for page in collection.pages]
        _feed.title = f"{self.SITE_TITLE} - {_feed.title}"
        _feed.link = f"{self.SITE_URL}/{_feed.slug}{extension}"

        self.route(cls=_feed)
        logging.debug(vars(_feed))


    def route(self, cls) -> None:
        self.routes.append(cls)


    def register_route(self, cls) -> None:
        self.routes.append(cls())


    def render(self, dry_run: bool = False) -> None:
        for _, collection in self.collections.items():

            if collection.subcollections:

                for subcollection_group in collection.get_subcollections():
                    logging.info(f'{subcollection_group=}')

                    _subcollection_group = collection.get_subcollections()[subcollection_group]
                    sorted_group = sorted(
                            _subcollection_group,
                            key=lambda x:(len(x.pages), x.title),
                            reverse=True,
                            )


                    for subcollection in sorted_group:

                        self.subcollections[subcollection_group] = sorted_group

                        for archive in subcollection.archive:
                            self.route(archive)



        route_count = len(self.routes)

        with Bar(
                f'Rendering {route_count} Pages',
                max=route_count,
                suffix='%(percent).1f%% - %(elapsed_td)s') as bar:
            for page in self.routes:
                suffix='%(percent).1f%% - %(elapsed_td)s'
                bar.suffix = suffix + f' ({page.title})'

                if page.engine:
                    engine = page.engine

                else:
                    engine = self.default_engine

                logging.debug(f'{engine=}')

                template_attrs = self.get_public_attributes(page)

                # breakpoint()

                content = engine.render(page, **template_attrs)

                route = self.output_path.joinpath(page.routes[0].strip("/"))
                route.mkdir(exist_ok=True)
                filename = Path(page.slug).with_suffix(engine.extension)
                filepath = route.joinpath(filename)
                filepath.write_text(content)
                logging.info(f'{filepath=} written!')

                if len(page.routes) > 1:

                    for new_route in page.routes[1:]:
                        new_route = self.output_path.joinpath(new_route.strip("/"))
                        new_route.mkdir(exist_ok=True)
                        new_filepath = new_route.joinpath(filename)
                        shutil.copy(filepath, new_filepath)
                        logging.info(f'{new_filepath=} written!')

                bar.next()

        if self.search:
            search_pages = filter(lambda x: x.no_index == False, self.routes)
            self.search.build_index(
                pages=search_pages,
                keys=self.search_keys,
                filepath=self.output_path.joinpath(self.search_index_filename),
            )


    def get_public_attributes(self, cls):
        site_filtered_attrs = itertools.filterfalse(lambda x:
                x[0].startswith('__'), inspect.getmembers(self))
        site_dict = {x: y for x, y in site_filtered_attrs}

        cls_filtered_attrs = itertools.filterfalse(lambda x:
                x[0].startswith('__'), inspect.getmembers(cls))

        cls_dict = {x: y for x, y in cls_filtered_attrs}

        return {**site_dict, **cls_dict}
