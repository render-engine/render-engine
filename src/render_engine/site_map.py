from collections.abc import Generator, Iterable
from pathlib import Path
from urllib.parse import urljoin

import slugify

from render_engine import Collection, Page
from render_engine._base_object import BaseObject
from render_engine.data_object import DataObject


class SiteMapEntry:
    """Entry in the site map"""

    def __init__(self, entry: BaseObject, route: str | Path, from_collection=False):
        """Initialize the entry"""
        self.slug = entry._slug
        self.title = entry._title
        self.path_name = entry.path_name
        route = str(route)
        match entry:
            case Page() | DataObject():
                # For a base page the _route created if we use the route is invalid - just use the path_name
                if entry.slug_only_url:
                    self._route = f"/{self.slug}"
                else:
                    self._route = f"/{route.lstrip('/')}/{self.path_name}" if from_collection else f"/{self.path_name}"
                self.entries = list()
            case Collection():
                self._route = f"/{str(entry.routes[0]).lstrip('/')}"
                self.entries = [
                    SiteMapEntry(collection_entry, self._route, from_collection=True) for collection_entry in entry
                ]
            case _:
                pass

    @property
    def url_for(self) -> str:
        """The URL for the given entry"""
        return str(self._route)

    def __str__(self) -> str:
        """String representation of the entry as its URL"""
        return self.url_for


class StaticSiteMapEntry(SiteMapEntry):
    """Site map entry for a static file"""

    def __init__(self, file_path: Path, static_root: Path, url_prefix: str = ""):
        """
        :param file_path: Absolute path to the static file on disk.
        :param static_root: The static directory this file lives under (e.g. "static").
        :param url_prefix: The folder name this static dir gets copied to in the
            output directory. `ThemeManager._render_static` copies each static_path
            to `output_path / static_path.name`, so this should be `static_root.name`.
        """
        relative = file_path.relative_to(static_root).as_posix()
        self.slug = slugify.slugify(f"{url_prefix}/{relative}" if url_prefix else relative)
        self.title = file_path.name
        self.path_name = relative
        prefix = url_prefix.strip("/")
        self._route = f"/{prefix}/{relative}" if prefix else f"/{relative}"
        self.entries: list = []


class SiteMap:
    """Site map"""

    def __init__(
        self,
        site_url: str = "",
        route_list: dict | None = None,
        static_paths: Iterable[str | Path] | None = None,
    ) -> None:
        """
        Create the site map based on the route_list

        :param site_url: Used for rendering the HTML to have absolute URLs.
        :param route_list: The route list to parse
        :param static_paths: Static directories to include in the site map
        """
        self._route_map = dict()
        self._collections = dict()
        self._site_url = site_url
        self.static_paths = static_paths
        self.static_include_patterns: Iterable[str] | None = None
        self.static_exclude_patterns: Iterable[str] | None = None
        self.static_exclude_dirs: Iterable[str] | None = None
        self.static_include_dirs: Iterable[str] | None = None
        self.include_static_in_site_map: bool = True
        if not route_list:
            return
        self.update(route_list)

    @property
    def site_url(self) -> str:
        return self._site_url

    @site_url.setter
    def site_url(self, value: str) -> None:
        self._site_url = value

    def update(self, route_list: dict) -> None:
        """
        Update the site map with a new route list.

        :param route_list: The route list to parse
        """
        route: str
        entry: BaseObject
        self._route_map = dict()
        for route, entry in route_list.items():
            if entry.skip_site_map:
                continue
            sm_entry = SiteMapEntry(entry, route)
            self._route_map[sm_entry.slug] = sm_entry
            if sm_entry.entries:
                self._collections[sm_entry.slug] = sm_entry
        if self.static_paths and self.include_static_in_site_map:
            self.add_static_files(
                self.static_paths,
                include_patterns=self.static_include_patterns,
                exclude_patterns=self.static_exclude_patterns,
                exclude_dirs=self.static_exclude_dirs,
                include_dirs=self.static_include_dirs,
            )

    def add_static_files(
        self,
        static_paths: Iterable[str | Path],
        include_patterns: Iterable[str] | None = None,
        exclude_patterns: Iterable[str] | None = None,
        exclude_dirs: Iterable[str] | None = None,
        include_dirs: Iterable[str] | None = None,
    ) -> None:
        """
        Add static files to the site map, optionally filtered by pattern or directory.

        :param static_paths: Static directories to include in the site map
        :param include_patterns: Glob patterns a file must match to be included. Default None: no filtering.
        :param exclude_patterns: Glob patterns that exclude a matching file even if it matched an include pattern.
        :param exclude_dirs: Directory names to skip entirely (matched against any path segment).
        :param include_dirs: Subdirectory paths that override exclude_dirs, forcing inclusion for matching
            subdirectories even if a parent directory was excluded.
        """
        for static in static_paths:
            static = Path(static)
            if not static.exists():
                continue
            url_prefix = static.name
            for file_path in static.rglob("*"):
                if not file_path.is_file():
                    continue
                rel_dir = file_path.relative_to(static).parent
                rel_parts = rel_dir.parts
                rel_dir_str = rel_dir.as_posix()

                excluded_by_dir = exclude_dirs is not None and any(part in exclude_dirs for part in rel_parts)
                included_override = include_dirs is not None and any(
                    rel_dir_str == d or rel_dir_str.startswith(f"{d}/") for d in include_dirs
                )
                if excluded_by_dir and not included_override:
                    continue
                if include_patterns is not None and not any(file_path.match(p) for p in include_patterns):
                    continue
                if exclude_patterns is not None and any(file_path.match(p) for p in exclude_patterns):
                    continue
                entry = StaticSiteMapEntry(file_path, static, url_prefix)
                self._route_map[entry.slug] = entry

    def __iter__(self) -> Generator[SiteMapEntry]:
        """Iterator for the site map object"""
        for entry in self._route_map.values():
            yield entry
            yield from entry.entries

    def find(
        self,
        value: str,
        attr: str = "slug",
        collection: str | None = None,
        full_search: bool = False,
    ) -> SiteMapEntry | None:
        """
        Find an entry in the site map

        Only one of the parameters slug, path_name, or title may be set.
        If collection is set that collection will be searched. If it is not set then all collections
        will be searched if full_search is True.
        If there would be a match in multiple collections - or for just a page, the first match will be returned.

        :param value: The value of attribute to search for
        :param attr: The name of attribute to search for, defaults to slug
        :param collection: The name of the collection to search
        :param full_search: Search recursively in collections
        :return: The first found match or None if not found
        """

        def search(s_attr: str, s_value: str, entries: Iterable) -> SiteMapEntry | None:
            """
            Search the list of entries for a match

            :param s_attr: The attribute to search by
            :param s_value: The value to search for
            :param entries: List of entries to search
            :return: First found match or None if not found
            """
            for s_entry in entries:
                if getattr(s_entry, s_attr, None) == s_value:
                    return s_entry
            return None

        if not value:
            return None
        if collection:
            # Collection was specified so check there
            return (
                search(attr, value, _collection.entries)
                if (_collection := self._collections[slugify.slugify(collection)])
                else None
            )
        if attr == "slug":
            # We can handle slug a bit differently since it's the key to the route map dictionary.
            if entry := self._route_map.get(value):
                return entry
        # Check the base route map
        elif entry := search(attr, value, self._route_map.values()):
            return entry
        if full_search:
            # Check each collection
            for collection in self._collections.values():
                if entry := search(attr, value, collection.entries):
                    return entry
        return None

    @property
    def html(self) -> str:
        """Build the site map as HTML"""
        html_string = "<ul>\n"
        # We can't iterate over `self` because that will flatten out the site map and we do not want that for the HTML
        # version.
        for entry in self._route_map.values():
            html_string += f'\t<li><a href="{urljoin(self.site_url, entry.url_for)}">{entry.title}</a></li>\n'
            if entry.entries:
                html_string += "\t<ul>\n"
                html_string += "".join(
                    f'\t\t<li><a href="{urljoin(self.site_url, sub_entry.url_for)}">{sub_entry.title}</a></li>\n'
                    for sub_entry in entry.entries
                )
                html_string += "\t</ul>\n"
        html_string += "</ul>\n"
        return html_string
